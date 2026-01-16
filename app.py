import streamlit as st
from deepface import DeepFace
from PIL import Image
import numpy as np
import os

# --- 1. THE REGISTER PAGE (Temporary/Session based) ---
if 'registered' not in st.session_state:
    st.session_state.registered = False

if not st.session_state.registered:
    st.title("🛡️ New Account Registration")
    st.info("Since we aren't using a database, this account is temporary for this session.")
    
    new_user = st.text_input("Choose Username")
    new_pass = st.text_input("Choose Password", type="password")
    
    if st.button("Register"):
        if new_user and new_pass:
            st.session_state.registered = True
            st.session_state.username = new_user
            st.success(f"Welcome {new_user}! Redirecting to Detector...")
            st.rerun()
        else:
            st.error("Please fill in both fields.")
    st.stop() 

# --- 2. THE MAIN APP (Only runs if registered) ---
st.title(f"🎭 {st.session_state.username}'s Face Expression Detector")

# Temporary Data List (Resets if page is refreshed)
if 'history' not in st.session_state:
    st.session_state.history = []

# File Uploader
uploaded_file = st.file_uploader("Upload a clear face photo", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', width=300)
    
    # Convert for DeepFace
    img_array = np.array(image)
    
    with st.spinner('AI is thinking...'):
        try:
            # Analyze
            results = DeepFace.analyze(img_array, actions=['emotion'], enforce_detection=True)
            emotion = results[0]['dominant_emotion']
            
            # Store in temporary list
            st.session_state.history.append(emotion)
            
            st.header(f"Detected: {emotion.upper()}")
        except Exception as e:
            st.error("Face not clear! Try another photo.")

# Show "Temporary Database" content
if st.session_state.history:
    st.sidebar.write("### Session Data (Temporary)")
    st.sidebar.write(st.session_state.history)
