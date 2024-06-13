import pandas as pd
import os, json
import numpy as np

def read_json_files_from_directory(directory):
    data = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as f:
                record = json.load(f)
                data.append(record)
    return data

def create_dataframe(data):
    rows = []
    for record in data:
        id = record['id']
        op = record['op']
        ts = record['ts']
        if op == 'c':
            data_fields = record.get('data', {})
        elif op == 'u':
            data_fields = record.get('set', {})
        else:
            data_fields = {}

        row = {
            'id': id,
            'op': op,
            'ts': pd.to_datetime(ts, unit='ms')
        }
        row.update(data_fields)

        rows.append(row)

    df = pd.DataFrame(rows)
    return df

accounts_data = read_json_files_from_directory(os.path.join(os.path.dirname(__file__), 'data/accounts'))
cards_data = read_json_files_from_directory(os.path.join(os.path.dirname(__file__),  'data/cards'))
savings_accounts_data = read_json_files_from_directory(os.path.join(os.path.dirname(__file__),  'data/savings_accounts'))

accounts_df = create_dataframe(accounts_data)
cards_df = create_dataframe(cards_data)
savings_accounts_df = create_dataframe(savings_accounts_data)
accounts_df.replace({'': '-', np.nan: '-'}, inplace=True)
cards_df.replace({'': '-', np.nan: '-'}, inplace=True)
savings_accounts_df.replace({'': '-', np.nan: '-'}, inplace=True)
accounts_df.sort_values(by='ts')
cards_df.sort_values(by='ts')
savings_accounts_df.sort_values(by='ts')

"""TASK 1"""

print("Accounts Data:")
print(accounts_df[['id', 'account_id', 'name', 'address', 'phone_number', 'email', 'card_id', 'savings_account_id']])

print("\nCards Data:")
print(cards_df[['id', 'card_id', 'card_number', 'credit_used', 'monthly_limit', 'status']])

print("\nSavings Accounts Data:")
print(savings_accounts_df[['id', 'savings_account_id', 'balance', 'interest_rate_percent', 'status']])

"""TASK 2"""

joined_df = pd.merge(accounts_df, cards_df, left_on='card_id', right_on='card_id', how='left')
joined_df2 = pd.merge(joined_df, savings_accounts_df, left_on='savings_account_id', right_on='savings_account_id', how='left')
joined_df2.replace({'': '-', np.nan: '-'}, inplace=True)
joined_df2.drop_duplicates(subset=['id', 'account_id', 'name', 'address', 'phone_number', 'email', 'card_id', 'savings_account_id', 'credit_used', 'card_number', 'monthly_limit', 'balance'], keep='first', inplace=True)
joined_df2.sort_values(by='ts')

print("Joined Table:")
print(joined_df2)

"""TASK 3"""

transactions = joined_df2[
    (joined_df2['balance'].notnull()) | (joined_df2['credit_used'].notnull())
]
transactions = transactions.sort_values(by='ts')
num_transactions = len(transactions)
print("\nNumber of Transactions:", num_transactions)

if num_transactions > 0:
    print("\nDetails of Transactions:")
    for idx, transaction in transactions.iterrows():
        transaction_type = []
        if not pd.isnull(transaction['balance']):
            transaction_type.append(f"Balance changed to {transaction['balance']}")
        if not pd.isnull(transaction['credit_used']):
            transaction_type.append(f"Credit used changed to {transaction['credit_used']}")
        transaction_details = ", ".join(transaction_type)
        print(f"Transaction ID: {transaction['id']}, Timestamp: {transaction['ts']}, Details: {transaction_details}")