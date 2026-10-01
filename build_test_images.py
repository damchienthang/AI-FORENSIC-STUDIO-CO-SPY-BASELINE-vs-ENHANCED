"""
2.1 Thu thap & phan loai Bo anh Mau Kiem thu (Co-Spy-Bench) -- v5

Muc tieu (theo bang cong viec): ~25-30 anh, chia thanh
  test_images/real/      7 anh that  (COCO val2017)
  test_images/ai_sd15/   7 anh Stable Diffusion v1.5   (Co-Spy-Bench, nguon mscoco)
  test_images/ai_flux/   7 anh mo hinh moi: Midjourney v6 (toi da 3, neu tai duoc) + FLUX.1-dev (bu cho du)
  test_images/degraded/  5 anh nen mo (mo phong Facebook/Zalo)
  test_images/manifest.csv

Cach dung:
  pip install datasets pillow huggingface_hub
  python build_test_images.py build
Tuy chon: --n 7  --n-mj 3  --n-deg 5  --keep (khong xoa test_images cu)
"""
import argparse, csv, io, os, random, shutil, urllib.request
from PIL import Image

REPO = "ruojiruoli/Co-Spy-Bench"
MJ_REPO = "CortexLM/midjourney-v6"      # chi luu prompt + image_url (link co the da het han)
OUT = "test_images"
SEED = 42
UA = {"User-Agent": "Mozilla/5.0"}

# ID anh COCO val2017 (du phong nhieu hon can de bo qua anh loi)
COCO_IDS = [39769, 397133, 37777, 252219, 87038, 174482, 403385, 6818, 480985, 458054]


def save_png(img, folder, name):
    p = os.path.join(OUT, folder, name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    img.convert("RGB").save(p)
    return f"{folder}/{name}"


def degrade(img, rounds=2, quality=(30, 50), scale=0.5):
    """Gia lap anh qua Facebook/Zalo: thu nho + JPEG chat luong thap, nen lap."""
    img = img.convert("RGB")
    for _ in range(rounds):
        w, h = img.size
        img = img.resize((max(64, int(w * scale)), max(64, int(h * scale))), Image.BILINEAR)
        buf = io.BytesIO()
        img.save(buf, "JPEG", quality=random.randint(*quality))
        buf.seek(0)
        img = Image.open(buf).convert("RGB")
        scale = 0.9
    return img


def fetch_url_image(url, timeout=15):
    req = urllib.request.Request(url, headers=UA)
    data = urllib.request.urlopen(req, timeout=timeout).read()
    img = Image.open(io.BytesIO(data))
    img.load()
    return img.convert("RGB")


def get_real(n):
    items = []
    for cid in COCO_IDS:
        if len(items) >= n:
            break
        url = f"http://images.cocodataset.org/val2017/{cid:012d}.jpg"
        try:
            img = fetch_url_image(url)
        except Exception as e:
            print(f"   bo qua {url}: {e}")
            continue
        name = f"coco_{cid:012d}.png"
        items.append((save_png(img, "real", name), img, "real", "COCO val2017", f"coco_id={cid}"))
    print(f"[real] {len(items)}/{n} anh tu COCO val2017")
    return items


def get_midjourney(n_mj, max_try=60):
    items = []
    if n_mj <= 0:
        return items
    try:
        from datasets import load_dataset
        ds = load_dataset(MJ_REPO, split="train", streaming=True)
        tried = 0
        for row in ds:
            if len(items) >= n_mj or tried >= max_try:
                break
            tried += 1
            try:
                img = fetch_url_image(row["image_url"])
            except Exception:
                continue
            name = f"mj_{len(items)+1:02d}.png"
            items.append((save_png(img, "ai_flux", name), img, "fake",
                          "midjourney-v6 (CortexLM/midjourney-v6)", f"prompt={row.get('prompt','')[:200]}"))
        print(f"[midjourney] {len(items)}/{n_mj} anh (thu {tried} link)")
    except Exception as e:
        print(f"[midjourney] khong tai duoc ({e}) -> se bu bang FLUX")
    return items


def pick_tar(tars, model_kw, prefer="mscoco"):
    c = [t for t in tars if model_kw in t.lower()]
    c.sort(key=lambda t: (prefer not in t.lower(), t))
    return c[0] if c else None


def get_cospy(tar, group, prefix, n):
    from datasets import load_dataset
    print(f"[{group}] dung {tar}")
    ds = load_dataset(REPO, data_files={"train": tar}, split="train", streaming=True)
    items = []
    for i, row in enumerate(ds):
        if i >= n:
            break
        j = row.get("json") or {}
        name = f"{prefix}_{i+1:02d}.png"
        note = f"caption={j.get('caption','')}; steps={j.get('num_inference_steps','')}; cfg={j.get('guidance_scale','')}"
        img = row["png"].convert("RGB")
        items.append((save_png(img, group, name), img, "fake", row["__key__"], note))
    return items


def main(n, n_mj, n_deg, keep):
    from huggingface_hub import HfApi
    random.seed(SEED)
    if not keep and os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT, exist_ok=True)

    tars = [f for f in HfApi().list_repo_files(REPO, repo_type="dataset") if f.endswith((".tar", ".tar.gz"))]

    real = get_real(n)
    sd15 = get_cospy(pick_tar(tars, "runwayml@stable-diffusion-v1-5"), "ai_sd15", "sd15", n)
    mj = get_midjourney(n_mj)
    flux = get_cospy(pick_tar(tars, "black-forest-labs@flux.1-dev"), "ai_flux", "flux", n - len(mj))

    rows = []
    for fp, _, lab, src, note in real + sd15 + flux + mj:
        rows.append([fp, lab, src, fp.split("/")[0], note])

    # anh nen mo: 2 real + 2 sd15 + 1 flux (giu nhan goc, ghi ro anh nguon)
    deg_src = real[:2] + sd15[:2] + flux[:1]
    for i, (fp, img, lab, src, _) in enumerate(deg_src[:n_deg], 1):
        name = f"degraded_{i:02d}.jpg"
        p = os.path.join(OUT, "degraded", name)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        degrade(img).save(p, "JPEG", quality=40)
        rows.append([f"degraded/{name}", lab, src, "degraded",
                     f"from={fp}; facebook/zalo-like (resize 50% + JPEG q30-50 x2)"])

    with open(os.path.join(OUT, "manifest.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["file", "label", "source", "group", "note"])
        w.writerows(rows)

    counts = {}
    for r in rows:
        counts[r[3]] = counts.get(r[3], 0) + 1
    print("\n=== TONG KET ===")
    for g, c in counts.items():
        print(f"  {g:10s}: {c}")
    print(f"  TONG      : {len(rows)} anh -> {OUT}/manifest.csv")
    if len(rows) < 25:
        print("[!] Duoi 25 anh: kiem tra loi o tren (thieu anh COCO / Co-Spy-Bench).")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["build"])
    ap.add_argument("--n", type=int, default=7)
    ap.add_argument("--n-mj", type=int, default=3)
    ap.add_argument("--n-deg", type=int, default=5)
    ap.add_argument("--keep", action="store_true")
    a = ap.parse_args()
    main(a.n, a.n_mj, a.n_deg, a.keep)
