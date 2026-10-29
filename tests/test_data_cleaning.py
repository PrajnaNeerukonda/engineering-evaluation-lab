
from tasks.data_cleaning import clean_transactions


def test_removes_duplicate_transactions():
    transactions = [
        {"transaction_id": 1, "amount": 100},
        {"transaction_id": 1, "amount": 100},
    ]

    result = clean_transactions(transactions)

    assert result == [
        {"transaction_id": 1, "amount": 100}
    ]


def test_keeps_zero_amount():
    transactions = [
        {"transaction_id": 2, "amount": 0}
    ]

    result = clean_transactions(transactions)

    assert result == [
        {"transaction_id": 2, "amount": 0}
    ]


def test_removes_missing_values():
    transactions = [
        {"transaction_id": None, "amount": 100},
        {"transaction_id": 3, "amount": None},
        {"transaction_id": 4, "amount": 200},
    ]

    result = clean_transactions(transactions)

    assert result == [
        {"transaction_id": 4, "amount": 200}
    ]


def test_keeps_first_duplicate():
    transactions = [
        {"transaction_id": 5, "amount": 100},
        {"transaction_id": 5, "amount": 250},
    ]

    result = clean_transactions(transactions)

    assert result == [
        {"transaction_id": 5, "amount": 100}
    ]


def test_handles_empty_input():
    assert clean_transactions([]) == []
