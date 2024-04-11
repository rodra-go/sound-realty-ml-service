# Sound Realty Machine Learning Service

Sound Realty's ML service for property value estimation

## Install

### 1. Create a virtual env with Python 3.9

```bash
python3.9 -m venv venv
```

### 2. Activate the virtual environment

**NOTE**: If you are running the commands from Windows, use GitBash or similar Unix-like shell

```bash
source venv/bin/activate
```

### 3. Install the project

```bash
make install
```

## Run Unit Tests and Lint

### 1. Run  unit tests
```bash
make test
```

### 2. Run code liting

```bash
make lint
```

## Run and Hit the API

### 1. Run the API

```bash
make run
```

### 2. Hit the API

```bash
make hit-api
```

### 3. Acess Swagger

This API has a Swagger endpoint that can be accessed at http://localhost:8000/docs#.


## Train and deploy a new version of the model

### 1. Train a new version

```bash
make train
```

### 2. Deploy a new version

The deployment process is handled by the CICD pipeline. After training a new
model version, just run the bumpversion to update the Tag for the new image
and push the changes to the repository.

## EDA

The notebooks used on the exploratory data analysis conducted to build
the application are available at the directory [`local_dev/`](local_dev/),
only present at branch `notebooks_and_eda`



