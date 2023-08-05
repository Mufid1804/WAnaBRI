#!/usr/bin/env python3

""" Copyright (c) 2023 Bank Rakyat Indonesia (Persero) Tbk.
For internal purpose use only
"""

import argparse
import sys
import subprocess
import time
import threading
from pathlib import Path
from datetime import datetime
from bin.domain_checker import domain_checker
from lib.asciiart import Color, asciiart
from version import __version__

# Default Variables
(W,Y,G,R,B,C,E) = Color.unpack()

# Tools dependency check
def check_tools_dependency():
    tools = {
        'go': 'go version',
        'subfinder': 'subfinder -version',
        'httprobe': 'httprobe -h'
    }

    all_installed = True

    for tool, command in tools.items():
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, check=True)
            print(f"{tool} is installed.")
        except subprocess.CalledProcessError:
            print(f"{tool} is not installed.")
            all_installed = False

    if not all_installed:
        print("One or more required tools are not installed. Exiting.")
        print("Checnk installation guide at README.md")
        sys.exit(1)

# Function to validate the output file path
def validate_output(args):
    log_folder = Path('log')
    log_folder.mkdir(exist_ok=True)  # Create the log folder if it doesn't exist

    if args.output is not None:
        file = log_folder / args.output
        if file.exists():
            print(f"{R}[!!]{E} The output file {args.output} already exists: Using default output file name")
            return log_folder / f"subdomain-enumeration--{datetime.now().strftime('%Y-%m-%d--%H-%M-%S')}.txt"
        else:
            return file.resolve()
    else:
        return log_folder / f"subdomain-enumeration--{datetime.now().strftime('%Y-%m-%d--%H-%M-%S')}.txt"

# Function to run SubFinder for subdomain enumeration
def subfinder(target, path):
    stop_loading = threading.Event()
    command = f"subfinder -d {target} -o {path} -silent"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # Start the loading animation in a separate thread
    loading_thread = threading.Thread(target=loading_animation, args=(stop_loading,))
    loading_thread.daemon = True
    loading_thread.start()

    # Collect the output from the subprocess
    output = []
    for line in iter(process.stdout.readline, b''):
        output.append(line.decode().strip())

    # Wait for the process to finish
    process.wait()

    # Stop the loading animation
    stop_loading.set()
    loading_thread.join(timeout=1)

    # Print the collected output
    print(f"\r{G}[~]{E} Done! Here's the output:\n")
    print("\n".join(output))
    print(f"\n{G}[~]{E} File output saved to {B}{path}{E}")

# Function to run httprobe for probing
def run_httprobe(input_file, output_file):
    stop_loading = threading.Event()
    # Start the loading animation in a separate thread
    loading_thread = threading.Thread(target=loading_animation, args=(stop_loading,))
    loading_thread.daemon = True
    loading_thread.start()

    command = f"cat {input_file} | httprobe > {output_file}"
    subprocess.run(command, shell=True)

    # Stop the loading animation
    stop_loading.set()
    loading_thread.join(timeout=1)

# Loading animation function
def loading_animation(stop_loading):
    chars = ["  🔍 Searching...  ","  🔎 Searching...  ","  📡 Scanning...  ","  📡 Scanning...  ","🕵️‍♂️ Investigating...","🕵️‍♂️ Investigating..."]
    while not stop_loading.is_set():
        for char in chars:
            sys.stdout.write(f'\r     {char}')
            sys.stdout.flush()
            time.sleep(0.2)

# Function to prompt the user to continue
def continue_prompt():
    while True:
        choice = input(f"{G}[+]{E} Do you want to continue? (Y/n): ")
        if choice in ('', 'Y', 'y'):
            print(f"{G}[~]{E} You chose 'yes'. Continuing...")
            break
        elif choice in ('N', 'n'):
            print(f"{G}[~]{E} You chose 'no'. Exiting...")
            sys.exit(1)
        else:
            print(f"{R}[!!]{E} Invalid choice. Please enter 'Y' or 'n', or press Enter for the default option.")

# Function to parse the target
def parse_target(args):
    if args.target.endswith('.txt'):
        with open(args.target, 'r') as file:
            return [line.strip() for line in file.readlines()]
    else:
        return [args.target]

# Main function
if __name__ == "__main__":
    # Check tools dependency
    check_tools_dependency()

    # Argument parsing
    parser = argparse.ArgumentParser(description="Web Application Firewall (WAF) Analyser BRI - WAnaBRI")
    parser.add_argument('-S', '--subdomain-enumeration', action='store_true', help='Enumerate subdomains using SubFinder')
    parser.add_argument('-t', '--target', type=str, help='Target domain or path to a .txt file containing domains ex: -t bri.co.id or -t domains.txt')
    parser.add_argument('-o', '--output', type=str, help='Name of the output file ex -o output.txt')
    parser.add_argument('-V', '--version', action='store_true', default=False, help='Print out the current version of WAnaBRI and exit.')
    parser.add_argument('--no-colors', dest='colors', action='store_false', default=True, help='Disable ANSI colors in output.')

    args = parser.parse_args()

    # Printing ASCII art to terminal
    if not args.colors or 'win' in sys.platform:
        Color.disable()

    print(asciiart())

    # Version
    if args.version:
        print(f"{G}[~]{E} The version of WAnaBRI you have is {B}v{__version__}{E}")

    # Handle no Arguments inputed
    if args.target is None:
        parser.error(f"{R}No test target specified.{E}")

    targets = parse_target(args)
    path = validate_output(args)

    # Subdomain enumeration process
    if args.subdomain_enumeration:
        for target in targets:
            print(f"{G}[*]{E} The target website is {B}{target}{E}")
            print(f"{G}[*]{E} Starting subdomain enumeration for {B}{target}{E} using SubFinder")
            print("")
            subfinder(target, path)
            print("")
            print(f"{G}[*]{E} The next step is to check the domains using domain_checker")
            continue_prompt()
            path_obj = Path(path)
            output_path = path_obj.parent / f"{path_obj.stem}-probe.txt"
            print("")
            print(f"{G}[*]{E} Starting probe using httprobe\n")
            run_httprobe(path, output_path)
            print(f"\r{G}[~]{E} Probing finished. The output is saved to {B}{output_path}{E}")
            print("")
            print(f"{G}[*]{E} Domain checking started\n")
            path_obj = Path(path)
            output_path = path_obj.parent / f"{path_obj.stem}-checked.txt"
            domain_checker(path, output_path)
            print(f"\n{G}[~]{E} Domain checking finished. The output is saved to {B}{output_path}{E}")

    else:
        print(f"{args.target}")
