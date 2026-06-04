import litellm
from models import ProductCategoryResponse

import os
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """
You are a product query classification agent for a chatbot.

When a user sends a message about a product, classify it into ONE of these categories:

- Product        → User is asking about a specific product by name or identity
                   e.g. "Tell me about iPhone 15", "What is Salesforce?"

- Category       → User is asking what type/group a product belongs to
                   e.g. "Is this a SaaS tool?", "What category does Slack fall under?"

- Feature        → User is asking about specific features or capabilities
                   e.g. "Does it have dark mode?", "What features does Notion offer?"

- UseCase        → User is asking how or where to use the product
                   e.g. "Can I use this for project management?", "What can I do with Zapier?"

- ProblemSolved  → User is asking what problem the product solves
                   e.g. "What problem does Grammarly fix?", "Why would I need this?"

- ValueProposition → User is asking about benefits or why to choose the product
                   e.g. "Why should I use this over competitors?", "What makes it worth it?"

- Technology     → User is asking about the tech stack or how it works
                   e.g. "Is it built on AWS?", "Does it use machine learning?"

- Industry       → User is asking which industries or sectors it targets
                   e.g. "Is this for healthcare?", "Which sectors use this product?"

- Integration    → User is asking about compatibility with other tools
                   e.g. "Does it integrate with Slack?", "Can I connect it to Shopify?"

- Pricing        → User is asking about cost, plans, or trials
                   e.g. "How much does it cost?", "Is there a free plan?"

- Limitation     → User is asking about drawbacks, restrictions, or what it can't do
                   e.g. "Does it work offline?", "What are the limitations?"

- Keyword        → User is using vague search terms without clear intent
                   e.g. "CRM tool", "project management software", "AI writing"

- Document       → User is referencing or asking for documentation, guides, or reports
                   e.g. "Show me the API docs", "Do you have a user manual?"

Return ONLY valid JSON (no markdown, no extra text):
{
    "category": "<ONE OF THE CATEGORIES ABOVE>",
    "confidence": <float between 0.0 and 1.0>,
    "reasoning": "<one sentence explaining why>",
    "secondary_category": "<optional second category or null>"
}
"""


def classify_product_query(user_input: str) -> ProductCategoryResponse:
    """
    Classify a user's product-related query into one of 13 predefined categories.

    Args:
        user_input: The user's message/query

    Returns:
        ProductCategoryResponse with category, confidence, reasoning, and optional secondary category
    """
    response = litellm.completion(
        model="azure/gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input},
        ],
        temperature=0,
    )

    content = response["choices"][0]["message"]["content"]

    return ProductCategoryResponse.model_validate_json(content)