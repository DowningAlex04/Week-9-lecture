from google import genai
client = genai.Client()

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents="""We run a yoga studio in minneapolis. Most of our clients are students and go home
    for the summer. How can we make up for the missing customers?"""
)

print(response.text)