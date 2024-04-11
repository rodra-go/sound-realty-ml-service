# Use the official Python 3.9 image as the base image
FROM python:3.9

# Install Jupyter Notebook explicitly
RUN pip install jupyter

# Optionally, if you have additional dependencies in a requirements.txt file, ensure it's copied and installed:
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Set the working directory in the container
WORKDIR /home/jovyan

# Expose the port Jupyter Notebook will run on
EXPOSE 8888

# Run Jupyter Notebook when the container launches
# Note: The --ip=0.0.0.0 argument allows connections from any IP address.
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root", "--no-browser", "--NotebookApp.token=''", "--NotebookApp.password=''"]