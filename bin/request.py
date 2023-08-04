#!bin/python3

import requests
import sys


# Check domain response
def check_status_code(domain):
    try:
        response = requests.get(domain, timeout=10)
        if response.status_code == 200:
            return True
    except requests.RequestException:
        pass
    return False


# Process domain and input into file
def process_domain(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            domain = line.strip()
            if check_status_code(domain):
                print(f"Success: {domain}")
                outfile.write(domain + '\n')
            else:
                print(f"Failed: {domain}")        


# Main request function
def main():
    # Check if arguments are correct
    if len(sys.argv) != 3:
        print("Invalid arguments!")
        print("Usage: python request.py <input_file> <output_file>")
        sys.exit(1)
    
    # Get input and output file
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Main process
    process_domain(input_file, output_file)
    print("Processing complete.")


if __name__ == "__main__":
    main()
