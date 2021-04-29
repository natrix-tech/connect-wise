# Connect Wise Scripts

## Introduction
A few scripts were created to automate some things with connect wise

## Usage
1. Create virtual environment
> python3 -m virtualenv env

2. Load virtual environment
> source ./env/Scripts/activate

3. Install dependencies
> pip install -r requirements.txt

4. Specify environment variables
> export publicKey=key
> export privateKey=key
> export company=company

### auto_close_ticket_by_summary.py
This program continously queries Connect Wise for new tickets matching the provided summary and automatically closes them.
> python3 auto_close_ticket_by_summary.py --summary Test --type 421

### all_clients_to_csv.py
This program queries Connect Wise and creates a csv file of all the active companies in a format that the 3CX system can understand.
> python3 all_clients_to_csv.py --output companies.csv