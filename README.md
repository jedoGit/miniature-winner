# Image Text and PII Detector

This is a simple Python application that uses OCR to extract text from images and detects Personally Identifiable Information (PII) using a hybrid of NLP (spaCy) and regex.

## Features

- Upload and display an image via a Tkinter GUI.
- Extract text using Tesseract OCR with preprocessing for better accuracy.
- Detect PII categories like names, locations, emails, phones, SSNs, credit cards, etc.
- Display results in separate text areas.

## Prerequisites

- Python 3.7+
- Tesseract OCR installed:
  - Windows: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki) and add to PATH.
  - macOS: `brew install tesseract`
  - Linux: `sudo apt-get install tesseract-ocr`

## Installation

1. Clone the repo:
   `git clone https://github.com/jedoGit/miniature-winner.git`
   `cd Image-text-pii-detector`
2. Create a virtual environment (optional but recommended):
   `python -m venv venv`
   `source venv/bin/activate  # On Windows: venv\Scripts\activate`
3. Install dependencies:
   `pip install -r requirements.txt`
4. Download spaCy model:
   `python -m spacy download en_core_web_sm`

## Usage

1. Run the application: `python text_detector.py`
2. In the GUI:

- Click "Upload Image" to select an image file.
- Click "Detect Text" to extract text.
- Click "Detect PII (NLP + Regex)" to scan for PII.

## Troubleshooting

- **Tesseract not found**: Add Tesseract to your PATH or specify in code: `pytesseract.pytesseract.tesseract_cmd = r'path/to/tesseract.exe'`.
- **Poor OCR**: Use high-quality images; experiment with preprocessing.
- **spaCy issues**: Ensure the model is downloaded correctly.

## License

MIT License - feel free to use and modify.

## Acknowledgments

- Built with pytesseract, OpenCV, Tkinter, spaCy, and regex.
