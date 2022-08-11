import json
import csv

def write_csv(csv_file,json_keys,dataset):
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=json_keys)
        writer.writeheader()
        writer.writerows(dataset)


def json_to_csv(json_file, csv_file):
    print("working on "+json_file)
    dataset = []
    json_keys= []

    count = 1
    file_part = 0
    with open(json_file, 'r') as infile:
        for line in infile:
            json_obj = json.loads(line)
            json_keys= list(set(json_keys) | set(json_obj.keys()))
            
            # clean object 
            del json_obj["description"]
            if(json_obj["category"]):
                for i,category in enumerate(json_obj["category"]):
                    if(len(category)>40):
                        json_obj["category"][i]=category[0:40]
            del json_obj["feature"]
            del json_obj["image"]

            dataset.append(json_obj)
            if(count%100==0):
                print(count)
            count += 1
            if(count>500000):
                out_file_path= "{}_part_{}.csv".format(csv_file,file_part)
                write_csv(out_file_path,json_keys,dataset)
                file_part += 1
                del dataset
                dataset = []
                json_keys= []
                count = 0
    out_file_path= "{}_part_{}.csv".format(csv_file,file_part)
    write_csv(out_file_path,json_keys,dataset)
 
    print("items found: {} in {}".format( len(dataset), json_file))
    json_keys.sort()
    print("keys found: ", json_keys)

  