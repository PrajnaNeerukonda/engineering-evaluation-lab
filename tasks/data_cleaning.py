def clean_transactions(transactions):
    cleaned = []

    for transaction in transactions:
        # BUG: Treats zero as missing.
        if not transaction.get("transaction_id") or not transaction.get("amount"):
            continue

        # BUG: Does not remove duplicate IDs.
        cleaned.append(transaction)

    return cleaned
