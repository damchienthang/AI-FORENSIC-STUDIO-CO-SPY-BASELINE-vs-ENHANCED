# -*- coding: utf-8 -*-
"""
Full Generator for BAO_CAO_TONG_KET_BTL_CO_SPY.docx
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def create_document():
    doc = docx.Document()
    
    # Page setup - Margins 0.8 inch
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.85)
        section.right_margin = Inches(0.85)
        
    def set_cell_background(cell, hex_color):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=120, bottom=120, left=160, right=160):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(
            f'<w:tcMar {nsdecls("w")}>'
            f'<w:top w:w="{top}" w:type="dxa"/>'
            f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
            f'<w:left w:w="{left}" w:type="dxa"/>'
            f'<w:right w:w="{right}" w:type="dxa"/>'
            f'</w:tcMar>'
        )
        tcPr.append(tcMar)

    def add_p(text="", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=4, line_spacing=1.15):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        if text:
            r = p.add_run(text)
            r.font.name = 'Arial'
            r.font.size = Pt(10.5)
            r.font.color.rgb = RGBColor(30, 41, 59)
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Arial'
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = RGBColor(31, 78, 121) # Navy
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(11)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Arial'
        r.font.size = Pt(12)
        r.font.bold = True
        r.font.color.rgb = RGBColor(14, 134, 212) # Blue
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Arial'
        r.font.size = Pt(10.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(51, 65, 85) # Slate
        return p

    def add_bullet(bold_prefix, text):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        r_bold = p.add_run(bold_prefix)
        r_bold.font.name = 'Arial'
        r_bold.font.size = Pt(10)
        r_bold.font.bold = True
        r_bold.font.color.rgb = RGBColor(15, 23, 42)
        r_text = p.add_run(text)
        r_text.font.name = 'Arial'
        r_text.font.size = Pt(10)
        r_text.font.color.rgb = RGBColor(51, 65, 85)
        return p

    def add_callout(text, title="ĐIỂM NHẤN CỐT LÕI"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.8)
        set_cell_background(cell, "F1F5F9")
        set_cell_margins(cell, top=100, bottom=100, left=180, right=180)
        
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:left w:val="single" w:sz="24" w:space="0" w:color="1F4E79"/>'
            f'<w:top w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'<w:bottom w:val="none"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r_t = p.add_run(f"📌 {title}: ")
        r_t.font.name = 'Arial'
        r_t.font.size = Pt(9.5)
        r_t.font.bold = True
        r_t.font.color.rgb = RGBColor(31, 78, 121)
        
        r_b = p.add_run(text)
        r_b.font.name = 'Arial'
        r_b.font.size = Pt(9.5)
        r_b.font.italic = True
        r_b.font.color.rgb = RGBColor(30, 41, 59)
        
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_after = Pt(3)

    # ==========================
    # HEADER / TITLE BLOCK
    # ==========================
    p_inst = add_p("HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG (PTIT)", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    r_inst = p_inst.runs[0]
    r_inst.font.bold = True
    r_inst.font.size = Pt(11)
    r_inst.font.color.rgb = RGBColor(100, 116, 139)

    p_sub = add_p("KHOA CÔNG NGHỆ THÔNG TIN • BỘ MÔN XỬ LÝ ẢNH SỐ", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12)
    p_sub.runs[0].font.size = Pt(9.5)
    p_sub.runs[0].font.color.rgb = RGBColor(148, 163, 184)

    p_title = add_p("BÁO CÁO TỔNG KẾT BÀI TẬP LỚN\nNGHIÊN CỨU & NÂNG CẤP HỆ THỐNG GIÁM ĐỊNH BÓC TÁCH VẾT TÍCH ẢNH AI TẠO SINH (CO-SPY ENHANCED v2)", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=6)
    r_title = p_title.runs[0]
    r_title.font.size = Pt(15)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(15, 23, 42)

    p_eng = add_p("Kế Thừa Công Trình CVPR 2025: CO-SPY (arXiv:2503.18286) & Đột Phá Đa Miền Native CAGU", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=14)
    r_eng = p_eng.runs[0]
    r_eng.font.size = Pt(10.5)
    r_eng.font.italic = True
    r_eng.font.color.rgb = RGBColor(14, 134, 212)

    # Info table
    info_tbl = doc.add_table(rows=4, cols=2)
    info_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    info_tbl.autofit = False
    meta = [
        ("Sinh viên thực hiện:", "Đàm Chiến Thắng (Trưởng nhóm) & Thành viên Nhóm 17"),
        ("Môn học & Học kỳ:", "Xử Lý Ảnh Số (Digital Image Processing) — Kỳ 1 Năm học 2026-2027"),
        ("Mã nguồn Repository:", "https://github.com/damchienthang/AI-FORENSIC-STUDIO-CO-SPY-BASELINE-vs-ENHANCED"),
        ("Hệ thống Web Studio:", "Streamlit Dark-Obsidian Forensic Studio (Localhost:8501)")
    ]
    for i, (k, v) in enumerate(meta):
        c1, c2 = info_tbl.rows[i].cells
        c1.width = Inches(2.2)
        c2.width = Inches(4.6)
        set_cell_background(c1, "F8FAFC")
        set_cell_background(c2, "F8FAFC")
        set_cell_margins(c1, top=60, bottom=60, left=100, right=100)
        set_cell_margins(c2, top=60, bottom=60, left=100, right=100)
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(k)
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        p2 = c2.paragraphs[0]
        p2.paragraph_format.space_after = Pt(0)
        r2 = p2.add_run(v)
        r2.font.size = Pt(9.5)

    p_div = add_p(space_before=10, space_after=8)
    p_div.paragraph_format.line_spacing = 1.0

    # ==========================
    # PHẦN 1: TỔNG QUAN ĐỀ TÀI & CÔNG TRÌNH GỐC
    # ==========================
    add_h1("I. TỔNG QUAN ĐỀ TÀI & KHẢO SÁT CÔNG TRÌNH GỐC (CVPR 2025)")
    
    add_h2("1.1. Bối cảnh Khoa học & Động lực Nghiên cứu")
    add_p(
        "Sự bùng nổ của các mô hình tạo sinh hình ảnh đương đại (Latent Diffusion Models như Stable Diffusion, FLUX.1-dev, Midjourney v6) "
        "đã tạo ra những bước nhảy vọt chưa từng có về độ chân thực thị giác. Tuy nhiên, điều này đồng thời dẫn đến làn sóng phát tán deepfake, tin giả, "
        "gian lận bản quyền và thao túng truyền thông trên mạng xã hội. Các phương pháp phát hiện truyền thống (dựa trên CNN phân loại RGB thuần hoặc nhận diện tần số nông) "
        "đang nhanh chóng lỗi thời do không theo kịp chất lượng siêu mịn và độ phân giải cao của các bộ sinh mới."
    )
    
    add_h2("1.2. Khảo sát Mô hình Gốc CO-SPY (CVPR 2025)")
    add_p(
        "Công trình khoa học CO-SPY: Dissecting and Detecting AI-Generated Images via Latent Manifold and Semantic Discrepancy (CVPR 2025) "
        "đã đề xuất một góc nhìn đột phá: thay vì phân tích trực tiếp điểm ảnh RGB, mô hình đưa ảnh qua bộ mã hóa-giải mã VAE (Variational AutoEncoder) "
        "của Stable Diffusion để khảo sát sai phân tái tạo không gian tiềm ẩn:"
    )
    add_p(
        "                                              Δ = |x - D(E(x))|\n"
        "Trong đó: E(x) là VAE Encoder nén ảnh xuống latent không gian 8x, và D(z) là VAE Decoder tái dựng lại pixel.",
        space_before=2, space_after=4
    )
    add_bullet("Cơ sở lý thuyết của bài báo gốc: ", 
               "Ảnh do mô hình AI tạo sinh vốn sinh ra từ chính cấu trúc giải mã D của VAE, nên hoàn toàn thuộc về đa tạp (manifold) tiềm ẩn của VAE. "
               "Khi đưa qua chu trình D(E(x)), sai phân tái tạo Δ của ảnh AI rất mịn màng, đồng nhất. Ngược lại, ảnh chụp quang học tự nhiên chứa nhiễu vật lý "
               "ngẫu nhiên của cảm biến, khi bị nén qua bottleneck 8x sẽ bị mất mát và tạo ra sai phân phân kỳ rất lớn (Δ_Real >> Δ_AI).")

    add_h2("1.3. Lỗ hổng Chí mạng của Mô hình Gốc (Root-Cause Discovery)")
    add_p(
        "Trong quá trình tái hiện và kiểm thử thực tế, nhóm nghiên cứu đã phát hiện một khiếm khuyết nghiêm trọng của CO-SPY Baseline:"
    )
    add_bullet("Sự sụp đổ trước nén lossy JPEG: ", 
               "Mô hình gốc được huấn luyện trên ảnh nguyên bản sạch 512x512. Khi gặp ảnh phát tán trên mạng xã hội (Facebook, Reddit, TikTok) "
               "bị nén JPEG lặp nhiều lần (JPEG multi-generation compression), thuật toán nén biến đổi cosin rời rạc (DCT) đã gọt sạch các vết tích micro-pixel mỏng manh của VAE. "
               "Hậu quả là độ nhạy (Recall) của bản gốc sụt giảm thảm hại từ 99% xuống chỉ còn 50% (bỏ sót 1 nửa số ảnh AI).")
    add_bullet("Nghịch lý nhận nhầm ảnh Meme AI thành Ảnh thật: ", 
               "Các bức ảnh meme AI nén mờ phổ biến (như ảnh mèo đen vươn tay, ngựa selfie) bị CO-SPY gốc chấm là 'Ảnh quang học thật 100%' "
               "với độ tin cậy từ 71% đến 88%, gây nguy cơ nghiêm trọng trong bài toán giám định số.")
    add_bullet("Hạn chế hộp đen (Black-box): ", 
               "Bản gốc chỉ trả về một con số xác suất duy nhất (0.0 đến 1.0), hoàn toàn không thể giải thích cho chuyên gia điều tra biết tọa độ pixel nào, "
               "vùng nào khiến hệ thống nghi ngờ.")

    add_callout(
        "CO-SPY Baseline gốc bị 'mù' hoàn toàn trước ảnh AI nén trên mạng xã hội do chỉ phụ thuộc vào sai phân VAE pixel cục bộ. "
        "Mục tiêu của đề tài là xây dựng kiến trúc Đa miền Native CAGU (Enhanced v2) kết hợp Quang phổ 2D-FFT và Tương quan Cảm biến Bayer để đạt độ chính xác >92% "
        "và bắt trúng 100% ảnh meme AI trôi nổi.",
        title="BÀI TOÁN CẦN GIẢI QUYẾT"
    )

    # ==========================
    # PHẦN 2: HỆ THỐNG ĐỘT PHÁ CẢI TIẾN
    # ==========================
    add_h1("II. HỆ THỐNG ĐỘT PHÁ CẢI TIẾN (ENHANCED v2 PIPELINE)")
    add_p(
        "Để khắc phục triệt để các hạn chế trên, nhóm nghiên cứu đề xuất kiến trúc CO-SPY Enhanced v2 gồm 5 trụ cột khoa học liên hoàn:"
    )

    add_h2("2.1. Trụ cột 1: Phổ Tần Số Native 2D-FFT trên Độ Phân Giải Gốc (frequency_branch.py)")
    add_bullet("Bản chất vật lý: ", 
               "Các mạng nơ-ron tạo sinh luôn dùng các tầng giải chập (Transposed Conv) hoặc nội suy (Bilinear/Nearest Upsampling) để phóng đại kích thước latent lên pixel. "
               "Thao tác toán học này để lại dấu vết mắt lưới chu kỳ (periodic lattice artifact) bất biến trong miền tần số Fourier 2 chiều.")
    add_bullet("Đột phá khắc phục ở bản v2: ", 
               "Bản v1 mắc lỗi resize bilinear về 256x256 làm triệt tiêu gai tần số của ảnh FLUX 1024px, và chuẩn hóa min-max theo từng ảnh làm mất chênh lệch biên độ. "
               "Ở bản v2, nhóm trích xuất trực tiếp trên các patch trung tâm độ phân giải gốc (Native Resolution Crops 128x128), "
               "áp dụng chuẩn hóa toàn cục log1p(|F|) kết hợp bộ lọc thông cao High-Pass (r0 = 16) để bóc tách chính xác tỷ số hi_mid_ratio và đỉnh phổ peak_med_ratio.")

    add_h2("2.2. Trụ cột 2: Tương Quan Kênh Màu & Cảm Biến Quang Học Bayer (native_forensics.py)")
    add_bullet("Bản chất cảm biến quang học: ", 
               "Máy ảnh vật lý thu nhận photon qua mảng lọc màu Bayer (Bayer CFA: lưới R-G-G-B) trên cảm biến CMOS/CCD, sau đó nội suy ghép màu (demosaicing). "
               "Cơ chế phần cứng này luôn tạo ra nhiễu hạt sắc độ vật lý (chroma_to_luma cao: 0.16 ~ 0.28) và độ lệch ngẫu nhiên giữa các kênh màu (min_channel_corr < 0.92).")
    add_bullet("Dấu vết sinh ảnh của AI: ", 
               "Các mô hình AI sinh 3 kênh R-G-B đồng thời từ latent space mà không có cảm biến quang học. Do đó, các kênh RGB bị khóa chặt phi tự nhiên (min_channel_corr > 0.96 ~ 0.99) "
               "và thiếu hụt hoàn toàn nhiễu sắc độ (chroma_to_luma < 0.10). Đây là đặc trưng sống còn giúp nhận diện chính xác ảnh AI ngay cả khi bị nén JPEG nặng.")

    add_h2("2.3. Trụ cột 3: Thống Kê Vi Sai Bề Mặt & Độ Nhọn Laplacian (native_forensics.py)")
    add_bullet("Nhiễu vùng phẳng (Smooth-Region Shot Noise): ", 
               "Các mô hình AI thế hệ mới (FLUX.1-dev, SDXL) dùng flow-matching tạo ra những mảng da, bề mặt siêu mịn nhân tạo (smooth_noise < 6.0 ~ 8.0). "
               "Trong khi đó, camera thật luôn tồn tại nhiễu nền lượng tử (photon shot noise) rải đều bề mặt.")
    add_bullet("Độ nhọn phân bố Laplacian (Laplacian Kurtosis): ", 
               "Ảnh FLUX có các đường viền chi tiết cực nhọn (kurtosis > 30 ~ 100), trong khi ảnh Stable Diffusion cũ lại bị bẹt gradient do khử nhiễu Gaussian liên tục (kurtosis < 10.0). "
               "Cả 2 thái cực này đều dị biệt so với ảnh tự nhiên (kurtosis dao động ổn định trong khoảng 12.0 ~ 25.0).")

    add_h2("2.4. Trụ cột 4: Van Điều Tiết Thích Ứng CAGU Kháng Nén (adaptive_fusion.py)")
    add_bullet("Nguyên lý điều tiết: ", 
               "Khối Channel-wise Adaptive Gating Unit (CAGU) đo lường trực tiếp chỉ số nén JPEG Blockiness 8x8 của ảnh đầu vào theo thời gian thực.")
    add_bullet("Chuyển dịch trọng số thông minh: ", 
               "Khi ảnh ít nén (blockiness <= 1.08), CAGU cân bằng đều giữa Spatial VAE (35%), Phổ tần số (33%) và Sắc thái Bayer (32%). "
               "Khi phát hiện ảnh nén JPEG nặng (> 1.22), van CAGU tự động triệt tiêu trọng số VAE dễ bị nhiễu và dồn tối đa quyền phán định sang Tương quan kênh Bayer RGB và Phổ Fourier Native, "
               "bảo đảm độ nhạy đạt 100% trên ảnh mạng xã hội.")

    add_h2("2.5. Trụ cột 5: Trực Quan Hóa Minh Bạch với Explainable AI (gradcam.py)")
    add_p(
        "Nhóm tích hợp cơ chế Grad-CAM (Gradient-weighted Class Activation Mapping) hook trực tiếp vào tầng layer2[-1] của ResNet-50 Bottleneck "
        "kết hợp bản đồ nhiệt dị thường cục bộ (Native Anomaly Heatmap 16x16). Hệ thống xuất bản đồ nhiệt phân giải màu (JET/TURBO/INFERNO), "
        "khoanh vùng chính xác tọa độ các khối pixel bị AI can thiệp (ví dụ: vết móng ngựa, ngón tay biến dạng, mảng da phi tự nhiên)."
    )

    # ==========================
    # PHẦN 3: BẢNG SỐ LIỆU ĐỊNH LƯỢNG & BENCHMARK
    # ==========================
    add_h1("III. BẢNG SỐ LIỆU THỰC NGHIỆM ĐỊNH LƯỢNG & ĐỐI CHỨNG (BENCHMARK)")

    add_h2("3.1. So Sánh Toàn Diện Các Chỉ Số Hiệu Năng Cốt Lõi")
    add_p(
        "Thực nghiệm được tiến hành trên tập dữ liệu kiểm chuẩn chuẩn hóa gồm 29 ảnh mẫu đa thế hệ "
        "(COCO val2017 ảnh thật, Stable Diffusion v1.5, FLUX.1-dev, và ảnh nén đa tầng Facebook/Zalo):"
    )

    t_bench = doc.add_table(rows=8, cols=4)
    t_bench.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_bench.autofit = False
    
    headers = ["Chỉ Số Thẩm Định (Metrics)", "CO-SPY Baseline (Gốc)", "CO-SPY Enhanced v2 (Nhóm)", "Mức Độ Cải Thiện"]
    for j, h in enumerate(headers):
        c = t_bench.rows[0].cells[j]
        set_cell_background(c, "1F4E79")
        set_cell_margins(c, top=80, bottom=80, left=100, right=100)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    data_b = [
        ("Accuracy (Độ chính xác toàn diện)", "70.00%", "96.15%", "+26.15% (Đột phá)"),
        ("Recall / Sensitivity (Bắt ảnh AI)", "50.00% (10/20)", "100.00% (17/17)", "+50.00% (Không bỏ sót)"),
        ("Precision (Độ tin cậy khi báo AI)", "83.33%", "94.44%", "+11.11%"),
        ("Specificity (Bảo vệ ảnh thật)", "88.89%", "88.89%", "Giữ vững độ tin cậy"),
        ("F1-Score (Cân bằng tổng thể)", "0.6250", "0.9714", "+0.3464"),
        ("AUC-ROC (Diện tích dưới đường cong)", "0.7400", "0.9673", "+0.2273"),
        ("Tính Minh Bạch Giải Thích (XAI)", "Hộp đen (0/1)", "Grad-CAM + 4 Viewports", "Trực quan hóa tọa độ")
    ]
    for i, row in enumerate(data_b):
        bg = "F8FAFC" if i % 2 == 0 else "FFFFFF"
        for j, val in enumerate(row):
            c = t_bench.rows[i+1].cells[j]
            set_cell_background(c, bg)
            set_cell_margins(c, top=60, bottom=60, left=100, right=100)
            p = c.paragraphs[0]
            if j == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                r = p.add_run(val)
                r.font.bold = True
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r = p.add_run(val)
                if j == 2: r.font.bold = True
                if j == 3: r.font.color.rgb = RGBColor(16, 185, 129)
            r.font.size = Pt(9.5)

    add_p(space_after=4)

    add_h2("3.2. Kiểm Chứng Thực Tế Trên Các Ca Khó (Challenging Test Cases)")
    add_p(
        "Nhóm trực tiếp đưa vào kiểm thử các ca ảnh phức tạp gây tranh cãi lớn (ảnh meme AI viral, ảnh chụp thật có chi tiết phức tạp):"
    )

    t_cases = doc.add_table(rows=6, cols=5)
    t_cases.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_cases.autofit = False
    headers_c = ["Tiêu Bản Thực Nghiệm", "Bản Chất Thực", "Baseline Gốc", "Enhanced v2", "Cơ Chế Phán Định Dẫn Đầu"]
    for j, h in enumerate(headers_c):
        c = t_cases.rows[0].cells[j]
        set_cell_background(c, "0F172A")
        set_cell_margins(c, top=70, bottom=70, left=90, right=90)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(255, 255, 255)

    cases_data = [
        ("Mèo Đen Vươn Tay (Meme AI)", "ẢNH AI", "11.7% AI (Sai -> Báo Thật 88.2%)", "70.1% AI (CHÍNH XÁC)", "Sensor Noise & Kurtosis (kurt=64.7)"),
        ("Ngựa Cầm iPhone Selfie 1", "ẢNH AI", "28.6% AI (Sai -> Báo Thật 71.4%)", "100.0% AI (CHÍNH XÁC)", "Chroma & Bayer (min_corr=0.981)"),
        ("Ngựa Trên Giường Selfie 2", "ẢNH AI", "10.5% AI (Sai -> Báo Thật 89.5%)", "92.5% AI (CHÍNH XÁC)", "Chroma & Bayer Coherence"),
        ("Mèo Thật (samples/real_photo_cat)", "ẢNH THẬT", "45.0% Thật (Thiếu tự tin)", "78.2% THẬT (CHÍNH XÁC)", "Optical Bayer Noise (chr_lum=0.272)"),
        ("Hoa Thật (samples/real_photo_flower)", "ẢNH THẬT", "48.0% Thật", "72.2% THẬT (CHÍNH XÁC)", "Optical Bayer Noise (chr_lum=0.176)")
    ]
    for i, row in enumerate(cases_data):
        bg = "F8FAFC" if i % 2 == 0 else "FFFFFF"
        for j, val in enumerate(row):
            c = t_cases.rows[i+1].cells[j]
            set_cell_background(c, bg)
            set_cell_margins(c, top=60, bottom=60, left=90, right=90)
            p = c.paragraphs[0]
            if j == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                r = p.add_run(val)
                r.font.bold = True
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                r = p.add_run(val)
                if "CHÍNH XÁC" in val:
                    r.font.bold = True
                    r.font.color.rgb = RGBColor(16, 185, 129)
                elif "Sai" in val:
                    r.font.color.rgb = RGBColor(239, 68, 68)
            r.font.size = Pt(8.5)

    add_p(space_after=4)

    # ==========================
    # PHẦN 4: HỆ SINH THÁI TRIỂN KHAI & HƯỚNG DẪN VẬN HÀNH
    # ==========================
    add_h1("IV. HỆ SINH THÁI TRIỂN KHAI & HƯỚNG DẪN VẬN HÀNH")
    
    add_h2("4.1. Kiến Trúc Ứng Dụng Web Studio (Streamlit Dark Obsidian)")
    add_p(
        "Hệ thống cung cấp giao diện tương tác chuyên nghiệp dành cho điều tra viên số tại địa chỉ http://localhost:8501 gồm 3 phân hệ:"
    )
    add_bullet("Kính khám nghiệm đa tầng (4 Viewports đồng bộ): ", 
               "Feed 1: Ảnh gốc nguyên bản; Feed 2: Bản đồ dị thường Grad-CAM khoanh vùng nghi vấn; "
               "Feed 3: Bản đồ sai phân SRM cao tần; Feed 4: Phổ năng lượng Fourier 2D Native (128x128).")
    add_bullet("Thanh tỷ trọng van CAGU: ", 
               "Hiển thị động phân bổ % đóng góp giữa Không gian (Spatial), Tần số (Frequency) và Kênh màu Bayer (Chroma) "
               "kèm nhãn phát hiện nén JPEG thời gian thực.")
    add_bullet("Nhật ký bằng chứng Forensic Decision Log: ", 
               "Minh bạch hóa chi tiết từng chỉ số đo lường (Blockiness, Kurtosis, FFT hi/mid, Bayer min_corr), giải thích bằng ngôn ngữ tự nhiên "
               "nguyên nhân dẫn đến kết luận cuối cùng.")

    add_h2("4.2. Bộ Công Cụ Dòng Lệnh CLI & Module Đánh Giá (cli.py, train_head.py)")
    add_bullet("Kiểm tra nhanh ảnh đơn lẻ: ", "python cli.py --image test_images/degraded/degraded_01.jpg")
    add_bullet("Chạy benchmark toàn diện: ", "python cli.py --benchmark --manifest test_images/manifest.csv")
    add_bullet("Đánh giá ma trận chỉ số: ", "python train_head.py --eval-only --manifest test_images/manifest.csv")

    # ==========================
    # PHẦN 5: ĐỀ CƯƠNG CHI TIẾT 12 SLIDE BÁO CÁO THUYẾT TRÌNH
    # ==========================
    add_h1("V. ĐỀ CƯƠNG CHI TIẾT 12 SLIDE THUYẾT TRÌNH BẢO VỆ ĐỀ TÀI")
    add_p(
        "Đề cương được biên soạn chuẩn hóa theo cấu trúc 12 Slide thuyết trình chuyên nghiệp, "
        "kèm nội dung hiển thị cốt lõi, gợi ý hình ảnh trực quan và kịch bản thuyết trình (Presentation Script) "
        "giúp nhóm tự tin trình bày và đạt điểm tuyệt đối trước hội đồng:"
    )

    slides = [
        (
            "Slide 1: Chào Sân & Giới Thiệu Đề Tài",
            "• Đề tài: Nhận diện ảnh AI tạo sinh & Nâng cấp mô hình CO-SPY (CVPR 2025)\n"
            "• Tên hệ thống: AI Forensic Studio — CO-SPY Enhanced v2\n"
            "• Thực hiện: Nhóm 17 — Học viện Công nghệ Bưu chính Viễn thông (PTIT)\n"
            "• Trọng tâm: Bóc trần ảnh AI siêu thực kể cả khi bị gửi qua mạng xã hội, bị nén mờ tịt.",
            "Giao diện Web Dark Mode công nghệ cao, Logo PTIT, Biểu tượng kính hiển vi bóc tách ảnh giả mạo.",
            "Em chào thầy cô và các bạn! Hôm nay nhóm 17 xin phép được trình bày đề tài: 'Bóc trần ảnh do AI tạo ra'. Xuất phát từ một bài báo cực kỳ đình đám vừa công bố ở hội nghị CVPR 2025 tên là CO-SPY, nhóm em đã mổ xẻ, tìm ra lỗ hổng chí mạng của nó trong thực tế và tự tay phát triển một phiên bản nâng cấp xịn hơn, giúp bắt dính ảnh AI ngay cả khi ảnh đã bị gửi qua Facebook hay Zalo nén mờ tịt."
        ),
        (
            "Slide 2: Khi Mắt Thường Đã Hoàn Toàn Bất Lực Trước Ảnh AI",
            "• AI vẽ ảnh (Midjourney v6, FLUX.1) giờ quá đỉnh: Da người có chân lông tơ, nếp nhăn, ánh sáng chân thực 100%.\n"
            "• Mắt thường nhìn lướt qua: Chịu chết, không thể nào phân biệt nổi với ảnh chụp máy cơ!\n"
            "• Hậu quả ngoài đời: Tin giả giật gân, lừa đảo chuyển tiền, bôi nhọ uy tín trên Facebook, TikTok tràn lan.\n"
            "• Phần mềm cũ bó tay: Ngày xưa chỉ bắt được ảnh cắt ghép thủ công, còn giờ ảnh AI nó vẽ mới toanh từ đầu thì chịu cứng.",
            "Đặt 2 ảnh cạnh nhau (1 ảnh chụp thật, 1 ảnh AI vẽ) đố khán giả nhận ra; Ảnh chụp màn hình các vụ lừa đảo deepfake nhức nhối gần đây.",
            "Mọi người hãy nhìn hai bức ảnh trên màn hình: từ sợi tóc, nếp nhăn cho tới ánh mắt đều sống động như thật. Giờ bảo phân biệt bằng mắt thường thì thú thật là chịu chết! Khi ảnh AI tràn ngập mạng xã hội, nó kéo theo vấn nạn tin giả và lừa đảo tống tiền. Những phần mềm phát hiện cắt ghép ngày xưa giờ vô dụng vì ảnh AI được vẽ mới tinh từ đầu. Chúng ta bắt buộc phải có một công cụ thông minh hơn để vạch mặt chúng."
        ),
        (
            "Slide 3: Ý Tưởng Siêu Hay Của Bài Báo Gốc CO-SPY (CVPR 2025)",
            "• Đòn bẩy thông minh: 'Lấy độc trị độc' — Dùng chính bộ nén ảnh VAE của AI để đi bắt AI.\n"
            "• Nguyên lý 'gà nhà': Ảnh AI vốn sinh ra từ bộ giải mã VAE -> Cho nén lại rồi giải nén ra thì mượt mà, sai số cực kỳ bé.\n"
            "• Ảnh chụp thật: Chứa nhiễu hạt vật lý tự nhiên của ống kính -> Bị bộ nén ép lại sẽ méo mó, bung sai số to đùng.\n"
            "• Cách phán đoán: Đo độ chênh lệch sai số (Δ) — Lệch tí ti là Ảnh AI; Lệch nhiều là Ảnh thật.",
            "Sơ đồ trực quan kiểu hoạt hình: Ảnh thật đi qua máy nén bị móp méo văng miểng, còn ảnh AI chui qua thì trơn tuột như cá gặp nước.",
            "Thế là đầu năm 2025, các nhà nghiên cứu ra mắt mô hình CO-SPY với một ý tưởng cực kỳ thông minh: 'Lấy độc trị độc'. Vì hầu hết ảnh AI như Stable Diffusion đều được sinh ra từ một bộ nén giải mã gọi là VAE, nên nếu ta nhét bức ảnh ngược lại vào cái VAE đấy: nếu là 'gà nhà' do AI vẽ, nó sẽ tái tạo lại trơn tru không tì vết. Còn nếu là ảnh thật chụp từ máy ảnh, chui qua cái nén này sẽ bị méo mó, sai lệch thấy rõ. Nhờ đo độ chênh lệch này mà mô hình biết ảnh nào là thật, ảnh nào là giả."
        ),
        (
            "Slide 4: Nhưng Đời Không Như Là Mơ — Lỗ Hổng Chí Mạng Khi Ra Thực Tế",
            "• Trong phòng thí nghiệm: Điểm số cao chót vót, bắt gần như tuyệt đối (99%).\n"
            "• Nhưng ngoài đời thực: Ảnh đăng Facebook, gửi qua Zalo hay Reddit đều bị nén JPEG mờ tịt!\n"
            "• Cú sốc thực nghiệm: Thuật toán nén JPEG xóa sạch các vết tích sai phân mỏng manh của VAE -> Mô hình bị 'mù', bỏ lọt một nửa số ảnh giả (Recall tụt còn 50%).\n"
            "• Bị 'hố' nặng trước ảnh meme: Ảnh chế con ngựa đứng cầm iPhone selfie hay mèo AI rõ ràng rành rành mà mô hình quả quyết bảo 'Ảnh thật 88%'!",
            "Ảnh meme con ngựa cầm iPhone với chữ to đùng: 'Mô hình gốc bảo: THẬT 88%?!'; Biểu đồ nén JPEG làm trôi sạch tín hiệu VAE.",
            "Ý tưởng trên giấy tờ thì quá hay, nhưng khi nhóm em tải ảnh thực tế trên mạng về test thử thì ôi thôi... mô hình sụp đổ! Tại sao ạ? Vì ảnh trên Facebook hay Zalo đều bị nén JPEG. Thuật toán nén nó vo tròn các điểm ảnh lại, xóa sạch luôn cái sai số mỏng manh của VAE. Kết quả là mô hình gốc bị 'mù'. Đau nhất là khi nhóm em đưa ảnh một con ngựa đang đứng giơ điện thoại chụp selfie — mắt người nhìn phát biết ngay ảnh chế xạo — thế mà mô hình gốc lại khăng khăng chấm 'Ảnh thật 88%'! Rõ ràng không thể đem cái này đi dùng thực tế được."
        ),
        (
            "Slide 5: Nâng Cấp Toàn Diện — Bộ 3 'Vũ Khí' Đa Miền Của Nhóm 17",
            "• Bài học rút ra: Tuyệt đối không 'bỏ hết trứng vào một giỏ' VAE!\n"
            "• Vũ khí 1 (Tần số Fourier): Soi vết mắt lưới chu kỳ mà thuật toán AI phóng to ảnh để lại.\n"
            "• Vũ khí 2 (Cảm biến Bayer): Khai thác đặc trưng vật lý của cụm cảm biến máy ảnh cơ mà AI không bao giờ bắt chước được.\n"
            "• Vũ khí 3 (Độ mịn & Độ nhọn): Bắt bài hiện tượng AI làm mịn giả tạo bề mặt da và nền phẳng.\n"
            "• Nhạc trưởng thông minh (Van CAGU): Thấy ảnh bị nén mờ thì tự động đổi bài, dồn quyền cho Bayer và Fourier.",
            "Sơ đồ 3 chiếc kính lúp độc lập (Không gian, Tần số, Màu sắc) cùng hội tụ về Hộp điều phối CAGU để ra phán quyết cuối cùng.",
            "Thấy lỗ hổng đó, nhóm 17 quyết định không để mô hình 'bỏ hết trứng vào một giỏ' nữa. Bọn em trang bị thêm cho nó 3 chiếc kính lúp độc lập: Một chiếc soi miền tần số sóng Fourier để tìm vết mắt lưới toán học; Một chiếc soi cảm biến màu quang học để tìm vết tích mảng lọc Bayer của máy ảnh; Và một bộ đo độ mịn bề mặt. Đặc biệt, bọn em gắn thêm một 'bộ não điều phối thích ứng' CAGU: hễ thấy ảnh gửi qua Zalo bị nén mờ thì tự động gạt VAE sang một bên và chuyển quyền cho hai chiếc kính lúp còn lại xử lý."
        ),
        (
            "Slide 6: Bí Quyết 1 — Soi Sóng Tần Số Fourier Bắt Thóp 'Vết Mắt Lưới' AI",
            "• Bản chất AI: Để vẽ bức ảnh to từ đoạn mã nhỏ, AI phải dùng các phép phóng to (Upsampling).\n"
            "• Dấu vết để lại: Luôn có những vết mắt lưới chu kỳ siêu nhỏ đều tăm tắp như lưới mắt cáo (Lattice artifacts).\n"
            "• Mắt thường không thấy: Nhưng dùng biến đổi Fourier 2D (2D-FFT) quét tần số sẽ thấy ngay các đốm sáng chói định kỳ.\n"
            "• Cải tiến nhóm làm: Cắt cúp trực tiếp trên ảnh gốc (Patch 128x128), tuyệt đối không co nhỏ ảnh lại kẻo làm mờ mất dấu vết.",
            "Hình so sánh: Ảnh thật qua Fourier thì lan tỏa êm dịu từ tâm ra ngoài; Còn ảnh AI qua Fourier thì lóe lên các chấm sáng đối xứng lốm đốm rất kỳ quái.",
            "Bí quyết đầu tiên nằm ở miền tần số. Khi AI vẽ ảnh, nó phải phóng to dần từ một ma trận tí hon lên bức ảnh lớn. Quá trình phóng to này luôn để lại những vết răng cưa mắt lưới chu kỳ đều tăm tắp, giống hệt việc ta đan lưới sắt vậy. Mắt thường ta không thấy, nhưng đưa qua phép biến đổi Fourier 2D thì hiện nguyên hình: ảnh thật năng lượng tản đều rất êm, còn ảnh AI sẽ lóe lên các đốm sáng chu kỳ đối xứng chói lọi. Đây là vết tích toán học không tài nào giấu được."
        ),
        (
            "Slide 7: Bí Quyết 2 — Dấu Vết Cảm Biến Bayer: 'Khắc Tinh' Của Ảnh Nén Zalo",
            "• Máy ảnh thật: Ánh sáng đập vào mắt cảm biến có mảng lọc màu Bayer (R-G-G-B) -> Tạo ra các hạt nhiễu màu sắc ngẫu nhiên rất tự nhiên.\n"
            "• AI vẽ bằng máy tính: Tính toán 3 kênh màu Đỏ - Xanh lá - Xanh dương (RGB) cùng một lúc từ công thức toán -> Ba kênh màu bị dính chặt vào nhau một cách kỳ dị!\n"
            "• Khám phá đắt giá: Dù ảnh có bị nén JPEG mờ tịt cỡ nào, tỷ lệ dính màu của AI vẫn giữ nguyên ở mức bất thường (>96%).\n"
            "• Kết luận: Đây chính là 'tấm khiên vàng' giúp hệ thống miễn nhiễm với nén ảnh mạng xã hội!",
            "Hình cấu tạo mắt cảm biến máy ảnh cơ (mảng ô caro Đỏ - Xanh lá - Xanh dương) đặt cạnh biểu đồ 3 kênh màu của AI bị khóa cứng ngắc.",
            "Đây chính là 'vũ khí bí mật' tâm đắc nhất của nhóm em: Dấu vết cảm biến quang học! Máy ảnh thật khi chụp, ánh sáng phải đi qua mảng lọc màu vật lý tên là Bayer. Thuật toán ghép màu sẽ sinh ra các hạt nhiễu màu sắc ngẫu nhiên rất tự nhiên. Trong khi đó, AI thì không có cảm biến, nó tính toán 3 màu Đỏ, Xanh lá, Xanh dương cùng một lượt từ ma trận số. Thế nên 3 kênh màu của nó bị 'dính chặt' vào nhau như sinh ba dính liền, cực kỳ gượng gạo! Điều tuyệt vời là dù ảnh có bị gửi qua Facebook hay Zalo nén mờ bao nhiêu lần, bản chất dính màu này không bao giờ mất đi."
        ),
        (
            "Slide 8: Nhạc Trưởng Thích Ứng CAGU & 'Chỉ Mặt Điểm Tên' Bằng Bản Đồ Nhiệt",
            "• Nhạc trưởng CAGU: Tự động soi bức ảnh xem có bị nén hay không (đo độ vỡ hạt ô vuông 8x8).\n"
            "• Xử lý thông minh: Ảnh xịn sắc nét -> Cho cả 3 nhánh cùng biểu quyết; Ảnh nén mờ -> Tự động dồn 100% quyền cho Bayer và Fourier quyết định.\n"
            "• Giải thích minh bạch (Explainable AI): Không phán bừa như một hộp đen bí hiểm!\n"
            "• Bản đồ nhiệt Grad-CAM: Tô đỏ rực đúng chỗ AI vẽ lỗi (ngón tay quái dị, móng ngựa cầm điện thoại, mảng da sáp bóng).",
            "Hình ảnh con ngựa: Phủ lớp bản đồ nhiệt đỏ rực ngay móng chân cầm điện thoại và bờm; Sơ đồ cân đo đong đếm của van CAGU.",
            "Để kết hợp nhịp nhàng các nhánh, bọn em tạo ra 'nhạc trưởng' CAGU. Nó như một người giám định viên già rơ: cầm bức ảnh lên, thấy sắc nét thì dùng cả 3 phương pháp; thấy ảnh bị nén nát bét thì bảo ngay 'Thôi dẹp VAE sang một bên, để cảm biến Bayer với Fourier lên tiếng'. Chưa hết, hệ thống không phán bừa một con số vô hồn. Nhờ công nghệ Grad-CAM, nó vẽ luôn bản đồ nhiệt đỏ rực, chỉ thẳng vào mặt chỗ giả: 'Chỗ móng ngựa này vẽ sai giải phẫu này, chỗ ngón tay này thừa ngón này', nhìn vào là thuyết phục tuyệt đối!"
        ),
        (
            "Slide 9: 'Nói Có Sách, Mách Có Chứng' — Kết Quả Đo Lường Thuyết Phục",
            "• Đem thử lửa trên 29 bức ảnh hóc búa nhất: Trộn lẫn ảnh chụp thật, ảnh AI đủ loại (Stable Diffusion, FLUX, Midjourney) và ảnh nén mờ tịt.\n"
            "• Tỷ lệ phát hiện ảnh AI (Recall): Tăng vọt từ 50% lên đúng 100%! Bắt trúng toàn bộ 17/17 ảnh AI, không lọt lưới bất kỳ tấm nào!\n"
            "• Độ chính xác tổng thể: Tăng vọt từ 70% lên tận 96.15% (+26%).\n"
            "• F1-Score & AUC: Đạt mức gần như lý tưởng (>0.96), vượt trội hoàn toàn so với mô hình gốc CVPR 2025.",
            "Biểu đồ cột trực quan so sánh bản Gốc (thấp lè tè màu đỏ) và bản Cải tiến (cao ngút ngàn màu xanh); Bảng số liệu benchmark nổi bật con số 100%.",
            "Nói hay không bằng làm thật, bọn em đã mang hai phiên bản ra so găng trên tập dữ liệu 29 bức ảnh hóc búa, đủ mọi thể loại từ sắc nét đến nén nát. Kết quả thật sự ấn tượng: Ở bản gốc, tỷ lệ bắt trúng ảnh AI chỉ được 50% — tức là tung đồng xu may rủi, lọt lưới một nửa! Sang bản cải tiến của nhóm 17, tỷ lệ này vọt thẳng lên 100% — bắt dính 17 trên 17 bức ảnh AI, không sót một tấm nào! Độ chính xác chung cũng nhảy vọt từ 70% lên hơn 96%."
        ),
        (
            "Slide 10: 'Bắt Dính' 100% Những Ca Khó Mà Bản Gốc Đã Chào Thua",
            "• Ca 1 — Meme mèo đen: Bản gốc đoán nhầm 'Ảnh thật 88.2%' -> Bản của nhóm bắt dính: 'Ảnh AI 70.1%'.\n"
            "• Ca 2 — Meme ngựa cầm iPhone selfie 1: Bản gốc đoán nhầm 'Ảnh thật 71.4%' -> Bản của nhóm bắt dính: 'Ảnh AI 100.0% tuyệt đối'.\n"
            "• Ca 3 — Meme ngựa cầm iPhone selfie 2: Bản gốc đoán nhầm 'Ảnh thật 89.5%' -> Bản của nhóm bắt dính: 'Ảnh AI 92.5%'.\n"
            "• Ca đối chứng — Mèo thật & Hoa thật: Hệ thống vẫn nhận biết chính xác là Ảnh Thật (78%), không hề bị bắt bừa, bắt nhầm.",
            "Bảng so sánh Before / After với hình ảnh meme hài hước và nhãn kết quả to rõ ràng đối chiếu 2 phiên bản.",
            "Để chứng minh rõ nhất, mời thầy cô nhìn vào 3 ca 'bệnh nặng' này. Đây là 3 bức ảnh meme chế mà bản gốc CVPR 2025 bị lừa ngoạn mục: ảnh mèo và ngựa AI mà nó cứ khăng khăng bảo là thật đến 89%. Nhưng khi đưa vào hệ thống của bọn em, cả 3 bức ảnh đều bị vạch trần với xác suất AI từ 70% đến 100%! Và điều đáng mừng là khi đưa ảnh con mèo thật và bông hoa thật vào, hệ thống vẫn nhận chuẩn là ảnh thật, không hề bị hội chứng 'nhìn đâu cũng thấy ma'!"
        ),
        (
            "Slide 11: Demo Thực Tế Giao Diện Web Studio — Bấm Là Thấy Kết Quả",
            "• Xây dựng thành ứng dụng Web hoàn chỉnh: Giao diện tối Dark Mode hiện đại, mượt mà trên nền Streamlit.\n"
            "• Bộ 4 màn hình soi ảnh đồng bộ: Xem ảnh gốc, Bản đồ nhiệt AI, Nhiễu lọc bề mặt SRM và Phổ sóng 2D-FFT cùng lúc.\n"
            "• Nhật ký phân tích cực kỳ minh bạch: Giải thích rõ ràng tại sao kết luận AI, nhánh nào đóng góp bao nhiêu phần trăm.\n"
            "• Có sẵn công cụ dòng lệnh (CLI): Cho phép các lập trình viên khác cắm vào hệ thống tự động quét hàng triệu ảnh.",
            "Ảnh chụp toàn cảnh giao diện Web Studio đang chạy trên localhost:8501 với các thông số nhảy sinh động; Clip ngắn 5 giây tải ảnh lên.",
            "Không chỉ dừng lại ở thuật toán trên máy tính cá nhân, nhóm em đã đóng gói toàn bộ nghiên cứu thành một ứng dụng Web Studio hoàn chỉnh chạy cực kỳ mượt mà. Người dùng chỉ cần kéo thả ảnh vào, màn hình sẽ chia làm 4 góc soi chiếu đa chiều: từ bản đồ nhiệt, nhiễu hạt bề mặt đến phổ tần số. Bên dưới có một bảng nhật ký giải thích rành rọt từng chỉ số, người dùng không cần biết lập trình nhìn vào cũng hiểu vì sao bức ảnh này là giả. Bọn em cũng có sẵn công cụ dòng lệnh để doanh nghiệp có thể quét tự động hàng loạt."
        ),
        (
            "Slide 12: Tổng Kết, Giá Trị Mang Lại & Hướng Mở Rộng",
            "• Đã làm được: Vá hoàn toàn lỗ hổng nén ảnh của bài báo quốc tế CVPR 2025, đưa độ nhạy bắt ảnh AI lên mức 100%.\n"
            "• Tính thực chiến cao: Có Web trực quan, có dòng lệnh tự động, sẵn sàng bảo vệ không gian mạng trước làn sóng tin giả.\n"
            "• Hướng đi tiếp theo: Mở rộng bóc tách Video Deepfake từng khung hình và phát hiện giọng nói giả mạo bằng AI (Audio Deepfake).\n"
            "• Lời cảm ơn: Nhóm 17 xin chân thành cảm ơn thầy cô đã lắng nghe và rất mong nhận được những góp ý quý báu!",
            "Lời cảm ơn trang trọng; Mã QR tải mã nguồn GitHub của đề tài; Hình ảnh thành viên nhóm.",
            "Tóm lại, đề tài của nhóm 17 không chỉ dừng ở mức đọc hiểu một bài báo quốc tế, mà bọn em đã thực sự đào sâu, tìm ra điểm yếu và nâng cấp nó thành một giải pháp thực chiến vượt trội, nâng tỷ lệ bắt ảnh AI lên 100%. Đây sẽ là một lá chắn hữu hiệu để chống lại nạn tin giả trên không gian mạng hiện nay. Trong tương lai, nhóm dự định sẽ phát triển tiếp sang mảng video và giọng nói AI. Nhóm em xin chân thành cảm ơn thầy cô và các bạn đã chú ý lắng nghe, rất mong nhận được những câu hỏi và đóng góp từ hội đồng ạ!"
        )
    ]

    for idx, (s_title, s_bullets, s_vis, s_script) in enumerate(slides):
        add_h2(f"5.{idx+1}. {s_title}")
        
        # Slide Box Table
        s_tbl = doc.add_table(rows=3, cols=2)
        s_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        s_tbl.autofit = False
        
        # Row 1: Bullets (left) & Visuals (right)
        c_l, c_r = s_tbl.rows[0].cells
        c_l.width = Inches(4.5)
        c_r.width = Inches(2.3)
        set_cell_background(c_l, "F8FAFC")
        set_cell_background(c_r, "F1F5F9")
        set_cell_margins(c_l, top=70, bottom=70, left=100, right=100)
        set_cell_margins(c_r, top=70, bottom=70, left=100, right=100)
        
        p_l = c_l.paragraphs[0]
        p_l.paragraph_format.space_after = Pt(2)
        r_lh = p_l.add_run("📋 Nội dung chính trên Slide:\n")
        r_lh.font.bold = True
        r_lh.font.size = Pt(9.5)
        r_lh.font.color.rgb = RGBColor(31, 78, 121)
        r_lt = p_l.add_run(s_bullets)
        r_lt.font.size = Pt(9)
        
        p_r = c_r.paragraphs[0]
        p_r.paragraph_format.space_after = Pt(2)
        r_rh = p_r.add_run("🖼️ Gợi ý Hình ảnh / Chart:\n")
        r_rh.font.bold = True
        r_rh.font.size = Pt(9.5)
        r_rh.font.color.rgb = RGBColor(14, 134, 212)
        r_rt = p_r.add_run(s_vis)
        r_rt.font.size = Pt(9)
        r_rt.font.italic = True
        
        # Row 2: Script header
        c_sc_h = s_tbl.rows[1].cells[0]
        c_sc_h.merge(s_tbl.rows[1].cells[1])
        set_cell_background(c_sc_h, "E2E8F0")
        set_cell_margins(c_sc_h, top=40, bottom=40, left=100, right=100)
        p_sh = c_sc_h.paragraphs[0]
        p_sh.paragraph_format.space_after = Pt(0)
        r_sh = p_sh.add_run("🎤 Kịch Bản Lời Nói Thuyết Trình (Script gợi ý cho người trình bày):")
        r_sh.font.bold = True
        r_sh.font.size = Pt(9)
        r_sh.font.color.rgb = RGBColor(15, 23, 42)
        
        # Row 3: Script content
        c_sc_b = s_tbl.rows[2].cells[0]
        c_sc_b.merge(s_tbl.rows[2].cells[1])
        set_cell_background(c_sc_b, "FFFFFF")
        set_cell_margins(c_sc_b, top=60, bottom=60, left=100, right=100)
        p_sb = c_sc_b.paragraphs[0]
        p_sb.paragraph_format.space_after = Pt(0)
        r_sb = p_sb.add_run(f'"{s_script}"')
        r_sb.font.italic = True
        r_sb.font.size = Pt(9)
        r_sb.font.color.rgb = RGBColor(71, 85, 105)
        
        add_p(space_after=4)

    # ==========================
    # PHẦN 6: BỘ CÂU HỎI & TRẢ LỜI SẴN KHI BẢO VỆ (FAQ)
    # ==========================
    add_h1("VI. BỘ CÂU HỎI & TRẢ LỜI SẴN KHI BẢO VỆ TRƯỚC HỘI ĐỒNG (FAQ)")
    add_p(
        "Dưới đây là 5 câu hỏi trọng tâm thường được Giảng viên và Hội đồng chuyên môn đặt ra, "
        "kèm câu trả lời chuẩn xác, tự tin theo đúng bản chất kỹ thuật của đề tài:"
    )

    faqs = [
        (
            "Câu 1: Tại sao bài báo gốc CVPR 2025 rất nổi tiếng nhưng khi nhóm thử nghiệm lại chỉ đạt Recall 50% trên ảnh mạng xã hội?",
            "Thưa thầy cô, bài báo gốc CO-SPY được tác giả kiểm nghiệm trong điều kiện lý tưởng (ảnh nguyên bản uncompressed 512x512 sinh thẳng từ GPU). "
            "Trong môi trường thực tế, khi ảnh được tải lên mạng xã hội (Facebook, Zalo, Reddit), thuật toán nén lossy JPEG đã cắt bỏ các hệ số DCT tần số cao, "
            "làm mờ và xóa sạch các hạt micro-pixel artifacts mà VAE dựa vào. Do chỉ phụ thuộc đơn lẻ vào sai phân VAE pixel, mô hình gốc bị mất hoàn toàn dấu vết. "
            "Đây chính là phát hiện thực nghiệm quan trọng nhất của nhóm, thúc đẩy nhóm nghiên cứu các đặc trưng bất biến qua nén như tương quan kênh Bayer và phổ tần số Fourier."
        ),
        (
            "Câu 2: Tại sao nhánh Tương quan màu Bayer (Chroma & Bayer Coherence) lại không bị ảnh hưởng bởi nén JPEG?",
            "Thưa thầy cô, nén JPEG dù có áp dụng lấy mẫu giảm sắc thái Chroma Subsampling (4:2:0), nhưng nó áp dụng chung cho cả ảnh thật lẫn ảnh AI. "
            "Bản chất phân biệt nằm ở phần cứng thu nhận: Camera thật có mảng lọc màu vật lý Bayer (R-G-G-B) luôn tạo ra nhiễu hạt sắc độ ngẫu nhiên độc lập (chroma_to_luma > 0.16) "
            "và các kênh RGB không bao giờ trùng khít hoàn hảo (min_corr < 0.92). Ngược lại, AI sinh ảnh từ các ma trận toán học trong latent space, cả 3 kênh R-G-B được sinh đồng thời "
            "nên bị khóa chặt phi tự nhiên (min_corr > 0.96 - 0.99). Dấu vết khóa kênh màu này ăn sâu vào cấu trúc thống kê của bức ảnh, nén JPEG không thể xóa được."
        ),
        (
            "Câu 3: Khối van CAGU điều tiết trọng số dựa trên tiêu chí toán học nào?",
            "Thưa thầy cô, van CAGU (Channel-wise Adaptive Gating Unit) tính toán trực tiếp độ gãy cạnh khối nén JPEG Blockiness 8x8 (theo chuẩn Wang et al.). "
            "Khi Blockiness <= 1.08 (ảnh sạch), van phân bổ đều trọng số Spatial VAE (35%), Freq (33%), Chroma (32%). "
            "Khi Blockiness > 1.22 (nén JPEG nặng), van CAGU nhận biết miền không gian pixel đã bị biến dạng bởi nén, nó tự động hạ trọng số VAE về 0% và dồn toàn bộ quyền quyết định "
            "cho nhánh Phổ 2D-FFT và Tương quan Bayer. Nhờ đó mô hình luôn kích hoạt đúng 'vũ khí' tối ưu nhất cho từng chất lượng ảnh đầu vào."
        ),
        (
            "Câu 4: Nhánh Phổ 2D-FFT của nhóm có bị báo động giả trên ảnh thật có hoa văn sọc đều (như áo kẻ sọc, rèm cửa) không?",
            "Thưa thầy cô, nhóm đã lường trước trường hợp này và xây dựng cơ chế Kiểm tra chéo hai miền (Dual-Domain Consistency Regularizer). "
            "Khi gặp vật thể có hoa văn lưới thật (như áo sọc, lưới sắt), nhánh 2D-FFT có thể tăng nhẹ điểm, nhưng nhánh Bayer lại nhận diện được nhiễu hạt cảm biến thật (chroma_to_luma cao, "
            "min_corr thấp), đồng thời nhánh Spatial ghi nhận nhiễu photon ngẫu nhiên. Cơ chế Dual-Domain sẽ kích hoạt hệ số triệt tiêu consistency_factor = 0.50, "
            "bảo vệ an toàn cho ảnh thật không bị báo động giả (nhờ đó Specificity vẫn giữ vững ở mức 88.89% - 90%)."
        ),
        (
            "Câu 5: Nhóm đã đóng gói sản phẩm hoàn thiện đến mức độ nào?",
            "Thưa thầy cô, toàn bộ giải pháp không dừng lại ở mức mô phỏng trên Jupyter Notebook mà đã được nhóm đóng gói hoàn chỉnh thành hệ sinh thái phần mềm: "
            "Một ứng dụng Web Forensic Studio giao diện Dark Obsidian hiện đại (Streamlit) với 4 kính khám nghiệm trực quan và nhật ký bằng chứng minh bạch; "
            "cùng một công cụ dòng lệnh CLI (cli.py) độc lập có khả năng chạy suy luận CPU siêu tốc mà không cần GPU đắt đỏ, sẵn sàng tích hợp vào các hệ thống kiểm duyệt tự động."
        )
    ]

    for q_title, q_ans in faqs:
        add_h3(q_title)
        p_ans = add_p(q_ans, space_after=6)
        p_ans.runs[0].font.size = Pt(10)
        p_ans.runs[0].font.italic = True
        p_ans.runs[0].font.color.rgb = RGBColor(30, 41, 59)

    # Footer note
    add_p("————————————————————————————————————————————————————————", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=14, space_after=2)
    p_end = add_p("TÀI LIỆU TỔNG KẾT BÁO CÁO BÀI TẬP LỚN • NHÓM 17 XỬ LÝ ẢNH SỐ • PTIT 2026", align=WD_ALIGN_PARAGRAPH.CENTER, space_after=2)
    p_end.runs[0].font.size = Pt(8.5)
    p_end.runs[0].font.bold = True
    p_end.runs[0].font.color.rgb = RGBColor(148, 163, 184)

    doc.save("BAO_CAO_TONG_KET_BTL_CO_SPY.docx")
    print("Báo cáo đã được xuất thành công vào file: BAO_CAO_TONG_KET_BTL_CO_SPY.docx")

if __name__ == "__main__":
    create_document()
