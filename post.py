import argparse
import requests
import os
import json

URL_single = "https://biosig.lab.uq.edu.au/csm_ab/api/prediction_single"

def process_folder(folder_path):
    json_dir = os.path.join(folder_path, 'json')
    os.makedirs(json_dir, exist_ok=True)

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.pdb'):
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as pdb_file:
                    files = {"pdb_file": pdb_file}
                    try:
                        req = requests.post(URL_single, files=files)
                        req.raise_for_status()  # Raise an HTTPError on bad status
                        response_json = req.json()
                    except requests.exceptions.RequestException as e:
                        print(f"Request failed for {file_path}: {e}")
                        response_json = {"error": str(e)}
                    except json.JSONDecodeError:
                        print(f"Invalid JSON response for {file_path}")
                        response_json = {"error": "Invalid JSON response"}

                # Define the output file name based on the input file name
                output_file = os.path.join(json_dir, f"{os.path.splitext(file)[0]}_response.json")
                with open(output_file, 'w') as f:
                    json.dump(response_json, f, indent=4)

                print(f"Stored response for {file} in {output_file}")

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
