import numpy as np
import os
import json
import argparse


def reject_outliers_iqr(data):
    if not isinstance(data, list):
        raise ValueError("Data should be a list of numbers")

    data = sorted(data)
    data = np.array(data)

    Q1 = np.percentile(data, 25)
    Q3 = np.percentile(data, 75)

    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    non_outliers = data[(data >= lower_bound) & (data <= upper_bound)]

    return non_outliers.tolist()  # Convert back to list for JSON serialization


def process_folder(folder_path):
    json_dir = os.path.join(folder_path, 'json')
    os.makedirs(json_dir, exist_ok=True)

    for json_file in os.listdir(json_dir):
        json_path = os.path.join(json_dir, json_file)
        if json_file.endswith('.json'):
            with open(json_path, 'r') as f:
                data = json.load(f)
                if 'prediction' in data and isinstance(data['prediction'], list):
                    print(f"Processing file: {json_path}")
                    try:
                        cleaned_data = reject_outliers_iqr(data['prediction'])
                        data['prediction'] = cleaned_data

                        # Save the cleaned data back to the JSON file
                        with open(json_path, 'w') as f:
                            json.dump(data, f, indent=4)
                    except ValueError as e:
                        print(f"Skipping file {json_path} due to error: {e}")


def main(args):
    for folder in os.listdir(args.pdb_folder):
        folder_path = os.path.join(args.pdb_folder, folder)
        if os.path.isdir(folder_path):
            process_folder(folder_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Job submission for CSM-AB')
    parser.add_argument('pdb_folder', help='PDB folder')
    args = parser.parse_args()

    main(args)
