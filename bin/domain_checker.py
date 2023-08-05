#!/usr/bin/env python3

"""Copyright (c) 2023 Bank Rakyat Indonesia (Persero) Tbk.
For internal purpose use only.
"""

import requests
import sys
from concurrent.futures import ThreadPoolExecutor
from lib.asciiart import Color

# Default Variables
(W,Y,G,R,B,C,E) = Color.unpack()

def check_status_code(url):
	try:
		response = requests.get(url, timeout=10, allow_redirects=True) # Allow redirects
		if response.status_code == 200:
			return True
	except Exception as e:  # Catching general exceptions
		pass
	return False

def process_domain(domain, outfile, progress_bar):
	urls = [f'http://{domain}', f'https://{domain}']
	for url in urls:
		if check_status_code(url):
			print(f"{B}[{Y}{progress_bar}{B}] {G}Success:{E} {url}")
			outfile.write(url + '\n')
		else:
			print(f"{B}[{Y}{progress_bar}{B}] {R}Failed:{E} {url}")

def domain_checker(input_file, output_file):
	try:
		with open(input_file, 'r') as infile:
			domains = [line.strip() for line in infile]
	except FileNotFoundError:
		print(f"Error: The input file {input_file} does not exist.")
		return

	total_domains = len(domains) # Considering both http and https

	try:
		with open(output_file, 'w') as outfile:
			# Using ThreadPoolExecutor to process domains concurrently
			with ThreadPoolExecutor() as executor:
				for i, domain in enumerate(domains):
					percentage = (i+1) / total_domains * 10
					progress_bar = "#" * int(percentage) + " " * (10 - int(percentage))
					process_domain(domain, outfile, progress_bar)

	except PermissionError:
		print(f"Error: Cannot write to the output file {output_file}. Check permissions.")
		sys.exit(1)
	except KeyboardInterrupt:
		print("\nOperation interrupted by user. Exiting.")
		sys.exit(1)
