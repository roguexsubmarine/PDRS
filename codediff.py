import plagiarism
import os

ext = ('.py', '.c', '.cpp', '.txt', '.java', '.html')


def strip_lines_and_return(p):
    stripped_lines = []

    if p.endswith('.docx'):
        import docx
        doc = docx.Document(p)
        for paragraph in doc.paragraphs:
            stripped_lines.append(paragraph.text.strip())

    elif p.endswith('.pdf'):
        import PyPDF2
        pdfFileObject = open(p, 'rb')
        reader = PyPDF2.PdfReader(pdfFileObject)
        for page in reader.pages:
            stripped_lines.extend(page.extract_text().split('\n'))

    elif p.endswith('.ipynb'):
        import nbformat
        notebook = nbformat.read(p, as_version=4)
        for cell in notebook.cells:
            if cell.cell_type == 'code':
                source_code_lines = cell.source.split('\n')
                stripped_lines.extend(source_code_lines)

    elif p.endswith(ext):
        with open(p, encoding='utf-8') as f:
            content = f.readlines()
            for line in content:
                stripped_lines.append(line.strip())

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

