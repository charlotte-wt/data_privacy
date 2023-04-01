import subprocess
import pandas as pd
import os
import datetime
import time
from encryption import encrypt_marketing_data, encrypt_transactions_data, encrypt_balance_data

data_dir = "data"
user_attributes_df = pd.read_csv(f"{data_dir}/InternalUserInfo3.csv")

# Where to store the private keys
private_key_directory = "private-keys"

'''
Function to do complete setup
'''
def complete_setup():
    # Generate master key and public key
    start_master_key = time.time()
    p = subprocess.run(["cpabe-setup"])
    print("Master key and public key generated: ", time.time() - start_master_key)

    # Generate private keys for everyone
    start_priv_key = time.time()
    user_attributes_df.apply(generate_private_keys, axis=1)
    print("Private keys generated: ", time.time() - start_priv_key)

    # Encrypt all information
    start_encrypt_marketing = time.time()
    user_marketing_info = pd.read_csv(f"{data_dir}/UserMarketingInfo2.csv")
    encrypt_marketing_data(user_marketing_info, "EncryptedUserMarketingInfo")
    print("Marketing data encrypted: ", time.time() - start_encrypt_marketing)
    start_encrypt_transactions = time.time()
    transactions_data_info = pd.read_csv(f"{data_dir}/TransactionsData2.csv")
    encrypt_transactions_data(transactions_data_info, "EncryptedTransactionsInfo")
    print("Transactions data encrypted: ", time.time() - start_encrypt_transactions)
    start_encrypt_balance = time.time()
    user_balance_info = pd.read_csv(f"{data_dir}/UserBalanceInfo2.csv")
    encrypt_balance_data(user_balance_info, "EncryptedUserBalanceInfo")
    print("Balance data encrypted: ", time.time() - start_encrypt_balance)

'''
Function to generate private keys for everyone
'''
def generate_private_keys(row):
    attributes_arr = [row['InternalUserId'].replace("-", ""), row['UserRole'].replace(" ", "_")]
    if row['UserRole'] != 'customer':
        attributes_arr.append(row['Rank'])
        attributes_arr.append(row['WorkCountry'])
        if row['Rank'] == "Intern":
            intern_date_end = int(datetime.datetime.strptime(row['InternDateEnd'], "%Y-%m-%d").timestamp())
            attributes_arr.append(f"Date = {intern_date_end}")
        
    # Make directory if does not exist
    os.makedirs(private_key_directory, exist_ok=True)

    # Generate private keys for the user
    p = subprocess.run(["cpabe-keygen", "-o", f"{private_key_directory}/{row['InternalUserId']}_priv_key", "pub_key", "master_key"] + attributes_arr)
    # print(p)
    return p

if __name__ == "__main__":
    complete_setup()