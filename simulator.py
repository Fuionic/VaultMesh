import random
import time
from datetime import datetime, timezone

import requests


API_URL = "http://127.0.0.1:8000/api/v1/transactions/"
TOTAL_REQUESTS = 1_000
DUPLICATE_REQUESTS = 50
UNIQUE_REQUESTS = TOTAL_REQUESTS - DUPLICATE_REQUESTS


def make_transactions() -> list[dict]:
    first_id = random.randint(1, 2_147_483_647 - UNIQUE_REQUESTS)
    now = datetime.now(timezone.utc).isoformat()

    return [
        {
            "transaction_id": first_id + index,
            "customer_id": 10_000 + index,
            "amount": round(random.uniform(1, 500), 2),
            "merchant": f"Simulator Merchant {index % 20 + 1}",
            "transaction_time": now,
        }
        for index in range(UNIQUE_REQUESTS)
    ]


def main() -> None:
    unique_transactions = make_transactions()
    transactions = unique_transactions + [
        unique_transactions[index].copy() for index in range(DUPLICATE_REQUESTS)
    ]

    success_count = 0
    duplicate_count = 0
    unexpected = []

    with requests.Session() as client:
        for number, payload in enumerate(transactions, start=1):
            response = client.post(API_URL, json=payload, timeout=10)

            if response.status_code == 201:
                success_count += 1
            elif response.status_code == 409:
                duplicate_count += 1
            elif len(unexpected) < 5:
                unexpected.append(
                    f"Request {number}: HTTP {response.status_code} - {response.text}"
                )

    print(f"Requests sent: {len(transactions)}")
    print(f"Transactions accepted (201): {success_count}")
    print(f"Duplicates detected (409): {duplicate_count}")
    for message in unexpected:
        print(message)

    if success_count != UNIQUE_REQUESTS or duplicate_count != DUPLICATE_REQUESTS:
        raise SystemExit("Unexpected response counts; check the API and database logs.")


if __name__ == "__main__":
    main()