# Vietnamese PDF OCR Processor

A Python tool for extracting text from scanned Vietnamese PDF documents using Tesseract OCR. This tool includes image preprocessing capabilities to improve OCR accuracy and handles multi-page PDF documents.

## Features

- PDF to image conversion
- Advanced image preprocessing
- Vietnamese language support
- Multi-page PDF processing
- Progress tracking
- Error handling
- Optional output file saving

## Prerequisites

- Python 3.6 or higher
- Tesseract OCR engine
- Vietnamese language data for Tesseract

## Installation

1. Install the required Python packages:

```bash
pip install pdf2image pytesseract opencv-python Pillow
```

2. Install Tesseract OCR and Vietnamese language data:

### For Ubuntu/Debian
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-vie
```

### For MacOS
```bash
brew install tesseract tesseract-lang
```

### For Windows
1. Download and install Tesseract from the [official GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki)
2. Add Tesseract to your system PATH
3. Download Vietnamese language data and place it in the Tesseract tessdata directory

## Usage

```python
from vietnamese_ocr import process_vietnamese_pdf, check_vietnamese_support

# First, check if Vietnamese language support is available
check_vietnamese_support()

# Process a PDF file
text = process_vietnamese_pdf('path/to/your/file.pdf', 'output.txt')
```

## Function Documentation

### process_vietnamese_pdf(pdf_path, output_path=None)

Process a scanned Vietnamese PDF file and extract text using Tesseract OCR.

Parameters:
- `pdf_path` (str): Path to the input PDF file
- `output_path` (str, optional): Path to save the extracted text

Returns:
- `str`: Extracted text from the PDF

### check_vietnamese_support()

Check if Vietnamese language data is installed for Tesseract OCR.

Returns:
- `bool`: True if Vietnamese is supported, False otherwise

## Image Preprocessing Steps

The tool applies several preprocessing techniques to improve OCR accuracy:
1. Conversion to grayscale
2. Adaptive thresholding
3. Noise removal using median blur

## Error Handling

The tool includes comprehensive error handling for common issues:
- Missing language data
- Invalid PDF files
- File access permissions
- OCR processing errors

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [pdf2image](https://github.com/Belval/pdf2image)
- [OpenCV](https://opencv.org/)

## Support

For issues and feature requests, please create an issue in the GitHub repository.