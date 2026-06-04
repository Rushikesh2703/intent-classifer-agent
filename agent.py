import litellm
from models import IntentResponce

import os
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """
You are an intent classification agent.

Classify the user message into ONE of these categories:
PRODUCT
CATEGORY 
FEATURE
USE_CASE 
TECHNOLOGY
INDUSTRY
INTEGRATION
PRICING
LIMITATION 
KEYWORD
DOCUMENT

Return output in JSON format:
{
    "intent": "<CATEGORY>",
    "confidence": <number between 0 and 1>
}
"""


def classify_intent(user_input: str) -> IntentResponce:
    response = litellm.completion(
        model="azure/gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input},
        ],
        temperature=0
    )

    content = response["choices"][0]["message"]["content"]

   
    return IntentResponce.model_validate_json(content)