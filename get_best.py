import argparse
import requests
import os
import json


def get_subfolder_bests(folder_path):
    json_dir = os.path.join(folder_path, 'json')
    os.makedirs(json_dir, exist_ok=True)

    best = 0

    for json_file in os.listdir(json_dir):
        with open(os.path.join(json_dir, json_file), 'r') as f:
            data = json.load(f)
            print(data)
            print(os.path.join(json_dir, json_file))
            if data['prediction'] is not None:
                best = min(best, data['prediction'])

    return best


def get_overall_best(folder_path):
    best = 0
    best_key = 0

    with open(folder_path, 'r') as json_file:
        data = json.load(json_file)

        for key, value in data.items():
            if value < best:
                best = value
                best_key = key

    return best_key, best

def main(args):
    best = {}

    for folder in os.listdir(args.pdb_folder):
        folder_path = os.path.join(args.pdb_folder, folder)
        if os.path.isdir(folder_path):
            best[folder] = get_subfolder_bests(folder_path)

    json_file_path = os.path.join(args.pdb_folder, "subfolder_bests.json")
    with open(json_file_path, 'w') as json_file:
        json.dump(best, json_file, indent=4)

    print(f"Best results stored in {json_file_path}")
    print(f"Best value is {get_overall_best(json_file_path)[1]} from folder {get_overall_best(json_file_path)[0]}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Job submission for CSM-AB')
    parser.add_argument('pdb_folder', help='PDB folder')
    args = parser.parse_args()

    main(args)
