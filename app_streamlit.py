import streamlit as st
from streamlit_echarts import st_echarts
import requests

API_BASE = "http://127.0.0.1:8000"
st.title("Credit Profiler Nasabah")

# Custom styling
st.markdown("""
    <style>
    html, body, .stApp {
        background-color: #fefefe;
        font-family: 'Segoe UI', sans-serif;
    }

    div[data-testid="stTextInput"] label,
    div[data-testid="stNumberInput"] label{
        background-color: #fefefe !important;
        font-weight: 800 !important;
        color: #1f1f1f !important;
    }
    
    div[data-testid="stAlertContentSuccess"] {
        color: #1f1f1f !important;
        font-weight: 600;
    }

    h1, h2, h3 {
        color: #1f1f1f !important;
    }
                   
    div[data-testid="text_input"]{
        border: 1px solid #e0e0e0 !important;
        border-radius: 6px !important;
        padding: 0.5em !important;  
    }
    
    .stButton > button {
        background-color: #e46c0a !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 6px;
        padding: 8px 16px;
    }

    .stButton > button:hover {
        background-color: #cc5a08 !important;
    }

    .stTabs [data-baseweb="tab"] {
        font-weight: 600;
        color: #666;
        border-bottom: 2px solid transparent;
    }

    .stTabs [aria-selected="true"] {
        color: #e46c0a;
        border-bottom: 3px solid #e46c0a;
        background-color: #fff;
    }

    div[data-testid="metric-container"] {
        color: #1f1f1f !important;
    }

    .stAlert-success {
        color: #155724 !important;
        background-color: #d4edda !important;
        border-color: #c3e6cb !important;
        font-weight: 600;
    }
            
    div.stFormSubmitButton > button {
        background-color: #e46c0a !important;
        color: white !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 8px 16px !important;
        box-shadow: 0px 1px 3px rgba(0,0,0,0.1) !important;
        width : 100%;
    }

    div.stFormSubmitButton > button:hover {
        background-color: #cc5a08 !important;
    }

    /* Untuk memastikan teks skor dan label terlihat */
    [data-testid="stMetricValue"] {
        color: #1f1f1f !important;  /* Hitam */
        font-weight: 700 !important;
    }

    [data-testid="stMetricLabel"] {
        color: #1f1f1f !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetricDelta"] {
        color: #1f1f1f !important;
    }

    div.stElementContainer {
        color: #000 !important;  /* Hitam */
    }        

    label[data-testid="stWidgetLabel"] p {
        font-weight: 600 !important;
        color: #1f1f1f !important;
        font-size: 18px !important;
    }

    input[data-testid="stNumberInputField"] {
        background-color: #282434 !important;  /* atau warna lain */
        color: #fffff !important;
        padding: 0.5em !important;
    }

    div[data-testid="stAlertContainer"] p {
        color: black !important;
    }
            
    div[data-testid="stAlertContentWarning"] p {
        color: red !important; /* Oranye peringatan */
    }

    </style>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📝 Input Profil", "💬 Rekomendasi WhatsApp"])

# Tab 1
with tab1:
    st.subheader("INPUT DATA NASABAH")
    with st.form("profile_form"):
        name = st.text_input("NAMA")
        age = st.number_input("UMUR", min_value=17, max_value=60, step=1)
        job = st.text_input("PEKERJAAN")
        hobbies = st.text_input("HOBI")
        city = st.text_input("KOTA")
        personality = st.text_input("KEPRIBADIAN")
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("SUBMIT")

        if submitted:
            payload = {
                "name": name,
                "age": age,
                "job": job,
                "hobbies": hobbies,
                "city": city,
                "personality": personality,
            }
            if not all([name, job, hobbies, city, personality]):
                st.warning("❗ Semua field wajib diisi.")
            elif name.isnumeric() or job.isnumeric() or city.isnumeric() or hobbies.isnumeric() or personality.isnumeric():
                st.warning("Nama, pekerjaan, dan kota tidak boleh berupa angka.")
            elif len(name) < 3 or len(job) < 3:
                st.warning("Nama dan pekerjaan minimal 3 karakter.")
            elif job.lower() in ["pelajar", "mahasiswa"] and age > 30:
                st.warning("Umur tidak sesuai dengan pekerjaan.")
            else:

                with st.spinner("Mengirim..."):
                    response = requests.post(f"{API_BASE}/manual-profile", json=payload)

                if response.status_code == 200:
                    data = response.json()
                    st.success("Profil berhasil dikirim!")

                    st.subheader("📊 Hasil Analisis Kredit")
                    score = data["credit_analysis"]["final_score"]
                    risk = data["credit_analysis"]["risk_level"]

                    col1, col2 = st.columns([0.5, 1])
                    with col1:
                        options = {
                            # "tooltip": {"trigger": "item"},
                            "series": [{
                                "name": "Skor",
                                "type": "pie",
                                "radius": ["50%", "80%"],
                                "avoidLabelOverlap": False,
                                "label": {"show": False},
                                "emphasis": {
                                    "label": {"show": False, "fontSize": 20, "fontWeight": "bold"}
                                },
                                "labelLine": {"show": False},
                                "data": [
                                    {"value": score, "name": "Skor Kredit"},
                                    {"value": 100 - score},
                                ],
                                "color": ["#e46c0a", "#f0f0f0"]
                            }]
                        }
                        st_echarts(options=options, height="160px")

                    with col2:
                        st.markdown("<br>", unsafe_allow_html=True)

                        # Tentukan warna dan ikon berdasarkan risk level
                        risk_badge_color = {
                            "Low Risk": "#c8f7c5",       # Hijau muda
                            "Medium Risk": "#fff3cd",    # Kuning muda
                            "High Risk": "#f8d7da",      # Merah muda
                        }

                        risk_text_color = {
                            "Low Risk": "#2e7d32",       # Hijau tua
                            "Medium Risk": "#856404",    # Kuning tua
                            "High Risk": "#842029",      # Merah tua
                        }

                        bg_color = risk_badge_color.get(risk, "#eee")
                        text_color = risk_text_color.get(risk, "#333")

                        st.markdown(f"""
                            <div style="font-size:16px;margin-bottom:6px;color:#444;">Skor Kredit</div>
                            <div style="font-size:32px;font-weight:bold;color:#222;">{score}</div>
                            <div style="background-color:{bg_color};color:{text_color};
                                        display:inline-block;
                                        border-radius:16px;font-weight:600;">
                                {risk}
                            </div>
                        """, unsafe_allow_html=True)

                    st.subheader("📦 Detail Profil & Hasil")
                    st.json(data)
                else:
                    st.error(f"Gagal: {response.text}")

# Tab 2
with tab2:
    st.subheader("Ambil Strategi Chat WhatsApp")

    profile_id = st.number_input("Masukkan ID Profil", min_value=1, step=1)
    if st.button("Ambil Rekomendasi"):
        with st.spinner("Mengambil strategi..."):
            response = requests.get(f"{API_BASE}/suggestion/{profile_id}")

        if response.status_code == 200:
            result = response.json()
            st.success("Rekomendasi berhasil diambil!")

            st.subheader("🔖 Label Minat")

            label_colors = {
                "tech": "#4caf50",
                "travel": "#2196f3",
                "finance": "#ff9800",
                "culinary_business": "#795548",
                "culinary_enthusiast": "#ff5722",
                "sport": "#9c27b0",
                "health": "#f44336"
            }

            styled_labels = [
                f'<span style="background-color:{label_colors.get(lbl, "#ccc")}; padding:4px 8px; border-radius:6px; color:white; margin-right:6px;">{lbl}</span>'
                for lbl in result["labels"]
            ]

            st.markdown(" ".join(styled_labels), unsafe_allow_html=True)

            st.subheader("🎯 Produk Relevan")
            st.write("- " + "\n- ".join(result["products"]))

            st.subheader("✅ Yang Boleh Dilakukan (Do)")
            st.markdown("\n".join([f"- {item}" for item in result["recommendation"]["do"]]))

            st.subheader("❌ Yang Tidak Boleh Dilakukan (Don't)")
            st.markdown("\n".join([f"- {item}" for item in result["recommendation"]["dont"]]))

            st.subheader("📨 Contoh Opener Chat")
            st.markdown(
                f"""<div style="background-color:#111;padding:1em;border-radius:5px;color:white;white-space:pre-wrap">{result["recommendation"]["opener"]}</div>""",
                unsafe_allow_html=True,
            )
        else:
            st.error(f"Gagal ambil data: {response.text}")
