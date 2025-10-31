from google import genai
from google.genai import types
from google.genai.types import GenerateContentConfig
from pydantic import BaseModel

client = genai.Client() 

class Produce(BaseModel):
    name: str
    color: str
    Fruit_or_veg: str #"Fruit" or "Vegetable"
with open('Image_Understanding/vegetables2.jpg', 'rb') as f:
    image_bytes = f.read()

response = client.models.generate_content(
    model = 'gemini-2.5-flash',
    contents=[
        types.Part.from_bytes(data=image_bytes, mime_type ='image/jpeg'),
        'What is this picture of?'
    ],
    config=GenerateContentConfig(
        system_instruction= """Identify as many produce items as possible. use 'Fruit' for fruit and 'Vegateble' for vegatebles.""",
        response_mime_type='application/json',
        response_schema=list[Produce]
    )
)

print(response.parsed)

for produce_item in response.parsed:
    print(produce_item.name)