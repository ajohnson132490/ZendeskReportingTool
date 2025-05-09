import json
import math
import os
import requests
import time
from tqdm import tqdm
import helper as h

## --Getting authorization-- ##
with open('credentials.txt', mode='r') as f:
    subdomain = f.readline().strip()
    email = f.readline()
    api_token = f.readline()
search_url = f"https://{subdomain}.zendesk.com/api/v2/search.json"
please = f'{email}/token', api_token

## --Cleaning up previous output-- ##
if os.path.exists("output.txt"):
    os.remove("output.txt")
if os.path.exists("json.txt"):
    os.remove("json.txt")

## --Setting the query-- ##
options = h.printMenu()
optionsDict = {0 : "ticket_type:", 1 : "subject:\"", 2 : "created", 3 : "requester:", 4 : "assignee:",
               5 : "form:\"", 6 : "tags:", 7 : "group:\"", 8 : "status"}
query = 'type:ticket '
pos = 0
for option in options:
    if option != '':
        query += optionsDict[pos] + option + " " 
    pos += 1

params = {
    'query': query,
    'sort_by': 'created_at',
    'sort_order': 'asc'
}

## --Searching-- ##
tickets = []
try:
    # Getting the first page of data
    response = requests.get(search_url, params = params, auth = please)
    if response.status_code == 429:
        print("Rate limit reached. Waiting to retry...")
        time.sleep(response.headers['retry-after'])
        response = requests.get(search_url, params = params, auth = please)
    data = response.json()
    with tqdm(range(0,100), total=math.ceil(data["count"]/100), ncols = 100, desc="Loading Pages") as progress_bar:
        tickets += data["results"]
        progress_bar.update(1)

        # Getting additional pages of data
        while (data["next_page"] != None):
            response = requests.get(data["next_page"], params = params, auth = please)
            if response.status_code == 429:
                print("Rate limit reached. Waiting to retry...")
                time.sleep(response.headers['retry-after'])
                response = requests.get(search_url, params = params, auth = please)
            data = response.json()
            tickets += data["results"]
            progress_bar.update(1)
except:
    print(data["description"])

print(f"{len(tickets)} tickets found.")

## --Uncomment this line to see raw JSON-- ##
#h.outputLastPageToTxt(response)

## --Formatting and writing all data to the output file-- ##
with open('output.txt', mode='w', encoding='utf-8') as f:
    with tqdm(range(0,100), total=len(tickets), ncols = 100, desc="Writing Tickets") as progress_bar:
        for ticket in tickets:
            f.write(f"TITLE: {ticket["subject"]}\n\n\nTICKET NUMBER: {ticket["id"]},  CREATED AT: {ticket["created_at"]}, LAST UPDATED: {ticket["updated_at"]}\
                    \nREQUESTER: {h.searchForUserById(ticket["requester_id"], please)} ASSIGNEE: {h.searchForUserById(ticket["assignee_id"], please)}\
                    \nTICKET FORM: {h.searchForTicketFormById(ticket["ticket_form_id"], please)}\nPRIORITY: {ticket["priority"]}\
                    \nSTATUS: {ticket["status"]}\nTAGS: {ticket["tags"]}\nSATISFACTION RATING: {ticket["satisfaction_rating"]}\n\n")
            f.write(h.searchForCommentsById(ticket["id"], please))
            f.write("\n\n\n\n\n--------------------------END TICKET--------------------------\n\n\n\n\n")
            progress_bar.update(1)

## --Uncomment to manually search for all tickets in a group using a file-- ##
#h.manuallySearchTickets(FILENAME, GROUP, please)
            
print ("Output complete!")