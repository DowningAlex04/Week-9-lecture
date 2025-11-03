from google import genai
import rich 
from rich.markdown import Markdown

client = genai.Client()
chat = client.chats.create(model='gemini-2.5-flash')

while True:
    prompt=input('Enter your message: ')
    response = chat.send_message(prompt+'Answer in a short sentance.')
    rich.print(Markdown(response.text))
    #print(response.usage_metadata.total_token_count)