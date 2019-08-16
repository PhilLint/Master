import math as m
import os
# reads.txt sudoku collection to a list
def read_txt(path, name):
    input_file = open(path + name)
    sudoku_lines = input_file.readlines()
    sudokus = list()

    for sd in sudoku_lines:
        sudokus.append(list((sd.strip('\n'))))

    return sudokus


# processes one sudoku_list to dimac format list
def one_sudoku_to_dimac(sudoku):
    colcounter = 1
    rowcounter = 1
    # one sudoku as one dimac
    dimac = list()
    for i in range(0, len(sudoku)):

        if sudoku[i] != '.':
            dimac.append(str(rowcounter) + str(colcounter) + str(sudoku[i]) + " 0")
        colcounter += 1

        if colcounter > m.sqrt(len(sudoku)):
            if rowcounter < m.sqrt(len(sudoku)):
                rowcounter += 1
            colcounter = 1

    return dimac


# loops the one_sudoku_to_dimac function over the entire sudoku_list in one .txt file
def sudokus_to_dimacs(sudokus):
    dimacs = list()
    for sd in sudokus:
        dimacs.append(one_sudoku_to_dimac(sd))
    return dimacs


# saves each sudoku from dimac_list in one .txt file
def save_sudokus_in_dimacs(dimacs, save_path, file_name):
    for i in range(len(dimacs)):
        sudoku_name = file_name[:-4] + "_" + str(i) + ".txt"
        file = open(save_path + sudoku_name, 'w')
        file.write("\n".join(map(lambda x: str(x), dimacs[i])) + "\n")
        file.close()


# saves sudokus of a collection in single .txt files
def save_collection(path, save_path,  name):
    dimacs = sudokus_to_dimacs(read_txt(path, name))

    save_sudokus_in_dimacs(dimacs, save_path, name)

save_path = ".\\data\\processed_sudokus\\"
path = ".\\data\\"

# all collections
filenames = ["damnhard.sdk.txt", "subig20.sdk.txt", "top91.sdk.txt", "top91.sdk.txt", "top95.sdk.txt", "top100.sdk.txt",
             "top870.sdk.txt", "top2365.sdk.txt"]

# save all sudokus of all collections
for name in filenames:
    save_collection(path, save_path, name)

all_sudokus = os.listdir("data\\processed_sudokus")

rule_path = ".\\data\\sudoku-rules.txt"
processed_path = ".\\data\\processed_sudokus\\"

# Add rules to sudoku DIMACS
for i in range(len(all_sudokus)):
    sudoku_name = all_sudokus[i]

    rule_list = open(rule_path).readlines()

    sudoku_list = open(processed_path + sudoku_name).readlines()

    merged_list = rule_list + sudoku_list

    with open(processed_path + sudoku_name, 'w') as f:
        for item in merged_list:
            f.write("%s" % item)
