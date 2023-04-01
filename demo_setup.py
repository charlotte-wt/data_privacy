from setup import generate_private_keys
import pandas as pd

data_dir = "data"
employees = pd.read_csv(f"{data_dir}/InternalUserInfo3.csv")[1000:]

employees.apply(generate_private_keys, axis=1)