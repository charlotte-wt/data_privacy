# Setting Up

1. Build the Docker image

```
docker build -t my-cpabe .
```

2. Launch the Docker container

```
docker run -it my-cpabe
```

3. Test if cpabe library is installed successfully on the Docker container (run this on the container bash)

```
cpabe-setup -h
```

4. Remote Container:

   1. Open command palette
   2. Search and Select Remote Containers: Open Folder in Container...

5. If you have the Dev Containers extension:
   1. Open command palette
   2. Search and Select Dev Containers: Attach to Running Container...

# Usage

To test it out:

1. Rebuild the Docker image
2. Run the container
3. Run `python3 setup.py` to generate keys (master, public, and private) and encrypt (entire) files
4. Run `python3 test_console.py` to see how the decryption class is utilised
5. Run `python3 console_app.py` to launch console app

# Console App Demo

Run `scriptreplay --timing=app_time.tm app_demo` to view an automatic replay of console app. Details about the demo users are listed in IdealUsers.txt.

# Mock Setup Demo

1. Run `python3 demo_setup.py` to generate private keys for 36 employees
2. Run `python3 demo_encryption_balance.py`, `python3 demo_encryption_marketing.py`, `python3 demo_encryption_transactions.py` to encrypt 5 rows of the respective data
3. Run `python3 demo_decryption_balance.py <internal employee id>`, `python3 demo_decryption_marketing.py <internal employee id>`, `python3 demo_decryption_transactions.py <internal employee id>` to decrypt 5 rows of the respective data using the specified employee's private key
