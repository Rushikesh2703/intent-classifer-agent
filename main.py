from classifier import classify_product_query
from models import ProductCategoryResponse


def format_response(query: str, result: ProductCategoryResponse) -> str:
    """Format the classification result for display."""
    lines = [
        f"\n{'─' * 50}",
        f"  Query     : {query}",
        f"  Category  : {result.category.value}",
        f"  Confidence: {result.confidence:.0%}",
    ]
    if result.reasoning:
        lines.append(f"  Reasoning : {result.reasoning}")
    if result.secondary_category:
        lines.append(f"  Also Could: {result.secondary_category.value}")
    lines.append(f"{'─' * 50}\n")
    return "\n".join(lines)


def run_chatbot():
    """Interactive chatbot loop for product query classification."""
    print("\n🤖 Product Query Classifier")
    print("=" * 50)
    print("Ask anything about a product and I'll classify your query.")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit", "q"}:
            print("Goodbye!")
            break

        try:
            result = classify_product_query(user_input)
            print(format_response(user_input, result))
        except Exception as e:  
            print(f"\n⚠️  Error classifying query: {e}\n")


def run_batch(queries: list[str]) -> list[dict]:
    """
    Classify a batch of queries.

    Args:
        queries: List of user query strings

    Returns:
        List of dicts with query + classification result
    """
    results = []
    for query in queries:
        try:
            result = classify_product_query(query)
            results.append({
                "query": query,
                "category": result.category.value,
                "confidence": result.confidence,
                "reasoning": result.reasoning,
                "secondary_category": result.secondary_category.value if result.secondary_category else None,
            })
            print(format_response(query, result))
        except Exception as e:
            results.append({"query": query, "error": str(e)})
    return results


if __name__ == "__main__":
    run_chatbot()
