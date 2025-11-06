from google import genai
from google.genai.types import GenerateContentConfig
import rich
from rich.markdown import Markdown
import sys

client = genai.Client()
chat = client.chats.create(model='gemini-2.5-flash')

try:
    with open('chat_system_instructions.txt','r') as f:
        system_instructions_text=f.read() 
    print(system_instructions_text)
except:
    print('Missing System Instruction, check file path ')
    sys.exit()

while True:
    question = input('>')
    response = chat.send_message(
        question,
        config=GenerateContentConfig(
            system_instruction=system_instructions_text
        )
    )

    rich.print(Markdown(response.text))