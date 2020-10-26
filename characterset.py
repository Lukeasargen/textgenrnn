

filename = 'datasets/doriangray.txt'
raw_text = open(filename, 'r', encoding='utf-8').read()
# raw_text = raw_text.lower()

chars = sorted(list(set(raw_text)))
# char_to_int = dict((c, i) for i, c in enumerate(chars))
print("Number of characters : ",len(chars))
print(chars)
