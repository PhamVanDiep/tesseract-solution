import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext
import pdf2image
import pytesseract
from PIL import Image
import cv2
import numpy as np
import os
from pathlib import Path

class OCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vietnamese OCR Application")
        self.root.geometry("800x600")
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Upload button
        self.upload_button = ttk.Button(
            self.main_frame, 
            text="Upload PDF File",
            command=self.upload_file
        )
        self.upload_button.grid(row=0, column=0, pady=10)
        
        # File path label
        self.file_label = ttk.Label(self.main_frame, text="No file selected")
        self.file_label.grid(row=1, column=0, pady=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            self.main_frame, 
            orient=tk.HORIZONTAL, 
            length=300, 
            mode='determinate'
        )
        self.progress.grid(row=2, column=0, pady=10)
        
        # Status label
        self.status_label = ttk.Label(self.main_frame, text="")
        self.status_label.grid(row=3, column=0, pady=5)
        
        # Text area for output
        self.text_area = scrolledtext.ScrolledText(
            self.main_frame,
            wrap=tk.WORD,
            width=70,
            height=20
        )
        self.text_area.grid(row=4, column=0, pady=10)
        
        # Save button
        self.save_button = ttk.Button(
            self.main_frame,
            text="Save Text",
            command=self.save_text,
            state=tk.DISABLED
        )
        self.save_button.grid(row=5, column=0, pady=10)

    def upload_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF files", "*.pdf")]
        )
        
        if file_path:
            self.file_label.config(text=f"Selected file: {Path(file_path).name}")
            self.process_file(file_path)

    def process_file(self, file_path):
        try:
            self.status_label.config(text="Converting PDF to images...")
            self.progress['value'] = 0
            self.text_area.delete(1.0, tk.END)
            
            # Convert PDF to images
            images = pdf2image.convert_from_path(file_path)
            total_pages = len(images)
            
            full_text = []
            
            for i, image in enumerate(images):
                # Update progress
                progress = (i + 1) / total_pages * 100
                self.progress['value'] = progress
                self.status_label.config(text=f"Processing page {i+1}/{total_pages}")
                self.root.update()
                
                # Convert PIL image to OpenCV format
                opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                
                # Preprocessing
                gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
                thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
                denoised = cv2.medianBlur(thresh, 3)
                
                # OCR
                text = pytesseract.image_to_string(denoised, lang='vie')
                full_text.append(text)
                
                # Update text area
                self.text_area.insert(tk.END, f"--- Page {i+1} ---\n{text}\n\n")
                self.text_area.see(tk.END)
                
            self.status_label.config(text="Processing complete!")
            self.save_button.config(state=tk.NORMAL)
            
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")
            self.progress['value'] = 0

    def save_text(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.text_area.get(1.0, tk.END))
                self.status_label.config(text="Text saved successfully!")
            except Exception as e:
                self.status_label.config(text=f"Error saving file: {str(e)}")

def main():
    root = tk.Tk()
    app = OCRApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
