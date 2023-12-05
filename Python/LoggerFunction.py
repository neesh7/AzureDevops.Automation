import base64


# use this while doing get calls

def loggerFunc(PAT):
    #Note: Username can be an empty string and Password will be your PAT
    username = ''
    login_info = username + ":" + PAT
    #Base 64 Encoding for Azure Devops Authorization 
    # b64 = base64.b64encode(login_info.encode()).decode()
    b64 = {"Authorization" : f"Basic {base64.b64encode(login_info.encode()).decode()}"}
    return b64


# use this for patch or post request 

def getb64(PAT):
    #Note: Username can be an empty string and Password will be your PAT
    username = ""
    login_info = username + ":" + PAT
    #Base 64 Encoding for Azure Devops Authorization 
    b64 = base64.b64encode(login_info.encode()).decode()
    return b64
