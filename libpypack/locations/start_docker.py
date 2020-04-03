import tarfile
import requests
import os
import libpypack.examples as examples
import subprocess
import docker
import time


def run_docker():
    # Check if the geonames_index has been downloaded
    if not os.path.isdir(examples.__path__[0] + '/geonames_index'):

        # If not, download it to the examples directory
        url = 'https://s3.amazonaws.com/ahalterman-geo/geonames_index.tar.gz'
        r = requests.get(url, allow_redirects=True)
        open('geonames_index.tar.gz', 'wb').write(r.content)

        # Extract the tar file
        my_tar = tarfile.open('geonames_index.tar.gz')
        my_tar.extractall(examples.__path__[0]) # specify which folder to extract to
        my_tar.close()

    # Using the Docker API, create a client to interact with
    print("-----Starting Docker-----", flush=True)
    client = docker.from_env()
    print("-----Docker Started-----", flush=True)


    # If the container is in existence, grab it
    try:
        print("-----Trying to download ontainer-----")
        elastic_container = client.containers.get("pypack_elastic")

        # If running, stop it and remove it.
        # NOTE: If the container is corrupt it messes up.
        if(elastic_container.status == "running"):
            elastic_container.stop()
            elastic_container.remove()

    except Exception as e:
        print(e)

    # Pull the new image
    try:
        print('Pulling container')
        client.images.pull('elasticsearch:5.5.2')
    except:
        print("Image could not be pulled, run 'docker pull elasticsearch:5.5.2'")

    # Bind the geonames_index in the examples directory, to the Docker container
    volumes = {examples.__path__[0] + "/geonames_index/":
               {"bind": "/usr/share/elasticsearch/data", "mode": "rw"}}

    ports = {'9200/tcp': ('127.0.0.1', 9200)}

    # Run the Docker container to interact with
    client.containers.run("elasticsearch:5.5.2", ports=ports, volumes=volumes, name="pypack_elastic", detach=True)
    time.sleep(30)   # Delays for 5 seconds. You can also use a float value.
