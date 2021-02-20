import codecs
import os
import re


def remove_html_markup(s):
    tag = False
    quote = False
    out = ""

    for c in s:
        if c == '<' and not quote:
            tag = True
        elif c == '>' and not quote:
            tag = False
        elif (c == '"' or c == "'") and tag:
            quote = not quote
        elif not tag:
            out = out + c

    return out


line = 0
entries = os.listdir("./tutanak/")
for entry in entries:
    if entry.endswith(".html"):
        file = "./tutanak/" + entry
        if os.path.getsize(file) != 0:
            with open(file, "r", encoding='utf-8') as f:
                text = f.read()
                text = remove_html_markup(text)
                text = text.replace("\n\n", " ")
                text = text.replace("  ", " ")
                oturum = re.findall('[A-ZĞÜŞIÖÇİ]+ OTURUM', text)
                print(oturum)
                çizgi = re.findall("-+0-+",text)
                print(çizgi)
                print(text)


                # Spliting speeches
                # x = re.findall('[A-ZĞÜŞIÖÇİ ]* \([A-ZĞÜŞÖÇİ][a-zğüşıöç]*\) - ', text)
                x = re.findall('[A-ZĞÜŞIÖÇİ\s*]{2,}\([a-zğüşıöçA-ZĞÜŞIÖÇİ]+\)', text)
                x = list(dict.fromkeys(x))

                for speech in x:
                    s = "\n" + speech[1: len(speech)]
                    text = text.replace(speech, s)
                # print(len(x), " : ", x)

                text = text.replace("BAŞKAN –", "\nBAŞKAN -")

                speeches = text.split("\n")

                for sp in speeches:
                    if len(sp.split("-")) >= 2:
                        print(end="")

    break
