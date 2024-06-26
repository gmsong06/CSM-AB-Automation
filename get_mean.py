import argparse
import requests
import os
import json
import math
import matplotlib.pyplot as plt
import numpy as np

def get_mean(folder_path):
    json_dir = os.path.join(folder_path, 'json')

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
    
    return (sum/count), f.name

def graph_mean(data):
    means, names = data
    
    fig, ax = plt.subplots(dpi = 150, figsize = (5,5))

    ax.scatter([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], means)

    ax.set_xticklabels(names,fontsize=12)
    ax.set_ylabel('Age',fontsize=14)
    ax.set_title('Age scatter plot by sex',fontsize=12)
    
    plt.show()
    plt.close()

def main(args):
    best = {}

    for folder in os.listdir(args.pdb_folder):
        folder_path = os.path.join(args.pdb_folder, folder)
        if os.path.isdir(folder_path):
            best[folder] = get_mean(folder_path)

    json_file_path = os.path.join(args.pdb_folder, "subfolder_avgs.json")
    with open(json_file_path, 'w') as json_file:
        json.dump(best, json_file, indent=4)

    print(f"Avg results stored in {json_file_path}")
    graph_mean(get_mean(folder_path))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Job submission for CSM-AB')
    parser.add_argument('pdb_folder', help='PDB folder')
    args = parser.parse_args()

    main(args)