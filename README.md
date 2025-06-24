# 🌾 Crop Disease Prediction

A deep learning-based web application that identifies crop diseases using leaf images. This project empowers farmers and agricultural professionals to detect diseases early, enabling timely and effective intervention to improve yield.

---

## 🧪 Tech Stack

- Python 🐍
- TensorFlow / Keras 🤖
- OpenCV 📷
- NumPy, Pandas, Matplotlib 📊
- Streamlit 🌐 (for web app)
- LabelImg (for custom dataset labeling)

---

## 📂 Project Structure

Crop-Disease-Prediction/
│
├── data/ # Dataset (train/test images)
├── models/ # Saved models
├── notebooks/ # Jupyter Notebooks for training & EDA
├── app.py # Streamlit application
├── model.py # CNN model definition
├── predict.py # Image prediction logic
├── utils.py # Helper functions (preprocessing etc.)
├── requirements.txt
└── README.md

yaml
Copy
Edit

---

## 🖼️ Sample Crop Diseases Detected

- Apple Scab
- Corn Rust
- Potato Early Blight
- Tomato Mosaic Virus
- ...and more

---

## 🚀 Installation & Usage

1. Clone the repository
```bash
git clone https://github.com/yourusername/Crop-Disease-Prediction.git
cd Crop-Disease-Prediction
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Run the app

bash
Copy
Edit
streamlit run app.py
Upload a crop leaf image and get prediction results.

🧠 Model Architecture
The model is a Convolutional Neural Network (CNN) consisting of:

Convolution Layers

MaxPooling

Dropout

Dense Layers (ReLU & Softmax)

Trained using categorical crossentropy loss and Adam optimizer.

📈 Results
Accuracy: ~95% on test data

Model trained with 80-20 split on augmented dataset

Early stopping and data normalization applied

🛠️ Future Improvements
Add real-time camera detection

Deploy as Android/iOS app

Add more crop types

Use attention-based CNN or transformers for accuracy boost

🤝 Contributing
Feel free to fork the project, submit pull requests, or open issues. Let's build smarter farming tools together!

📜 License
This project is licensed under the MIT License. See the LICENSE file for more info.
