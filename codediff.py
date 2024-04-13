import plagiarism
import os

ext = ('.py', '.c', '.cpp', '.txt','.java','.html')
def strip_lines_and_return(p):
    stripped_lines = []
    # with open(filename, 'r') as file:
    #     for line in file:
    #         stripped_line = line.strip()
    #         stripped_lines.append(stripped_line)
    # return stripped_lines

    if p.endswith('.docx'):
        
        # file_path = os.path.join(p, filename)
        # file_names.append(filename)
        import docx
        doc = docx.Document(p)
        text = ''
        for paragraph in doc.paragraphs:
            text += paragraph.text + '\n'
        stripped_lines = text
        # for line in text:
        #     stripped_line = line.strip()
        #     stripped_lines.append(stripped_line)
        return stripped_lines
            
            
    if p.endswith('.pdf'):
        # file_path = os.path.join(p, filename)
        # file_names.append(filename)
        import PyPDF2
        pdfFileObject = open(p, 'rb')
        reader = PyPDF2.PdfReader(pdfFileObject)
        count = len(reader.pages)
        output=""
        for i in range(count):
            page = reader.pages[i]
            stripped_lines.append(page)
        return stripped_lines        
    
    if p.endswith('.ipynb'):
        # file_path = os.path.join(p, filename)
        # file_names.append(filename)
        import nbformat
        notebook = nbformat.read(p, as_version=4)
        source_code = []
        for cell in notebook.cells:
            if cell.cell_type == 'code':
                source_code.append(cell.source)
        stripped_lines=source_code
        # for line in source_code:
        #     stripped_line = line.strip()
        #     stripped_lines.append(stripped_line)
        return stripped_lines

        notebook_text = '\n'.join(source_code)
        
    if p.endswith(ext):
        # file_path = os.path.join(p, filename)
        try:
            with open(p, encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            print(f"UnicodeDecodeError: Unable to decode '{filename}'")
        stripped_lines=content
        # for line in content:
        #     stripped_line = line.strip()
        #     stripped_lines.append(stripped_line)
        return stripped_lines




def codediff(file1, file2):
    file1_lines = strip_lines_and_return(str(file1))
    file2_lines = strip_lines_and_return(str(file2))

    diff_file1 = []
    diff_file2 = []

    for line in file1_lines:
        if line in file2_lines:
            diff_file1.append("*" + line)
        else:
            diff_file1.append("~" + line)

    for line in file2_lines:
        if line not in file1_lines:
            diff_file2.append("*" + line)
        else:
            diff_file2.append("~" + line)

    return [diff_file1, diff_file2]

# Example usage
# diff_result = codediff('html1.txt', 'html2.txt')
# for line in diff_result[0]:
#     print(line)

