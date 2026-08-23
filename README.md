# AI Tooth Decay Prediction

An AI-based dental image analysis project that predicts tooth decay risk from dental images.

## Features

- Upload a dental image for prediction
- AI-based tooth decay risk classification
- Risk levels: Healthy, Medium, and High
- Heatmap visualization
- Prediction history
- Dental report generation
- Nearby hospital suggestions

## Technologies

- Python
- TensorFlow / Keras
- OpenCV
- Streamlit
- NumPy
- Pandas
- Pillow

## Model

The project uses a deep learning image classification model trained on dental images to identify tooth decay risk.

## Project Structure

- `streamlit_app.py` – Streamlit application
- `app.py` – Application logic
- `camera_module.py` – Camera/image capture functionality
- `tooth_decay_model.keras` – Trained model
- `requirements.txt` – Python dependencies

## How to Run

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py


## Disclaimer

This project is for educational and demonstration purposes and is not a substitute for professional dental diagnosis.
