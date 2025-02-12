import requests, json, base64, sys, csv
import pandas as pd
from io import StringIO
from datetime import datetime
import numpy as np

# PAT Will be supplied through Pipeline Variables 
PAT = sys.argv[1]

organization, project,  = "", ""
RepoID, branchName, path =  "", "", ""



def updated_vars(PAT, organization, project, RepoID, branchname, filepath):
    """This function takes basic details to make an API call to ADO like org, proj, repoid, branchname, filepath. 
        it make api call to ado files api and check for referance csv file and extract data with which it has to return update vars to main function.
    Keyword arguments:
    argument -- organization, project, RepoID, branchname, filepath
    Return: it returns updated_vars which will be used to update our vg
    """
    #Login Details 
    username = ''
    login_info = username + ":" + PAT
    #Base 64 Encoding for Azure Devops Authorization 
    b64 = base64.b64encode(login_info.encode()).decode()

    #To Fetch data from any Topic Branch use this url  
    url = f"https://dev.azure.com/{organization}/{project}/_apis/git/repositories/{RepoID}/items?path={filepath}&versionDescriptor.version={branchName}&api-version=7.1-preview.1"

    #Sending a Requests
    r = requests.get(url =url,headers={"Authorization" : f"Basic {b64}"})
    # print('status code','=',r)

    # Check if the request was successful and print the csv
    if r.status_code == 200:
        # Convert response content to a pandas DataFrame
        csv_data = r.text
        df = pd.read_csv(StringIO(csv_data))
        # Print the DataFrame
        # print(df)

        # Get all csv data
        data_ls = ['Train','CurrentTrainVersion','NextTrainVersion','BiweeklyAutoPromoteTrain','BranchCut']
        csv_data = {}

        # Loop through data_ls and dynamically assign values to dictionary keys
        for i in data_ls:
            csv_data[f'{i}'] = df.iloc[-1][i]

        # Example of how to access the values
        # print(csv_data['NextTrainVersion'])
        # Print the full dictionary with values
        for key, value in csv_data.items():
            print(f"{key}: {value}")
        BranchCut = csv_data['BranchCut']


    today = datetime.today().strftime("%A")  # Returns the full name of the day (e.g., Monday)
    print("\nToday is:", today)

    # Logic behind vg variable updates

    if today == "Wednesday":
        # update wedy-train
        # These are new VG updates we are planning to introduce
        updated_vars = {
        "Wednesday_Train": {"isSecret": False, "value": int(csv_data['NextTrainVersion'])}
        }
        print("\nNew incoming Variable updates\n",updated_vars)
        return updated_vars
        
    elif today == "Thursday" and BranchCut == "YES":
        # update thursday-train and AutoPromoteTrain
        updated_vars = {
        "Thursday_Train": {"isSecret": False, "value": int(csv_data['NextTrainVersion'])},
        "AutoPromoteTrain": {"isSecret": False, "value": float(csv_data['BiweeklyAutoPromoteTrain'])}
        }
        print("\nNew incoming Variable updates\n",updated_vars)
        return updated_vars
    elif  today == "Thursday" and BranchCut == "NO":
        # update thursday-train only
        updated_vars = {
        # "Thursday_Train": {"isSecret": False, "value": int(csv_data['NextTrainVersion'])}
        "Thursday_Train": {"isSecret": False, "value": int(int(csv_data['NextTrainVersion']))}
        }
        print("\nNew incoming Variable updates\n",updated_vars)
        return updated_vars
        
    elif  today == "Friday" and BranchCut == "YES":
        # update train, cca-branch and bwt
        updated_vars = {
        "Train": {"isSecret": False, "value": int(csv_data['NextTrainVersion'])},
        "BiWeekly_Train": {"isSecret": False, "value": float(csv_data['Train'])},
        "CCA_CE_OldWeeklyBranch": {"isSecret": False, "value": f"release/{float(csv_data['BiweeklyAutoPromoteTrain'])}"}
        }
        print("\nNew incoming Variable updates\n",updated_vars)
        return updated_vars
    elif  today == "Friday" and BranchCut == "NO":
        # update train only
        updated_vars = {
        "Train": {"isSecret": False, "value": int(csv_data['NextTrainVersion'])}
        }
        print("\nNew incoming Variable updates\n",updated_vars)
        return updated_vars

# Calling the function
# updated_vars(organization, project, RepoID, branchName, path)

# what this code is doing ?
# we are basically accessing csv file using api which have the logic for the variable updation
# then we are updating our variables based on that csv files
# the the updated_vars will be sent to another driver code which will eventually update vg .