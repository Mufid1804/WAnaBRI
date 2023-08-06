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

# Parser
class CustArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        if "-S" in message and "-D" in message:
            print("usage: WAnaBRI.py [MODE] -t <target> [OPT] [OTHERS]")
            print(f"{R}[!!]{E} -S and -D cannot be used together. Exiting.")
        else:
            super().error(message)
        sys.exit(1)

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
        except subprocess.CalledProcessError:
            print(f"{tool} is not installed.")
            all_installed = False

    if not all_installed:
        print("One or more required tools are not installed. Exiting.")
        print("Check installation guide at README.md")
        sys.exit(1)

# Function to validate the output file path
def validate_output(args, target):
    log_folder = Path('log')
    log_folder.mkdir(exist_ok=True)  # Create the log folder if it doesn't exist

    if args.output is not None:
        file = log_folder / args.output
        if file.exists():
            print(f"{R}[!!]{E} The output file {args.output} already exists: Using default output file name")
            return log_folder / f"subdomain-enumeration--{target}--{datetime.now().strftime('%Y-%m-%d--%H-%M-%S')}.txt"
        else:
            return file.resolve()
    else:
        return log_folder / f"subdomain-enumeration--{target}--{datetime.now().strftime('%Y-%m-%d--%H-%M-%S')}.txt"

# Function to run SubFinder for subdomain enumeration
def subfinder(target, base_path):

    # Start the SubFinder process
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
    print(f"\n{G}[~]{E} Subdomain enumeration finished: File output saved to {B}{path}{E}")

# Loading animation function
def loading_animation(stop_loading):
    chars = ["  🔍 Searching...  ","  🔎 Searching...  ","  📡 Scanning...  ","  📡 Scanning...  ","🕵️‍♂️ Investigating...","🕵️‍♂️ Investigating..."]
    while not stop_loading.is_set():
        for char in chars:
            sys.stdout.write(f'\r     {char}')
            sys.stdout.flush()
            time.sleep(0.2)

# Main function
if __name__ == "__main__":
    try:
        # Check tools dependency
        check_tools_dependency()

        # Argument parsing
        parser = CustArgumentParser(description="Web Application Firewall (WAF) Analyzer BRI - WAnaBRI",
                                         usage="WAnaBRI.py [MODE] -t <target> [OPT] [OTHERS]",
                                         add_help=False)
        # Target
        target = parser.add_argument_group('Target')
        target.add_argument('-t', '--target', type=str, help='Target domain or path to a .txt file containing domains, e.g., -t bri.co.id or -t domains.txt')

        # Mode
        mode_group = parser.add_argument_group('Mode')
        exclusive_group = mode_group.add_mutually_exclusive_group()
        exclusive_group.add_argument('-S', '--subdomain-enumeration', action='store_true', help='Enumerate subdomains using SubFinder. Accepts only one target domain, e.g., -S bri.co.id')
        exclusive_group.add_argument('-D', '--domain-checker', action='store_true', help='Filter 200 HTTP/HTTPS responses using the domain_checker tool. Accepts only a file, e.g., -D domains.txt')
        
        # Options
        options_group = parser.add_argument_group('Options')
        options_group.add_argument('--no-filter', action='store_false', dest='filter', help='Disable filtering of 200 HTTP/HTTPS responses using the domain_checker tool. Default is True.')
        options_group.add_argument('-o', '--output', type=str, help='Name of the output file, e.g., -o output.txt. If not, default will be used.')
        
        # Others
        others_group = parser.add_argument_group('Others')
        others_group.add_argument('-V', '--version', action='store_true', default=False, help='Print the current version of WAnaBRI and exit.')
        others_group.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit.')

        args = parser.parse_args()

        # Printing ASCII art to terminal
        print(asciiart())

        # Version
        if args.version:
            print(f"{G}[~]{E} The version of WAnaBRI you have is {B}v{__version__}{E}")

        # Handle no Arguments inputed
        if args.target is None:
            print("usage: WAnaBRI.py [MODE] -t <target> [OPT] [OTHERS]")
            print(f"{R}[!!]{E} No test target specified.")
            sys.exit(1)
        

        # Subdomain enumeration process
        if args.subdomain_enumeration and not args.target.endswith('.txt'):
            # Initiating subdomain enumeration
            target = args.target
            path = validate_output(args, target)
            print(f"{G}[*]{E} The target website is {B}{target}{E}")
            print(f"{G}[*]{E} Starting subdomain enumeration for {B}{target}{E} using SubFinder")

            # Run subfinder
            print("")
            subfinder(target, path)
            print("")

            if args.filter:
                print(f"{G}[*]{E} Filtering the subdomains using domain_checker\n")
                path_obj = Path(path)
                output_path = path_obj.parent / f"./{path_obj.stem}-filtered.txt"
                                
                # t0 = time.time()
                # domain_checker(path, output_path)
                # t1 = time.time()
                # print(t1-t0)
                
                # command = f"go run knocknock.go -i {path_obj}"
                # process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                # # Collect the output from the subprocess
                # output = []
                # for line in iter(process.stdout.readline, b''):
                #     output.append(line.decode().strip())

                # # Wait for the process to finish
                # process.wait()
                # # Print the collected output
                # print(f"\r{G}[~]{E} Done! Here's the output:\n")
                # print("\n".join(output))
                # print(f"\n{G}[~]{E} Subdomain enumeration finished: File output saved to {B}{path}{E}")
                
                command = ['go', 'run', 'knocknock.go', '-i', path_obj]
                with subprocess.Popen(command, stdout = subprocess.PIPE) as p:
                    while True:
                        text = p.stdout.read1().decode("utf-8")
                        if not text and p.poll() is not None:
                            break
                        print(text, end='', flush=True)
                
                print(f"\n{G}[~]{E} Subdomain enumeration finished: Filtered output is saved to {B}{output_path}{E}")

                # Print the collected output
                print(f"\r{G}[~]{E} Done! Here's the output:\n")
            
            sys.exit(0)
        
        # Filter the subdomains using domain_checker
        if args.domain_checker and args.target.endswith('.txt'):
            # Initiating domain_checker
            path = args.target
            print(f"{G}[*]{E} The target file is {B}{path}{E}")
            print(f"{G}[*]{E} Filtering the domains using domain_checker\n")
            
            # Run domain_checker
            path_obj = Path(path)
            output_path = path_obj.parent / f"{path_obj.stem}-filtered.txt"
            domain_checker(path, output_path)

            print(f"\n{G}[~]{E} Domain filtering finished: Filtered output is saved to {B}{output_path}{E}")
        
        else:
            print(f"{R}[!!]{E} Invalid arguments: Wrong target format. Exiting.")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print(f"\n{R}[!!]{E} Operation interrupted by user. Exiting.")
        sys.exit(0)

    except Exception as e:
        print(f"\n{R}[!!]{E} An unexpected error occurred: {str(e)}. Exiting.")
        sys.exit(1)