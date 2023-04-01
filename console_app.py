import base64
import bcrypt
import hashlib
import pandas as pd
# import encryption
import decryption

'''
Load data from AppUserInfo3.csv
'''
def load_appuserinfo():
    return pd.read_csv('data/AppUserInfo3.csv')

'''
Return hashed password after encryption
'''
def hash_pwd(user_id: str, pwd: str):
    hash_object = hashlib.sha256((pwd + user_id).encode('utf-8'))
    return hash_object.hexdigest()

'''
Retrieve user's profile details
'''
def view_profile(uid):
    # TO IMPLEMENT
    print('function 1')
    decrypt = decryption.Decryption('EncryptedUserMarketingInfo', uid)
    decrypt.query_by_user_id(uid)
    decrypt.do_decryption()

'''
Retrieve user's transaction details
'''
def view_transactions(uid):
    # TO IMPLEMENT
    print('function 2')
    decrypt = decryption.Decryption('EncryptedTransactionsInfo', uid)
    decrypt.query_by_user_id(uid)
    decrypt.do_decryption()

'''
Retrieve other user's profile details
'''
def query_profile(uid, current_uid):
    # TO IMPLEMENT
    print('function 3')
    decrypt = decryption.Decryption('EncryptedUserMarketingInfo', current_uid)
    decrypt.query_by_user_id(uid)
    decrypt.do_decryption()
'''
Retrieve other user's transaction details
'''
def query_transactions(uid, current_uid):
    # TO IMPLEMENT
    print('function 4', uid, current_uid)
    decrypt = decryption.Decryption('EncryptedTransactionsInfo', current_uid)
    decrypt.query_by_user_id(uid)
    decrypt.do_decryption()

# Loads user info
app_user_info = load_appuserinfo()
current_user = None

while True:
    print('*****************')
    print('***CONSOLE APP***')
    print('*****************')

    if input('Enter "0" to quit, enter any other key to login: ') == '0':
        break

    print('\n****** LOGIN ******')
    try_id = input('User ID: ')
    try_pwd = input('Password: ')
    # print(list(app_user_info.loc[app_user_info['LoginUserId'] == try_id]['Password'])[0])
    # print(hash_pwd(try_id, try_pwd))
    if len(app_user_info.loc[app_user_info['LoginUserId'] == try_id]) == 0 or \
        (list(app_user_info.loc[app_user_info['LoginUserId'] == try_id]['Password'])[0] != hash_pwd(try_id, try_pwd)):
        print('Invalid login attempt, returning to main screen\n')
        continue

    print('Welcome!')
    current_user_internal_id = list(app_user_info.loc[app_user_info['LoginUserId'] == try_id]["InternalUserId"])[0]
    current_user_role = list(app_user_info.loc[app_user_info['LoginUserId'] == try_id]["UserRole"])[0]
    while True:
        print('**********************************************************************************')
        print(f'Internal User ID: {current_user_internal_id}')
        print(f'Role: {current_user_role}')
        print('[0] Logout')
        print('[1] View your own profile')
        print('[2] View your own transactions')
        print('[3] Query another user\'s profile')
        print('[4] Query another user\'s transactions')
        option = input('Enter option number: ')
        if option not in ['0', '1', '2', '3', '4']:
            print('Invalid input!\n')
            continue
        if option == '0':
            print('You are now logged out.\n\n')
            break
        if option == '1':
            view_profile(current_user_internal_id)
        elif option == '2':
            view_transactions(current_user_internal_id)
        elif option == '3':
            query_id = input('Enter the User ID of the user you want to query for: ')
            query_id_login = list(app_user_info.loc[app_user_info['LoginUserId'] == query_id]["InternalUserId"])[0]
            query_profile(query_id_login, current_user_internal_id)
        elif option == '4':
            query_id = input('Enter the User ID of the user you want to query for: ')
            query_id_login = list(app_user_info.loc[app_user_info['LoginUserId'] == query_id]["InternalUserId"])[0]
            query_transactions(query_id_login, current_user_internal_id)
        print()


# print(type(app_user_info.loc[app_user_info['LoginUserId'] == 'fPfuylSs']['Password'][0]))

# print(app_user_info)
# b'$2b$12$cfDRDb4WEVY/XGBh8KopFen3.dQzXokoqzEJtX55bPkvu2Im.or.m'
# print(hash_pwd('fPfuylSs', 'meBVpcAXTD'))