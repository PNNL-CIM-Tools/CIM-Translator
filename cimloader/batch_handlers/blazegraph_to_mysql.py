
# from cimloader.databases.blazegraph import Blazegraph
from cimloader.databases.mysql import MySQL
from cimloader.converters.dss_to_cim import DSStoCIM
from cimloader.databases import ConnectionInterface, ConnectionParameters, Parameter, QueryResponse

import os
import logging
import subprocess


_log = logging.getLogger(__name__)

class BlazegraphtoMySQL():
    def __init__(self, naerm_params:ConnectionInterface, neo4j_params:ConnectionInterface, 
                 tmp_dir:str, docker_container:str):
        # self.NaermDownloader = NAERM(naerm_params)
        # self.Neo4jConnection= Neo4j(neo4j_params)
        pass