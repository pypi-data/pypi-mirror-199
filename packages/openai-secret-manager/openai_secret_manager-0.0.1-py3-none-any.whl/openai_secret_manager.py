import openai
from openai_secret_manager import get_secret

# Get OpenAI API key
api_key = get_secret("openai")["api_key"]

# Set up OpenAI API client
openai.api_key = api_key

# Make a request to the OpenAI API
response = openai.Completion.create(
    engine="text-davinci-002",
    prompt="Hello, World!",
    max_tokens=5,
)
print(response.choices[0].text.strip())
