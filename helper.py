import requests

def printMenu():
    options = ["Ticket Type", "Subject", "Date", "Requester", "Assignee", "Ticket Form", "Tag", "Group", "Status"]
    populatedSelections = ["", "", "", "", "", "", "", "", "", ""]
    i = 1
    print("Please select which options you'd like to search with")
    for option in options:
        print(f"{i}  --  {option}")
        i += 1
    
    userSelection = input("For example, to search by creation date, requester, and group, type \"348\"\n")
    while (userSelection.isdigit() == False):
        userSelection = input("Selection invalid, please try again.\n")
    
    if "1" in userSelection:
        ticketType = input("Is the ticket a question (1), incident (2), problem (3), or task (4): ")
        while (not (ticketType.isdigit()) & (len(ticketType) == 1)):
            ticketType = input("Selection invalid, please type 1, 2, 3, or 4.\n")

        if "1" in ticketType:
            tType = "question"
        if "2" in ticketType:
            tType = "incident"
        if "3" in ticketType:
            tType = "problem"
        else:
            tType = "task"
        populatedSelections[0] = tType
    if "2" in userSelection:
        subject = input("Subject: ") + "\""
        populatedSelections[1] = subject
    if "3" in userSelection:
        beforeOrAfter = input("Do you want to get tickets created before (1) or after (2) a certain date? ")
        while (beforeOrAfter.isdigit() == False):
            beforeOrAfter = input("Selection invalid, please type 1 or 2.\n")
        if "1" in beforeOrAfter: 
            creationDate = "<" + input("Type the date using the format yyyy-mm-dd: ")
        else:
            creationDate = ">" + input("Type the date using the format yyyy-mm-dd: ")
        populatedSelections[2] = creationDate
    if "4" in userSelection:
        requester = input("Requester: ")
        populatedSelections[3] = requester
    if "5" in userSelection:
        assignee = input("Assignee: ")
        populatedSelections[4] = assignee
    if "6" in userSelection:
        ticketForm = input("Form name: ") + "\""
        populatedSelections[5] = ticketForm
    if "7" in userSelection:
        tag = input("Tag (only one): ")
        populatedSelections[6] = tag
    if "8" in userSelection:
        group = input("Group name: ") + "\""
        populatedSelections[7] = group
    if "9" in userSelection:
        initStatus = input("Status: ").lower()
        greaterLessEqual = input("Do you want to get tickets that are greater than (1), less than (2), or equal to (3) this status? ")
        
        while (not (greaterLessEqual.isdigit()) & (len(greaterLessEqual) == 1)):
            greaterLessEqual = input("Selection invalid, please type 1, 2, or 3.\n")

        if "1" in greaterLessEqual:
            status = ">" + initStatus
        if "2" in greaterLessEqual:
            status = "<" + initStatus
        else:
            status = ":" + initStatus
        
        populatedSelections[8] = status
        
    return populatedSelections

def searchForUserById(userId, please) :
    try:
        users_url = "https://cotservicedesk.zendesk.com/api/v2/users/" + str(userId) + ".json"
        user = requests.get(users_url, auth = please).json()
        return user["user"]["name"]
    except:
        return "Permanently deleted user"

def searchForCommentsById(ticketId, please):
    comments_url = "https://cotservicedesk.zendesk.com/api/v2/tickets/" + str(ticketId) + "/comments.json"
    comments = requests.get(comments_url, auth = please).json()
    output = ""
    for comment in comments["comments"]:
        output += f"COMMENT:\nAUTHOR: {searchForUserById(comment["author_id"], please)}, CREATED AT: {comment["created_at"]}, PUBLIC: {comment["public"]}\
            \n\n{comment["body"]}\n\n"

    return output

def getAllComments(comments, please):
    # TODO ADD AUTHOR
    output = ""
    for comment in comments:
        output += f"COMMENT:\nAUTHOR: {searchForUserById(comment["author_id"], please)}, CREATED AT: {comment["created_at"]}, PUBLIC: {comment["public"]}\
            \n\n{comment["body"]}\n\n"

    return output

def searchForTicketFormById(formId, please):
    forms_url = "https://cotservicedesk.zendesk.com/api/v2/ticket_forms/" + str(formId) + ".json"
    form = requests.get(forms_url, auth = please).json()
    return form["ticket_form"]["raw_display_name"]

def getGroupById(groupId, please):
    groups_url = "https://cotservicedesk.zendesk.com/api/v2/groups/" + str(groupId) + ".json"
    group = requests.get(groups_url, auth = please).json()
    return group["group"]["name"]