import tarfile
import requests
import os
import libpypack.examples as examples
import subprocess
import docker
import time

import sys
import requests

# Download function and progress bar
def download(url, filename):
    with open(filename, 'wb') as f:
        response = requests.get(url, stream=True, allow_redirects=True)
        total = response.headers.get('content-length')

        if total is None:
            f.write(response.content)
        else:
            downloaded = 0
            total = int(total)
            for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                downloaded += len(data)
                f.write(data)
                done = int(50*downloaded/total)
                sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50-done)))
                sys.stdout.flush()
    sys.stdout.write('\n')

    # Extract the tar file
    print("-----Extracting geonames_index-----")
    my_tar = tarfile.open('geonames_index.tar.gz')
    my_tar.extractall(examples.__path__[0]) # specify which folder to extract to
    my_tar.close()

def run_docker():
    """

    Docker is needed for Mordecai to work, this function starts Docker automatically,
    and configues the Docker image appropriately.

    Returns
    -------
    : Running Docker Image.
      N/A

    """
    # Check if the geonames_index has been downloaded
    if not os.path.isdir(examples.__path__[0] + '/geonames_index'):

        # If not, download it to the examples directory

        url = 'https://s3.amazonaws.com/ahalterman-geo/geonames_index.tar.gz'
        print("-----Downloading geonames_index-----")
        download(url, 'geonames_index.tar.gz')

    # Using the Docker API, create a client to interact with
    print("-----Starting Docker-----", flush=True)
    client = docker.from_env()
    print("-----Docker Started-----", flush=True)


    # If the container is in existence, grab it
    try:
        print("-----Downloading Container-----")
        elastic_container = client.containers.get("pypack_elastic")

        # If running, stop it and remove it.
        # NOTE: If the container is corrupt it messes up.
        if(elastic_container.status == "running"):
            return 0

    except Exception as e:
        print(e)

    # Pull the new image
    try:
        print('Pulling container')
        client.images.pull('elasticsearch:5.5.2')
    except:
        print("Image could not be downloaded, run 'docker pull elasticsearch:5.5.2' from a terminal.", flush=True)

    # Bind the geonames_index in the examples directory, to the Docker container
    volumes = {examples.__path__[0] + "/geonames_index/":
               {"bind": "/usr/share/elasticsearch/data", "mode": "rw"}}

    ports = {'9200/tcp': ('127.0.0.1', 9200)}

    # Run the Docker container to interact with
    try:
        client.containers.run("elasticsearch:5.5.2", ports=ports, volumes=volumes, name="pypack_elastic", detach=True)
        time.sleep(30)   # Delays for 5 seconds. You can also use a float value.
    except:
        print("An error occured while running the container. Either it is already running, or you need to have 'root' access.", flush=True)
        return 1
