from openai import OpenAI
from os import environ
from dotenv import load_dotenv

load_dotenv()


client = OpenAI(
    api_key=environ.get('OPENAI_API_KEY'),
    base_url= environ.get('BASE_URL') 
    )

def get_response(messages):
    system_role = [{'role': 'system', 'content': """You are a chatbot designed to help people.
                                                    please don't mention that you are a LLM."""}]
    response = client.chat.completions.create(
        model=environ.get("LLM_MODEL"),
        messages= system_role+messages,
        temperature=0.1,
        #max_tokens=200,
    )
    if response.choices[0].message.content:
        return response.choices[0].message.content
    else :
        raise Exception("No response from the model")