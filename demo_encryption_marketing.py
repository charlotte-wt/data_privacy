import time
import pandas as pd
from encryption import encrypt_marketing_data

data_dir = "data"
user_marketing_info = pd.read_csv(f"{data_dir}/UserMarketingInfo2.csv").head()

start_time = time.time()
encrypt_marketing_data(user_marketing_info, "Demo_EncryptedUserMarketingInfo")
print("Time taken to encrypt marketing data: ", time.time() - start_time)