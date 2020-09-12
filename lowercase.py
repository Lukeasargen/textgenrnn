raw_lines = [line.rstrip('\n').lower().replace('é','e') for line in open('doriangray_v2.txt', 'r', encoding="utf-8-sig")]

with open('doriangray_v2_lowercase.txt', 'a+') as filehandle:
    # for comment in raw_lines:
    #     filehandle.writelines("%s\n" % comment)
    [filehandle.writelines("%s\n" % comment) for comment in raw_lines]
print("---- Complete ----")
