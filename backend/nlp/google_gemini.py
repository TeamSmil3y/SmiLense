import os
import google.generativeai as genai

os.environ['GOOGLE_API_KEY'] = "API-KEY-REDACTED"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel('gemini-pro')

def generate_content(query):

    response = model.generate_content(query)
    return response.text

if __name__ == '__main__':
    # Example usage:
    planets_fact = generate_content("List 5 planets each with an interesting fact")
    print(planets_fact)

    emojis = generate_content("what are top 5 frequently used emojis?")
    print(emojis)