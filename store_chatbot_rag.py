from google import genai
from google.genai import types
from google.genai.types import GenerateContentConfig
import rich
from rich.markdown import Markdown
import sys
import os
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
import pandas

class GeminiEmbeddingFunction(EmbeddingFunction):
    document_mode = True #true = generating embeddings, False = searching for embeddings in the db

    def __call__(self, input: Documents):
        if self.ducument_mode:
            embedding_task = 'retrieval_document'
        else:
            embedding_task= 'retrieval_query'
        
        response = client.models.embed_content(
            model='models/text-embedding-004',
            contents=input,
            config=types.EmbedContentConfig(
                task_type=embedding_task
            )
        )

        return [e.values for e in response.embeddings] #list comprehension
    
embed_function = GeminiEmbeddingFunction()
embed_function.document_mode=True 

chroma_client = chromadb.PersistentClient()
db = chroma_client.get_or_create_collection(name='zommies_clothes',embedding_function=embed_function)

with open('zommies_products.csv','r') as file:
    clothing_data = pandas.read_csv(file)
    ids = list(clothing_data.style_code)
    documents= list(clothing_data.discription)

db.upsert(
    ids=ids,
    documents=documents
)

embed_function.document_mode=False
#query='What are the best pants for running in winter?'
#result = db.query(query_texts=[query],n_results=5)
#[all_items] = result['documents']
#print(all_items)

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
    prompt_with_rag = input('>')

    # Preform a RAG search to find the most relevant documents (descriptions)
    result = db.query(query_texts=[prompt_with_rag],n_results=5)
    [all_items] = result['documents']
    #print(all_items)
    # Create a prompt which includes those documents. 

    prompt = f"""The user has the following question 
    
    USER_QUESTION: {prompt_with_rag}

    here is the information from the product database that may help answer the users question
    """

    for item in all_items:
        item_one_line = item.replace('\n', ' ') #easier for the llm to diffrentiate between documents. 
        prompt_with_rag += f"PRODUCT: {item_one_line}\n"


    response = chat.send_message(
        prompt_with_rag,
        config=GenerateContentConfig(
            system_instruction=system_instructions_text
        )
    )

    rich.print(Markdown(response.text))