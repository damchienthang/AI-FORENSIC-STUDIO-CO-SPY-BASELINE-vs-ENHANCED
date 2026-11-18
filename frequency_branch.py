"""
frequency_branch.py — Cải tiến 2: Nhánh tần số 2D-FFT với CNN 3 lớp
======================================================================
Áp dụng bộ lọc High-Pass (HPF) trên phổ Fourier 2D để bắt các dấu vết
upsampling grid artifact đặc trưng của AI, kể cả khi ảnh đã bị nén JPEG.

Kiến trúc:
  Ảnh RGB → Grayscale → 2D-FFT → Mask High-Pass (r₀=16) → iFFT → 
  3-layer CNN (Conv→BN→ReLU) → AdaptiveAvgPool → 128-dim feature vector

Cách dùng:
    from frequency_branch import FrequencyBranch
    branch = FrequencyBranch(out_features=128).eval()
    feat = branch(tensor_input)   # [B, 128]
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


class HighPassFFTLayer(nn.Module):
    """
    Bộ lọc High-Pass 2D-FFT không tham số (không học được).
    
    Quy trình:
        1. Chuyển ảnh sang grayscale
        2. FFT2D + fftshift
        3. Zero-out vùng tần số thấp (vòng tròn r < r0)
        4. ifftshift + iFFT2D → lấy phần thực
        5. Normalize → tensor [B, 1, H, W]
    """

    def __init__(self, r0: int = 16):
        """
        Args:
            r0: Bán kính ngưỡng tần số thấp cần loại bỏ (pixel, trong miền tần số).
                r0=16 là giá trị tốt nhất theo thực nghiệm trong báo cáo.
        """
        super().__init__()
        self.r0 = r0

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: Tensor [B, 3, H, W], float32 ∈ [0, 1]
        Returns:
            Tensor [B, 1, H, W] — ảnh high-pass frequency residual
        """
        # Grayscale: luminance = 0.299R + 0.587G + 0.114B
        gray = 0.299 * x[:, 0] + 0.587 * x[:, 1] + 0.114 * x[:, 2]  # [B, H, W]

        # 2D FFT (trên CPU hoặc GPU đều được)
        fft = torch.fft.fft2(gray)
        fft_shifted = torch.fft.fftshift(fft, dim=(-2, -1))

        # Tạo high-pass mask: 1 ở mọi nơi, 0 trong vòng tròn r < r0
        B, H, W = gray.shape
        cy, cx = H // 2, W // 2
        y_idx = torch.arange(H, device=x.device).view(-1, 1).float() - cy
        x_idx = torch.arange(W, device=x.device).view(1, -1).float() - cx
        dist = torch.sqrt(y_idx ** 2 + x_idx ** 2)                    # [H, W]
        mask = (dist >= self.r0).float().unsqueeze(0)                  # [1, H, W]

        # Áp mask
        fft_filtered = fft_shifted * mask                              # [B, H, W] complex

        # iFFT → ảnh không gian
        ifft_shifted = torch.fft.ifftshift(fft_filtered, dim=(-2, -1))
        recon = torch.fft.ifft2(ifft_shifted).real                    # [B, H, W]

        # Normalize [−1, 1] → [0, 1] per sample
        recon_min = recon.view(B, -1).min(dim=1)[0].view(B, 1, 1)
        recon_max = recon.view(B, -1).max(dim=1)[0].view(B, 1, 1)
        recon_norm = (recon - recon_min) / (recon_max - recon_min + 1e-8)

        return recon_norm.unsqueeze(1)                                 # [B, 1, H, W]


class FrequencyBranch(nn.Module):
    """
    Nhánh tần số đầy đủ: HPF Layer → 3-layer CNN → Feature vector.
    
    Architecture detail:
        HPF(r0=16) → Conv(1→32, k=3) → BN → ReLU →
                      Conv(32→64, k=3, stride=2) → BN → ReLU →
                      Conv(64→128, k=3, stride=2) → BN → ReLU →
                      AdaptiveAvgPool(1×1) → Flatten → Linear(128→out_features)
    """

    def __init__(self, r0: int = 16, out_features: int = 128):
        """
        Args:
            r0:           Bán kính high-pass cutoff
            out_features: Kích thước vector đặc trưng đầu ra
        """
        super().__init__()
        self.hpf = HighPassFFTLayer(r0=r0)

        self.cnn = nn.Sequential(
            # Layer 1: 1 → 32 channels, capture local frequency patterns
            nn.Conv2d(1, 32, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),

            # Layer 2: 32 → 64, stride=2 (downsample H/2, W/2)
            nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),

            # Layer 3: 64 → 128, stride=2 (downsample H/4, W/4)
            nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1, bias=False),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
        )

        self.pool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc   = nn.Linear(128, out_features)
        self.out_features = out_features

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: [B, 3, H, W]
        Returns:
            feat: [B, out_features]
        """
        hpf_map = self.hpf(x)             # [B, 1, H, W]
        feat_map = self.cnn(hpf_map)      # [B, 128, H/4, W/4]
        pooled = self.pool(feat_map)       # [B, 128, 1, 1]
        flat = pooled.view(pooled.size(0), -1)  # [B, 128]
        out = self.fc(flat)               # [B, out_features]
        return out

    def get_hpf_visualization(self, x: torch.Tensor):
        """
        Trả về ảnh HPF grayscale dưới dạng numpy để visualize trong notebook.
        
        Returns:
            np.ndarray [H, W] ∈ [0, 1]
        """
        with torch.no_grad():
            hpf_map = self.hpf(x)                             # [B, 1, H, W]
        return hpf_map[0, 0].cpu().numpy()                    # [H, W]


# ------------------------------------------------------------------ #
#  Utility: FFT power spectrum (cho visualization trong app.py)       #
# ------------------------------------------------------------------ #
def compute_fft_power_spectrum(pil_image, size: int = 256) -> np.ndarray:
    """
    Tính phổ năng lượng Fourier 2D (log scale), trả về numpy [size, size] ∈ [0, 255].
    
    Dùng để so sánh trực quan giữa ảnh thật và AI trong notebook.
    """
    from PIL import Image
    import numpy as np

    gray = np.array(pil_image.convert("L").resize((size, size)), dtype=np.float32)
    fft = np.fft.fft2(gray)
    fft_shifted = np.fft.fftshift(fft)
    power = np.log(np.abs(fft_shifted) ** 2 + 1e-7)
    power_norm = (power - power.min()) / (power.max() - power.min() + 1e-8)
    return (power_norm * 255).astype(np.uint8)


if __name__ == "__main__":
    print("FrequencyBranch — standalone test")
    model = FrequencyBranch(r0=16, out_features=128)
    dummy = torch.rand(2, 3, 224, 224)
    out = model(dummy)
    print(f"Input shape:  {dummy.shape}")
    print(f"Output shape: {out.shape}")   # Expected: [2, 128]
    print("OK — FrequencyBranch hoạt động bình thường.")
