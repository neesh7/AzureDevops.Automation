## How to Find `AUTO_COMPLETE_SETBY`

To retrieve the `AUTO_COMPLETE_SETBY` ID, use the following API request:

https://vssps.dev.azure.com/{ADO_organization}/_apis/identities?searchFilter=General&filterValue={mailID}&api-version=7.1-preview.1

### 📌 Steps:
1. Replace `{ADO_organization}` with your Azure DevOps organization name.
2. Replace `{mailID}` with the email ID of the user.
3. Make a GET request to the above URL.
4. Extract the **ID** from the response JSON.

This ID can then be used for setting auto-completion in Azure DevOps PRs.