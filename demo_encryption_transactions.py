import time
import pandas as pd
from encryption import encrypt_transactions_data

data_dir = "data"
transactions_data_info = pd.read_csv(f"{data_dir}/TransactionsData2.csv").head()

start_time = time.time()
encrypt_transactions_data(transactions_data_info, "Demo_EncryptedTransactionsInfo")
print("Time taken to encrypt transactions data: ", time.time() - start_time)