# Import the os package -- idea is to use os module to get api key which we store as env var
import os
# Import the openai package
import openai

# Set openai.api_key to the OPENAI environment variable
openai.api_key = "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"

#### Generate a dataset

# Define the system message
system_msg = 'You are a helpful assistant who understands data science.'

# Define the user message
user_msg = 'Create a small dataset about total sales over the last year. The format of the dataset should be a data frame with 12 rows and 2 columns. The columns should be called "month" and "total_sales_usd". The "month" column should contain the shortened forms of month names from "Jan" to "Dec". The "total_sales_usd" column should contain random numeric values taken from a normal distribution with mean 100000 and standard deviation 5000. Provide Python code to generate the dataset, then provide the output in the format of a markdown table.'
print("Hello")
# Create a dataset using GPT
response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                        messages=[{"role": "system", "content": system_msg},
                                         {"role": "user", "content": user_msg}])


# Check the status of response 
print(response["choices"][0]["finish_reason"])


#print exact api response for your ask 
print(response["choices"][0]["message"]["content"])
