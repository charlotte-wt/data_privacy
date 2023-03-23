import subprocess
import pandas as pd
import os

data_dir = "data"
user_attributes_df = pd.read_csv(f"{data_dir}/InternalUserInfo2.csv")

employees = user_attributes_df[1000:]

# Where to store the private keys
private_key_directory = "private-keys"

'''
Function to generate private keys for everyone
'''
def generate_private_keys(row):
    attributes_arr = [row['InternalUserId'].replace("-", ""), row['UserRole'].replace(" ", "_")]
    if row['Rank']:
        attributes_arr.append(row['Rank'])
    if row['WorkCountry']:
        attributes_arr.append(row['WorkCountry'])
        
    # Make directory if does not exist
    os.makedirs(private_key_directory, exist_ok=True)

    # Generate private keys for the user
    p = subprocess.run(["cpabe-keygen", "-o", f"{private_key_directory}/{row['InternalUserId']}_priv_key", "pub_key", "master_key"] + attributes_arr)
    print(p)
    return p

print(user_attributes_df[1000:])
print(user_attributes_df.columns)

employees.apply(generate_private_keys, axis=1)