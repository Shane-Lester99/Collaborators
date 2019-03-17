from py2neo import Graph
from plumbum import (cli, local)
import yaml
import sys
import os
sys.path.append(local.path(__file__).dirname.up())
from db_helper_methods import neo4j_helper as n_h
from db_helper_methods import mongodb_helper as m_h
class DbService:

    _yaml_link = '../config/db.yaml'

    _config = None

    _neo4j_graph = None

    def __init__(self):
        self._load_config_file()      
        self._connect_to_graph()

    def _load_config_file(self):
        with open(self._yaml_link) as raw_config_file:
            try:
                self._config = yaml.load(raw_config_file, yaml.FullLoader)
            except yaml.YAMLError as err:
                raise err

    def _connect_to_graph(self):
        self.neo4j_graph= Graph(
                host=self._config['neo4j']['host'], 
                password=self._config['neo4j']['password'],
                port=self._config['neo4j']['port'],
                scheme=self._config['neo4j']['scheme'],
                user=self._config['neo4j']['user'],
        )

    def _connect_to_mongo(self):
        pass

    def add_many_new_user_nodes(self, dataframe):
        # Take the dataframe and for each row add a new node
        for row in dataframe.iterrows():
            index, data = row
            row_items = data.tolist()
            self.add_new_user_node('user', row_items[0], row_items[1], row_items[2], row_items[3]))
    def add_new_user_node(self, label, first_name, last_name, user_id, other_data_items):
        print('label: {0}, f: {1}, l: {2}, id: {3}, other: {4}'.format(label, first_name, last_name, user_id, description))
        

if __name__ == '__main__':
    x = DbService()


#g = Graph()


