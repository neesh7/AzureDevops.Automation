# Close many workitems based on Query Result 
import os, requests, json, base64, sys
import LoggerFunction as Logger
import CloseAdoWorkitem as wit_close

PAT = "Enter your PAT here"

Credential = Logger.loggerFunc(PAT)
b64 = Logger.getb64(PAT)

organization, project, queryid  = "orgname","Project","1565769c-ft95-407d-2306-17095f4d191b"

closingComment = "Close as these are part of queries "

def getwitdetails(id):
    wit_url = f"https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{id}?api-version=6.0"
    response = requests.get(url =url,headers=Credential).json()
    print(f" {response['fields']['System.Tags']}")
# Fetch 
url = f"https://dev.azure.com/{organization}/{project}/_apis/wit/wiql/{queryid}?api-version=6.0"

# Get request to fetch the list of all associated workitem with the query
response = requests.get(url =url,headers=Credential).json()

work_items = response['workItems']
print(f"Total number of open workitems as per ADO Query is : {len(work_items)}")
# print the work items
for wit in work_items:
    # print(wit)
    # verify tags before closing 
    # getwitdetails(wit['id'])
    # close the workitems 
    wit_close.closeWit(wit['id'],closingComment,b64)
# print(response)