import tkinter as tk
from tkinter import messagebox
import openai

# Set up your OpenAI API credentials
openai.api_key = "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"

# # Function to handle user input and generate AI response
# def get_ai_response():
#     user_input = user_input_entry.get()
    
#     # Make a request to the OpenAI API
#     response = openai.Completion.create(
#         engine='davinci',
#         prompt=user_input,
#         max_tokens=50
#     )
    
#     ai_response = response.choices[0].text.strip()
#     messagebox.showinfo("AI Response", ai_response)

# # Create the main window
# window = tk.Tk()
# window.title("AI Assistant")

# # Create and configure the user input entry
# user_input_entry = tk.Entry(window, width=50)
# user_input_entry.pack(pady=10)

# # Create the "Ask" button
# ask_button = tk.Button(window, text="Ask", command=get_ai_response)
# ask_button.pack(pady=5)

# # Run the main window loop
# window.mainloop()

import tkinter as tk
from tkinter import messagebox, Scrollbar, Text
import openai

# Set up your OpenAI API credentials
# openai.api_key = 'YOUR_API_KEY'

# Create the main window
window = tk.Tk()
window.title("Chatbot")
window.geometry("400x500")

# Create and configure the chat display
chat_display = Text(window, width=50, height=20, bg="#F5F5F5", bd=0, font=("Helvetica", 10), padx=10, pady=10)
chat_display.config(state=tk.DISABLED)

scrollbar = Scrollbar(window)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

chat_display.pack(pady=10)
chat_display.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=chat_display.yview)

# Create and configure the user input entry
user_input_entry = tk.Entry(window, width=50, font=("Helvetica", 10), bd=0)
user_input_entry.pack(pady=5)

# Function to handle user input and generate chatbot response
def get_chatbot_response():
    user_input = user_input_entry.get()
    
    # Append user input to the chat display
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, "User: " + user_input + "\n")
    chat_display.config(state=tk.DISABLED)
    
    # Make a request to the OpenAI API
    response = openai.Completion.create(
        engine='davinci',
        prompt=user_input,
        max_tokens=50
    )
    
    chatbot_response = response.choices[0].text.strip()
    
    # Append chatbot response to the chat display
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, "Chatbot: " + chatbot_response + "\n")
    chat_display.config(state=tk.DISABLED)
    chat_display.see(tk.END)  # Scroll to the latest message
    
    # Clear the user input entry
    user_input_entry.delete(0, tk.END)

# Create the "Send" button
send_button = tk.Button(window, text="Send", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", command=get_chatbot_response)
send_button.pack(pady=5)

# Run the main window loop
window.mainloop()
