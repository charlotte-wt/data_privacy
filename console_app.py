import base64
import bcrypt
import hashlib
import pandas as pd
# import encryption, decryption

'''
Load data from AppUserInfo2.csv
'''
def load_appuserinfo():
    return pd.read_csv('data/AppUserInfo2.csv')

'''
Return hashed password after encryption
'''
def hash_pwd(user_id: str, pwd: str):
    hash_object = hashlib.sha256((pwd + user_id).encode('utf-8'))
    return hash_object.hexdigest()

'''
Retrieve user's profile details
'''
def view_profile():
    # TO IMPLEMENT
    print('function 1')

'''
Retrieve user's transaction details
'''
def view_transactions():
    # TO IMPLEMENT
    print('function 2')

'''
Retrieve other user's profile details
'''
def query_profile(user_id):
    # TO IMPLEMENT
    print('function 3', user_id)

'''
Retrieve other user's transaction details
'''
def query_transactions(user_id):
    # TO IMPLEMENT
    print('function 4', user_id)


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
    if len(app_user_info.loc[app_user_info['LoginUserId'] == try_id]) == 0 or \
        (app_user_info.loc[app_user_info['LoginUserId'] == try_id]['Password'][0] != hash_pwd(try_id, try_pwd)):
        print('Invalid login attempt, returning to main screen\n')
        continue

    print('Welcome!')
    current_user = app_user_info.loc[app_user_info['LoginUserId'] == try_id]
    while True:
        print('**********************************************************************************')
        print(f'Role: {current_user["UserRole"][0]}')
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
            view_profile()
        elif option == '2':
            view_transactions()
        elif option == '3':
            query_id = input('Enter the User ID of the user you want to query for: ')
            query_profile(query_id)
        elif option == '4':
            query_id = input('Enter the User ID of the user you want to query for: ')
            query_transactions(query_id)
        print()


# print(type(app_user_info.loc[app_user_info['LoginUserId'] == 'fPfuylSs']['Password'][0]))

# print(app_user_info)
# b'$2b$12$cfDRDb4WEVY/XGBh8KopFen3.dQzXokoqzEJtX55bPkvu2Im.or.m'
# print(hash_pwd('fPfuylSs', 'meBVpcAXTD'))