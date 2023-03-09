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
