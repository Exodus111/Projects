from docx2html import convert

html = convert('./Geit (utkast).docx')
myfile = open('testfile.txt', 'rw+')
myfile.write(html)
myfile.close()
