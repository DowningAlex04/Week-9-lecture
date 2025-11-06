from google import genai
client = genai.Client()

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents="""We are a buisness selling logging and monitoring products 
    What are good products to give away at our booth at PyCon? 
    Last Year we gave away tote bags and they were popular and met the budget.
    The year before we gave away pens and they were cheap but not popular. 
    the year before we gave away water bottles and they were popular but expensive."""
)

print(response.text)