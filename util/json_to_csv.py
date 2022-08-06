import json
import csv

def json_to_csv(json_file, csv_file):
    print("working on "+json_file)
    dataset = []
    json_keys= []

    with open(json_file, 'r') as infile:
        for line in infile:
            json_obj = json.loads(line)
            json_keys= list(set(json_keys) | set(json_obj.keys()))
            dataset.append(json_obj)
 
    print("items found: {} in {}".format( len(dataset), json_file))
    json_keys.sort()
    print("keys found: ", json_keys)

    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=json_keys)
        writer.writeheader()
        writer.writerows(dataset)
