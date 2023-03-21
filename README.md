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
    2. Search and Select `Remote Containers: Open Folder in Container...

# Usage

To test it out:
1. Rebuild the Docker image
2. Run the container
3. Run these commands in order:
   - `cpabe-setup`
   - `python3 setup.py`
   - `python3 encrypt.py`
   - `python3 decrypt.py`