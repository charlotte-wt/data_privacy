import time
import pandas as pd
from encryption import encrypt_balance_data

data_dir = "data"
user_balance_info = pd.read_csv(f"{data_dir}/UserBalanceInfo2.csv").head()

start_time = time.time()
encrypt_balance_data(user_balance_info, "Demo_EncryptedUserBalanceInfo")
print("Time taken to encrypt marketing data: ", time.time() - start_time)