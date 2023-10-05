#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 14:32:12 2023
"""

import os
import requests
import re
import pandas as pd

# Open GDC manifest file.
mf_name = input('Write manifest file name: ')  # gdc_manifest.2023-09-19.txt
data = pd.read_csv(mf_name, delimiter='\t')

# Directory where the files are saved.
output_directory = "/home/marti/Escriptori/Bioinfo"
os.makedirs(output_directory, exist_ok=True)

count = 0
for _, row in data.iterrows():
    # Loop through the file IDs and download each file.
    file_id = str(row[0])  
    data_endpt = "https://api.gdc.cancer.gov/data/{}".format(file_id)
    response = requests.get(data_endpt, headers={"Content-Type": "application/json"})

    # Check if the request was successful before proceeding.
    if response.status_code == 200:
        # The file name can be found in the header within the Content-Disposition key.
        response_head_cd = response.headers.get("Content-Disposition")
        if response_head_cd:
            file_name = re.findall("filename=(.+)", response_head_cd)[0]

            # Join the directory path with the file name to create the complete file path.
            output_file_path = os.path.join(output_directory, file_name)

            with open(output_file_path, "wb") as output_file:
                output_file.write(response.content)
                count = count + 1
                print(f"Downloaded file nº {count}: {file_name} " )
        else:
            print(f"Failed to get file name for file ID: {file_id}")
    else:
        print(f"Failed to download file ID: {file_id} - Status Code: {response.status_code}")
