import numpy as np

infile1 = "dev/com_upper.txt"
alpha1 = 1.0

infile2 = "datasets/bible.txt"
alpha2 = 0.2

out_name = "datasets/out.txt"


data1 = [line.rstrip('\n') for line in open(infile1, 'r')]
data2 = [line.rstrip('\n') for line in open(infile2, 'r')]

size = min(len(data1), len(data2))
print("Size :", size)

valid_indices1 = np.array(range(len(data1)))
indices1 = np.random.choice(valid_indices1, size = int(size*alpha1), replace = False)

valid_indices2 = np.array(range(len(data2)))
indices2 = np.random.choice(valid_indices2, size = int(size*alpha2), replace = False)


with open(out_name, 'a+') as filehandle:

    for idx in indices1:
        try:
            out = data1[idx]
            if out != "":
                filehandle.writelines("%s\n" % out)
        except UnicodeEncodeError:
            pass
    
    for idx in indices2:
        try:
            out = data2[idx]
            if out != "":
                filehandle.writelines("%s\n" % out)
        except UnicodeEncodeError:
            pass
