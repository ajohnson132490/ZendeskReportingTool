# Installation
---
1. Locally clone the repo to your machine
2. Open credentials.txt and update the subdomain, email address, and API key to match your environment
3. Open a command prompt and cd over to that location and set up a virtual environment
    - https://www.geeksforgeeks.org/create-virtual-environment-using-venv-python/
4. Install all requirements with pip install -r requirements.txt
5. Run it with "python main.py" in the command prompt

# Usage
---
Once you have the ZendeskReportingTool up and running, you'll then be able to search with a variety of parameters including ticket type, subject, date, who requested the ticket, who the ticket is assigned to, what form the ticket uses, a ticket tag, what user group the ticket was assigned to, and the current status of that ticket.

After you've put in your search criteria, it'll begin getting all the pages. Due to the limits of the API, each page only contains 100 tickets, and unless you have an upgraded plan, you can only return at most 1000 tickets per API search. Then, once it's written all the tickets, you can find the output in the output.txt file, which will have all the data formatted.

# Customization
---
## Output formatting
If you want to change the way that the output is formatted, you'll need to change the big f.write statement in main.py
```
f.write(f"TITLE: {ticket["subject"]}\n\n\nTICKET NUMBER: {ticket["id"]},  CREATED AT: {ticket["created_at"]}, LAST UPDATED: {ticket["updated_at"]}\
                    \nREQUESTER: {h.searchForUserById(ticket["requester_id"], please)} ASSIGNEE: {h.searchForUserById(ticket["assignee_id"], please)}\
                    \nTICKET FORM: {h.searchForTicketFormById(ticket["ticket_form_id"], please)}\nPRIORITY: {ticket["priority"]}\
                    \nSTATUS: {ticket["status"]}\nTAGS: {ticket["tags"]}\nSATISFACTION RATING: {ticket["satisfaction_rating"]}\n\n")
f.write(h.searchForCommentsById(ticket["id"], please))
f.write("\n\n\n\n\n--------------------------END TICKET--------------------------\n\n\n\n\n")

```
Every ticket will have certain data fields returned based on your environment, which you can write like this.
```
f.write(f"{ticket["data_field"]}")
```
I've found that the easiest way to find the exact names of those data fields is by checking out the JSON output of the search.

## Seeing the JSON
To get that JSON, I've left in a function from developemnt that takes the JSON of last page (final 100 tickets) of the search and outputs it to its own .txt file. To call it you can run the following in main.py:
```
h.outputLastPageToTxt(response)
```
