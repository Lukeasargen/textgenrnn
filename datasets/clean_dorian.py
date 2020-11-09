
infile1 = "datasets/doriangray.txt"

out_name = "datasets/out.txt"


data1 = [line.rstrip('\n') for line in open(infile1, 'r')]

with open(out_name, 'a+') as filehandle:
    for line in data1:
        try:
            if line != "":
                filehandle.writelines("%s\n" % line)

        except UnicodeEncodeError:
            pass
