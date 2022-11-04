fh2 = open("mapping.all.map", "r")
id_dict = {}
for line in fh2:
    id_dict[line.split("\t")[1].upper().rstrip()] = line.split("\t")[0].upper().rstrip()
fh2.close()

fh1 = open("combined_benchmark.tsv", "r")
fhw = open("CAFA_benchmark.tsv", "w")
for line in fh1:
    # print(line.split("\t")[0].upper())
    try:
        # print(id_dict[line.split("\t")[0].upper().rstrip()])
        fhw.write(str(id_dict[line.split("\t")[0].upper().rstrip()]) + "\t" + str(line.split("\t")[1]))
    except:
        continue
fh1.close()
fhw.close()
