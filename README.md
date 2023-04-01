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
3. Run `python3 setup.py` to generate keys and encrypt files
4. Run `python3 test_console.py` to see how the decryption class is utilised
