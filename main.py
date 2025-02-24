import pdf2image
import pytesseract
from PIL import Image
import cv2
import numpy as np
import os

def process_vietnamese_pdf(pdf_path, output_path=None):
    """
    Process a scanned Vietnamese PDF file using Tesseract OCR.
    
    Args:
        pdf_path (str): Path to the PDF file
        output_path (str, optional): Path to save the extracted text
        
    Returns:
        str: Extracted text from the PDF
    """
    try:
        # Convert PDF to images
        images = pdf2image.convert_from_path(pdf_path)
        
        # Configure Tesseract to use Vietnamese
        pytesseract.pytesseract.tesseract_cmd = r'tesseract'  # Update path if needed
        
        full_text = []
        
        for i, image in enumerate(images):
            # Convert PIL image to OpenCV format
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Preprocessing steps
            # Convert to grayscale
            gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
            
            # Apply thresholding to handle different lighting conditions
            thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
            
            # Noise removal
            denoised = cv2.medianBlur(thresh, 3)
            
            # OCR with Vietnamese language
            text = pytesseract.image_to_string(denoised, lang='vie')
            full_text.append(text)
            
            print(f"Processed page {i+1}/{len(images)}")
        
        # Combine all text
        final_text = '\n\n'.join(full_text)
        
        # Save to file if output path is provided
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(final_text)
            print(f"Text saved to {output_path}")
            
        return final_text
    
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        return None

def check_vietnamese_support():
    """
    Check if Vietnamese language data is installed for Tesseract
    """
    try:
        languages = pytesseract.get_languages()
        if 'vie' in languages:
            return True
        else:
            print("Vietnamese language data not found. Please install it:")
            print("sudo apt-get install tesseract-ocr-vie  # For Ubuntu/Debian")
            print("brew install tesseract-lang  # For MacOS")
            return False
    except Exception as e:
        print(f"Error checking language support: {str(e)}")
        return False