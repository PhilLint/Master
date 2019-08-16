import os
from Sat_final import main
import json
from sudoku_print import check_sudoku

# Exemplary how we came up with experiments
all_sudokus = os.listdir("data\\processed_sudokus")
heuristics = ["jeroslow_min", "dlcs"]
# solve all sudokus with random heuristic and save the stuff
evaluation_dict = {}
evaluation_list = []
full_evaluation_dict = {}

for i in range(40, 740):
    evaluation_dict = {}
    evaluation_list = []
    sudoku = all_sudokus[i]
    print(sudoku)
    for heuristic in heuristics:
        sols = {}
        evaluation_list, truth_assignments = main(sudoku, heuristic)
        sols = {k: v for k, v in truth_assignments.items() if v}
        print(check_sudoku(sorted(sols)))
        evaluation_dict[heuristic] = evaluation_list

    full_evaluation_dict[sudoku] = evaluation_dict

with open('full_evaluation_40_740_min.json', 'w') as f:
    json.dump(full_evaluation_dict, f)




# for i in range(10000, 10020):
#     sudoku = all_sudokus[i]
#     print(sudoku)
#     for heuristic in heuristics:
#         evaluation_list = main(sudoku, heuristic)
#         evaluation_dict[heuristic] = evaluation_list
# #
#     full_evaluation_dict[sudoku] = evaluation_dict