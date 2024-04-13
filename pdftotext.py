import os
import pytesseract
import time
from PIL import Image
from pdf2image import convert_from_path

current_directory = os.getcwd()
submissions_directory = "./submissions/"
processed_directory = "./processed_submissions/"

if not os.path.exists(processed_directory):
    os.makedirs(processed_directory)


files = os.listdir(submissions_directory)
pdf_files = [file for file in files if file.endswith('.pdf')]
# print(pdf_files)

# tesseract_cmd = os.path.join(current_directory, 'env', 'bin', 'pytesseract', 'tesseract')

for pdf_file in pdf_files:
    pages = convert_from_path(submissions_directory + '/' + pdf_file, 500)
    extracted_text = ''
    for page in pages:
        extracted_text += pytesseract.image_to_string(page)
    
    output_file_path = os.path.join(processed_directory, os.path.splitext(pdf_file)[0] + '.txt')
    with open(output_file_path, 'w') as file:
        file.write(extracted_text)