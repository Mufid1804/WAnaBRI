#!/usr/bin/env python3

"""Copyright (c) 2023 Bank Rakyat Indonesia (Persero) Tbk.
For internal purpose use only.
"""

import requests
import argparse
from concurrent.futures import ThreadPoolExecutor

# Function to check the HTTP status code of a given domain
def check_status_code(domain):
	try:
		response = requests.get(domain, timeout=10)
		if response.status_code == 200:
			return True
	except Exception as e:  # Catching general exceptions
		pass
	return False

# Function to process a single domain, print the result, and write to the output file if successful
def process_domain(domain, outfile):
	if check_status_code(domain):
		print(f"Success: {domain}")
		outfile.write(domain + '\n')
	else:
		print(f"Failed: {domain}")

# Main function to read domains from the input file and process them using a thread pool
def domain_checker(input_file, output_file):
	try:
		with open(input_file, 'r') as infile:
			domains = [line.strip() for line in infile]
	except FileNotFoundError:
		print(f"Error: The input file {input_file} does not exist.")
		exit(1)

	try:
		with open(output_file, 'w') as outfile:
			# Using ThreadPoolExecutor to process domains concurrently
			with ThreadPoolExecutor() as executor:
				executor.map(lambda domain: process_domain(domain, outfile), domains)
	except PermissionError:
		print(f"Error: Cannot write to the output file {output_file}. Check permissions.")
		exit(1)
	except KeyboardInterrupt:
		print("\nOperation interrupted by user. Exiting.")

	print("Processing complete.")

# Entry point of the script
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Takes a domain names and checks their HTTP response status.')
	parser.add_argument('input_file', type=str, help='Path to the input domain names file.')
	parser.add_argument('output_file', type=str, help='Path to the output domain names file.')

	args = parser.parse_args()

	# Check if the input and output files can be accessed
	try:
		with open(args.input_file, 'r'), open(args.output_file, 'w'):
			pass
	except FileNotFoundError:
		print(f"Error: The input file {args.input_file} does not exist.")
		exit(1)
	except PermissionError:
		print(f"Error: Cannot write to the output file {args.output_file}. Check permissions.")
		exit(1)

	# Call the main function
	domain_checker(args.input_file, args.output_file)
