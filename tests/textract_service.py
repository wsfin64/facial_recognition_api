import textract

text = textract.process(filename='../teste1.jpg')

print(text)