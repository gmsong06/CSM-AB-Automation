import argparse
import requests
import os
import json
import math
import matplotlib.pyplot as plt
import numpy as np

def get_mean(folder_path):
    json_dir = os.path.join(folder_path, 'json')

    sum = 0
    count = 0

    for json_file in os.listdir(json_dir):
        with open(os.path.join(json_dir, json_file), 'r') as f:
            data = json.load(f)
            print(data)
            print(os.path.join(json_dir, json_file))
            if data['prediction'] is not None:
                sum += data['prediction']
                count += 1
    
    return (sum/count)

