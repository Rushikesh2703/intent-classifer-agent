from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class IntentResponce(BaseModel):
    intent: str = Field(description="Classified intent: SUPPORT | SALES | GREETING | OTHER")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score between 0 and 1")


# ── Product category enum ─────────────────────────────────────────────────────
class ProductCategory(str, Enum):
    PRODUCT = "Product"
    CATEGORY = "Category"
    FEATURE = "Feature"
    USE_CASE = "UseCase"
    PROBLEM_SOLVED = "ProblemSolved"
    VALUE_PROPOSITION = "ValueProposition"
    TECHNOLOGY = "Technology"
    INDUSTRY = "Industry"
    INTEGRATION = "Integration"
    PRICING = "Pricing"
    LIMITATION = "Limitation"
    KEYWORD = "Keyword"
    DOCUMENT = "Document"


# ── Product category response ─────────────────────────────────────────────────
class ProductCategoryResponse(BaseModel):
    category: ProductCategory = Field(description="The classified product query category")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence score between 0 and 1")
    reasoning: Optional[str] = Field(default=None, description="Brief explanation for the classification")
    secondary_category: Optional[ProductCategory] = Field(default=None, description="Second most relevant category if applicable")


# ── NEW: Multi-dimension analysis models ──────────────────────────────────────

class UserIntentResult(BaseModel):
    label: str = Field(description="Intent label")
    confidence: float = Field(ge=0.0, le=1.0)
    description: str = Field(description="One sentence explanation")


class CategoryResult(BaseModel):
    primary: str = Field(description="Primary category")
    secondary: Optional[str] = Field(default=None)
    confidence: float = Field(ge=0.0, le=1.0)


class FeatureKnowledgeResult(BaseModel):
    topics: List[str] = Field(description="Key topics extracted")
    depth: str = Field(description="Surface | Intermediate | Deep")
    confidence: float = Field(ge=0.0, le=1.0)


class RelationshipResult(BaseModel):
    type: str = Field(description="Direct Query | Comparative | Exploratory | Decision-Making | Troubleshooting | Research")
    entities: List[str] = Field(description="Named entities found")
    connection: str = Field(description="How entities relate")


class ProductResult(BaseModel):
    identified: Optional[str] = Field(default=None, description="Product name if found")
    domain: str = Field(description="e.g. CRM | AI | Productivity | DevTools | Marketing | Finance | Other")
    confidence: float = Field(ge=0.0, le=1.0)
    tags: List[str] = Field(description="Relevant tags")


class MultiDimensionResponse(BaseModel):
    user_intent: UserIntentResult
    category: CategoryResult
    feature_knowledge: FeatureKnowledgeResult
    relationship: RelationshipResult
    product: ProductResult