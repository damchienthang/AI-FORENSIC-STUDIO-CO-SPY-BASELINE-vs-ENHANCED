# 🔬 AI-FORENSIC-STUDIO: CO-SPY BASELINE vs ENHANCED (CVPR 2025)

> **Dự án Bài tập lớn Môn Xử Lý Ảnh Số**  
> Nghiên cứu và Phát triển Hệ thống Giám định, Bóc tách Vết tích Ảnh AI Tạo sinh kết hợp Không gian Pixel (VAE) và Miền Tần số (2D-FFT).

---

## 📌 1. Giới Thiệu Tổng Quan

Dự án này kế thừa và phát triển từ công trình nghiên cứu khoa học xuất sắc tại hội nghị thị giác máy tính hàng đầu thế giới **CVPR 2025**:
* **Bài báo gốc:** *CO-SPY: Dissecting and Detecting AI-Generated Images via Latent Manifold and Semantic Discrepancy* (arXiv:2503.18286).

### Lỗ hổng của mô hình gốc (CO-SPY Baseline):
Mô hình gốc chủ yếu dựa vào mạng nơ-ron phân loại sai phân tái tạo điểm ảnh VAE $\Delta = |x - \mathcal{D}(\mathcal{E}(x))|$. Khi gặp các ảnh AI trôi nổi trên mạng xã hội (TikTok, Facebook, Reddit), ảnh bị **nén JPEG nhiều thế hệ (multi-generation lossy compression)** làm nhòe và gọt sạch các hạt micro-pixel artifacts. Điều này khiến độ nhạy bắt ảnh AI (Recall) của mô hình gốc **tụt dốc từ 99% xuống chỉ còn ~50%** (nhận nhầm hàng loạt ảnh AI thành ảnh thật).

### 4 Đột phá Cải tiến (Proposed Enhancements):
1. **Explainable AI (XAI) với Grad-CAM:** Xuất bản đồ nhiệt (Heatmap) chỉ rõ chính xác tọa độ vùng bị nghi ngờ giả mạo thay vì chỉ đưa ra xác suất "hộp đen".
2. **Nhánh Miền Tần Số 2D-FFT (Frequency-Domain Branch):** Ứng dụng biến đổi Fourier 2 chiều kết hợp bộ lọc High-Pass ($r_0 = 16$) và mạng CNN 3 lớp để bóc tách dấu vân tay mắt lưới chu kỳ (upsampling grid spikes) không bị phá hủy bởi nén JPEG.
3. **Bộ Van Điều Tiết Thích Ứng CAGU (Channel-wise Adaptive Gating Unit):** Tự động cân đối trọng số giữa miền Pixel (VAE) và miền Tần số (2D-FFT) dựa trên chất lượng và độ nén của ảnh đầu vào.
4. **Cơ Chế Kiểm Tra Chéo Hai Miền (Dual-Domain Consistency):** Lọc bỏ báo động giả (False Positive) trên các ảnh thật có hoa văn sọc lặp lại (áo kẻ, rèm cửa, lưới tản nhiệt).

---

## 📊 2. Bảng So Sánh Chỉ Số Thực Nghiệm

| Chỉ số đánh giá | CO-SPY Baseline (Gốc) | CO-SPY Enhanced (Đề xuất cải tiến) | Mức độ cải thiện |
|---|:---:|:---:|:---:|
| **Accuracy (Độ chính xác toàn diện)** | 70.0% | **92.5%** | **+22.5%** 🚀 |
| **Recall / Sensitivity (Độ nhạy bắt ảnh AI)** | 50.0% | **95.0%** | **+45.0%** 🎯 |
| **Specificity (Độ tin cậy xác nhận ảnh thật)** | 90.0% | **90.0%** | Giữ vững chất lượng |
| **F1-Score** | 0.6250 | **0.9268** | **+0.3018** |
| **AUC-ROC** | 0.7400 | **0.9600** | **+0.2200** |
| **Tính minh bạch (XAI)** | ❌ Hộp đen | ✅ **Grad-CAM + VAE Residual Heatmap** | Trực quan hóa đầy đủ |

---

## 🏗️ 3. Cấu Trúc Thư Mục Dự Án

```
AI-FORENSIC-STUDIO/
├── app.py                      # Giao diện Web Forensic Studio (Streamlit Dark Theme)
├── engine.py                   # Bộ máy suy luận kết hợp (Dual-Engine Inference Core)
├── gradcam.py                  # Module Cải tiến 1: Grad-CAM Explainable AI
├── frequency_branch.py         # Module Cải tiến 2: 2D-FFT High-Pass Filter + CNN 3 lớp
├── adaptive_fusion.py          # Module Cải tiến 3 & 4: Van CAGU + Dual-Domain Consistency
├── evaluation_metrics.ipynb    # Jupyter Notebook chạy benchmark và in đầy đủ biểu đồ chỉ số
├── chay_evaluation.bat         # File click-to-run khởi chạy nhanh Jupyter Notebook
├── BAO_CAO_TONG_KET_BTL_CO_SPY.docx # Báo cáo tổng kết đồ án chi tiết (Word)
├── Co-Spy/                     # Thư mục mã nguồn gốc và cấu trúc mạng CO-SPY
└── README.md                   # Tài liệu hướng dẫn sử dụng
```

---

## 🚀 4. Hướng Dẫn Cài Đặt & Khởi Chạy

### Bước 1: Clone kho mã nguồn
```bash
git clone https://github.com/damchienthang/AI-FORENSIC-STUDIO-CO-SPY-BASELINE-vs-ENHANCED.git
cd AI-FORENSIC-STUDIO-CO-SPY-BASELINE-vs-ENHANCED
```

### Bước 2: Cài đặt các thư viện phụ thuộc
```bash
pip install torch torchvision diffusers transformers open-clip-torch streamlit opencv-python matplotlib scikit-learn pandas
```

### Bước 3: Khởi chạy Giao diện Web Forensic Studio
```bash
python -m streamlit run app.py
```
👉 Mở trình duyệt tại địa chỉ: `http://localhost:8501`

### Bước 4: Chạy Đánh giá Chỉ số Mô hình bằng Notebook
Nhấp đúp chuột vào file `chay_evaluation.bat` hoặc chạy lệnh:
```bash
jupyter notebook evaluation_metrics.ipynb
```
Chọn **Cell** $\to$ **Run All** để tự động xuất bảng so sánh 7 chỉ số và biểu đồ phân tích ROC curve, Confusion Matrix, Boxplot năng lượng tần số.

---

## 👥 5. Tác Giả & Đóng Góp
* **Sinh viên thực hiện:** Đàm Chiến Thắng
* **Khoa / Chuyên ngành:** Kỹ thuật Điện tử / Công nghệ Thông tin - Học viện Công nghệ Bưu chính Viễn thông (PTIT)
* **Môn học:** Xử Lý Ảnh Số (Digital Image Processing)
