import decryption

thingy1 = decryption.Decryption(user_id='',file_name='')
thingy1.set_filename('EncryptedUserMarketingInfo')
thingy1.set_user_id('E-f12dfc5e-c57c-498e-ae88-661f49e986d6')
thingy1.do_decryption()

thingy1.set_filename('EncryptedTransactionsInfo')
thingy1.set_user_id('E-a67fb2ee-e94b-4238-9d40-6b2aa8a55f40')
thingy1.do_decryption()

thingy1.query_by_user_id('C-57ec78fa-e81f-40b6-a8e2-f35eb529a3e1')
thingy1.do_decryption()

thingy1.query_first_n_rows(2)
thingy1.do_decryption()

# Note: You select the columns after you query & it automatically appends unencrypted data
thingy1.query_all()
thingy1.select_columns(["Type", "OriginAccNumber"])
thingy1.do_decryption()