import openai

# Set up your OpenAI API credentials
openai.api_key = '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'

promptdata=input("Ask me anything: \n")

# Make a request to the OpenAI API
response = openai.Completion.create(
#   engine='davinci',
  engine='gpt-3.5-turbo-0301',
  prompt=promptdata,
  max_tokens=100
)

# Print the generated text
print(response)
# print(response.choices[0].text.strip())
