from model.transactionmodel import TransactionDB

def to_text(transaction: TransactionDB) -> str:
    return (
        f"Transaction {transaction.transaction_id} "
        f"was made by customer {transaction.customer_id} "
        f"for an amount of {transaction.amount} at {transaction.merchant} "
        f"on {transaction.transaction_time.isoformat()}."
    )