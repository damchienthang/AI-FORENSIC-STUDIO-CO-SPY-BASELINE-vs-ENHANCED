import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

import torch
from PIL import Image

def test_progan():
    print("Testing progan detector...")
    from detectors.progan.fusion import CoSpyFusionDetector
    sem_path = os.path.join(BASE_DIR, "pretrained", "progan", "semantic_weights.pth")
    art_path = os.path.join(BASE_DIR, "pretrained", "progan", "artifact_weights.pth")
    fus_path = os.path.join(BASE_DIR, "pretrained", "progan", "fusion_weights.pth")
    
    detector = CoSpyFusionDetector(sem_path, art_path)
    detector.load_weights(fus_path)
    detector.eval()
    
    img_path = os.path.join(BASE_DIR, "imgs", "test.png")
    img = Image.open(img_path).convert("RGB")
    tensor = detector.test_transform(img).unsqueeze(0)
    
    with torch.no_grad():
        x_sem = detector.sem_transform(tensor)
        x_art = detector.art_transform(tensor)
        p_sem = detector.sem(x_sem).sigmoid().item()
        p_art = detector.art(x_art).sigmoid().item()
        feat = torch.cat([detector.sem(x_sem), detector.art(x_art)], dim=1)
        p_fusion = detector.fc(feat).sigmoid().item()
        
    print(f"Results on {os.path.basename(img_path)}:")
    print(f"  Semantic Score: {p_sem:.4f}")
    print(f"  Artifact Score: {p_art:.4f}")
    print(f"  Fusion Score:   {p_fusion:.4f} -> {'AI-Generated' if p_fusion > 0.5 else 'Real'}")

if __name__ == "__main__":
    test_progan()



def test_sd_artifact():
    print("\nTesting sd-v1_4 artifact detector...")
    import importlib
    mod = importlib.import_module("detectors.sd-v1_4.artifact")
    ArtifactDetector = getattr(mod, "ArtifactDetector")
    art_path = os.path.join(BASE_DIR, "pretrained", "sd-v1_4", "artifact_weights.pth")
    detector = ArtifactDetector()
    detector.load_weights(art_path)
    detector.eval()
    
    img_path = os.path.join(BASE_DIR, "imgs", "test.png")
    img = Image.open(img_path).convert("RGB")
    tensor = detector.test_transform(img).unsqueeze(0)
    
    with torch.no_grad():
        score = detector.predict(tensor)[0]
    print(f"sd-v1_4 Artifact Score on test.png: {score:.4f} -> {'AI-Generated' if score > 0.5 else 'Real'}")

if __name__ == "__main__":
    test_progan()
    test_sd_artifact()
