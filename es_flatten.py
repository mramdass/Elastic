'''
    Munieshwar Ramdass
    2022-04-20

    es_flatten.py

    Usage:
        es_flatten.py <path to JSON>
'''

import sys
import json

def read_json(path):
    with open(path) as reader:
        return json.load(reader)

def write_json(path, data):
    with open(path, 'w') as writer:
        json.dump(data, writer, indent=4)

def flatten(data, mapping={}, key_chain=[]):
    for key in data:
        if isinstance(data[key], dict):
            key_chain.append(key)
            flatten(data[key], mapping, key_chain)
        elif isinstance(data[key], list):
            for count in range(len(data[key])):
                if isinstance(data[key][count], dict) or isinstance(data[key][count], list):
                    flatten(data[key][count], mapping, key_chain + [count])
                else:
                    mapping['.'.join(str(item) for item in key_chain + [key, count])] = data[key][count]
        else:
            mapping['.'.join(str(item) for item in key_chain) + f'.{key}'] = data[key]
    return mapping

if __name__ == '__main__':
    data = read_json(sys.argv[1])
    mapping = flatten(data)
    write_json(f'{sys.argv[1]}_flatten.json', mapping)
    print('fin')
