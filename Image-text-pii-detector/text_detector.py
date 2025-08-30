import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import pytesseract
import numpy as np
import re
import spacy

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

def find_pii(text):
    """
    Detects PII using a hybrid approach: spaCy NLP for entities and regex for structured patterns.
    Returns a dictionary with lists of detected items, including source (NLP/regex).
    """
    pii = {
        'persons': [],  # From NLP (names)
        'locations': [],  # From NLP (addresses/places)
        'organizations': [],  # From NLP
        'dates': [],  # From NLP
        'emails': [],  # From regex
        'phones': [],  # From regex
        'ssns': [],  # From regex
        'credit_cards': []  # From regex
    }
    
    # NLP Detection with spaCy
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            pii['persons'].append(ent.text)
        elif ent.label_ in ['GPE', 'LOC']:  # Geo-political entities or locations
            pii['locations'].append(ent.text)
        elif ent.label_ == 'ORG':
            pii['organizations'].append(ent.text)
        elif ent.label_ == 'DATE':
            pii['dates'].append(ent.text)
    
    # Regex Detection (as before)
    pii['emails'] = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    pii['phones'] = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b', text)
    pii['ssns'] = re.findall(r'\b\d{3}-\d{2}-\d{4}\b', text)
    pii['credit_cards'] = re.findall(r'\b(?:\d{4}[- ]?){3}\d{4}\b', text)
    
    # Deduplicate within each category using sets
    for key in pii:
        pii[key] = list(set(pii[key]))  # Remove duplicates
    
    return pii

class TextDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Detection App with NLP PII Detection")
        self.root.geometry("800x800")  # Height for elements

        # Initialize variables
        self.image_path = None
        self.extracted_text = None

        # Create UI elements
        self.label_title = tk.Label(root, text="Image Text Detection with NLP PII", font=("Arial", 16))
        self.label_title.pack(pady=10)

        self.btn_upload = tk.Button(root, text="Upload Image", command=self.upload_image)
        self.btn_upload.pack(pady=10)

        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

        self.btn_detect = tk.Button(root, text="Detect Text", command=self.detect_text)
        self.btn_detect.pack(pady=10)

        self.label_extracted = tk.Label(root, text="Extracted Text:", font=("Arial", 12))
        self.label_extracted.pack(pady=5)

        self.text_area = tk.Text(root, height=10, width=50)
        self.text_area.pack(pady=10)

        self.btn_detect_pii = tk.Button(root, text="Detect PII (NLP + Regex)", command=self.detect_pii)
        self.btn_detect_pii.pack(pady=10)

        self.label_pii = tk.Label(root, text="Detected PII:", font=("Arial", 12))
        self.label_pii.pack(pady=5)

        self.text_area_pii = tk.Text(root, height=10, width=50)
        self.text_area_pii.pack(pady=10)

    def upload_image(self):
        # Open file dialog to select an image
        self.image_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if self.image_path:
            # Load and display the image
            img = Image.open(self.image_path)
            img = img.resize((300, 300), Image.Resampling.LANCZOS)  # Resize for display
            img_tk = ImageTk.PhotoImage(img)
            self.image_label.config(image=img_tk)
            self.image_label.image = img_tk  # Keep a reference
            self.text_area.delete(1.0, tk.END)  # Clear previous text
            self.text_area_pii.delete(1.0, tk.END)  # Clear PII area
            self.extracted_text = None
            self.text_area.insert(tk.END, "Image loaded. Click 'Detect Text' to extract text.")

    def preprocess_image(self, image_path):
        # Read image with OpenCV
        img = cv2.imread(image_path)
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Apply thresholding to enhance text
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return thresh

    def detect_text(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please upload an image first!")
            return

        try:
            # Preprocess the image
            processed_img = self.preprocess_image(self.image_path)
            # Extract text using pytesseract
            self.extracted_text = pytesseract.image_to_string(processed_img)
            # Clear text area and display extracted text
            self.text_area.delete(1.0, tk.END)
            self.text_area_pii.delete(1.0, tk.END)  # Clear PII on new detection
            if self.extracted_text.strip():
                self.text_area.insert(tk.END, self.extracted_text)
            else:
                self.text_area.insert(tk.END, "No text detected in the image.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to detect text: {str(e)}")

    def detect_pii(self):
        if not self.extracted_text:
            messagebox.showerror("Error", "Please detect text first!")
            return

        try:
            pii = find_pii(self.extracted_text)
            self.text_area_pii.delete(1.0, tk.END)
            if any(pii.values()):
                for key, values in pii.items():
                    if values:
                        self.text_area_pii.insert(tk.END, f"{key.capitalize()}:\n" + "\n".join(values) + "\n\n")
            else:
                self.text_area_pii.insert(tk.END, "No PII detected in the text.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to detect PII: {str(e)}")

# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = TextDetectionApp(root)
    root.mainloop()