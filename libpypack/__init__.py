__version__ = "0.1.1"

import docker
import tarfile
import requests
import os
import libpypack.examples as examples

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
client = docker.from_env()

# If the container is in existence, grab it
elastic_container = client.containers.get("pypack_elastic")

# If running, stop it and remove it.
# NOTE: If the container is corrupt it messes up.
if(elastic_container.status == "running"):
    elastic_container.stop()
    elastic_container.remove()

# Pull the new image
client.images.pull('elasticsearch:5.5.2')

# Bind the geonames_index in the examples directory, to the Docker container
volumes = {examples.__path__[0] + "/geonames_index/":
           {"bind": "/usr/share/elasticsearch/data", "mode": "rw"}}

ports = {'9200/tcp': ('127.0.0.1', 9200)}

# Run the Docker container to interact with
client.containers.run("elasticsearch:5.5.2", ports=ports, volumes=volumes, name="pypack_elastic", detach=True)
