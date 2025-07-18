import streamlit as st
import requests
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests as req_lottie

st.set_page_config(page_title="Prediksi Diabetes", layout="wide")

def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        st.error("Gagal memuat animasi Lottie. Periksa URL atau koneksi internet.")
        return None
    return r.json()

# Animasi sidebar tetap ada
lottie_health = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_ktwnwv5m.json")

# Inisialisasi session_state agar tidak error
if "hasil" not in st.session_state:
    st.session_state.hasil = ""
if "risiko" not in st.session_state:
    st.session_state.risiko = 0

with st.sidebar:
    if lottie_health is not None:
        st_lottie(lottie_health, height=100, key="lottie-health")
    else:
        st.info("Animasi kesehatan tidak dapat dimuat saat ini.")
    st.title("Tips Sehat Hari Ini 🥗")
    st.info("Jaga pola makan, rutin olahraga, dan cek kesehatan secara berkala.")
    st.markdown("---")
    st.caption("Dikembangkan oleh: Nandito Raka • IG: @ditoowww_")

col1, col2 = st.columns([1, 2])

with col1:
    st.header("Masukkan Data Anda 📝")
    glucose = st.number_input("Kadar Glukosa (mg/dL)", min_value=0.0, max_value=300.0, value=100.0)
    berat = st.number_input("Berat Badan (kg)", min_value=10.0, max_value=200.0, value=60.0)
    tinggi = st.number_input("Tinggi Badan (cm)", min_value=100.0, max_value=250.0, value=170.0)
    age = st.number_input("Umur (tahun)", min_value=1, max_value=120, value=30)
    blood_pressure = st.number_input("Tekanan Darah (mmHg)", min_value=40.0, max_value=200.0, value=80.0)

    bmi = berat / ((tinggi / 100) ** 2) if tinggi > 0 else 0
    st.write(f"Indeks Massa Tubuh (BMI): **{bmi:.2f}**")

    # Soft warning, edukasi untuk konsultasi
    if bmi >= 30:
        st.info("BMI Anda menunjukkan kecenderungan obesitas. Sebaiknya konsultasikan dengan dokter atau ahli gizi untuk mendapatkan saran yang tepat.")
    if glucose >= 200:
        st.info("Kadar glukosa Anda cukup tinggi. Sebaiknya lakukan pemeriksaan medis lebih lanjut ke dokter.")
    elif glucose >= 140:
        st.info("Kadar glukosa Anda berada pada rentang pra-diabetes. Konsultasikan ke dokter untuk pencegahan lebih lanjut.")
    if blood_pressure >= 140:
        st.info("Tekanan darah Anda cukup tinggi. Pertimbangkan untuk konsultasi ke dokter mengenai tekanan darah Anda.")
    elif blood_pressure >= 120:
        st.info("Tekanan darah Anda berada pada ambang prehipertensi. Pemeriksaan rutin ke dokter sangat dianjurkan.")

    if st.button("Prediksi Diabetes"):
        with st.spinner("Sedang memproses prediksi..."):
            payload = {
                "glucose": glucose,
                "bmi": bmi,
                "age": age,
                "blood_pressure": blood_pressure
            }
            try:
                # Pastikan URL ini sesuai dengan lokasi API Flask yang di-deploy
                response = requests.post("http://127.0.0.1:5000/predict", json=payload)

                if response.status_code == 200:
                    data = response.json()
                    st.session_state.hasil = data.get('prediksi', '-')
                    st.session_state.risiko = data.get('risiko', 0)
                    st.success(f"**{st.session_state.hasil}**")
                elif response.status_code == 400:
                    st.error(f"Kesalahan Input: {response.json().get('error','Terjadi kesalahan input.')}")  # Perbaikan error handling
                else:
                    st.error(f"Terjadi kesalahan saat memanggil API. Status Code: {response.status_code}")
            except requests.exceptions.ConnectionError:
                st.error("Koneksi ke API gagal! Pastikan API Flask Anda berjalan di `http://127.0.0.1:5000`.")  # Penanganan error jika API tidak terhubung
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")

with col2:
    st.markdown("### Hasil Visualisasi & Analisis 📊", unsafe_allow_html=True)
    risiko = st.session_state.get("risiko", 0)
    hasil = st.session_state.get("hasil", "")

    pred_color = "#FF4B4B" if (hasil and "berisiko" in hasil.lower()) else "#4BB543"
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risiko,
        number={'suffix': " %", "font": {"size": 34}},
        title={'text': f"Tingkat Risiko (%)", 'font': {'size': 18}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 2},
            'bar': {'color': pred_color},
            'bgcolor': "white",
            'borderwidth': 2,
            'steps': [
                {'range': [0, 50], 'color': "#C6FFC6"},
                {'range': [50, 100], 'color': "#FFD1D1"}
            ],
            'threshold': {
                'line': {'color': pred_color, 'width': 4},
                'thickness': 0.75,
                'value': risiko
            },
            'shape': "angular"
        },
        domain={'x': [0, 1], 'y': [0, 1]}
    ))
    fig_gauge.update_layout(
        autosize=False,
        width=340, height=330,
        margin=dict(l=40, r=40, t=50, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})

    if hasil:
        st.success(f"**{hasil}**")

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; font-size: small; color: #888;'>
    <b>Disclaimer:</b> Hasil prediksi ini hanya estimasi berbasis data.<br>
    Untuk diagnosis pasti, konsultasikan dengan tenaga medis profesional.<br>
    &copy; 2025 [Nandito] | Kontak: 2211501038@unisa.com
    </div>
    """, unsafe_allow_html=True
)



