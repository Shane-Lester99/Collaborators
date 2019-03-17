from py2neo import Graph
from pymongo import MongoClient
from plumbum import (cli, local)
from datetime import datetime
import yaml
import sys
import os
sys.path.append(local.path(__file__).dirname.up())
from db_helper_methods import neo4j_helper as n_h
from db_helper_methods import mongodb_helper as m_h

# Get access to mongo
#import pymongo
#from pymongo import MongoClient
#print(pymongo)
#myclient = pymongo.MongoClient()
#mydb = myclient['mydatabase']
#mycol=myclient['cusomters']

class DbService:

    _yaml_link = '../config/db.yaml'

    _config = None

    _neo4j_graph = None

    _mongo_client = None

    # For convience
    _mongo_db = None

    def __init__(self):
        self._load_config_file()       
        print('Connecting to Neo4j at ... {0}'.format(datetime.now()))
        self._connect_to_graph()
        try:
            self._neo4j_graph.match_one()
        except Exception as err:
            print("Neo4j failed to connect at ... {0}\nPlease check readme for proper neo4j connection. Exiting.".format(datetime.now()))
            sys.exit(1)
        print('Now connected to Neo4j at ... {0}\n'.format(datetime.now()))
        print('Connecting to MongoDb at ... {0}'.format(datetime.now()))
        self._connect_to_mongo()
        try: 
            self._mongo_db = self._mongo_client[self._config['mongodb']['database_name']]
            print(self._mongo_db.collection_names(), self._mongo_db['user'])
            
        except Exception as err:
            print(err)
            print("MongoDb failed to connect at ... {0}\nPlease check readme for proper MongoDb connection. Exiting.".format(datetime.now()))
            sys.exit(1)
        print('Now connected to MongoDb at ... {0}\n'.format(datetime.now()))
        


    def _load_config_file(self):
        with open(self._yaml_link) as raw_config_file:
            try:
                self._config = yaml.load(raw_config_file, yaml.FullLoader)
            except yaml.YAMLError as err:
                raise err

    def _connect_to_graph(self):
        self._neo4j_graph= Graph(
                host=self._config['neo4j']['host'], 
                password=self._config['neo4j']['password'],
                port=self._config['neo4j']['port'],
                scheme=self._config['neo4j']['scheme'],
                user=self._config['neo4j']['user'],
        )

    def _connect_to_mongo(self):
        username = self._config['mongodb']['username']
        password = self._config['mongodb']['password']
        uri = None
        if all([username, password]):
            uri = ''.join('mongodb://{0}:{1}@{2}:{3}/'.format(
                username, 
                password, 
                self._config['mongodb']['host'],
                self._config['mongodb']['port'],
                ))
        else:
            uri = 'mongodb://{0}:{1}/'.format( 
                self._config['mongodb']['host'],
                self._config['mongodb']['port'],
                #self._config['mongodb']['database_name']
                ) 
        self._mongo_client = MongoClient(uri)

    def add_many_new_user_nodes(self, dataframe):
        # Take the dataframe and for each row add a new nor
        for row in dataframe.iterrows():
            index, data = row
            row_items = data.tolist()
            self._add_new_user_node('user', row_items[0], row_items[1], row_items[2], row_items[3])
            

    def _add_new_user_node(self, label, user_id, first_name, last_name, description):
        #print('label: {0}, f: {1}, l: {2}, id: {3}, other: {4}'.format(label, first_name, last_name, user_id, description))
        # TODO: push user data to neo4j and mongo here 
        query = n_h.find_node(label, user_id)
        #query = n_h.create_node(label, [user_id, first_name, last_name])
        #print(query)
        exist_nodes_with_id = self._neo4j_graph.run(query)
        if len(exist_nodes_with_id.data()) == 0: 
            query = n_h.create_node(label, [user_id, first_name, last_name])
            self._neo4j_graph.run(query)
            mongo_user = m_h.MongoDbSchema.User(first_name, last_name, user_id, description)
            #self._mongo_db[mongo_user.table_name].            
            new_user_doc = mongo_user.create_new_user_doc()
            self._mongo_db[mongo_user.table_name].insert(new_user_doc)
            print('Data saved for user with id {0} at ... {1}'.format(user_id, datetime.now()))
        else:
            print('Data already downloaded for user with id: {0}\nNew user rejected at ... {1}\n'.format(user_id, datetime.now()))





if __name__ == '__main__':
    x = DbService()

