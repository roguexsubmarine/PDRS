import os
import pytesseract
import time
from PIL import Image
from pdf2image import convert_from_path
from plagiarism import has_images

def pdfwriter(dirpath):
    current_directory = os.getcwd()
    submissions_directory = dirpath
    processed_directory = dirpath
    ext=('.pdf','.PDF')

    files = os.listdir(submissions_directory)
    pdf_files = [file for file in files if file.endswith(ext)]
    print(pdf_files)

    # tesseract_cmd = os.path.join(current_directory, 'env', 'bin', 'pytesseract', 'tesseract')
    
    for pdf_file in pdf_files:
        filepath = os.path.join(dirpath,pdf_file)
        if has_images(filepath)==True:
            
            pages = convert_from_path(submissions_directory + '/' + pdf_file, 100)
            extracted_text = ''
            for page in pages:
                extracted_text += pytesseract.image_to_string(page)
            
            output_file_path = os.path.join(processed_directory, os.path.splitext(pdf_file)[0] + '.txt')
            with open(output_file_path, 'w') as file:
                file.write(extracted_text)
