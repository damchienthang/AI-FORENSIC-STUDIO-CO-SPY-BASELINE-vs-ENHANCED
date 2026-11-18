"""
gradcam.py — Cải tiến 1: Explainable AI (XAI) bằng Gradient-weighted Class Activation Mapping
=================================================================================================
Hook vào layer2[-1] của VAEReconEncoder (ResNet-50 Bottleneck) để sinh bản đồ nhiệt
chỉ ra VÙNG CỤ THỂ trong ảnh mà mô hình nghi ngờ là giả.

Cách dùng:
    from gradcam import GradCAMExplainer
    explainer = GradCAMExplainer(artifact_encoder)
    heatmap_pil = explainer.explain(tensor_input, pil_image)
"""

import torch
import torch.nn as nn
import numpy as np
import cv2
from PIL import Image
from typing import Optional


class GradCAMExplainer:
    """
    Grad-CAM cho VAEReconEncoder (ResNet-50 backbone trong CO-SPY).
    
    Hook vào: artifact_encoder.layer2[-1]  (output shape: [B, 512, 14, 14])
    Gradient được tính từ output classifier (fc) so với feature map đó.
    """

    def __init__(self, artifact_encoder: nn.Module, fc_layer: nn.Module, target_layer: Optional[nn.Module] = None):
        """
        Args:
            artifact_encoder: VAEReconEncoder instance (có self.layer2)
            fc_layer:         Linear layer phân loại (ArtifactDetector.fc)
            target_layer:     Layer cần hook (mặc định: artifact_encoder.layer2[-1])
        """
        self.encoder = artifact_encoder
        self.fc = fc_layer
        self.target_layer = target_layer if target_layer is not None else artifact_encoder.layer2[-1]

        self._feature_maps = None   # Activation maps từ forward hook
        self._gradients = None      # Gradients từ backward hook
        self._hooks = []

    # ------------------------------------------------------------------ #
    #  Hook registration                                                   #
    # ------------------------------------------------------------------ #
    def _register_hooks(self):
        """Đăng ký forward + backward hooks lên target_layer."""
        def _fwd_hook(module, input, output):
            self._feature_maps = output.detach().clone()

        def _bwd_hook(module, grad_input, grad_output):
            self._gradients = grad_output[0].detach().clone()

        h1 = self.target_layer.register_forward_hook(_fwd_hook)
        h2 = self.target_layer.register_full_backward_hook(_bwd_hook)
        self._hooks = [h1, h2]

    def _remove_hooks(self):
        for h in self._hooks:
            h.remove()
        self._hooks = []

    # ------------------------------------------------------------------ #
    #  Core explain method                                                 #
    # ------------------------------------------------------------------ #
    def explain(
        self,
        tensor_input: torch.Tensor,
        pil_original: Image.Image,
        colormap: int = cv2.COLORMAP_JET,
        alpha: float = 0.45,
    ) -> Image.Image:
        """
        Sinh ra ảnh overlay Grad-CAM lên ảnh gốc.

        Args:
            tensor_input:  Tensor [1, 3, H, W] đã qua test_transform (float32)
            pil_original:  Ảnh PIL gốc (để overlay)
            colormap:      OpenCV colormap ID
            alpha:         Độ trong suốt của heatmap khi overlay lên ảnh gốc

        Returns:
            PIL.Image — Ảnh overlay Grad-CAM (RGB)
        """
        self.encoder.eval()
        self.fc.eval()
        self._register_hooks()

        # Cần gradient cho backward
        x = tensor_input.clone().requires_grad_(True)

        try:
            # Forward pass qua toàn bộ pipeline artifact_encoder → fc
            feat = self.encoder(x)                    # [1, 512]
            score = self.fc(feat)                     # [1, 1]

            # Backward — gradient của score so với feature map layer2[-1]
            self.encoder.zero_grad()
            if self.fc.weight.grad is not None:
                self.fc.zero_grad()
            score.backward(torch.ones_like(score))

        finally:
            self._remove_hooks()

        # --- Grad-CAM calculation ---
        # gradients: [1, C, H, W] → Global Average Pooling → [C]
        weights = self._gradients.mean(dim=(2, 3), keepdim=True)   # [1, C, 1, 1]
        cam = (weights * self._feature_maps).sum(dim=1).squeeze(0) # [H_feat, W_feat]
        cam = torch.relu(cam).cpu().numpy()                         # Chỉ giữ activation dương

        # Normalize [0, 255]
        if cam.max() > 0:
            cam = cam / cam.max()
        cam_uint8 = (cam * 255).astype(np.uint8)

        # Resize về kích thước ảnh gốc
        h_orig, w_orig = pil_original.size[1], pil_original.size[0]
        cam_resized = cv2.resize(cam_uint8, (w_orig, h_orig), interpolation=cv2.INTER_LINEAR)

        # Áp colormap
        heatmap_bgr = cv2.applyColorMap(cam_resized, colormap)
        heatmap_rgb = cv2.cvtColor(heatmap_bgr, cv2.COLOR_BGR2RGB)

        # Overlay lên ảnh gốc
        orig_np = np.array(pil_original.convert("RGB"))
        overlay = cv2.addWeighted(orig_np, 1 - alpha, heatmap_rgb, alpha, 0)

        return Image.fromarray(overlay)

    def get_raw_cam(self, tensor_input: torch.Tensor, output_size: tuple = (224, 224)) -> np.ndarray:
        """
        Trả về raw CAM array [H, W] trong khoảng [0, 1].
        Dùng để tính chỉ số định lượng hoặc ghép vào pipeline đánh giá.
        """
        self.encoder.eval()
        self.fc.eval()
        self._register_hooks()

        x = tensor_input.clone().requires_grad_(True)
        try:
            feat = self.encoder(x)
            score = self.fc(feat)
            self.encoder.zero_grad()
            score.backward(torch.ones_like(score))
        finally:
            self._remove_hooks()

        weights = self._gradients.mean(dim=(2, 3), keepdim=True)
        cam = (weights * self._feature_maps).sum(dim=1).squeeze(0)
        cam = torch.relu(cam).cpu().numpy()
        if cam.max() > 0:
            cam = cam / cam.max()

        cam_resized = cv2.resize(cam, output_size, interpolation=cv2.INTER_LINEAR)
        return cam_resized


# ------------------------------------------------------------------ #
#  Quick test standalone                                               #
# ------------------------------------------------------------------ #
if __name__ == "__main__":
    print("GradCAMExplainer — module test mode")
    print("Import từ notebook: from gradcam import GradCAMExplainer")
    print("Xem notebook evaluation_metrics.ipynb để chạy đầy đủ.")
