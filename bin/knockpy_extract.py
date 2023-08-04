#!/usr/bin/env python3

"""Copyright (c) 2023 Bank Rakyat Indonesia (Persero) Tbk.
For internal purpose use only.
"""

import csv
import argparse


def knockpy_extract(input_file_path, output_file_path):
    # Open the CSV file
    with open(input_file_path, 'r') as file:
        reader = csv.reader(file, delimiter=';')

        # Open the output text file
        with open(output_file_path, 'w') as output_file:
            # Iterate through the rows
            for row in reader:
                # Check if the response code is 200
                if row[1] == '200':
                    # Write the URL to the output file, followed by a newline
                    output_file.write(row[2] + '\n')

    print(f"Extracted URLs have been written to {output_file_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract DNS with response code 200 from a Knockpy_report CSV file.')
    parser.add_argument('input_file_path', type=str, help='Path to the input CSV file.')
    parser.add_argument('output_file_path', type=str, help='Path to the output text file.')

    args = parser.parse_args()

    knockpy_extract(args.input_file_path, args.output_file_path)
    