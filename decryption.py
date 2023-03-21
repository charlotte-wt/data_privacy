import subprocess
import tempfile
import pandas as pd
import base64

# Read the encrypted file
data_dir = "data"
encrypted_user_marketing_info = pd.read_csv(f"{data_dir}/EncryptedUserMarketingInfo.csv", encoding='utf-8')

queried = encrypted_user_marketing_info[encrypted_user_marketing_info['InternalUserId'] == 'C-ec85437f-d70c-4fc3-8990-9c685fe5827a']

employee_id = 'E-f12dfc5e-c57c-498e-ae88-661f49e986d6'

# Where to retrieve the private keys
private_key_directory = "private-keys"

# Name of private key file
priv_key = f'{private_key_directory}/{employee_id}_priv_key'

'''
Wrapper function to decrypt all rows of a given dataframe
'''
def decrypt_rows(df: pd.DataFrame):
    decrypted_rows = [_decrypt_row(row) for _, row in df.iterrows()]

    return pd.concat(decrypted_rows, axis=0, ignore_index=True)

'''
Internal function to decrypt each row
'''
def _decrypt_row(row: pd.Series):
    # Create a dictionary to store the decryption results of each row
    decrypted_row = dict()

    decrypted_row['InternalUserId'] = row['InternalUserId']

    # Create temporary directory
    temp_dir = tempfile.TemporaryDirectory()

    # For each cell in the row
    for col in row.index:
        if col == "InternalUserId":
            continue
        
        # Encode as Base64 bytes, then decode the Base64 bytes to CPABE binary
        base64_encoded_data = row[col].encode('utf-8')
        encrypted_bytes = base64.decodebytes(base64_encoded_data)

        filename = f"{row['InternalUserId']}_{col}"

        output_filename = f"{temp_dir.name}/{filename}"

        input_filename = f"{temp_dir.name}/{filename}.cpabe"

        # Create .cpabe files in the temporary folder with each cell's binary
        with open(input_filename, 'wb') as input_file:
            input_file.write(encrypted_bytes)

        # Run the decryption command
        p = subprocess.run(["cpabe-dec", "-o", output_filename, "pub_key", priv_key, input_filename])

        # If decryption fails because attributes in key do not satisfy policy, return redacted for that cell
        if p.returncode == 1:
            decrypted_row[col] = ["REDACTED"]
            continue
        
        # Read the decrypted information and put it into the dictionary
        with open(f"{output_filename}", 'r') as f:
            decrypted_data = f.read()
            decrypted_row[col] = [decrypted_data]

    # Delete the temporary directory
    temp_dir.cleanup()

    # Return the decrypted row as a dataframe
    return pd.DataFrame(decrypted_row)

print(decrypt_rows(encrypted_user_marketing_info))
