'''
    Munieshwar Ramdass
    2022-04-18

    es_mapping.py

    Creates Elasticsearch mappings from JSON files.
    Note that mapping can only be applied to an index once.
    It is best to "update" a mapping by creating a new index.

    Usage:
        python es_mapping.py <path to JSON file>
'''

import sys
import json

import ipaddress


# Notes
# 2022-04-19: https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html
# 'flattened' can be used as a nested JSON catch-all


# Detect data type

def map_type(value):

    if isinstance(value, list): return 'object'
    if isinstance(value, bytes): return 'binary'
    if isinstance(value, bool): return 'boolean'
    if isinstance(value, int): return 'long'
    if isinstance(value, float): return 'double'

    try:
        var = ipaddress.ip_address(value)
        return 'ip'
    except: pass
    
    try:
        var = ipaddress.ip_network(value)
        return 'ip_range'
    except: pass
    
    if value == None:
        print('Found a null value. It is best not to use this mapping.')
    
    # Date and time fields have not been implemented yet.

    return 'text'



# Get data JSON and write mapping JSON

def read_json(path):
    with open(path) as reader:
        return json.load(reader)

def write_json(path, data):
    with open(path, 'w') as writer:
        json.dump(data, writer, indent=4)

def traverse_dict(data, mapping={'properties': {}}):
    for key in data:
        if isinstance(data[key], dict):
            mapping['properties'][key] = {'properties': {}}
            traverse_dict(data[key], mapping['properties'][key])
        else:
            mapping['properties'][key] = {'type': map_type(data[key])}
    return mapping

if __name__ == '__main__':
    data = read_json(sys.argv[1])
    mapping = traverse_dict(data)
    write_json(f'es_mapping_{sys.argv[1]}', mapping)
    print('fin')
