import requests

# Setting stuff up 
with open('credentials.txt', mode='r') as f:
    email = f.readline()
    api_token = f.readline()
search_url = "https://cotservicedesk.zendesk.com/api/v2/search.json"
please = f'{email}/token', api_token

def searchForUserById(userId) :
    try:
        users_url = "https://cotservicedesk.zendesk.com/api/v2/users/" + str(userId) + ".json"
        user = requests.get(users_url, auth = please).json()
        return user["user"]["name"]
    except:
        return "Permanently deleted user"

def searchForCommentsById(ticketId):
    comments_url = "https://cotservicedesk.zendesk.com/api/v2/tickets/" + str(ticketId) + "/comments.json"
    comments = requests.get(comments_url, auth = please).json()
    output = ""
    for comment in comments["comments"]:
        output += f"COMMENT:\nAUTHOR: {searchForUserById(comment["author_id"])}, CREATED AT: {comment["created_at"]}, PUBLIC: {comment["public"]}\
            \n\n{comment["body"]}\n\n"

    return output

def getAllComments(comments):
    # TODO ADD AUTHOR
    output = ""
    for comment in comments:
        output += f"COMMENT:\nAUTHOR: {searchForUserById(comment["author_id"])}, CREATED AT: {comment["created_at"]}, PUBLIC: {comment["public"]}\
            \n\n{comment["body"]}\n\n"

    return output

def searchForTicketFormById(formId):
    forms_url = "https://cotservicedesk.zendesk.com/api/v2/ticket_forms/" + str(formId) + ".json"
    form = requests.get(forms_url, auth = please).json()
    return form["ticket_form"]["raw_display_name"]

def getGroupById(groupId):
    groups_url = "https://cotservicedesk.zendesk.com/api/v2/groups/" + str(groupId) + ".json"
    group = requests.get(groups_url, auth = please).json()
    return group["group"]["name"]

# Setting the query
params = {
    'query': 'type:ticket group:32107987 -status<solved -created>2025-05-01',
    'sort_by': 'created_at',
    'sort_order': 'asc'
}

# Searching
response = requests.get(search_url, params = params, auth = please)

# Writing the data to a text file for storage
#json_string = json.dumps(response.json(), indent=2)
#with open('json.txt', mode='w', encoding='utf-8') as f:
#    f.write(json_string)

data = response.json()

with open('output.txt', mode='w', encoding='utf-8') as f:
    for ticket in data["results"]:
        #if (getGroupById(ticket["group_id"]) == "TS Service Desk"):
        f.write(f"TITLE: {ticket["subject"]}\n\n\nTICKET NUMBER: {ticket["id"]},  CREATED AT: {ticket["created_at"]}, LAST UPDATED: {ticket["updated_at"]}\
                \nREQUESTER: {searchForUserById(ticket["requester_id"])} ASSIGNEE: {searchForUserById(ticket["assignee_id"])}\
                \nTICKET FORM: {searchForTicketFormById(ticket["ticket_form_id"])}\nPRIORITY: {ticket["priority"]}\
                \nSTATUS: {ticket["status"]}\nTAGS: {ticket["tags"]}\nSATISFACTION RATING: {ticket["satisfaction_rating"]}\n\n")
        f.write(searchForCommentsById(ticket["id"]))
        f.write("\n\n\n\n\n--------------------------END TICKET--------------------------\n\n\n\n\n")

# Manually reading all tickets from an export of all tickets
#with open('Reports/export-2025-04-28-1748-1213727-407417159082436f25_3.json', mode='r', encoding='utf-8') as f:
#    data = [json.loads(line) for line in f]

# Manual writing
#with open('output1.txt', mode='w', encoding='utf-8') as f:
#    for i in range(len(data)):
#        if (data[i]["group"]["name"] == "SA Retrieval"):
#            try:
#                f.write(f"TITLE: {data[i]["subject"]}\n\n\nTICKET NUMBER: {data[i]["id"]},  CREATED AT: {data[i]["created_at"]}, LAST UPDATED: {data[i]["updated_at"]}\
#                        \nREQUESTER: {data[i]["requester"]["name"]} ASSIGNEE: {data[i]["assignee"]["name"]}\
#                        \nTICKET FORM: {searchForTicketFormById(data[i]["ticket_form_id"])}\nPRIORITY: {data[i]["priority"]}\
#                        \nSTATUS: {data[i]["status"]}\nTAGS: {data[i]["tags"]}\nSATISFACTION RATING: {data[i]["satisfaction_rating"]}\n\n")
#            except:
#                f.write(f"TITLE: {data[i]["subject"]}\n\n\nTICKET NUMBER: {data[i]["id"]},  CREATED AT: {data[i]["created_at"]}, LAST UPDATED: {data[i]["updated_at"]}\
#                        \nREQUESTER: {data[i]["requester"]["name"]} ASSIGNEE: Permanently deleted user\
#                        \nTICKET FORM: {searchForTicketFormById(data[i]["ticket_form_id"])}\nPRIORITY: {data[i]["priority"]}\
#                        \nSTATUS: {data[i]["status"]}\nTAGS: {data[i]["tags"]}\nSATISFACTION RATING: {data[i]["satisfaction_rating"]}\n\n")
#            f.write(getAllComments(data[i]["comments"]))
#            f.write("\n\n\n\n\n--------------------------END TICKET--------------------------\n\n\n\n\n")
            

       

