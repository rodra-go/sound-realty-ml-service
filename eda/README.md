# Build image

```bash
docker build -t jupyter_phdata -f jupyter.Dockerfile .
```

# Run Jupyter

```bash
docker run -it --rm -v $(pwd):/home/jovyan -p 8888:8888 jupyter_phdata
```