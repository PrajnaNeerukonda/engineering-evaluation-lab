
def clean_transactions(transactions):
    cleaned = []
    seen_ids = set()

    for transaction in transactions:
        transaction_id = transaction.get("transaction_id")
        amount = transaction.get("amount")

        # Skip records with missing required values.
        if transaction_id is None or amount is None:
            continue

        # Skip transaction IDs we have already processed.
        if transaction_id in seen_ids:
            continue

        seen_ids.add(transaction_id)
        cleaned.append(transaction)

    return cleaned
