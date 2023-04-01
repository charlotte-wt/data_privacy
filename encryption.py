import subprocess
import tempfile
import pandas as pd
import base64
import datetime

data_dir = "data"

'''
Encrypt marketing data
'''
def encrypt_marketing_data():
    user_marketing_info = pd.read_csv(f"{data_dir}/UserMarketingInfo2.csv").head()

    # Access policy for User Marketing Info by column
    user_marketing_access_policy = {
        "FullName": "customer_support or (finance and VP) or marketing",
        "NRIC": "customer_support or (finance and VP) or (marketing and VP)",
        "PhoneNumber": "customer_support or (finance and VP) or (marketing and VP) or (marketing and senior)",
        "Email": "customer_support or (finance and VP) or (marketing and VP) or (marketing and senior)",
        "age": "customer_support or (finance and VP) or marketing",
        "job": "customer_support or (finance and VP) or marketing",
        "marital": "customer_support or (finance and VP) or marketing",
        "education": "customer_support or (finance and VP) or marketing"
    }

    # For the attributes, you cannot have special characters, remove - from the user ID
    user_ids = [uid.replace("-", "") for uid in user_marketing_info['InternalUserId']]

    # Define all row-wise policies here
    row_policy = [[f"(customer and {user_id})"] for user_id in user_ids]

    row_identifiers = ['InternalUserId']

    encrypted_user_marketing_info = _encrypt_rows(user_marketing_info, row_policy, user_marketing_access_policy, row_identifiers)

    encrypted_user_marketing_info.to_csv(f"{data_dir}/EncryptedUserMarketingInfo.csv", index=False, encoding='utf-8')

'''
Encrypt transaction data
'''
def encrypt_transactions_data():
    transactions_data_info = pd.read_csv(f"{data_dir}/TransactionsData2.csv").head()

    # Access policy for Transactions Info by column
    transactions_access_policy = {
        "OriginAccNumber": "(customer_support and VP)",
        "Type": "(customer_support and VP)",
        "OriginOldBalance": "(customer_support and VP)",
        "OriginNewBalance": "(customer_support and VP)",
        "DestAccNumber": "(customer_support and VP)",
        "Amount": "(customer_support and VP)",
        "TransactionDate": "(customer_support and VP)",
        "OrigCountry": "(customer_support and VP)"
    }

    # For the attributes, you cannot have special characters, remove - from the user ID
    user_ids = [uid.replace("-", "") for uid in transactions_data_info['OriginInternalUserId']]

    # Define all row-wise policies here
    row_policy = [[
        f"(customer and {user_id})", 
        f"(finance and {country})",
        f"(finance and Intern and {country} and Date > {_convert_datetime(date)})"
        ] for user_id, country, date in 
        zip(user_ids, transactions_data_info['OrigCountry'], transactions_data_info['TransactionDate'])]

    # Define row identifiers
    row_identifiers = ['TransactionId', 'OriginInternalUserId']

    encrypted_transactions_info = _encrypt_rows(transactions_data_info, row_policy, transactions_access_policy, row_identifiers)

    encrypted_transactions_info.to_csv(f"{data_dir}/EncryptedTransactionsInfo.csv", index=False, encoding='utf-8')

'''
Encrypt user balance info
'''
def encrypt_balance_data():
    user_balance_info = pd.read_csv(f"{data_dir}/UserBalanceInfo2.csv").head()

    # Access policy for User Balance Info by column
    user_balance_access_policy = {
        "CurrentBalance": "(customer_support and VP) or (finance and VP) or (marketing and VP)",
        "AverageAnnualBalance": "(customer_support and VP) or (finance and VP) or (marketing and VP)"
    }

    # For the attributes, you cannot have special characters, remove - from the user ID
    user_ids = [uid.replace("-", "") for uid in user_balance_info['InternalUserId']]

    # Define all row-wise policies here
    row_policy = [[f"(customer and {user_id})"] for user_id in user_ids]

    # Define row identifiers
    row_identifiers = ['InternalUserId']

    encrypted_user_balance_info = _encrypt_rows(user_balance_info, row_policy, user_balance_access_policy, row_identifiers)

    encrypted_user_balance_info.to_csv(f"{data_dir}/EncryptedUserBalanceInfo.csv", index=False, encoding='utf-8')

############################################################
def _convert_datetime(date_str: str):
    return int(datetime.datetime.strptime(date_str, "%Y-%m-%d").timestamp())

'''
Internal wrapper function to encrypt all rows of a dataframe
'''
def _encrypt_rows(df: pd.DataFrame, row_policy: list, column_policy: dict, row_identifiers: list):

    encrypted_rows = [_encrypt_row(row, row_policy[idx], column_policy, row_identifiers) for idx, row in df.iterrows()]

    return pd.concat(encrypted_rows, axis=0, ignore_index=True)

'''
Internal function to encrypt individual rows of a dataframe
'''
def _encrypt_row(row: pd.Series, row_policy: list, column_policy: dict, row_identifiers: list):
    # Create temporary directory
    temp_dir = tempfile.TemporaryDirectory()

    # Create a dictionary to store the encrypted results
    encrypted_row = dict()

    # Keep row identifiers as plaintext
    for row_identifier in row_identifiers:
        encrypted_row[row_identifier] = row[row_identifier]

    # For each cell in the row
    for col in row.index:
        if col in row_identifiers:
            continue

        # Join the column policies as the full policy statement 
        full_policy = ' or '.join(row_policy + [column_policy[col]])

        # Create a temporary file to store each cell's plaintext information
        cell_plaintext = tempfile.NamedTemporaryFile(mode = 'w+')
        with open(cell_plaintext.name, 'w') as f:
            f.write(str(row[col]))

        output_filename = f"{temp_dir.name}/{row[row_identifiers[0]]}_{col}.cpabe"

        # Run the encryption command
        p = subprocess.run(["cpabe-enc", "-o", output_filename, "pub_key", cell_plaintext.name, full_policy, "-k"])
        print(p)

        # Read the generated .cpabe files
        with open(output_filename, 'rb') as f:
            encrypted_bytes = f.read()

            # Encode as Base64 bytes, then decode the Base64 bytes to UTF-8
            base64_encoded_data = base64.b64encode(encrypted_bytes)
            base64_message = base64_encoded_data.decode('utf-8')
            encrypted_row[col] = [base64_message]

        # Delete the plaintext file
        cell_plaintext.close()

    # Delete the temporary directory
    temp_dir.cleanup()

    # Return encrypted row
    return pd.DataFrame(encrypted_row)