from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Pastikan path file sesuai dengan lokasi file model dan scaler kamu
model = joblib.load("knn_diabetes_model.pkl")
scaler = joblib.load("scaler.pkl")

@app.route('/')
def home():
    return "REST API untuk Prediksi Diabetes (KNN)"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    try:
        glucose = float(data['glucose'])
        bmi = float(data['bmi'])
        age = float(data['age'])
        blood_pressure = float(data['blood_pressure'])
        
        # Susun input sesuai urutan fitur training!
        X_input = np.array([[glucose, bmi, age, blood_pressure]])
        X_scaled = scaler.transform(X_input)
        prediction = model.predict(X_scaled)[0]
        
        # Ambil probabilitas prediksi (kelas 1 = 'berisiko diabetes')
        probas = model.predict_proba(X_scaled)[0]
        risiko = float(probas[1]) * 100  # Probabilitas dalam persen (0-100)

        # Hasil prediksi dalam Bahasa Indonesia
        if prediction == 1:
            hasil = "Anda berisiko diabetes"
        else:
            hasil = "Anda tidak berisiko diabetes"

        return jsonify({'prediksi': hasil, 'risiko': risiko})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Jangan gunakan app.run() di sini. Streamlit akan menangani server.
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)  # Hanya untuk pengujian lokal, jika diperlukan
