import os
import re

entries = os.listdir("Tutanak/")

txtcount = 0
linecount = 0
wordcount = 0
speechcount = 0
reCount = 0
for entry in entries:
    if entry.endswith(".txt"):
        file = "Tutanak/" + entry
        if os.path.getsize(file) != 0:
            txtcount += 1
            f = open(file, encoding="utf-8")

            #find line and word count
            for line in f:

                if "BAŞKAN -" in line:
                    speechcount +=1

                x = re.findall('[A-Z ]{2,}\(.*?\)', line)
                reCount += len(x)

                linecount += 1
                line.replace(',', '')
                line.replace('-', '')
                line.replace(':', '')
                line.replace(';', '')
                res = len(line.split())
                wordcount += res

print("txtcount: ",txtcount)
print("linecount: ", linecount, ", ", linecount/txtcount)
print("wordcount: ", wordcount, ", ", wordcount/txtcount)
print("BAŞKAN speech: ", speechcount, ", ", speechcount/txtcount)
print("other speech: ", reCount, ", ", reCount/txtcount)

