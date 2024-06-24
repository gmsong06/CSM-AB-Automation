import argparse
import requests
import os
import json

URL_single = "https://biosig.lab.uq.edu.au/csm_ab/api/prediction_single"


def main(args):
    no_prediction_count = 0  # Counter for files without 'prediction' key

    for folder in os.listdir(args.pdb_folder):
        folder_path = os.path.join(args.pdb_folder, folder)
        if os.path.isdir(folder_path):
            json_dir = os.path.join(folder_path, 'json')
            if os.path.exists(json_dir) and os.path.isdir(json_dir):
                for json_file in os.listdir(json_dir):
                    if json_file.endswith('.json'):
                        json_file_path = os.path.join(json_dir, json_file)
                        with open(json_file_path, 'r') as f:
                            data = json.load(f)

                            # Skip if 'prediction' key is already present
                            if 'prediction' in data:
                                print(f"Skipping {json_file_path}, 'prediction' key already present.")
                                continue

                            if 'job_id' in data:
                                job_id = data['job_id']
                                print(f"Processing {json_file_path} with job_id: {job_id}")

                                # Make the request using the job_id
                                params = {"job_id": job_id}
                                try:
                                    req = requests.get(URL_single, params=params)
                                    req.raise_for_status()
                                    response_json = req.json()
                                    print(response_json)

                                    # Remove 'status' key from response
                                    if 'status' in response_json:
                                        del response_json['status']

                                    # Update the JSON file with the response
                                    data.update(response_json)
                                    with open(json_file_path, 'w') as fw:
                                        json.dump(data, fw, indent=4)

                                    print(f"Updated {json_file_path} with response.")
                                except requests.exceptions.RequestException as e:
                                    print(f"Request failed for job_id {job_id}: {e}")
                                except json.JSONDecodeError:
                                    print(f"Invalid JSON response for job_id {job_id}")

                            else:
                                no_prediction_count += 1

    print(f"Number of files without a prediction: {no_prediction_count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Job submission for CSM-AB')
    parser.add_argument('pdb_folder', help='PDB folder')
    args = parser.parse_args()

    main(args)
