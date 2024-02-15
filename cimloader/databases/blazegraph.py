import re
import mysql.connector
import logging
import importlib
import json
import enum
import subprocess

from cimloader.databases import ConnectionInterface, ConnectionParameters, Parameter, QueryResponse
from cimgraph.data_profile.known_problem_classes import ClassesWithoutMRID
from cimgraph.models import GraphModel
from SPARQLWrapper import JSON, POST, SPARQLWrapper

_log = logging.getLogger(__name__)

class BlazegraphConnection(ConnectionInterface):
    def __init__(self, connection_params: ConnectionInterface) -> None:
        self.cim_profile = connection_params.cim_profile
        self.cim = importlib.import_module('cimgraph.data_profile.' + self.cim_profile)
        self.namespace = connection_params.namespace
        self.iec61970_301 = connection_params.iec61970_301
        self.url = connection_params.url
        self.connection_params = connection_params
        self.sparql_obj = None

    def connect(self):
        if not self.sparql_obj:
            self.sparql_obj = SPARQLWrapper(self.connection_parameters.url)
            self.sparql_obj.setReturnFormat(JSON)

    def disconnect(self):
        self.sparql_obj = None
        
    def execute(self, query_message: str) -> QueryResponse:
        self.connect()
        self.sparql_obj.setQuery(query_message)
        self.sparql_obj.setMethod(POST)
        query_output = self.sparql_obj.query().convert()
        return query_output
    

    def configure(self):
        pass


    def upload_from_file(self, filename):
        subprocess.call(["curl", "-s", "-D-", "-H", "Content-Type: application/xml", "--upload-file", filename, "-X", "Post", self.url])
        
    def upload_from_url(self):
        pass

    def upload_from_rdflib(self, rdflib_graph):

        pass

    def upload_from_cimgraph(self, network:GraphModel):
        prefix = f"""PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX cim: <{self.namespace}>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        """
        triples = []
        for cim_class in list(network.graph.keys()):
            
            for obj in network.graph[cim_class].values():
#                 obj_triple = "<{url}#_{mRID}> a cim:{class_type}."
                obj_triple = """
        <urn:uuid:{mRID}> a cim:{class_type}.
                """
                triple = obj_triple.format(url = self.url, mRID = obj.mRID, class_type = cim_class.__name__)
                triples.append(triple)
                parent_classes = list(cim_class.__mro__)
                parent_classes.pop(len(parent_classes)-1)
                for class_type in parent_classes:
                    attribute_list = list(class_type.__annotations__.keys())
                    for attribute in attribute_list:
                        
                        try: #check if attribute is in data profile
                            attribute_type = cim_class.__dataclass_fields__[attribute].type
                        except:
                            #replace with warning message                       
                            _log.warning('attribute '+str(attribute) +' missing from '+str(cim_class.__name__))
                        
                        if 'List' not in attribute_type: #check if attribute is association to a class object
                            if '\'' in attribute_type: #handling inconsistent '' marks in data profile
                                at_cls = re.match(r'Optional\[\'(.*)\']',attribute_type)
                                attribute_class = at_cls.group(1)
                            else:        
                                at_cls = re.match(r'Optional\[(.*)]',attribute_type)
                                attribute_class = at_cls.group(1)

                            if attribute_class in self.cim.__all__:
                                attr_obj = getattr(obj,attribute)
                                if attr_obj is not None:
                                    value = attr_obj.mRID
                                    attr = """
        <urn:uuid:{mRID}> cim:{class_type}.{att} <urn:uuid:{value}>.
                                    """

                                    triple = attr.format(url = url, mRID = obj.mRID, class_type = class_type.__name__, att = attribute, value = value)
                                    triples.append(triple)

                            else:
                                value = GraphModel.item_dump(getattr(obj, attribute))
                                if value:
        #                              <{url}#_{mRID}> cim:{class_type}.{attr} \"{value}\".
                                    attr = """
        <urn:uuid:{mRID}> cim:{class_type}.{attr} \"{value}\".
                                     """
                                    triple = attr.format(url = url, mRID = obj.mRID, class_type = class_type.__name__, attr = attribute, value = value)
                                    triples.append(triple)
        triples.append ('}')
        query = prefix + ' INSERT DATA { ' + ''.join(triples)

        self.execute(query)