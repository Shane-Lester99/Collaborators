from py2neo import Graph
from plumbum import (cli, local)
import yaml

class DbService:

    _yaml_link = '../config/db.yaml'

    _config = None

    _neo4j_graph = None

    def load_config_file(self):
        with open(self._yaml_link) as raw_config_file:
            try:
                self._config = yaml.load(raw_config_file, yaml.FullLoader)
            except yaml.YAMLError as err:
                raise err

    def connect_to_graph(self):
        self._neo4j_graph= Graph(
                host=self._config['neo4j']['host'], 
                password=self._config['neo4j']['password'],
                port=self._config['neo4j']['port'],
                scheme=self._config['neo4j']['scheme'],
                user=self._config['neo4j']['user'],
        )

    def __init__(self):
        self.load_config_file()      
        self.connect_to_graph()
      
if __name__ == '__main__':
    x = DbService()


#g = Graph()


