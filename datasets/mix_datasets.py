import numpy as np

infile1 = "dev/com_upper.txt"

infile2 = "datasets/bible.txt"

out_name = "datasets/out.txt"


data1 = [line.rstrip('\n') for line in open(infile1, 'r')]
data2 = [line.rstrip('\n') for line in open(infile2, 'r')]

size = min(len(data1), len(data2))
print("Size :", size)

valid_indices1 = np.array(range(len(data1)))
indices1 = np.random.choice(valid_indices1, size = size, replace = False)

valid_indices2 = np.array(range(len(data2)))
indices2 = np.random.choice(valid_indices2, size = size, replace = False)


with open(out_name, 'a+') as filehandle:
    for i in range(size):
        try:
            out1 = data1[indices1[i]]
            if out1 != "":
                filehandle.writelines("%s\n" % out1)
    
            out2 = data2[indices2[i]]
            if out2 != "":
                filehandle.writelines("%s\n" % out2)
    
        except UnicodeEncodeError:
            pass
