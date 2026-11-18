import os
import sys
import streamlit as st
from PIL import Image
import numpy as np

# Page configuration
st.set_page_config(
    page_title="CO-SPY Forensic Terminal | AI Synthetic Image Detector",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Precision Forensic Terminal Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* Global canvas */
    .stApp {
        background-color: #080D1A;
        color: #E2E8F0;
        font-family: 'Space Grotesk', -apple-system, sans-serif;
    }

    /* Headings */
    h1, h2, h3, h4 {
        font-family: 'Space Grotesk', sans-serif !important;
        letter-spacing: -0.02em;
        color: #F8FAFC !important;
    }

    /* Code & Telemetry numbers */
    code, pre, .telemetry-num {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Brand Header Banner */
    .terminal-header {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.9) 0%, rgba(8, 13, 26, 0.95) 100%);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 12px;
        padding: 24px 28px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    
    .terminal-header::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #06B6D4 0%, #3B82F6 50%, #8B5CF6 100%);
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(6, 182, 212, 0.1);
        border: 1px solid rgba(6, 182, 212, 0.3);
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.78rem;
        font-family: 'JetBrains Mono', monospace;
        color: #38BDF8;
    }

    .pulse-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: #10B981;
        box-shadow: 0 0 8px #10B981;
    }

    /* Verdict Panels */
    .verdict-box-ai {
        background: radial-gradient(circle at top left, rgba(244, 63, 94, 0.15), rgba(15, 23, 42, 0.85));
        border: 1px solid rgba(244, 63, 94, 0.4);
        border-left: 4px solid #F43F5E;
        border-radius: 10px;
        padding: 20px 24px;
        margin-bottom: 20px;
    }

    .verdict-box-real {
        background: radial-gradient(circle at top left, rgba(16, 185, 129, 0.15), rgba(15, 23, 42, 0.85));
        border: 1px solid rgba(16, 185, 129, 0.4);
        border-left: 4px solid #10B981;
        border-radius: 10px;
        padding: 20px 24px;
        margin-bottom: 20px;
    }

    .verdict-title {
        font-size: 1.45rem;
        font-weight: 700;
        margin: 0 0 6px 0;
    }

    .verdict-prob {
        font-family: 'JetBrains Mono', monospace;
        font-size: 2.2rem;
        font-weight: 700;
        letter-spacing: -0.03em;
    }

    /* Forensic Viewport Card */
    .viewport-card {
        background: #0E1626;
        border: 1px solid #1E293B;
        border-radius: 8px;
        padding: 12px;
        transition: border-color 0.2s ease;
    }

    .viewport-card:hover {
        border-color: rgba(56, 189, 248, 0.4);
    }

    .viewport-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: #94A3B8;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
    }

    /* Telemetry grid */
    .telemetry-cell {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid #1E293B;
        border-radius: 6px;
        padding: 10px 14px;
    }
    
    .telemetry-title {
        font-size: 0.75rem;
        color: #64748B;
        margin-bottom: 2px;
        font-family: 'Space Grotesk', sans-serif;
    }
    
    .telemetry-val {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.05rem;
        font-weight: 600;
        color: #38BDF8;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid #1E293B;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px 6px 0 0;
        padding: 8px 18px;
        color: #94A3B8;
        font-family: 'Space Grotesk', sans-serif;
    }
    .stTabs [aria-selected="true"] {
        background-color: rgba(14, 165, 233, 0.1) !important;
        color: #38BDF8 !important;
        border-bottom: 2px solid #38BDF8 !important;
    }

    /* Forensic Log Panel */
    .log-panel {
        background: #070C18;
        border: 1px solid #1E293B;
        border-radius: 10px;
        padding: 0;
        overflow: hidden;
        margin-top: 8px;
    }
    .log-header {
        background: rgba(14, 165, 233, 0.08);
        border-bottom: 1px solid #1E293B;
        padding: 10px 18px;
        display: flex;
        align-items: center;
        gap: 10px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        color: #38BDF8;
        letter-spacing: 0.08em;
    }
    .log-entry {
        display: flex;
        align-items: flex-start;
        gap: 14px;
        padding: 12px 18px;
        border-bottom: 1px solid rgba(30, 41, 59, 0.6);
        transition: background 0.15s;
    }
    .log-entry:last-child { border-bottom: none; }
    .log-entry:hover { background: rgba(30, 41, 59, 0.4); }
    .log-entry-icon {
        font-size: 1.1rem;
        min-width: 22px;
        margin-top: 2px;
    }
    .log-entry-body { flex: 1; }
    .log-entry-title {
        font-weight: 600;
        font-size: 0.9rem;
        margin-bottom: 4px;
    }
    .log-entry-detail {
        font-size: 0.82rem;
        color: #94A3B8;
        line-height: 1.55;
        font-family: 'Space Grotesk', sans-serif;
    }
    .log-entry-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.82rem;
        min-width: 100px;
        text-align: right;
        padding-top: 2px;
        font-weight: 600;
    }
    .log-critical .log-entry-title { color: #F87171; }
    .log-critical .log-entry-value { color: #F87171; }
    .log-warning  .log-entry-title { color: #FCD34D; }
    .log-warning  .log-entry-value { color: #FCD34D; }
    .log-ok       .log-entry-title { color: #34D399; }
    .log-ok       .log-entry-value { color: #34D399; }
    .log-info     .log-entry-title { color: #38BDF8; }
    .log-info     .log-entry-value { color: #38BDF8; }
</style>
""", unsafe_allow_html=True)

# Import engine
from engine import CoSpyEngine, _build_analysis_log

@st.cache_resource
def get_engine():
    return CoSpyEngine()

engine = get_engine()

# --- SIDEBAR: INSTRUMENT CONTROLS ---
with st.sidebar:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 16px;">
            <div style="font-size: 1.8rem;">🔬</div>
            <div>
                <div style="font-weight: 700; font-size: 1.15rem; color: #F8FAFC;">CO-SPY TERMINAL</div>
                <div style="font-size: 0.75rem; font-family: 'JetBrains Mono', monospace; color: #38BDF8;">v2.5 CVPR 2025 EDITION</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### Chọn Bộ Khám Nghiệm")
    model_choice = st.selectbox(
        "Chế độ phân tích:",
        options=[
            "CO-SPY Cải Tiến",
            "CO-SPY Gốc",
            "Diffusion (sd-v1_4) — Dành riêng cho Stable Diffusion, FLUX, Midjourney",
            "GANs (progan) — Dành riêng cho StyleGAN, ProGAN, CycleGAN"
        ],
        index=0,
        help="Chế độ Cải tiến tích hợp Miền Tần số 2D-FFT và bộ van CAGU, giải quyết triệt để lỗi bỏ sót ảnh AI bị nén mạng xã hội."
    )
    
    st.markdown("#### Ngưỡng Phân Định (Threshold)")
    threshold = st.slider(
        "Độ nhạy phân loại AI:",
        min_value=0.05,
        max_value=0.95,
        value=0.50,
        step=0.05,
    )
    
    st.markdown("---")
    st.markdown("#### Quang Phổ Sai Phân (Spectral Colormap)")
    colormap_choice = st.selectbox(
        "Bảng màu biểu diễn vết tích pixel:",
        options=["JET", "TURBO", "INFERNO", "MAGMA", "BONE"],
        index=0
    )
    
    heatmap_gain = st.slider(
        "Độ khuếch đại sai phân (Contrast Gain):",
        min_value=0.5,
        max_value=3.0,
        value=1.0,
        step=0.25,
    )
    
    st.markdown("---")
    st.markdown("#### Trạng Thái Trạm Tính Toán")
    hw_color = "#10B981" if engine.device == "cuda" else "#38BDF8"
    st.markdown(f"""
        <div class="telemetry-cell">
            <div class="telemetry-title">PHẦN CỨNG TĂNG TỐC</div>
            <div class="telemetry-val" style="color: {hw_color};">{engine.device.upper()} EXECUTION</div>
            <div style="font-size: 0.75rem; color: #64748B; margin-top: 4px;">PyTorch 2.14 • Diffusers 0.42</div>
        </div>
    """, unsafe_allow_html=True)

# --- MAIN TERMINAL VIEW ---
st.markdown("""
<div class="terminal-header">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
        <div class="status-pill">
            <div class="pulse-dot"></div>
            NEURAL FORENSIC ENGINE ONLINE
        </div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #64748B;">
            LATENT ARTIFACT SPECTROMETRY
        </div>
    </div>
    <div style="font-size: 1.85rem; font-weight: 700; color: #F8FAFC; margin-bottom: 6px;">
        Hệ Thống Giám Định & Bóc Tách Vết Tích Ảnh AI
    </div>
    <div style="color: #94A3B8; font-size: 0.95rem; max-width: 860px; line-height: 1.5;">
        Ứng dụng kiến trúc CO-SPY kết hợp phân tích sai phân giải mã VAE và không gian biểu diễn đa tầng 
        để phát hiện chính xác ảnh tổng hợp từ các mô hình tạo sinh Diffusion & GANs.
    </div>
</div>
""", unsafe_allow_html=True)

tab_inspect, tab_theory, tab_benchmark = st.tabs([
    " Bàn Khám Nghiệm Thị Giác",
    " Nguyên Lý Sai Phân VAE",
    " Đánh Giá & Benchmark Nghiên Cứu"
])

with tab_inspect:
    uploaded_file = st.file_uploader(
        "📁 Tải ảnh cần giám định lên hệ thống:",
        type=["png", "jpg", "jpeg", "webp"],
        help="Hỗ trợ các định dạng ảnh phổ biến (PNG, JPG, JPEG, WEBP) ở mọi kích thước & độ phân giải"
    )
    
    current_image = None
    image_filename = ""
    if uploaded_file is not None:
        current_image = Image.open(uploaded_file)
        image_filename = uploaded_file.name

    if current_image is not None:
        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
        
        # --- IMMEDIATE IMAGE PREVIEW & ACTION CONSOLE ---
        col_preview, col_action = st.columns([1, 1.2])
        
        with col_preview:
            st.markdown(f"""
                <div class="viewport-card" style="border-color: rgba(56, 189, 248, 0.4); margin-bottom: 8px;">
                    <div class="viewport-label">
                        <span> TIÊU BẢN ĐÃ TIẾP NHẬN</span>
                        <span>{current_image.size[0]} × {current_image.size[1]} PX</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.image(current_image, use_container_width=True)
            st.caption(f" Tệp: `{image_filename}` • Kích thước: `{current_image.size[0]}×{current_image.size[1]}` px • Hệ màu: `RGB 24-bit`")

        with col_action:
            st.markdown(f"""
                <div style="background: rgba(15, 23, 42, 0.65); border: 1px solid #1E293B; border-radius: 8px; padding: 20px 22px; margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                        <span class="status-pill" style="color: #10B981; border-color: rgba(16, 185, 129, 0.3); background: rgba(16, 185, 129, 0.08);">
                            <span class="pulse-dot"></span> ĐÃ NẠP ẢNH THÀNH CÔNG
                        </span>
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #64748B;">INPUT READY</span>
                    </div>
                    <div style="font-size: 1.15rem; font-weight: 600; color: #F8FAFC; margin-bottom: 8px;">
                        Tiêu bản đã được tải lên và sẵn sàng phân tích
                    </div>
                    <div style="font-size: 0.88rem; color: #94A3B8; line-height: 1.5; margin-bottom: 16px;">
                        Bấm nút bên dưới để hệ thống bóc tách vết tích pixel bằng mạng nơ-ron VAE Decoder, 
                        đo lường năng lượng tần số 2D Fourier (FFT) và trích xuất vector đặc trưng deepfake.
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            run_trigger = st.button(" KHỞI ĐỘNG PHÂN TÍCH FORENSIC", type="primary", use_container_width=True)
            
        # Re-run or get from session state
        if run_trigger:
            with st.spinner("Đang bóc tách vết tích pixel qua VAE và trích xuất vector đặc trưng..."):
                res = engine.analyze_image(
                    current_image,
                    model_type=model_choice,
                    colormap_name=colormap_choice,
                    gain=heatmap_gain
                )
                st.session_state["analysis_res"] = res
                st.session_state["analyzed_file"] = image_filename
                
        # Display results if available for the current image
        if "analysis_res" in st.session_state and st.session_state.get("analyzed_file") == image_filename:
            res = st.session_state["analysis_res"]
                
            p_ai = res["probability_ai"]
            is_ai_verdict = p_ai >= threshold
            
            st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
            
            # --- VERDICT DISPLAY ---
            if is_ai_verdict:
                st.markdown(f"""
                <div class="verdict-box-ai">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <div class="verdict-title" style="color: #F43F5E;">
                                PHÁT HIỆN: ẢNH DO AI TẠO SINH
                            </div>
                            <div style="color: #CBD5E1; font-size: 0.95rem; margin-top: 4px; max-width: 650px;">
                                {res["verdict_reasoning"]}
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 0.8rem; font-family: 'JetBrains Mono', monospace; color: #94A3B8;">XÁC SUẤT TẠO SINH</div>
                            <div class="verdict-prob" style="color: #F43F5E;">{p_ai * 100:.2f}%</div>
                            <div style="font-size: 0.75rem; color: #64748B;">Ngưỡng chuẩn: {threshold * 100:.0f}%</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="verdict-box-real">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                        <div>
                            <div class="verdict-title" style="color: #10B981;">
                                 XÁC NHẬN: ẢNH CHỤP QUANG HỌC TỰ NHIÊN
                            </div>
                            <div style="color: #CBD5E1; font-size: 0.95rem; margin-top: 4px; max-width: 650px;">
                                {res["verdict_reasoning"]}
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 0.8rem; font-family: 'JetBrains Mono', monospace; color: #94A3B8;">ĐỘ TIN CẬY ẢNH THẬT</div>
                            <div class="verdict-prob" style="color: #10B981;">{(1.0 - p_ai) * 100:.2f}%</div>
                            <div style="font-size: 0.75rem; color: #64748B;">Ngưỡng chuẩn: {threshold * 100:.0f}%</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            # --- MULTI-SPECTRAL FORENSIC VIEWPORT ---
            st.markdown("#### Kính Khám Nghiệm Đa Tầng (Multi-stage Forensic Viewport)")
            
            if res.get("reconstructed_image") is not None:
                v1, v2, v3, v4 = st.columns(4)
                with v1:
                    st.markdown("""
                        <div class="viewport-card">
                            <div class="viewport-label">
                                <span>[FEED 01] ẢNH GỐC</span>
                                <span>RGB SPACE</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.image(current_image, use_container_width=True)
                    st.caption(f"`{image_filename}` • `{current_image.size[0]}×{current_image.size[1]}` px")
                    
                with v2:
                    st.markdown("""
                        <div class="viewport-card">
                            <div class="viewport-label">
                                <span>[FEED 02] TÁI TẠO VAE</span>
                                <span>D(E(x))</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.image(res["reconstructed_image"], use_container_width=True)
                    st.caption("Ảnh tái lập qua nén tiềm ẩn và giải mã VAE Decoder")
                    
                with v3:
                    st.markdown(f"""
                        <div class="viewport-card">
                            <div class="viewport-label">
                                <span>[FEED 03] SAI PHÂN PIXEL</span>
                                <span>{colormap_choice} ({heatmap_gain}x)</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.image(res["heatmap_image"], use_container_width=True)
                    st.caption("Bản đồ nhiệt sai phân |x - x'| làm rõ vết tích nén")
                    
                with v4:
                    st.markdown("""
                        <div class="viewport-card">
                            <div class="viewport-label">
                                <span>[FEED 04] PHỔ TẦN SỐ 2D</span>
                                <span>FFT MAGNITUDE</span>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.image(res["fft_image"], use_container_width=True)
                    st.caption("Phổ năng lượng Fourier 2D phát hiện bất thường dạng lưới")
            else:
                v1, v2, v3 = st.columns(3)
                with v1:
                    st.markdown("<div class='viewport-label'>[FEED 01] ẢNH GỐC ĐẦU VÀO</div>", unsafe_allow_html=True)
                    st.image(current_image, use_container_width=True)
                with v2:
                    st.markdown(f"<div class='viewport-label'>[FEED 02] GRADIENT ARTIFACT ({colormap_choice})</div>", unsafe_allow_html=True)
                    st.image(res["heatmap_image"], use_container_width=True)
                with v3:
                    st.markdown("<div class='viewport-label'>[FEED 03] PHỔ FOURIER 2D (FFT)</div>", unsafe_allow_html=True)
                    st.image(res["fft_image"], use_container_width=True)
                    
            st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
            
            # --- TELEMETRY DATA STRIP ---
            st.markdown("#### 📡 Bảng Chỉ Số Đo Lường Kỹ Thuật (Forensic Telemetry)")
            metric_items = list(res["metrics"].items())
            tel_cols = st.columns(len(metric_items))
            for i, (m_label, m_val) in enumerate(metric_items):
                with tel_cols[i]:
                    st.markdown(f"""
                    <div class="telemetry-cell">
                        <div class="telemetry-title">{m_label.upper()}</div>
                        <div class="telemetry-val">{m_val}</div>
                    </div>
                    """, unsafe_allow_html=True)

            # --- FORENSIC ANALYSIS LOG ---
            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
            st.markdown("#### Nhật Ký Phân Tích Forensic (Analysis Decision Log)")
            st.markdown(
                "<div style='font-size:0.85rem; color:#64748B; margin-bottom:10px;'>"
                "Các điểm bằng chứng cụ thể khiến hệ thống đưa ra kết luận — được phân tích tự động "
                "từ VAE reconstruction, phổ tần số 2D-FFT, và bản đồ sai phân pixel.</div>",
                unsafe_allow_html=True
            )

            analysis_log = _build_analysis_log(res, threshold=threshold)

            # Render log panel
            entries_html = ""
            for entry in analysis_log:
                lvl = entry["level"]
                entries_html += f"""
                <div class="log-entry log-{lvl}">
                    <div class="log-entry-icon">{entry["icon"]}</div>
                    <div class="log-entry-body">
                        <div class="log-entry-title">{entry["title"]}</div>
                        <div class="log-entry-detail">{entry["detail"]}</div>
                    </div>
                    <div class="log-entry-value">{entry["value"]}</div>
                </div>"""

            verdict_color = "#F43F5E" if is_ai_verdict else "#10B981"
            verdict_label = "AI DETECTED" if is_ai_verdict else "AUTHENTIC"

            st.markdown(f"""
            <div class="log-panel">
                <div class="log-header">
                    <span style="color:{verdict_color}; font-weight:700;">▌</span>
                    FORENSIC DECISION LOG
                    <span style="margin-left:auto; color:{verdict_color}; font-weight:700;">
                        {verdict_label} — {p_ai*100:.2f}%
                    </span>
                </div>
                {entries_html}
            </div>
            """, unsafe_allow_html=True)

with tab_theory:
    st.markdown("### Bản Chất Khoa Học Của Phương Pháp Bóc Tách Vết Tích VAE")
    
    st.markdown("""
    Trong các mô hình tạo sinh khuếch tán đương đại (**Latent Diffusion Models** như *Stable Diffusion*, *FLUX*, *Midjourney*), 
    ảnh được tạo ra không phải trong không gian pixel thô mà trong không gian tiềm ẩn (latent space), sau đó giải mã về pixel bằng:
    """)
    
    st.latex(r"x_{\text{synthetic}} = \mathcal{D}(z), \quad z \sim p_{\text{diffusion}}(z)")
    
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        st.markdown("""
        #### 1. Ảnh do AI sinh ra (AI-Generated Image)
        * Vốn sinh ra từ chính cấu trúc giải mã của $\mathcal{D}$, nên ảnh này **hoàn toàn thuộc về manifold của VAE**.
        * Khi đưa qua chu trình tái tạo $x' = \mathcal{D}(\mathcal{E}(x))$, sai phân:
        """)
        st.latex(r"\Delta_{\text{AI}} = |x - \mathcal{D}(\mathcal{E}(x))|")
        st.markdown("""
        rất mượt mà, đồng nhất và mang vết tích toán học dạng đặc trưng.
        Mạng ResNet-50 được huấn luyện nhận ra vết tích này với **độ nhạy vượt trội (>99%)**.
        """)
        
    with col_t2:
        st.markdown("""
        #### 2. Ảnh chụp quang học tự nhiên (Real Camera Image)
        * Mang nhiễu vật lý tự nhiên: photon shot noise, nhiễu nhiệt cảm biến CMOS/CCD, và dải tương phản không bị nén qua bottleneck 8x.
        * Khi ép qua VAE Encoder $\to$ Decoder, bộ giải mã làm mờ các tần số ngẫu nhiên này, tạo ra sai phân phân kỳ:
        """)
        st.latex(r"\Delta_{\text{Real}} \neq \Delta_{\text{AI}}")
        st.markdown("""
        giúp mô hình phân biệt rạch ròi giữa ảnh nhân tạo và quang học thực tế.
        """)

    st.markdown("---")
    st.markdown("""
    #### Khả Năng Kháng Nén JPEG (Robustness Against Lossy Compression)
    * Các kỹ thuật cũ (như NPR, LNP) dựa vào phép nội suy upsampling rất dễ bị mất dấu khi ảnh bị nén JPEG (75–95).
    * Ngược lại, sai phân tái tạo qua VAE nằm ở **tầng trừu tượng cao hơn (higher abstraction level)** nên không bị nén JPEG phá hủy, 
    giải quyết triệt để điểm yếu cố hữu của các bộ phát hiện deepfake trước đây.
    """)

with tab_benchmark:
    st.markdown("### Đánh Giá Thực Nghiệm & Kết Quả Benchmark")
    st.markdown("""
    Bộ kiểm thử **CO-SPY-Bench** gồm 22 mô hình tạo sinh tiên tiến nhất (FLUX, SD3, SDXL, Midjourney...) 
    được đánh giá trên 5 tập ảnh thực tế và điều kiện nén JPEG ngẫu nhiên:
    """)
    
    st.table({
        "Bộ phát hiện (Detector)": ["LNP (2024)", "NPR (2024)", "UnivFD (2023)", "DIRE (2023)", "DRCT (2024)", "CO-SPY"],
        "Cơ chế cốt lõi": ["Pixel Noise", "Upsampling Artifacts", "CLIP Semantic", "Diffusion Inversion", "CLIP + SD Recon", "Adaptive VAE + Semantic Fusion"],
        "Độ chính xác (Accuracy)": ["64.2%", "73.5%", "78.2%", "68.5%", "81.2%", "92.2% - 96.6%"],
        "Khả năng kháng nén JPEG": ["Kém", "Kém", "Tốt", "Trung bình", "Khá", "Xuất sắc"],
        "Tổng quát hóa (OOD Generalization)": ["Trung bình", "Khá", "Kém", "Khá", "Tốt", "Vượt trội (+11% đến +34%)"]
    })
    
    st.info(" Nghiên cứu được công bố tại hội nghị thị giác máy tính hàng đầu thế giới **CVPR 2025** (arXiv:2503.18286).")
