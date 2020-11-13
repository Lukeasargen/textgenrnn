import numpy as np

np.set_printoptions(precision=4, suppress=True)

# [file path, ratio of final dataset]

infiles = [
    ["dev/com_upper.txt", 7],
    ["datasets/bible.txt", 2],
    ["datasets/ba_brad.txt", 1],
    ["datasets/ba_claire.txt", 1],
]

out_name = "datasets/out.txt"

def load_file(path):
    return [line.rstrip('\n') for line in open(path, 'r')]

data = [load_file(x[0]) for x in infiles]

alphas = np.array([x[1] for x in infiles])
print("alphas :", alphas)

data_len = np.array([len(x) for x in data])
print("data_len :", data_len)

# find the highest scale to get the most data
scale = 2.718281
for i in range(50):
    temp = alphas * scale
    # print(temp)
    # print(data_len - temp)
    min_idx = np.argmin(data_len-temp)
    t = (data_len[min_idx]-temp[min_idx] ) / data_len[min_idx]
    # print(i, t, scale)
    scale += scale*t*0.367879441  # 1/e, idk why but it works

print("Final scale:", scale)

get_n = np.floor(alphas * scale)
print("Number from each dataset :", get_n)
print("Percent of final dataset :", get_n/np.sum(get_n))
print("Total samples :", np.sum(get_n))


def get_random_indices(length, n):
    return np.random.choice(range(length), size = int(n), replace = False)

indices = [get_random_indices(data_len[i], get_n[i]) for i in range(len(infiles))]

print("Writing to output file...")

with open(out_name, 'w+') as filehandle:

    for i in range(len(infiles)):

        for idx in indices[i]:
            try:
                out = data[i][idx]
                if out != "":
                    filehandle.writelines("%s\n" % out)
            except UnicodeEncodeError:
                pass

print("Done")