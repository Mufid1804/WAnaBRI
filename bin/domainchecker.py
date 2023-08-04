import requests


# Function to check the status code of a given domain
def check_status_code(domain):
    try:
        response = requests.get(domain, timeout=10)
        # Return True if the status code is 200
        if response.status_code == 200:
            return True
    except requests.RequestException as e:
        pass
    return False


# Function to process domains from an input file and write successful ones to an output file
def process_domain(input_file, output_file):
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                domain = line.strip()
                if check_status_code(domain):
                    print(f"Success: {domain}")
                    outfile.write(domain + '\n')
                else:
                    print(f"Failed: {domain}")
    except FileNotFoundError as e:
        # Handle the case where the input file is not found
        print(f"File not found: {str(e)}")
        exit(0)
    except KeyboardInterrupt:
        # Handle Ctrl+C interruption
        print("\nOperation interrupted by user. Exiting...")
        exit(0)
    except Exception as e:
        # Handle other unexpected errors
        print(f"An unexpected error occurred: {str(e)}")
        exit(0)


# Main function to run the domain checker
def domainchecker(input_file, output_file):
    # Main process to check domains
    process_domain(input_file, output_file)
    print("Processing complete.\n")
    print(f"The results have been saved to: {output_file}\n")
                