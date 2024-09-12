import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import sqlite3

# 1. Initialize the SQLite database connection
def init_db():
    conn = sqlite3.connect('crop_management.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS crops
                 (username TEXT, crop_name TEXT, plant_date DATE, expected_yield REAL, location TEXT,
                  disease TEXT, suggested_cure TEXT)''')
    conn.commit()
    return conn, c

# Check if column exists in a table
def column_exists(table_name, column_name):
    conn = sqlite3.connect('crop_management.db')
    c = conn.cursor()
    c.execute(f"PRAGMA table_info({table_name})")
    columns = [row[1] for row in c.fetchall()]
    conn.close()
    return column_name in columns

# Update database schema to add new columns
def update_db_schema():
    conn = sqlite3.connect('crop_management.db')
    c = conn.cursor()
    # Check and add new columns if they don't exist
    if not column_exists('crops', 'disease'):
        c.execute('ALTER TABLE crops ADD COLUMN disease TEXT')
    
    if not column_exists('crops', 'suggested_cure'):
        c.execute('ALTER TABLE crops ADD COLUMN suggested_cure TEXT')
    
    conn.commit()
    conn.close()

# Call this function once to update the schema if needed
update_db_schema()

conn, c = init_db()

# 2. User Authentication functions
def login_user(username, password):
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    return c.fetchone()

def register_user(username, password):
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()

# 3. Session state for maintaining login status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None

# 4. Define the main app function after the login block
def app(username):
    # Load your model
    try:
        model = load_model('model_best.keras')  # Ensure the model file is in the correct directory
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return

    st.title("Crop Disease Prediction and Management")

    # Upload an image file for prediction
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        try:
            img = image.load_img(uploaded_file, target_size=(150, 150))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
            img_array /= 255.0  # Rescale to [0, 1]

            prediction = model.predict(img_array)
            class_idx = np.argmax(prediction, axis=1)[0]
            class_labels = ['Healthy', 'Powdery', 'Rust']  # Update based on your actual labels
            suggested_cures = {
                'Healthy': 'No action needed, keep monitoring the crop.',
                'Powdery': 'Apply fungicide and remove affected leaves.',
                'Rust': 'Use a rust-resistant variety or apply appropriate fungicide.'
            }

            if class_idx < len(class_labels):
                class_label = class_labels[class_idx]
                suggested_cure = suggested_cures[class_label]
                st.write(f"Predicted disease: {class_label}")
                st.write(f"Suggested cure: {suggested_cure}")
            else:
                class_label = "NOT CROP"
                suggested_cure = "No cure available."
                st.write(class_label)
        except Exception as e:
            st.error(f"Error during prediction: {e}")

    # Allow user to manage their crops
    st.subheader("Manage Your Crops")
    crop_name = st.text_input("Crop Name")
    plant_date = st.date_input("Planting Date")
    expected_yield = st.number_input("Expected Yield (tons)", min_value=0.0)
    location = st.text_input("Location")

    if st.button("Save Crop"):
        try:
            c.execute('INSERT INTO crops (username, crop_name, plant_date, expected_yield, location, disease, suggested_cure) VALUES (?, ?, ?, ?, ?, ?, ?)',
                      (username, crop_name, plant_date, expected_yield, location, class_label, suggested_cure))
            conn.commit()
            st.success("Crop data saved successfully!")
        except Exception as e:
            st.error(f"Error saving crop data: {e}")

    st.subheader("Your Crop Records")
    try:
        c.execute('SELECT * FROM crops WHERE username=?', (username,))
        rows = c.fetchall()
        for row in rows:
            st.write(f"Crop: {row[1]}, Plant Date: {row[2]}, Expected Yield: {row[3]} tons, Location: {row[4]}, Disease: {row[5]}, Suggested Cure: {row[6]}")
    except Exception as e:
        st.error(f"Error retrieving crop records: {e}")

# 5. Streamlit app begins
st.title("Crop Management System")

# 6. User login/sign-up menu
menu = ["Login", "Sign Up"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Sign Up":
    st.subheader("Create a New Account")
    new_user = st.text_input("Username")
    new_password = st.text_input("Password", type='password')
    if st.button("Sign Up"):
        if new_user and new_password:
            try:
                register_user(new_user, new_password)
                st.success("You have successfully created an account")
                st.info("Go to Login Menu to login")
            except Exception as e:
                st.error(f"Error during account creation: {e}")
        else:
            st.warning("Please fill in both fields")

elif choice == "Login":
    st.subheader("Login to Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        user = login_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.write("Logged In successfully!")
        else:
            st.warning("Incorrect Username/Password")

# 7. Display the app content if logged in
if st.session_state.logged_in:
    app(st.session_state.username)

# 8. Close the database connection when the script ends
conn.close()
