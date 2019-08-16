# Formulating a set of constraints used to solve the problem
# creates cnf from rule_list and sudoku_dimac
def get_cnf(sudoku_path):

    sudoku_list = open(sudoku_path).readlines()

    cnf = list()

    for line in sudoku_list: # ignore c/p = start of rule set

        if len(line) == 0 or "c" == line[0] or "p" == line[0]:
            continue

        # extract clauses
        clause_elements = line.split(" ")[0:-1] # drop the 0 at end of line
        clause = list()

        for literal in clause_elements:
            clause.append((abs(int(literal)), "-" not in literal)) # store tuple of literal and its boolean state

        cnf.append(clause)
        # removes tautologies
    cnf = contains_tautologies(cnf)

    return cnf


def contains_tautologies(cnf):
    for clause in cnf.copy():
        positives = list()
        negatives = list()

        for literal in clause:
            if literal[1] == True:
                positives.append(literal[0])
            else:
                negatives.append(literal[0])

        for literal in clause:
            if literal[0] in negatives and literal[0] in positives:
                cnf.remove(clause)
                break
    return cnf