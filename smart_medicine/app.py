import streamlit as st
import pytesseract
import pyttsx3
import json
import cv2
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image
import time
import os
from rapidfuzz import fuzz, process
import base64
from io import BytesIO

def image_to_base64(image_array):
    """Convert a NumPy array (RGB image) to a base64 string."""
    img = Image.fromarray(image_array)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str

st.set_page_config(page_title="MEDISENSE")

st.markdown("""
<style>
body {
    background-color: #F5F6F5; 
    color: #1A1A1A; 
    font-family: Arial, sans-serif;
    text-align: center; 
    margin: 0 auto; 
    max-width: 1200px;  
}

h1 {
    background: linear-gradient(90deg, #0052A2, #0078D4); 
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center; 
    margin: 20px 0; 
    font-size: 48px; 
}

h2.subtitle {
    color: #003087; 
    text-align: center;
    font-size: 24px;
    margin-bottom: 20px;
}

h2, h3 {
    color: #003087; 
    text-align: center; 
}

.stAlert {
    background-color: #E6F3FF; 
    color: #1A1A1A;
    border: 1px solid #003087;
    text-align: center; 
    margin: 10px auto; 
    padding: 10px;
}

.stWarning {
    background-color: #FFF4CC; 
    color: #1A1A1A;
    border: 1px solid #FFB300; 
    text-align: center;
    margin: 10px auto;
    padding: 10px;
}
.stError {
    background-color: #FFDDDD; 
    color: #1A1A1A;
    border: 1px solid #A10000; 
    text-align: center;
    margin: 10px auto;
    padding: 10px;
}

p, .stMarkdown, .caption {
    color: #1A1A1A; 
    text-align: center; 
    margin: 10px auto; 
}

.caption {
    font-style: italic;
    color: #4A4A4A; 
    text-align: center;
}

.medicine-box {
    padding: 10px; 
    margin: 5px 0; 
    border-radius: 5px;
    text-align: left; 
    font-size: 14px; 
    width: 100%; 
    box-sizing: border-box; 
}
.name-box {
    background-color: #E6FFFA; 
    color: #006666; 
    border: 1px solid #006666;
}
.type-box {
    background-color: #FFF4CC; 
    color: #FFB300; 
    border: 1px solid #FFB300;
}
.usage-box {
    background-color: #E6F3FF; 
    color: #003087; 
    border: 1px solid #003087;
}
.side-effects-box {
    background-color: #EDEDED; 
    color: #1A1A1A; 
    border: 1px solid #1A1A1A;
}


* {
    text-shadow: none !important; 
}

.logo-container {
    text-align: left;
    margin: 20px 0 20px -50px; 
}

.camera-feed img {
    width: 600px !important; 
    height: 300px !important; 
    object-fit: cover; 
}
</style>
""", unsafe_allow_html=True)

engine = pyttsx3.init()
engine.setProperty('rate', 150)  
engine.setProperty('volume', 0.9)  
voices = engine.getProperty('voices')
english_voice_set = False
for voice in voices:
    if "english" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        english_voice_set = True
        break
if not english_voice_set:
    st.warning("No English voice found. Using default voice, which may not be in English.")
    engine.say("Warning: No English voice found. Using default voice.")
    engine.runAndWait()

def speak(text):
    """Speak text in English with error handling."""
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        st.error(f"Speech error: {str(e)}")

try:
    with open('pillbox_dataset.json', 'r', encoding='utf-8') as file:
        medicine_data = json.load(file)
except FileNotFoundError:
    st.error("Error: 'pillbox_dataset.json' file not found. Please ensure the file exists.")
    speak("Error: Medicine dataset file not found.")
    st.stop()

def get_medicine_info(text):
    """Search for medicine in the dataset by name using fuzzy matching."""
    medicine_names = [medicine['name'].lower() for medicine in medicine_data]
    best_match = process.extractOne(text.lower(), medicine_names, scorer=fuzz.partial_ratio)
    if best_match and best_match[1] >= 80:  
        for medicine in medicine_data:
            if medicine['name'].lower() == best_match[0]:
                return medicine
    return None

def preprocess_image(image):
    """Preprocess image for better OCR results."""
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    return thresh

def extract_text_or_qr(image):
    """Extract text or QR/barcode from an image."""
    img_array = np.array(image)
    decoded = decode(img_array)
    if decoded:
        return decoded[0].data.decode('utf-8')

    preprocessed = preprocess_image(img_array)
    try:
        text = pytesseract.image_to_string(preprocessed, lang='eng+tur', config='--psm 6')
        return text.strip()
    except pytesseract.TesseractNotFoundError:
        st.error(
            "Tesseract is not installed or not in your PATH. "
            "Please install Tesseract using 'brew install tesseract' on macOS."
        )
        speak("Tesseract is not installed. Please install it to continue.")
        return ""
    except Exception as e:
        if current_time - st.session_state.last_error_time >= 2:
            st.error(f"Error during OCR processing: {str(e)}")
            speak("Error during text recognition. Please try again.")
            st.session_state.last_error_time = current_time
        return ""

col_logo, col_title = st.columns([1, 3])

with col_logo:
    try:
        st.image("images/medisense_logo.png", width=300)  
    except FileNotFoundError:
        st.error("Error: 'images/medisense_logo.png' not found. Please ensure the file exists.")
        speak("Error: Logo file not found.")

with col_title:
    st.markdown("<h1>MEDISENSE</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='subtitle'>Smart Medicine Advisor for Blind Patients</h2>", unsafe_allow_html=True)

st.info(
    "📸 Camera Instructions: Hold the medicine box clearly in front of the camera. "
    "Ensure the medicine name is visible for text scanning or show the QR/barcode. "
    "To scan a new medicine, simply hold a new medicine box in front of the camera."
)

if 'welcome_spoken' not in st.session_state:
    st.session_state.welcome_spoken = True
    welcome_message = (
        "Welcome to the Smart Medicine Advisor. "
        "Please hold the medicine box in front of the camera, ensuring the name or QR code is visible. "
        "To scan a new medicine, simply hold a new medicine box in front of the camera. When the camera get activated you will hear camera is active voice."
    )
    speak(welcome_message)

if 'last_error_time' not in st.session_state:
    st.session_state.last_error_time = 0
if 'last_success_time' not in st.session_state:
    st.session_state.last_success_time = 0
if 'camera_paused' not in st.session_state:
    st.session_state.camera_paused = False
if 'last_success_frame' not in st.session_state:
    st.session_state.last_success_frame = None
if 'last_extracted_text' not in st.session_state:
    st.session_state.last_extracted_text = ""

cap = cv2.VideoCapture(0)  
if not cap.isOpened():
    st.error("Error: Could not open camera. Please ensure your webcam is connected.")
    speak("Error: Could not open camera.")
    st.stop()
else:
    st.write("📷 Camera is active. Scanning for medicine information...")
    speak("The camera is now active.")

    col1, col2 = st.columns([3, 1])  

    with col1:
        frame_placeholder = st.empty()
        text_placeholder = st.empty()

    with col2:
        medicine_info_placeholder = st.empty()

    last_processed = 0
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                st.error("Error: Failed to capture image from camera.")
                speak("Error: Failed to capture image from camera.")
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            if st.session_state.camera_paused and st.session_state.last_success_frame is not None:
                frame_placeholder.markdown(
                    f'<div class="camera-feed"><img src="data:image/png;base64,{image_to_base64(st.session_state.last_success_frame)}" alt="Medicine Detected - Camera Paused"><p class="caption">Medicine Detected - Camera Paused</p></div>',
                    unsafe_allow_html=True
                )
            else:
                frame_placeholder.markdown(
                    f'<div class="camera-feed"><img src="data:image/png;base64,{image_to_base64(frame_rgb)}" alt="Live Camera Feed"><p class="caption">Live Camera Feed</p></div>',
                    unsafe_allow_html=True
                )

            global current_time
            current_time = time.time()
            if current_time - last_processed >= 1:
                if not st.session_state.camera_paused:
                    try:
                        image = Image.fromarray(frame_rgb)
                        text_or_qr = extract_text_or_qr(image)
                        if text_or_qr:
                            st.session_state.last_extracted_text = text_or_qr
                        text_placeholder.markdown(f"**Extracted Text/QR:** {st.session_state.last_extracted_text}")

                        if text_or_qr:
                            medicine_info = get_medicine_info(text_or_qr)
                            if medicine_info:
                                with medicine_info_placeholder.container():
                                    st.markdown('<div class="medicine-box name-box"><b>Name:</b> ' + medicine_info['name'] + '</div>', unsafe_allow_html=True)
                                    st.markdown('<div class="medicine-box type-box"><b>Type:</b> ' + medicine_info['type'] + '</div>', unsafe_allow_html=True)
                                    st.markdown('<div class="medicine-box usage-box"><b>Usage Instructions:</b> ' + medicine_info['usage_instructions'] + '</div>', unsafe_allow_html=True)
                                    st.markdown('<div class="medicine-box side-effects-box"><b>Side Effects:</b> ' + medicine_info['side_effects'] + '</div>', unsafe_allow_html=True)

                                medicine_details = (
                                    f"Medicine found: {medicine_info['name']}. "
                                    f"Type: {medicine_info['type']}. "
                                    f"Usage instructions: {medicine_info['usage_instructions']}. "
                                    f"Side effects: {medicine_info['side_effects']}. "
                                    "To scan a new medicine, hold a new medicine box in front of the camera."
                                )
                                speak(medicine_details)

                                st.session_state.camera_paused = True
                                st.session_state.last_success_frame = frame_rgb
                                st.session_state.last_success_time = current_time

                            else:
                                if current_time - st.session_state.last_error_time >= 2:
                                    st.warning("No medicine found. Please show the medicine box clearly.")
                                    speak("No medicine found. Please show the medicine box clearly.")
                                    st.session_state.last_error_time = current_time
                                medicine_info_placeholder.empty()  
                        else:
                            if current_time - st.session_state.last_error_time >= 2:
                                st.warning("No medicine found. Please show the medicine box clearly.")
                                speak("No medicine found. Please show the medicine box clearly.")
                                st.session_state.last_error_time = current_time
                            medicine_info_placeholder.empty()  
                    except Exception as e:
                        if current_time - st.session_state.last_error_time >= 2:
                            st.error(f"Error during processing: {str(e)}")
                            speak("Error during text recognition. Please try again.")
                            st.session_state.last_error_time = current_time
                        medicine_info_placeholder.empty()
                else:
                    if current_time - st.session_state.last_success_time >= 10:
                        st.session_state.camera_paused = False
                        st.session_state.last_success_frame = None
                        st.write("🔊 Ready to scan a new medicine. Please hold a new medicine box in front of the camera.")
                        speak("Ready to scan a new medicine. Please hold a new medicine box in front of the camera.")
                        medicine_info_placeholder.empty()  

                last_processed = current_time

            time.sleep(0.1)

    finally:
        cap.release()
        engine.stop()