# CIM-Loader
Automated scripts for 
* uploading and downloading CIM files from various databases
* converting CIM files between common formats (XML, TTL, etc.)


## Installation
PyPi version coming soon.

Clone the repo and run
`pip install -e CIM-Loader`


## Usage

To use CIM-Loader for bulk upload and download, set the connection parameters with the correct url / host / port / username / password and then invoke the associated upload / download method

```python
from cimloader.databases import ConnectionParameters
from cimloader.uploaders import BlazegraphUploader
params = ConnectionParameters(url = "http://localhost:8889/bigdata/namespace/kb/sparql")
loader = BlazegraphUploader(params)

loader.upload_from_file(filename='./test_models/ieee13_seto.xml')
```


## Databases Supported
Databases to be supported in first full release:
* Blazegraph
* Neo4J
* GraphDB
* MySQL

Support may be added in the future for:
* Apache Tinkerpop
* SQlite
* AVEVA PI Historian
* Others as requested


## Attribution and Disclaimer

This software was created under a project sponsored by the U.S. Department of Energy’s Office of Electricity, an agency of the United States Government.  Neither the United States Government nor the United States Department of Energy, nor Battelle, nor any of their employees, nor any jurisdiction or organization that has cooperated in the development of these materials, makes any warranty, express or implied, or assumes any legal liability or responsibility for the accuracy, completeness, or usefulness or any information, apparatus, product, software, or process disclosed, or represents that its use would not infringe privately owned rights.

Reference herein to any specific commercial product, process, or service by trade name, trademark, manufacturer, or otherwise does not necessarily constitute or imply its endorsement, recommendation, or favoring by the United States Government or any agency thereof, or Battelle Memorial Institute. The views and opinions of authors expressed herein do not necessarily state or reflect those of the United States Government or any agency thereof.

PACIFIC NORTHWEST NATIONAL LABORATORY
operated by
BATTELLE
for the
UNITED STATES DEPARTMENT OF ENERGY
under Contract DE-AC05-76RL01830


