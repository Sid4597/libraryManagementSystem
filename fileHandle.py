r_file = open("book_info.txt", "r")
a_file = r_file.readlines()
string_without_line_breaks = ""
for line in a_file:
    print(line)
    stripped_line = line.rstrip()
    string_without_line_breaks += stripped_line

print(string_without_line_breaks)
b_file = open("book_infov2.txt",'w')
b_file.write(string_without_line_breaks)

r_file.close()
b_file.close()
