import re

infile1 = "datasets/bible_w_verses.txt"

out_name = "datasets/out.txt"


data1 = [line.rstrip('\n') for line in open(infile1, 'r')]


with open(out_name, 'a+') as filehandle:
        
    for line in data1:

        try:
            out = re.sub(r'([\d]+:[\d]+)', "", line).strip()

            if out != "":
                filehandle.writelines("%s\n" % out)
    
        except UnicodeEncodeError:
            pass
        


