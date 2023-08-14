from __future__ import annotations
import math
import importlib
import logging
import re
import rdflib


from typing import Dict, List, Optional


from neo4j import GraphDatabase, RoutingControl
from neo4j.exceptions import DriverError, Neo4jError

from cimgraph.databases import ConnectionInterface, ConnectionParameters, Parameter, QueryResponse
from cimgraph.databases import Neo4JConnection

import rdflib
# from rdflib import Graph, Namespace
from rdflib.namespace import RDF

_log = logging.getLogger(__name__)

class Neo4jUploader(ConnectionInterface):
    def __init__(self, connection_parameters):
        self.connection_parameters = connection_parameters
        self.cim_profile = connection_parameters.cim_profile
        self.namespace = connection_parameters.namespace
        self.url = connection_parameters.url
        self.username = connection_parameters.username
        self.password = connection_parameters.password
        self.database = connection_parameters.database
        self.driver = None

    def connect(self):
        if not self.driver:
            self.driver = GraphDatabase.driver(self.url, auth=(self.username, self.password))
            self.driver.verify_connectivity()

    def disconnect(self):
        self.driver.close()
        self.driver = None

    def execute(self, query_message: str) -> QueryResponse:
        self.connect()

        try:
            records, summary, keys = self.driver.execute_query(query_message, database_=self.database )
            return records, summary, keys
        # Capture any errors along with the query and data for traceability
        except (DriverError, Neo4jError) as exception:
            _log.error("%s raised an error: \n%s", query_message, exception)

    def configure(self):
        if self.cim_profile is not None and self.namespace is not None:
            self.execute("CREATE CONSTRAINT n10s_unique_uri FOR (r:Resource) REQUIRE r.uri IS UNIQUE;")
            self.execute("CALL n10s.nsprefixes.add(\""+self.cim_profile+"\",\""+self.namespace+"\");")
        else:
            _log.exception("CIM profile and namespace must be defined in ConnectionParameters")

        graph_config = """call n10s.graphconfig.init({
            handleMultival: "ARRAY", 
            handleVocabUris: "KEEP",
            keepCustomDataTypes: true,
            handleRDFTypes: "LABELS"})"""
        self.execute(graph_config)

    def upload_from_ttl(self, file):
        self.execute(f"call n10s.rdf.import.fetch( {file}, \"Turtle\") ") 
        

    def upload_from_xml(self, file):
        
        # rdf_namespace = rdflib.Namespace(self.namespace)
        # rdf_graph = rdflib.Graph()
        # rdf_graph.parse(file)
        # rdf_graph.bind("cim", rdf_namespace)
        # rdf_graph.bind("rdf", RDF)

        self.execute(f"call n10s.rdf.import.fetch( {file}, \"RDF/XML\") ")



    def upload_from_rdflib(self, rdflib_graph):

        pass

    def upload_from_cimgraph(self):
        pass

