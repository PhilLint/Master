import json
import os

def merge(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a

all_jsons = os.listdir('./Final results')
path = './Final results/'

print(all_jsons)
with open(path +all_jsons[0]) as f:
    dict_1 = json.load(f)
with open(path +all_jsons[1]) as f:
    dict_2 = json.load(f)
with open(path +all_jsons[2]) as f:
    dict_3 = json.load(f)
with open(path +all_jsons[3]) as f:
    dict_4 = json.load(f)
with open(path +all_jsons[4]) as f:
    dict_5 = json.load(f)
with open(path + all_jsons[5]) as f:
    dict_6 = json.load(f)
with open(path +all_jsons[6]) as f:
    dict_7 = json.load(f)
with open(path +all_jsons[7]) as f:
    dict_8 = json.load(f)
with open(path +all_jsons[8]) as f:
    dict_9 = json.load(f)
with open(path +all_jsons[9]) as f:
    dict_10 = json.load(f)
with open(path +all_jsons[10]) as f:
    dict_11 = json.load(f)
with open(path +all_jsons[11]) as f:
    dict_12 = json.load(f)


dict_7767_8652 = merge(dict_1, dict_2)
dict_11532_11945 = merge(dict_3, dict_4)
dict_12666_13565 = merge(dict_5, dict_6)
dict_10000_10630 = merge(dict_7, dict_8)
dict_14466_15365 = merge(dict_9, dict_10)
dict_10632_11520 = merge(dict_11, dict_12)

all_dicts = [dict_11532_11945,dict_12666_13565 , dict_10000_10630, dict_14466_15365, dict_10632_11520]
full_dict = {}

for i in range(len(all_dicts)):
    full_dict = merge(full_dict, all_dicts[i])

with open('full_experiment_results.json', 'w') as f:
    json.dump(full_dict, f)

with open('last_experiment_results.json', 'w') as f:
    json.dump(dict_7767_8652, f)




