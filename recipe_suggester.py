from google import genai 
from google.genai.types import GenerateContentConfig
from pydantic import BaseModel
from pprint import pprint
import os 

class Recipe(BaseModel):
    recipe_name: str 
    ingredients: list[str]
    instructions: list[str]


GOOGLE_API_KEY = os.environ.get('GEMINI_API_KEY')
client = genai.Client(api_key=GOOGLE_API_KEY)

user_prompt = input('Enter your ingredients: ') # example: cheese, brocolai and chicken

response = client.models.generate_content(
    model='gemini-2.5-flash', 
    contents= user_prompt,
    config=GenerateContentConfig(
        system_instruction="""Our users want both metric and US units, with metric units in parentheses after the US units. if the prompt includes non-eddible things explain that the givin ingredeints are not eddible """,
        response_mime_type='application/json',
        response_schema=Recipe,
        )
    )



recipe = response.parsed  # Pydantic Recipe object 
print(f'How to make {recipe.recipe_name}')  # Can use fields to access data 
print('*** You will need these ingredients ***')
for ingredient in recipe.ingredients:
    print(ingredient)
print('*** And here are the instructions ***')
for step in recipe.instructions:
    print(step)

print()

# Or, if you want dictionaries and lists 
recipe_dictionary = response.parsed.model_dump()

pprint(recipe_dictionary)
print('*** You will need these ingredients ***')
print(recipe_dictionary['recipe_name'])
for ingredient in recipe_dictionary['ingredients']:
    print(ingredient)
print('*** And here are the instructions ***')
for step in recipe_dictionary['instructions']:
    print(step)