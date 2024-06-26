import argparse
import requests
import os
import json
import math
import matplotlib.pyplot as plt
import numpy as np

def get_mean(folder_path):
    json_dir = os.path.join(folder_path, 'json')

    means = []
    names = []

    sum = 0.0
    count = 0.0

    for json_file in os.listdir(json_dir):
        with open(os.path.join(json_dir, json_file), 'r') as f:
            data = json.load(f)
            print(data)
            print(os.path.join(json_dir, json_file))
            if data['prediction'] is not None:
                sum += data['prediction']
                count += 1          
    means.append(sum/count)
    names.append(f.name[7])
            
    return means, names

def graph_mean(data):

    keys = []
    for folder in data:
        keys.append(folder)

    fig, ax = plt.subplots(dpi = 150, figsize = (5,5))

    for data_dict in data.values():
        print(data_dict)
        x = data_dict[1][0]
        y = data_dict[0][0]
        print(f"x is{x}")
        print(f"y is {y}")
        ax.scatter(x,y,color='red')


    ax.set_xlabel('Antibody',fontsize=14)
    ax.set_ylabel('Average Delta G',fontsize=14)
    
    plt.show()
    plt.close()

def main(args):
    means = {}

    for folder in os.listdir(args.pdb_folder):
        folder_path = os.path.join(args.pdb_folder, folder)
        print(folder_path)
        if os.path.isdir(folder_path):
            means[folder] = get_mean(folder_path)

    json_file_path = os.path.join(args.pdb_folder, "subfolder_avgs.json")
    with open(json_file_path, 'w') as json_file:
        json.dump(means, json_file, indent=4)

    print(f"Avg results stored in {json_file_path}")
    graph_mean(means)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Job submission for CSM-AB')
    parser.add_argument('pdb_folder', help='PDB folder')
    args = parser.parse_args()

    main(args)