from google import genai
client = genai.Client()

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents="""We are a buisness selling logging and monitoring products 
    What are good products to give away at our booth at PyCon? 
    Last Year we gave away tote bags and they were popular and met the budget."""
)

print(response.text)