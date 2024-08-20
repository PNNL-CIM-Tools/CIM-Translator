import logging
import subprocess

from cimloader.databases import ConnectionInterface, QueryResponse
from SPARQLWrapper import JSON, POST, SPARQLWrapper

_log = logging.getLogger(__name__)

class BlazegraphConnection(ConnectionInterface):
    def __init__(self, connection_params: ConnectionInterface) -> None:
        self.cim_profile = connection_params.cim_profile
        # self.cim = importlib.import_module('cimgraph.data_profile.' + self.cim_profile)
        self.namespace = connection_params.namespace
        self.iec61970_301 = connection_params.iec61970_301
        self.url = connection_params.url
        self.connection_params = connection_params
        self.sparql_obj = None

    def connect(self):
        if not self.sparql_obj:
            self.sparql_obj = SPARQLWrapper(self.connection_params.url)
            self.sparql_obj.setReturnFormat(JSON)

    def disconnect(self):
        self.sparql_obj = None
        
    def execute(self, query_message: str) -> QueryResponse:
        self.connect()
        self.sparql_obj.setQuery(query_message)
        self.sparql_obj.setMethod(POST)
        query_output = self.sparql_obj.query().convert()
        return query_output
    
    def drop(self):
        self.execute('drop all')
    

    def configure(self):
        pass


    def upload_from_file(self, filename):
        subprocess.call(["curl", "-s", "-D-", "-H", "Content-Type: application/xml", "--upload-file", filename, "-X", "Post", self.url])
        
    def upload_from_url(self):
        pass

    def upload_from_rdflib(self, rdflib_graph):

        pass
