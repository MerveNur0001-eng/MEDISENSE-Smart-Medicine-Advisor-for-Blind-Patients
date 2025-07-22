# 💊 MEDISENSE – Smart Medicine Advisor for Blind Patients

**MEDISENSE** is a Streamlit-based real-time medicine recognition application designed to assist blind or visually impaired users. By using live camera input, the system detects and reads medicine names or QR/barcodes, matches them against a local medicine dataset, and provides clear **text-to-speech** feedback about the medicine’s details.

---

##  Features

-  **Live Camera Integration** – Real-time webcam scanning for medicine boxes
-  **OCR and QR/Barcode Detection** – Reads both text and barcodes
-  **Fuzzy Matching** – Matches scanned text to medicines using approximate matching
-  **Text-to-Speech** – Speaks medicine name, type, usage, and side effects
-  **Custom Accessible UI** – Optimized for readability and clarity
-  **Offline Support** – Works with a local JSON database

---

##  Technologies Used

- **Streamlit** – Web app framework
- **OpenCV** – Camera and image handling
- **Tesseract OCR** – Optical character recognition
- **Pyzbar** – Barcode and QR code reading
- **Pyttsx3** – Text-to-speech engine (offline)
- **RapidFuzz** – Fast fuzzy string matching
- **Pillow** – Image processing
- **NumPy, JSON, Base64** – Data handling

---
##  How to Run

This guide explains how to set up and run the MEDISENSE application locally. MEDISENSE is a Streamlit-based application designed to assist blind patients by scanning medicine boxes (via text or QR codes) and providing audio feedback with medicine details.

### Prerequisites

Before running the application, ensure you have the following installed:

- **Python 3.8 or higher:** [Download Python](https://www.python.org/downloads/)
- **Tesseract OCR:** Required for text recognition.  
  - **Windows:** Download and install from [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki). Make sure to add Tesseract to your system PATH.  
  - **macOS:** Install using Homebrew:
    ```bash
    brew install tesseract
    ```
  - **Linux:** Install using:
    ```bash
    sudo apt-get install tesseract-ocr
    ```
- **Webcam:** A functioning webcam connected to your device.
- **Git:** To clone the repository (optional).

### Installation

1. **Clone the Repository** (or download the code as a ZIP file):

    ```bash
    git clone https://github.com/MerveNur0001-eng/MEDISENSE-Smart-Medicine-Advisor-for-Blind-Patients.git
    cd MEDISENSE-Smart-Medicine-Advisor-for-Blind-Patients
    ```

2. **Create a Virtual Environment** (recommended):

    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3. **Install Dependencies:** Install the required Python packages listed in `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

    If you don't have a `requirements.txt` file, install the following packages manually:

    ```bash
    pip install streamlit pytesseract pyttsx3 opencv-python pillow numpy pyzbar rapidfuzz
    ```

4. **Download the Dataset:**  
   Ensure the `pillbox_dataset.json` file is in the root directory of the project. This file contains the medicine data used by the application.

   If you don't have this file, create or obtain a JSON file with the following structure:

    ```json
    [
      {
        "name": "Medicine Name",
        "type": "Medicine Type",
        "usage_instructions": "Usage Instructions",
        "side_effects": "Side Effects"
      }
    ]
    ```

![output](images/output.jpeg)

## EXAMPLES (you can use them for test)

![parol](images/parol_barcode.jpg)

![paroltext](images/parol_text.jpg)

### Running the Application

Start the Streamlit application by running this command from the project directory:

```bash
streamlit run medisense_app.py


## License
This project is for educational and non-commercial use.
