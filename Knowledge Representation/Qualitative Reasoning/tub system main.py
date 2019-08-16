import itertools                        # permutations
import copy                             # copies objects
from graphviz import Digraph            # graph visualization
from tubsystemclass import State        # defines objects for entities and quantities
from tubsystemclass import Quantity

# trace of algorithm is saved in .txt file
global trace
trace_counter1 = 0
trace_counter2 = 0
trace_counter3 = 0

# system assumptions
# 1) constant versus random positive inflow
# 2) the bathtub has unknown but yet finite dimensions (finite height, width & length)
#    -> the bathtub reaches its maximally filled state and then overflows
# 3) the bathtubs's drain is an opening of a certain, fixed size that remains open all the time
#    -> it is not possible to close the drain. If water is in the tub, there will be a positive outflow
# 5) Initially, the bathtub is empty and the tab is closed
# 6) the environment surrounding the bathtub system can be imagined as an infinite space
#    -> the bathtub can overflow forever / the impact of the overflowing water on the surrounding is neglected

# quantity spaces
zero_pos_max = ["0", "+", "max"]
# inflow quantity space
zero_pos = ["0", "+"]
# derivative space (same for all)
minus_zero_pos = ["-", "0", "+"]
# landmarks of quantities
landmarks = ["0", "max"]
# all appearing quantities
all_quantities = ["inflow", "volume", "height", "pressure", "outflow"]

# create all object instances in their initial state
# Quantity objects
def create_all_possible_states():
    global trace
    # list of all possible states
    all_permutations = list(
        itertools.product(zero_pos, minus_zero_pos, zero_pos_max, minus_zero_pos, zero_pos_max, minus_zero_pos,
                          zero_pos_max, minus_zero_pos, zero_pos_max, minus_zero_pos))

    full_state_list = []
    for i in range(len(all_permutations)):
        tmp_quant = []
        tmp_quant = all_permutations[i]
        full_state_list.append(State(Quantity("inflow", zero_pos, tmp_quant[0], tmp_quant[1], ["I+", "volume"], []),
                                      Quantity("volume", zero_pos_max, tmp_quant[2], tmp_quant[3], ["P+", "height"],
                                               ["height", "pressure", "outflow"]),
                                      Quantity("height", zero_pos_max, tmp_quant[4], tmp_quant[5], ["P+", "pressure"],
                                               ["volume", "pressure", "outflow"]),
                                      Quantity("pressure", zero_pos_max, tmp_quant[6], tmp_quant[7], ["P+", "outflow"],
                                               ["volume", "height", "outflow"]),
                                      Quantity("outflow", zero_pos_max, tmp_quant[8], tmp_quant[9], ["I-", "volume"],
                                               ["volume", "height", "pressure"])))

    trace.write("All possible states are created as a list (valid and invalid) with a total of :" + str(len(full_state_list)) + '\n')
    return full_state_list

# Check for valid states
# 1. Check for correspondences: if the quantity of either volume, pressure, height or outflow is landmark value
# then the respective quantity/magnitude values of all other quantities have to be the same
def check_correspondences(state):
    if state.quantities[1].quantity in landmarks:
        if not state.quantities[1].quantity == state.quantities[2].quantity == state.quantities[3].quantity == \
               state.quantities[4].quantity:
            return False
    if state.quantities[2].quantity in landmarks:
        if not state.quantities[1].quantity == state.quantities[2].quantity == state.quantities[3].quantity == \
               state.quantities[4].quantity:
            return False
    if state.quantities[3].quantity in landmarks:
        if not state.quantities[1].quantity == state.quantities[2].quantity == state.quantities[3].quantity == \
               state.quantities[4].quantity:
            return False
    if state.quantities[4].quantity in landmarks:
        if not state.quantities[1].quantity == state.quantities[2].quantity == state.quantities[3].quantity == \
               state.quantities[4].quantity:
            return False
    return True

def delete_failed_correspondences(state_list):
    # delete_failed_correspondences(full_state_list[57]) -> If not fulfilled return False -> delete of list
    return_list = []
    trace.write("  States not consistent with correspondences are deleted" + '\n')
    # delete all states that do not fulfill correspondence rules
    for i in range(len(state_list)):
        if check_correspondences(state_list[i]):
            return_list.append(state_list[i])
    return return_list

# cheack for proportionalities: As shown in our causal model: these proportionality influences exist
# and if one state does not meet that criteria, it is considered invalid
def check_proportionalities(state):
    if state.quantities[1].derivative == "+":
        if not (state.quantities[2].derivative == "+" and state.quantities[3].derivative == "+" and state.quantities[
            4].derivative == "+"):
            return False
    elif state.quantities[1].derivative == "-":
        if not (state.quantities[2].derivative == "-" and state.quantities[3].derivative == "-" and state.quantities[
            4].derivative == "-"):
            return False
    elif state.quantities[1].derivative == "0":
        if not (state.quantities[2].derivative == "0" and state.quantities[3].derivative == "0" and state.quantities[
            4].derivative == "0"):
            return False
    return True

# check for system constraints: 1) there can not be a quantity with a max magnitude and a positive derivative
#                               2) if the inflow is 0 and the quantity/magnitude of another quantity max, then
#                                  the respective derivative has to be -
#                               3) there can not be a quantity with a 0 magnitude and a negative derivative
def check_system_constraints(state):
    if state.quantities[1].quantity == "max" and state.quantities[1].derivative == "+":
        return False
    if state.quantities[0].quantity == "0" and state.quantities[1].quantity == "max":
        if not state.quantities[1].derivative == "-":
            return False
    if state.quantities[1].quantity == "0" and state.quantities[1].derivative == "-":
        return False
    return True

def delete_failed_proportionalities(state_list):
    trace.write("  States not consistent with system constraints and proportionalities are deleted" + '\n')
    return_list = []
    for i in range(len(state_list)):
        if check_system_constraints(state_list[i]):
            if check_proportionalities(state_list[i]):
                return_list.append(state_list[i])
    return return_list

# 2. Check possible transitions
# inflow_outflow_ratio: '<' | '>' | '='
def check_failed_influences(state):
    if state.quantities[0].quantity == "0" and state.quantities[4].quantity == "0":
        if not state.quantities[1].derivative == "0":
            return False
    if state.quantities[0].quantity == "+" and state.quantities[4].quantity == "0":
        if not state.quantities[1].derivative == "+":
            return False
    if state.quantities[0].quantity == "0" and state.quantities[4].quantity == "+":
        if not state.quantities[1].derivative == "-":
            return False
    if state.quantities[0].quantity == "0" and state.quantities[0].derivative == "-":
        return False
    return True

# 3. check for invalid influences
def delete_failed_influences(state_list):
    # influences(corr_full_list[57]) -> If not fulfilled return False -> delete of list
    return_list = []
    trace.write("  States not consistent with influences are deleted" + '\n')
    # delete all states that do not fulfill influence rules
    for i in range(len(state_list)):
        if check_failed_influences(state_list[i]):
            return_list.append(state_list[i])

    trace.write("  Only valid states left. A total of: " + str(len(return_list)) + '\n')
    return return_list

# Bundle the above functions to obtain only 24 valid states
def create_all_valid_states():
    # all possible permutations created
    full_state_list = create_all_possible_states()
    # only states fulfilling correspondences, proportionalities and system constraints
    # remain in the state_list
    current_state_list = delete_failed_correspondences(full_state_list)
    current_state_list = delete_failed_proportionalities(current_state_list)
    current_state_list = delete_failed_influences(current_state_list)
    return current_state_list

########################################################################################################################
## FUNCTIONS FOR THE 'MAIN' PART: How to obtain the graph

# return quantities that do not change in current step, as magnitude is in landmarks and derivative 0
# def get_constant_quantities(state):
#     constant_quantities = []
#     for i in range(len(state.quantities)):
#         if state.quantities[i].quantity in landmarks and state.quantities[i].derivative == '0':
#             constant_quantities.append(state.quantities[i].name)
#     return constant_quantities

# quantities that have derivatives not 0 and quantity that allow certain change are returned
# e.g either (0,+) or if max is allowed: (+,+)
# landmark_quantities: those which have magnitude of landmark of respective quantity
# quantities: not landmark magnitude value
def get_inconstant_quantities(state):
    quantities = []
    landmark_quantities = []
    for i in range(len(state.quantities)):
        if state.quantities[i].derivative != '0':
            if not (state.quantities[i].quantity == state.quantities[i].quantity_space[-1] and
                    state.quantities[i].derivative == "+") and not (
                    state.quantities[i].quantity == state.quantities[i].quantity_space[0] and
                    state.quantities[i].derivative == "-"):
                if state.quantities[i].quantity in landmarks:
                    landmark_quantities.append(state.quantities[i].name)
                else:
                    quantities.append(state.quantities[i].name)
    return quantities, landmark_quantities

# given indices of changing quantities -> get all possible combination of changes
# takes strings of the quantity names as input and outputs all possible permutations
def get_all_possible_changes(changeable_quantities):
    combinations = []
    for i in range(1, len(changeable_quantities) + 1):
        combinations.extend(list(list(itertools.combinations(changeable_quantities, i))))
    return combinations

# disadvantage of objects: need to find the index of given quantity name to then access the respective quantity
# could also hardcode "inflow" -> 0, but not as elegant...
# find index of quantityname within quantity_object
def get_index_of_quantity(quantity_obj, q_name):
    for i in range(len(quantity_obj.quantities)):
        # print("quantity name: " + str(quantity_obj.quantities[i].name))
        if quantity_obj.quantities[i].name == q_name:
            return i

# return possible new_states that can follow given one state and possible_next_quantities by performing changes
# according to the derivative values of the incoming quantities and state
def change_quantities(state, possible_next_quantities):
    new_states = []
    for possible_next_quantity in possible_next_quantities:
        # print("index: " + str(i))
        # necessary, as python uses references and would otherwise alter the reference object
        changed_state = copy.deepcopy(state)
        for quantity in possible_next_quantity:
            q_index = get_index_of_quantity(state, quantity)
            # positive derivative -> increase quantity if possible
            if state.quantities[q_index].derivative == '+':
                changed_state = change_quantity(changed_state, q_index, "+")
            else:
                # negative derivative -> decrease quantitiy if possible
                changed_state = change_quantity(changed_state, q_index, "-")
        new_states.append(changed_state)
    return new_states

# perform the actual change of quantity for one state depending on the type_of_change (+,-)
def change_quantity(state, q_index, type_of_change):
    # new_state is copy of old one with changes made in the process
    new_state = copy.deepcopy(state)
    # which index of the quantity_space does the current magnitude of q_index magnitude have
    index = state.quantities[q_index].quantity_space.index(state.quantities[q_index].quantity)
    # if magnitude decreases
    if type_of_change == "-":
        # if not first quantity -> decrease quantity by one
        if index != 0:
            new_state.quantities[q_index].quantity = state.quantities[q_index].quantity_space[index - 1]
    # if magnitude increases
    elif type_of_change == "+":
        # if not largest quantity already -> increase quantity per one
        if index != (len(state.quantities[q_index].quantity_space) - 1):
            new_state.quantities[q_index].quantity = state.quantities[q_index].quantity_space[index + 1]
    return new_state

# Depending on the user input (which exogenous is given), the exogenous derivative can change during the process (- -> 0)
# Also if the quantity is max, then the derivative can not be + anymore
def get_following_inflow_derivative(state):
    possible_derivatives = []
    # stable exogenous derivative -> can not change to + or -
    if user_input == 's':
        possible_derivatives = ['0']
    # decreasing inflow derivative -> can change to 0, if magnitude of inflow is 0
    elif user_input == 'd':
        if state.quantities[0].quantity == state.quantities[0].quantity_space[0]:
            possible_derivatives = ['0']
        else:
            possible_derivatives = ['-']
    # no maximum magnitude of inflow, therefore no reason to change derivative in this scenario
    elif user_input == 'i':
            possible_derivatives = ['+']
    return possible_derivatives

# depending on the user_input: The derivative of the exogenous inflow is set for decreasing -, increasing +, stable 0
def get_inflow_derivative():
    inflow_derivative = []
    if user_input == 'd':
        inflow_derivative = ['-']
    elif user_input == 's':
        inflow_derivative = ['0']
    elif user_input == 'i':
        inflow_derivative = ['+']
    return inflow_derivative

# check if quantity stays the same
def quantity_consistency(new_state, state):
    break_bool = True
    for quantity_index in range(len(new_state.quantities)):
        if new_state.quantities[quantity_index].quantity != state.quantities[quantity_index].quantity:
            break_bool = False
            break
    return break_bool

# check if constant derivatives stay constant
def constant_derivative_consistiency(new_state, state, constant_derivatives):
    break_bool = True
    for index in constant_derivatives:
        quantity_index = get_index_of_quantity(new_state, index)
        if new_state.quantities[quantity_index].derivative != state.quantities[quantity_index].derivative:
            break_bool = False
            break
    return break_bool

# check if derivative of new_state is in possible next inflow derivative
def possible_next_inflow_derivative(new_state, state):
    break_bool = True
    possible_derivs = get_following_inflow_derivative(new_state)
    if state.quantities[0].derivative not in possible_derivs:
        break_bool = False
    return break_bool

# check if derivative transition is continous and not of 'stepsize' larger than one
def transition_continuity(new_state, state):
    break_bool = True
    # continuity check (only derivative changes of one)
    for quantity_index in range(len(state.quantities)):
        if abs(minus_zero_pos.index(state.quantities[quantity_index].derivative) - minus_zero_pos.index(
                new_state.quantities[quantity_index].derivative)) > 1:
            break_bool = False
            break
    return break_bool

# given all valid states and a new_state that has been determined by the
# previous steps as a valid next step -> return the incoming step as parent and
# the following state as child: get_edge between new_state and
# Input are all valid states, the supposed new state and all the quantities whose derivatives are not changing
def get_children(all_valid_states, new_state, constant_derivatives):
    children = []
    # quantity filtering
    for state in all_valid_states:
        if quantity_consistency(new_state, state):
            if constant_derivative_consistiency(new_state, state, constant_derivatives):
                if possible_next_inflow_derivative(new_state, state):
                    if transition_continuity(new_state, state):
                        children.append(all_valid_states.index(state))
                    else:
                        continue
                else:
                    continue
            else:
                continue
        else:
            continue
    return children

# Objects are not as easily accessible as dicts or lists, therefore function for proper printing needed
def quantity_object_to_string(state):
    # decode objects to list of strings -> for graph printing
    return_state = []
    if state == "Start":
        return "Start"
    counter = 0
    for i in range(len(state)):
        counter += 1
        if counter == 1:
            return_state.append(state[i].name + ": (" + state[i].quantity + "," + state[i].derivative + ")\n")
        elif counter > 1 and counter < 5:
            return_state.append(state[i].name + "  = ")
        else:
            return_state.append(state[i].name + ": (" + state[i].quantity + "," + state[i].derivative + ")")
    return return_state

# makes it easier to see, which states are currently valid -> for debugging purposes
def print_all_states(state_list):
    string_states = []
    for i in range(len(state_list)):
        string_states.append(quantity_object_to_string(state_list[i].quantities))
    return string_states

# return states with same derivative as exogenous state
def get_exogenous_derivative_states(all_valid_states):
    exog_states = []
    for state in all_valid_states:
        # only states with same inflow derivative as the original exogenous value are possible
        if state.quantities[0].derivative in get_inflow_derivative():
            exog_states.append(state)
    return exog_states

# if valid child has change in exogenous derivative -> add to possible_start_states, as sometimes changes
# in exogenous quantities can happen (e.g. 'decreasing': (+,-) -> (0,0) instead of (0,-), whereas (0,0) was
# not part of possible_start_states
def add_to_possible_start_states(children, all_valid_states, possible_start_states):
    # element of children that is not part of possible_states -> add o possible states
    for child_index in children:
        if all_valid_states[child_index] not in possible_start_states:
            possible_start_states.append(all_valid_states[child_index])
    return possible_start_states

# Only if there are possible children to state, then add children to adjacency_list at index of state, while
# removing the state itself from children
def add_child_to_adjacency_list(state, all_valid_states, children, adjacency_list):
    if len(children) > 0:
        state_index = all_valid_states.index(state)
        if state_index in children:
            children.remove(state_index)
        adjacency_list[state_index].extend(children)
    return adjacency_list

def coherent_derivative_proceeding(children, new_state, all_valid_states, changing_quantities):
    # if there are no children -> check if derivative is constant: if quantity is not in landmarks
    # derivative does not change
    if len(children) == 0:
        constant_derivatives = []
        for changing_quantity in changing_quantities:
            q_index = get_index_of_quantity(new_state, changing_quantity)
            if new_state.quantities[q_index].quantity not in landmarks:
                constant_derivatives.append(changing_quantity)

        children = get_children(all_valid_states, new_state, constant_derivatives)
        if not len(children) == 0:
            children = [children[0]]

    return children

# depending on the amount of changing states -> get possible children to parent state
def add_children(state, new_states, changing_quantities, all_valid_states, possible_start_states, adjacency_list):
    for new_state in new_states:
        if not len(changing_quantities) == 0:
            # if changing quantities exist -> children states are returned
            children = get_children(all_valid_states, new_state, all_quantities)
            children = coherent_derivative_proceeding(children, new_state, all_valid_states, changing_quantities)
        else:
            children = get_children(all_valid_states, new_state, [])
        # if transition leads to child with different exogenous derivative -> add child to possible_start_states
        possible_start_states = add_to_possible_start_states(children, all_valid_states, possible_start_states)
        # create final adjacency list based on the obtained children from above (if children not empty only)
        adjacency_list = add_child_to_adjacency_list(state, all_valid_states, children, adjacency_list)
    return adjacency_list


def transform_adjacency_list_to_graph_format(all_valid_states, adjacency_list):
    adjacency_list_string = []
    for adjacency in adjacency_list:
        neighbours = []
        for position in adjacency:
            # last position is start
            if position == len(all_valid_states):
                neighbours.append('Start')
            else:
                neighbours.append(" ".join(quantity_object_to_string(all_valid_states[position].quantities)))
        adjacency_list_string.append(neighbours)

    return adjacency_list_string

# Main function to fill adjacency list for graph
def fill_adjacency_list(all_valid_states):
    global trace_counter1, trace_counter2, trace_counter3
    trace.write("   Given: exogenous variable [inflow] with start derivative: [" + str(trace_input) + "]" + "\n")
    trace.write("   Derive possible starting states based on exogenous derivative" + "\n")
    possible_start_states = get_exogenous_derivative_states(all_valid_states)
    adjacency_list = []
    # edge list stores which state from all the valid states is followed by which other state
    for i in range(len(all_valid_states) + 1):
        adjacency_list.append([i])
    # which states of all_valid states are possible for user_input exogeneous variable of inflow
    # last list entry is list of the index of states that are in possible_states -> all appearing states
    # due to inflow derivative fulfilling
    for possible_state in possible_start_states:
        adjacency_list[-1].append(all_valid_states.index(possible_state))
    trace.write("   Build adjacency list: which originally valid state is a neighbor to which other valid state" + "\n")
    trace.write("   For every possible starting state (based on exogenous derivative), find possible following states"+ "\n")
    trace.write("       Gather instanteous (e.g. (0,+) -> (+,+)) and possibly changing quantities" + "\n")

    for state in possible_start_states:
        # quantities that dont have to change; momentary_quantities have to change (0,+) -> (+,+)
        possibly_changing_quantities, changing_quantities = get_inconstant_quantities(state)

        if len(changing_quantities) != 0 and len(possibly_changing_quantities) != 0 and trace_counter1 == 0:
            qindex = get_index_of_quantity(state, changing_quantities[0])
            qindex2 = get_index_of_quantity(state, possibly_changing_quantities[-1])
            trace_counter1 += 1
            trace.write("       Example: possibly changing quantity: " + str(print_all_states([state])[0][qindex2])+ "\n")
            trace.write("       Example: instanteous changing quantity: " + str(print_all_states([state])[0][qindex])+ "\n")

        # if there are no quantities changing immediately, all possible combinations have to be searched
        if len(changing_quantities) == 0:
            if trace_counter2 == 0:
                trace.write("       No instanteous quantity possible: create a list of every possible combination of changable quantities to explore" + "\n")
                trace.write("       No instanteous quantity possible: apply according transitions to each combination and add original state as no transitions is an option as well" + "\n")
            trace_counter2 += 1
            # all possible change combinations done (eventhough temp results appear that
            # can not happen according to correspondences, but is more generic)
            combinations = get_all_possible_changes(possibly_changing_quantities)
            # change quantities of states according to combinations and save as possibly new_state
            new_states = change_quantities(state, combinations)
            # If no instanteous change then the state itself can be next state too
            new_states.append(state)

        else:
            # if there are momentary_quantities -> change them right away
            if trace_counter3 == 0:
                trace.write("       Instanteous quantity possible: apply all instanteous changes to obtain a new state"+ "\n")
                trace.write("       Quantities are changed (instanteous and all possible combinations) according to derivatives"+ "\n")
                trace.write("   Possible children based on these transitions are added to adjacency_list" + "\n")
                trace.write("All children for all possible start states are created, thus adjacency list is complete" + "\n")
                trace.write("Adjacency list is transformed to graph format by changing entity objects to strings" + "\n")
            trace_counter3 += 1
            # change all changing quantities to end up with one new_state in new_states
            new_states = change_quantities(state, [changing_quantities])
        # get possible children for each new_state -> only add children that fulfill criteria
        adjacency_list = add_children(state, new_states, changing_quantities, all_valid_states, possible_start_states, adjacency_list)
    # turn adjacency list into graph format (strings of states to print for the graph)
    return_list = transform_adjacency_list_to_graph_format(all_valid_states, adjacency_list)

    return return_list

# change input to words for trace file
def trace_user_input(user_input):
    trace_input = "Unaccepted input"
    if user_input == "i":
        trace_input = "increasing"
    elif user_input == "d":
        trace_input = "decreasing"
    elif user_input == "s":
        trace_input = "stable"
    return trace_input

# given the full adjacency_list output the graph in dot language with numbers as node ids
def create_graph(adjacency_list):
    dot = Digraph(comment='state graph bathtub')
    nodes = {}
    # number of nodes as name of node
    id = 0
    for i in range(len(adjacency_list)):
        # no edge if only one or no state involved
        if len(adjacency_list[i]) > 1:
            parent = adjacency_list[i][0]
            if parent not in nodes:
                id += 1
                parent_id = str("State " + str(id))
                nodes[parent] = parent_id
                dot.node(parent_id, parent_id + ' \n '+ parent)
            for j in range(1, len(adjacency_list[i])):
                child = adjacency_list[i][j]
                if child not in nodes:
                    id += 1
                    child_id = str("State " + str(id))
                    nodes[child] = child_id
                    dot.node(child_id, child_id + ' \n ' + child)
                dot.edge(nodes[parent], nodes[child])
    dot.render('stategraph_bath_tub', view = False)


def simulation():
    # create all possibly valid states (all permutations of derivatives and magnitudes
    # for all appearing quantities)
    trace.write("###############################################################" + '\n')
    trace.write("Qualitative Simulation algorithm for possible system behaviour" + '\n')
    trace.write("###############################################################" + '\n')
    trace.write("According to our Entity definition, all possible states are created" + '\n')
    all_valid_states = create_all_valid_states()
    # adjacency list for the state-graph (where are edges and nodes and how are they combined)
    adjacency_list = []
    trace.write("###############################################################" + '\n' + '\n')
    trace.write("Find parent and children nodes for graph by filling an adjacency list (state transitions)" + '\n')
    adjacency_list = fill_adjacency_list(all_valid_states)
    trace.close()
    create_graph(adjacency_list)

# start qualitative_reasoning by asking for input of exogenous derivative (income)
if __name__ == "__main__":
    user_input = input('    Choose the exogenous derivative value for inflow:  [i]=increasing, [s]=stable, [d]=decreasing' + '\n')
    if user_input not in ["i", "s", "d"]:
        print('You entered an input not equal to [i],[s] or [d]')
    print(user_input + ' has been set as derivative value of the exogeneous value inflow. \n The trace of the algorithm is saved in trace.txt file and the \n' \
                            'state-graph is saved in a pdf file named stategraph_bath_tub (Make sure Graphviz is installed!!!).\n')
    trace_input = trace_user_input(user_input)
    global trace
    trace = open('trace.txt', 'w')
    simulation()