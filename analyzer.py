import litellm
from models import MultiDimensionResponse
from dotenv import load_dotenv

load_dotenv()

SYSTEM_PROMPT = """
You are an advanced product query analysis engine.

Given a user message, analyze it across FIVE dimensions and return ONLY valid JSON (no markdown, no extra text):

{
  "user_intent": {
    "label": "<one of: PRODUCT | CATEGORY | FEATURE | USE_CASE | TECHNOLOGY | INDUSTRY | INTEGRATION | PRICING | LIMITATION | KEYWORD | DOCUMENT>",
    "confidence": <0.0-1.0>,
    "description": "<one short sentence>"
  },
  "category": {
    "primary": "<one of: Product | Category | Feature | UseCase | ProblemSolved | ValueProposition | Technology | Industry | Integration | Pricing | Limitation | Keyword | Document>",
    "secondary": "<another category or null>",
    "confidence": <0.0-1.0>
  },
  "feature_knowledge": {
    "topics": ["<topic1>", "<topic2>", "<topic3>"],
    "depth": "<Surface | Intermediate | Deep>",
    "confidence": <0.0-1.0>
  },
  "relationship": {
    "type": "<one of: Direct Query | Comparative | Exploratory | Decision-Making | Troubleshooting | Research>",
    "entities": ["<entity1>", "<entity2>"],
    "connection": "<brief description of how entities relate>"
  },
  "product": {
    "identified": "<product name or null>",
    "domain": "<e.g. CRM | AI | Productivity | DevTools | Marketing | Finance | Healthcare | Other>",
    "confidence": <0.0-1.0>,
    "tags": ["<tag1>", "<tag2>"]
  }
}
"""


def analyze_query(user_input: str) -> MultiDimensionResponse:
    response = litellm.completion(
        model="azure/gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input},
        ],
        temperature=0,
    )

    content = response["choices"][0]["message"]["content"]
    return MultiDimensionResponse.model_validate_json(content)