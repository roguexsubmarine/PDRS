import plagiarism

def strip_lines_and_return(filename):
    stripped_lines = []
    with open(filename, 'r') as file:
        for line in file:
            stripped_line = line.strip()
            stripped_lines.append(stripped_line)
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

