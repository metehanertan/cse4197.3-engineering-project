import os
import re

entries = os.listdir("Tutanak/")

linecount = 0
wordcount = 0
speechcount = 0
reCount = 0
for entry in entries:
    if entry.endswith(".txt"):
        file = "Tutanak/" + entry
        if os.path.getsize(file) != 0:
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

print("linecount: ", linecount)
print("wordcount: ", wordcount)
print("BAŞKAN speech: ", speechcount)
print("other speech: ", reCount)

