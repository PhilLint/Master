import timeit

import numpy as np
from itertools import chain
global FAILURES, NUMBER_OF_ASSIGNMENTS, NUMBER_OF_REMOVED_UNIT_CLAUSES, NUMBER_OF_SPLITS
global DPLL_CALLS, SAVE_SOLUTION

FAILURES = 0
NUMBER_OF_ASSIGNMENTS = 0
NUMBER_OF_REMOVED_UNIT_CLAUSES = 0
NUMBER_OF_SPLITS = 0
DPLL_CALLS = 0
SAVE_SOLUTION = False
# -> always false -> inconsistent problem
def contains_empty_clause(cnf):
    for clause in cnf:
        if not clause:
            return True
    return False

# -> always true
def empty_set_of_clauses(cnf):
    return not cnf

def delete_unit_clauses(cnf, truth_assignments):
    global NUMBER_OF_REMOVED_UNIT_CLAUSES
    new_cnf = cnf
    change = True
    while change:
        change = False
        for clause in new_cnf:
                    if len(clause) == 1:
                        change = True
                        NUMBER_OF_REMOVED_UNIT_CLAUSES += 1
                        unitliteral = (clause[0][0], clause[0][1])
                        new_cnf, truth_assignments = assign_truth(unitliteral, new_cnf, truth_assignments)
                        break

    return new_cnf, truth_assignments

# only to be applied once at the start
def contains_tautologies(cnf):
    for clause in cnf:
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

def assign_truth(literal_tuple, cnf, truth_assignments):
    global NUMBER_OF_ASSIGNMENTS
    NUMBER_OF_ASSIGNMENTS += 1
    new_cnf = remove_true_and_false_clauses(cnf, literal_tuple)
    truth_assignments[literal_tuple[0]] = literal_tuple[1]
    return new_cnf, truth_assignments

def remove_true_and_false_clauses(cnf, literal_tuple):
    new_cnf = [[elem for elem in c if not literal_tuple[0] in elem] for c in cnf if literal_tuple not in c]
    return new_cnf

def count_pos_neg(cnf):
    pos_neg_dict = {}

    for c in cnf:
        for tuple in c:
            if tuple[0] not in pos_neg_dict:

                pos_neg_dict[tuple[0]] = [0,0,0]

                if tuple[1] == True:
                    pos_neg_dict[tuple[0]][0] += 1
                else:
                    pos_neg_dict[tuple[0]][1] += 1
            else:
                if tuple[1] == True:
                    pos_neg_dict[tuple[0]][0] += 1
                else:
                    pos_neg_dict[tuple[0]][1] += 1
            pos_neg_dict[tuple[0]][2] = pos_neg_dict[tuple[0]][0] + pos_neg_dict[tuple[0]][1]

    return pos_neg_dict

def clause_length(cnf):
    clause_len_dict = {}
    id = 0
    for c in cnf:
        id += 1
        clause_len_dict[id] = len(c)

    return clause_len_dict

def create_literal_dict(cnf):
    literal_dict = {}
    clause_counter = 0

    for c in cnf:
        clause_counter += 1
        for literal in c:
            if literal not in literal_dict:
                literal_dict[literal] = [clause_counter]
            else:
                literal_dict[literal].append(clause_counter)
    return literal_dict

def jeroslow_heuristic_max(cnf):

    clause_len_dict = clause_length(cnf)
    literal_dict = create_literal_dict(cnf)

    jeroslow_dict = {}

    for key, value in literal_dict.items():
        jeroslow_dict[key] = 0
        for clause_id in value:
            jeroslow_dict[key] += 2**(-clause_len_dict[clause_id])

    select_tuple = max(jeroslow_dict, key = jeroslow_dict.get)

    return select_tuple[0], select_tuple[1]

def jeroslow_heuristic_min(cnf):

    clause_len_dict = clause_length(cnf)
    literal_dict = create_literal_dict(cnf)

    jeroslow_dict = {}

    for key, value in literal_dict.items():
        jeroslow_dict[key] = 0
        for clause_id in value:
            jeroslow_dict[key] += 2**(-clause_len_dict[clause_id])

    select_tuple = min(jeroslow_dict, key = jeroslow_dict.get)

    return select_tuple[0], select_tuple[1]

def dlcs_heuristic(pos_neg_dict):
    sum_max = 0

    for key, value in pos_neg_dict.items():
        if value[2] > sum_max:
            sum_max = value[2]
            select_literal = key

    if pos_neg_dict[select_literal][0] >= pos_neg_dict[select_literal][1]:
        select_truth = True
    else:
        select_truth = False

    return select_literal, select_truth

def dlis_heuristic(pos_neg_dict):
    total_max = 0

    for key, value in pos_neg_dict.items():
        tmp_max = max(value[0], value[1])
        if tmp_max > total_max:
            total_max = tmp_max
            select_literal = key

    if pos_neg_dict[select_literal][0] >= pos_neg_dict[select_literal][1]:
        select_truth = True
    else:
        select_truth = False

    return select_literal, select_truth

def simple_select(cnf):
    select_literal = cnf[0][0][0]
    select_truth = True
    return select_literal, select_truth

def select(cnf, heuristic):
    global NUMBER_OF_SPLITS
    NUMBER_OF_SPLITS += 1

    if heuristic == "random":
        select_literal, select_truth = simple_select(cnf)

    elif heuristic == "dlcs":
        pos_neg_dict = count_pos_neg(cnf)
        select_literal, select_truth = dlcs_heuristic(pos_neg_dict)

    elif heuristic == "dlis":
        pos_neg_dict = count_pos_neg(cnf)
        select_literal, select_truth = dlis_heuristic(pos_neg_dict)

    elif heuristic == "jeroslow_max":
        select_literal, select_truth = jeroslow_heuristic_max(cnf)

    elif heuristic == "jeroslow_min":
        select_literal, select_truth = jeroslow_heuristic_min(cnf)

    return select_literal, select_truth


def dpll(cnf, truth_assignments = {}):
    global FAILURES, DPLL_CALLS
    DPLL_CALLS += 1
    # simplification steps: delete unitclauses and pure literals
    cnf, truth_assignments = delete_unit_clauses(cnf, truth_assignments)

    if contains_empty_clause(cnf):
        #print("failure")
        FAILURES += 1
        return False, {}

    if empty_set_of_clauses(cnf):
        #print("success")
        return True, truth_assignments

    select_literal, select_truth = select(cnf, HEURISTICS)

    new_cnf, truth_assignments_after_split = assign_truth((select_literal, select_truth), cnf, truth_assignments)

    satisfied, truth_assignments_after_split = dpll(new_cnf, truth_assignments_after_split)

    if satisfied:
        return satisfied, truth_assignments_after_split
    else:

        new_cnf, truth_assignments_after_split = assign_truth((select_literal, not select_truth), cnf, truth_assignments)

        satisfied, truth_assignments_after_split = dpll(new_cnf, truth_assignments_after_split)

        if satisfied:
            return satisfied, truth_assignments_after_split
        else:
            return False, {}

def find_solution(cnf):
    # dont even start if cnf is flawed
    if contains_empty_clause(cnf):
        #print("failure")
        return False, {}
    if empty_set_of_clauses(cnf):
        # print("success")
        return True, truth_assignments

    return dpll(cnf)

def main():
    global FAILURES, NUMBER_OF_ASSIGNMENTS, NUMBER_OF_REMOVED_UNIT_CLAUSES, NUMBER_OF_SPLITS
    global DPLL_CALLS, SAVE_SOLUTION
    global HEURISTICS
    import sys
    from get_cnf import get_cnf

    if len(sys.argv) > 1:
        method = sys.argv[1]
        filename = sys.argv[2]

    if method == '-S1':
        HEURISTICS = "random"

    elif method == '-S2':
        HEURISTICS = "dlcs"

    elif method == "-S3":
        HEURISTICS = "dlis"

    elif method == "-S4":
        HEURISTICS = "jeroslow_max"

    elif method == "-S5":
        HEURISTICS = "jeroslow_min"

    FAILURES = 0
    NUMBER_OF_ASSIGNMENTS = 0
    NUMBER_OF_REMOVED_UNIT_CLAUSES = 0
    NUMBER_OF_SPLITS = 0
    DPLL_CALLS = 0
    SAVE_SOLUTION = True

   # sudoku_folder_path = ".\\data\\processed_sudokus\\"
    #sudoku_solution_path = ".\\data\\solved_sudokus\\"

    cnf = get_cnf(filename)

    start = timeit.default_timer()
    sat, truth_assignments = find_solution(cnf)
    stop = timeit.default_timer()

    if SAVE_SOLUTION:
        output = sudoku_solution_path + filename + "_out.txt"

        fo = open(output, "w")
        for key, value in truth_assignments.items():
            if value == False:
                key = "-" + str(key) + " 0"
            else:
                key = str(key) + " 0"
            fo.write(key + "\n")
        fo.close()

    runtime = stop - start
    runtime = "{0:.4f}".format(runtime)

    print("truth_assignments:", truth_assignments)
    #evaluation_list = []
    #evaluation_list = [FAILURES, NUMBER_OF_ASSIGNMENTS, NUMBER_OF_REMOVED_UNIT_CLAUSES,
    #                   NUMBER_OF_SPLITS, DPLL_CALLS, runtime, given_literals]

if __name__ == "__main__":
    main()