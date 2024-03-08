from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import os

# Path to Tesseract executable (replace with your path if necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

image_file = 'test-tha.png'
text = pytesseract.image_to_string(image_file, lang='tha')

print(text)