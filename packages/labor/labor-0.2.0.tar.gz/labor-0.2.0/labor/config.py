import json

def write(json_file): 
    with open('config.json', 'w') as file:
        json.dump(json_file, file)

def load():
    with open('config.json', 'r') as file:
        return json.load(file)