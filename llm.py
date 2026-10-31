# A hosted app wont have local AZURE CLI login - so configure Azure credentials
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

ENDPOINT = os.getenv("AZURE_AI_ENDPOINT")
DEPLOYMENT_NAME = os.getenv("AZURE_AI_DEPLOYMENT")
API_KEY = os.getenv("AZURE_AI_API_KEY")

if not ENDPOINT or not DEPLOYMENT_NAME or not API_KEY:
    raise ValueError("Azure configuration missing. Check environment variables.")

client = OpenAI(
    base_url=ENDPOINT,
    api_key=API_KEY
)

def ask_llm(system_prompt: str, user_prompt: str) -> str:
    response = client.responses.create(
        model=DEPLOYMENT_NAME,
        instructions=system_prompt,
        input=user_prompt,
        max_output_tokens=600
    )
    return response.output_text



# THIS IS FOR LOCAL AZURE CLI LOGIN 
# import os
# from dotenv import load_dotenv
# from openai import OpenAI
# from azure.identity import (
#     DefaultAzureCredential,
#     get_bearer_token_provider
# )

# load_dotenv()

# ENDPOINT = os.getenv("AZURE_AI_ENDPOINT")
# DEPLOYMENT_NAME = os.getenv("AZURE_AI_DEPLOYMENT")

# if not ENDPOINT or not DEPLOYMENT_NAME:
#     raise ValueError("Azure endpoint or deployment name missing in .env")

# credential = DefaultAzureCredential()

# token_provider = get_bearer_token_provider(
#     credential,
#     "https://ai.azure.com/.default"
# )

# client = OpenAI(
#     base_url=ENDPOINT,
#     api_key=token_provider
# )


# def ask_llm(system_prompt: str, user_prompt: str) -> str:
#     response = client.responses.create(
#         model=DEPLOYMENT_NAME,
#         instructions=system_prompt,
#         input=user_prompt,
#         max_output_tokens=600
#     )

#     return response.output_text



