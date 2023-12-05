import os, requests, json, base64, sys
import LoggerFunction as Logger

PAT = "Enter your pat here"

b64 = Logger.getb64(PAT)

organization, project, work_item_id  = "orgname/acname","project","2"

# Closing comment for work itmes
comment = 'Closing work item for test 3'


def closeWit(work_item_id,comment,b64):
    url = f"https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{work_item_id}?api-version=6.0"

    # Our Json Body 
    data = [
        {
            "op": "add",
            "path": "/fields/System.State",
            "value": "Closed"
        },
        {
            "op": "add",
            "path": "/fields/System.History",
            "value": comment
        }
        # ,
        # {
        #     "op": "add",
        #     "path": "/fields/System.AssignedTo",
        #     "value": "Avaneesh Kumar"
        # }
    ]

    # Api call for patch request
    response = requests.patch(url, json=data, 
        headers={'Content-Type': 'application/json-patch+json',"Authorization" : f"Basic {b64}"})
    result = response.json()
    # print(result)
    print(f"Work Item with id {result['id']} is {result['fields']['System.State']} which has these tags {result['fields']['System.Tags']} now.")


# closeWit('3',comment, b64)