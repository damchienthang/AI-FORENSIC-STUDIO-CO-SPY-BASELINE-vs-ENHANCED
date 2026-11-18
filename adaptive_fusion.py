"""
adaptive_fusion.py — Cải tiến 3 & 4: CAGU + Dual-Domain Consistency
======================================================================
CAGU (Channel-wise Adaptive Gating Unit):
  Nhận spatial_feat [B, 512] từ VAE-ResNet và freq_feat [B, 128] từ FrequencyBranch,
  sinh ra gating vector g ∈ (0,1)^640, thực hiện weighted fusion adaptively.

Dual-Domain Consistency:
  Lọc false-positive: nếu tần số nghi cao nhưng VAE reconstruction error thấp
  (ảnh thật có hoa văn lặp lại như rèm, lưới xe...) → giảm xác suất AI.

Cách dùng:
    from adaptive_fusion import CAGU, DualDomainConsistency, EnhancedCoSpyHead
    head = EnhancedCoSpyHead(spatial_dim=512, freq_dim=128)
    prob, gate_weights = head(spatial_feat, freq_feat, vae_mse)
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


# ================================================================== #
#  CAGU — Channel-wise Adaptive Gating Unit                          #
# ================================================================== #
class CAGU(nn.Module):
    """
    Bộ van điều tiết thích nghi theo kênh đặc trưng.
    
    Cơ chế:
        1. Concat [spatial_feat || freq_feat] → [B, D_total]
        2. Squeeze-Excite 2 lớp FC để học gating vector g ∈ (0,1)^D_total
        3. Output = g ⊙ [spatial_feat || freq_feat]  (Hadamard product)
    
    Điểm khác biệt so với simple concat:
        - Gate g phụ thuộc vào NỘI DUNG ảnh, không phải cố định
        - Khi ảnh JPEG nén mạnh: g tự động up-weight kênh tần số
        - Khi ảnh nét: g ưu tiên kênh spatial VAE
    """

    def __init__(self, spatial_dim: int = 512, freq_dim: int = 128, reduction: int = 8):
        """
        Args:
            spatial_dim: Chiều vector từ VAE-ResNet encoder
            freq_dim:    Chiều vector từ FrequencyBranch
            reduction:   Reduction ratio cho bottleneck FC (giống SE-Net)
        """
        super().__init__()
        self.total_dim = spatial_dim + freq_dim
        bottleneck_dim = max(self.total_dim // reduction, 32)

        # Squeeze-Excite gating network
        self.gate_net = nn.Sequential(
            nn.Linear(self.total_dim, bottleneck_dim),
            nn.ReLU(inplace=True),
            nn.Linear(bottleneck_dim, self.total_dim),
            nn.Sigmoid(),   # g ∈ (0, 1)^D_total
        )

        # Layer norm cho ổn định training
        self.layer_norm = nn.LayerNorm(self.total_dim)

    def forward(self, spatial_feat: torch.Tensor, freq_feat: torch.Tensor):
        """
        Args:
            spatial_feat: [B, spatial_dim]  — đặc trưng miền không gian
            freq_feat:    [B, freq_dim]     — đặc trưng miền tần số

        Returns:
            fused:        [B, total_dim]    — đặc trưng đã gating
            gate_weights: [B, total_dim]    — vector gate (để phân tích)
        """
        # Concatenate
        combined = torch.cat([spatial_feat, freq_feat], dim=1)  # [B, 640]
        combined = self.layer_norm(combined)

        # Compute gating vector
        gate_weights = self.gate_net(combined)                  # [B, 640] ∈ (0,1)

        # Gated fusion
        fused = gate_weights * combined                         # Hadamard product

        return fused, gate_weights

    def get_gate_stats(self, gate_weights: torch.Tensor, spatial_dim: int = 512):
        """
        Phân tích tỷ lệ trọng số spatial vs frequency.
        Dùng để in ra bảng thống kê trong notebook.

        Returns:
            dict với 'spatial_weight_pct' và 'freq_weight_pct'
        """
        spatial_avg = gate_weights[:, :spatial_dim].mean().item()
        freq_avg    = gate_weights[:, spatial_dim:].mean().item()
        total = spatial_avg + freq_avg + 1e-8
        return {
            "spatial_weight_pct": spatial_avg / total * 100,
            "freq_weight_pct":    freq_avg    / total * 100,
        }


# ================================================================== #
#  Dual-Domain Consistency Regularizer                               #
# ================================================================== #
class DualDomainConsistency(nn.Module):
    """
    Cải tiến 4: Lọc false-positive dựa trên tính nhất quán giữa 2 miền.
    
    Logic:
        - freq_score cao  + vae_mse cao  → AI thật sự (tần số lạ, reconstruction khó)
        - freq_score cao  + vae_mse thấp → Có thể là ảnh thật có hoa văn (giảm confidence)
        - freq_score thấp + vae_mse thấp → Ảnh thật rõ ràng (xác suất AI thấp)
    
    Công thức điều chỉnh:
        consistency_weight = sigmoid(w1 * freq_score + w2 * log(vae_mse + ε))
        adjusted_prob = raw_prob * consistency_weight
    """

    def __init__(self):
        super().__init__()
        # Trọng số học được (khởi tạo theo heuristic)
        self.w_freq = nn.Parameter(torch.tensor(1.5))
        self.w_mse  = nn.Parameter(torch.tensor(0.8))
        self.bias   = nn.Parameter(torch.tensor(0.0))

    def forward(
        self,
        raw_prob: torch.Tensor,    # [B, 1] xác suất AI thô
        freq_score: torch.Tensor,  # [B, 1] ∈ (0,1) điểm nghi tần số
        vae_mse: torch.Tensor,     # [B, 1] VAE reconstruction MSE
    ) -> torch.Tensor:
        """
        Returns:
            adjusted_prob: [B, 1] xác suất AI đã được hiệu chỉnh tính nhất quán
        """
        # Log-scale MSE để ổn định giá trị rất nhỏ
        log_mse = torch.log(vae_mse + 1e-7)                    # [B, 1]

        # Consistency score: cao khi cả 2 đều đồng thuận AI
        consistency = torch.sigmoid(
            self.w_freq * freq_score + self.w_mse * log_mse + self.bias
        )                                                        # [B, 1] ∈ (0,1)

        # Điều chỉnh xác suất (không dùng raw_prob * consistency vì sẽ crash recall)
        # Dùng weighted average để bảo toàn tính ổn định
        adjusted = 0.7 * raw_prob + 0.3 * raw_prob * consistency

        return adjusted.clamp(0.0, 1.0)


# ================================================================== #
#  EnhancedCoSpyHead — Đầu phân loại tích hợp đầy đủ 4 cải tiến    #
# ================================================================== #
class EnhancedCoSpyHead(nn.Module):
    """
    Thay thế ArtifactDetector.fc đơn thuần bằng pipeline đầy đủ:
        spatial_feat + freq_feat → CAGU → MLP → prob → DualDomainConsistency → adjusted_prob
    
    Dùng như một drop-in replacement cho head của CO-SPY.
    """

    def __init__(self, spatial_dim: int = 512, freq_dim: int = 128):
        super().__init__()
        self.spatial_dim = spatial_dim
        self.freq_dim    = freq_dim
        total_dim        = spatial_dim + freq_dim   # 640

        # CAGU gating
        self.cagu = CAGU(spatial_dim=spatial_dim, freq_dim=freq_dim)

        # MLP classifier sau gating
        self.classifier = nn.Sequential(
            nn.Linear(total_dim, 256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(256, 64),
            nn.ReLU(inplace=True),
            nn.Linear(64, 1),
        )

        # Dual-domain consistency
        self.consistency = DualDomainConsistency()

    def forward(
        self,
        spatial_feat: torch.Tensor,   # [B, 512]
        freq_feat:    torch.Tensor,    # [B, 128]
        vae_mse:      torch.Tensor,    # [B, 1] — VAE reconstruction MSE
        return_gate:  bool = False,
    ):
        """
        Returns:
            adjusted_prob: [B, 1] — xác suất AI cuối cùng
            gate_weights:  [B, 640] (chỉ khi return_gate=True)
        """
        # Cải tiến 3: CAGU fusion
        fused, gate_weights = self.cagu(spatial_feat, freq_feat)

        # Classification logit → prob
        logit = self.classifier(fused)                          # [B, 1]
        raw_prob = torch.sigmoid(logit)                         # [B, 1]

        # Freq score: lấy norm của freq_feat qua gating như proxy
        freq_gate_portion = gate_weights[:, self.spatial_dim:]  # [B, 128]
        freq_score = freq_gate_portion.mean(dim=1, keepdim=True)  # [B, 1]

        # Cải tiến 4: Dual-domain consistency adjustment
        adjusted_prob = self.consistency(raw_prob, freq_score, vae_mse)

        if return_gate:
            return adjusted_prob, gate_weights
        return adjusted_prob


# ================================================================== #
#  Quick test                                                         #
# ================================================================== #
if __name__ == "__main__":
    print("=== CAGU + DualDomainConsistency Test ===")
    B = 4
    spatial = torch.randn(B, 512)
    freq    = torch.randn(B, 128)
    mse     = torch.rand(B, 1) * 0.1   # VAE MSE nhỏ ∈ [0, 0.1]

    head = EnhancedCoSpyHead(spatial_dim=512, freq_dim=128)
    prob, gates = head(spatial, freq, mse, return_gate=True)

    gate_stats = head.cagu.get_gate_stats(gates)
    print(f"Input:   spatial {spatial.shape}, freq {freq.shape}, mse {mse.shape}")
    print(f"Output prob shape: {prob.shape}")
    print(f"Gate stats: Spatial={gate_stats['spatial_weight_pct']:.1f}%, "
          f"Freq={gate_stats['freq_weight_pct']:.1f}%")
    print(f"Sample probs: {prob.squeeze().tolist()}")
    print("OK — EnhancedCoSpyHead hoạt động bình thường.")
