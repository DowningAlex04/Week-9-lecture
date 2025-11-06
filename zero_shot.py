from google import genai
client = genai.Client()

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents="""We are a buisness selling logging and monitoring products 
    What are good products to give away at our booth at PyCon? """
)

print(response.text)