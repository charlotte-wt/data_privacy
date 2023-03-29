import subprocess
import tempfile
import pandas as pd
import base64

data_dir = "data"
transactions_data_info = pd.read_csv(f"{data_dir}/TransactionsData2.csv")

# Access policy for Transactions Info by column
transactions_access_policy = {
    "OriginInternalUserId": "(customer_support and VP)",
    "OriginAccNumber": "(customer_support and VP)",
    "Type": "(customer_support and VP)",
    "OriginOldBalance": "(customer_support and VP)",
    "OriginNewBalance": "(customer_support and VP)",
    "DestAccNumber": "(customer_support and VP)",
    "Amount": "(customer_support and VP)",
    "TransactionDate": "(customer_support and VP)",
    "OrigCountry": "(customer_support and VP)"
} 


# Dataframe to store encrypted information
encrypted_transactions_data_info = pd.DataFrame(columns = transactions_data_info.columns)

def encrypt_transactions_data(row: pd.Series):
    global encrypted_transactions_data_info

    # For the attributes, you cannot have special characters, remove - from the user ID
    user_id = row['OriginInternalUserId'].replace("-", "")


    # Define all row-wise policies here
    row_policy = [f"(customer and {user_id})", f"(finance and {row['OrigCountry']})"]

    # Create temporary directory
    temp_dir = tempfile.TemporaryDirectory()

    # Create a dictionary to store the encrypted results
    encrypted_row = dict()

    encrypted_row['TransactionId'] = row['TransactionId']

    # For each cell in the row
    for col in row.index:
        if col == 'TransactionId':
            continue

        # Join the column policies as the full policy statement 
        full_policy = ' or '.join(row_policy + [transactions_access_policy[col]])

        # Create a temporary file to store each cell's plaintext information
        cell_plaintext = tempfile.NamedTemporaryFile(mode = 'w+')
        with open(cell_plaintext.name, 'w') as f:
            f.write(str(row[col]))

        output_filename = f"{temp_dir.name}/{row['TransactionId']}_{col}.cpabe"


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
    
    # Append the row to the dataframe
    encrypted_transactions_data_info = pd.concat([encrypted_transactions_data_info, pd.DataFrame(encrypted_row)], axis=0, ignore_index=True)


# Apply it on the first 5 rows of Transactions Info
transactions_data_info.head().apply(encrypt_transactions_data, axis=1)

# Save the file as CSV
encrypted_transactions_data_info.to_csv(f"{data_dir}/EncryptedTransactionsInfo.csv", index=False, encoding='utf-8')