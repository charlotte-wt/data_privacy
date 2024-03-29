import subprocess
import tempfile
import pandas as pd
import base64

row_identifiers_dict = {
    "EncryptedTransactionsInfo": ['TransactionId', 'OriginInternalUserId'],
    "EncryptedUserBalanceInfo": ['InternalUserId'],
    "EncryptedUserMarketingInfo": ['InternalUserId']
}

class Decryption:
    # constructor
    def __init__(self, file_name, user_id):
        # Instance variables of class

        # Read the encrypted file
        self.data_dir = "data"
        self.file_name = file_name

        if (self.file_name != ''):
            self.encrypted_info = pd.read_csv(f"{self.data_dir}/{self.file_name}.csv", encoding='utf-8')
            self.queried = self.encrypted_info
            self.row_identifiers = row_identifiers_dict.get(self.file_name, [])
        else:
            self.encrypted_info = None
            self.queried = None
            self.row_identifiers = row_identifiers_dict.get(self.file_name, [])
        

        self.user_id = user_id # E-f12dfc5e-c57c-498e-ae88-661f49e986d6

        # Where to retrieve the private keys
        self.private_key_directory = "private-keys"

        # Name of private key file
        self.priv_key = f'{self.private_key_directory}/{self.user_id}_priv_key'

    '''
    Wrapper function to do decryption based on content in instance variables
    '''
    def do_decryption(self):
        print(self.decrypt_rows(self.queried))

    def set_filename(self, filename):
        self.file_name = filename
        self.encrypted_info = pd.read_csv(f"{self.data_dir}/{self.file_name}.csv", encoding='utf-8')
        self.queried = self.encrypted_info
        self.row_identifiers = row_identifiers_dict.get(self.file_name, [])

    def set_user_id(self, uid):
        self.user_id = uid
        self.priv_key = f'{self.private_key_directory}/{self.user_id}_priv_key'

    '''
    Query functionalities
    '''
    def query_all(self):
        self.queried = self.encrypted_info

    def query_first_n_rows(self, n:int):
        self.queried = self.encrypted_info.head(n)

    def query_by_user_id(self, user_id:str):
        if self.file_name == "EncryptedTransactionsInfo":
            self.queried = self.encrypted_info[self.encrypted_info["OriginInternalUserId"] == user_id]
        else:
            self.queried = self.encrypted_info[self.encrypted_info["InternalUserId"] == user_id]
        print("successfuly queried :>")

    def select_columns(self, colnames:list):
        # Note: You select the columns after you query & it automatically appends unencrypted data
        self.queried = self.queried[self.row_identifiers + colnames]

    '''
    Wrapper function to decrypt all rows of a given dataframe
    '''
    def decrypt_rows(self, df: pd.DataFrame):
        decrypted_rows = [self._decrypt_row(row) for _ , row in df.iterrows()]

        return pd.concat(decrypted_rows, axis=0, ignore_index=True)

    '''
    Internal function to decrypt each row
    '''
    def _decrypt_row(self, row: pd.Series):
        # Create a dictionary to store the decryption results of each row
        decrypted_row = dict()

        # Create temporary directory
        temp_dir = tempfile.TemporaryDirectory()

        # For each cell in the row
        for col in row.index:
            if col in self.row_identifiers:
                decrypted_row[col] = row[col]
                continue
            
            # Encode as Base64 bytes, then decode the Base64 bytes to CPABE binary
            base64_encoded_data = row[col].encode('utf-8')
            encrypted_bytes = base64.decodebytes(base64_encoded_data)

            filename = f"{row[self.row_identifiers[0]]}_{col}"

            output_filename = f"{temp_dir.name}/{filename}"

            input_filename = f"{temp_dir.name}/{filename}.cpabe"

            # Create .cpabe files in the temporary folder with each cell's binary
            with open(input_filename, 'wb') as input_file:
                input_file.write(encrypted_bytes)

            # Run the decryption command
            p = subprocess.run(["cpabe-dec", "-o", output_filename, "pub_key", self.priv_key, input_filename])

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
