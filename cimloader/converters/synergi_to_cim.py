from converters import mdb2dss
from cimloader.converters import dss_to_cim
class MDBToCIM:
    def __init__(self, input_file):
        self.input_file = input_file
        self.out_dir = None
        self.file_name = None
        self.synergi_json = {}
        self.main_method()

    def main_method(self):
        self.make_synergi_json()
        self.convert_mdb_to_dss()
        self.convert_dss_to_cim()

    def make_synergi_json(self):
        pass

    def convert_mdb_to_dss(self):
        mdb2dss.ConvertMDB(self.synergi_json)

    def convert_dss_to_cim(self):
        dss_converter = dss_to_cim.DSStoCIM()
        dss_converter.convert_file(file_path=f'{self.out_dir}', master_file='Master.dss')