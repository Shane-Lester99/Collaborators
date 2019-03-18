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
            self._mongo_db.collection_names()
            
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


    def _make_list_correct_length(self, wanted_length, row_items):
        if wanted_length < len(row_items):
            print('Error in list resize. Critical error. Exiting.\n')
            sys.exit(1)
        for i in range(0, wanted_length - 1, 1):
            try:
                row_items[i]
            except IndexError as err:
                row_items.append(None)
        return row_items

    def add_many_new_interest_nodes(self, dataframe):
        for row in dataframe.iterrows():
            index, data = row
            row_items = data.tolist()
            row_items = self._make_list_correct_length(4, row_items)
            self._add_new_interest_node('interest', row_items[0], row_items[1], row_items[2], row_items[3])

    def _add_new_interest_node(self, label, user_id, interest_name, interest_level, description):
        query = n_h.find_node('user', user_id)
        exist_nodes_with_id = self._neo4j_graph.run(query)
        if exist_nodes_with_id.data():
            query = n_h.create_node(label, [interest_name])
            self._neo4j_graph.run(query)
            query = n_h.match_associated_interest(user_id, interest_name) 
            exist_interest_with_name = self._neo4j_graph.run(query).data()
            if len(exist_interest_with_name) == 0:
                query = n_h.add_associated_interest(user_id, interest_name, interest_level)
                self._neo4j_graph.run(query)
                mongo_interest = m_h.MongoDbSchema.Interest(interest_name, description)
                new_interest_doc = mongo_interest.create_new_interest_doc()
                self._mongo_db[mongo_interest.table_name].insert(new_interest_doc) 
                print('\tData saved for interest {0} at ... {1}\n'.format(interest_name, datetime.now()))
            else:
                print('\tData associated with interest {0} already present.\n\tInterest data rejected at ... {1}\n'.format(interest_name, datetime.now()))
        else:
            print('\tUser associated with id: {0} does not exist.\n\tInterest data rejected at ... {1}\n'.format(user_id, datetime.now()))

    def add_many_new_skill_nodes(self, dataframe):
        for row in dataframe.iterrows():
            index, data = row
            row_items = data.tolist()
            row_items = self._make_list_correct_length(4, row_items)
            self._add_new_skill_node('skill', row_items[0], row_items[1], row_items[2], row_items[3])

    def _add_new_skill_node(self, label, user_id, skill_name, skill_level, description):
        query = n_h.find_node('user', user_id)
        exist_nodes_with_id = self._neo4j_graph.run(query)
        if exist_nodes_with_id.data():
            query = n_h.create_node(label, [skill_name])
            self._neo4j_graph.run(query)
            query = n_h.match_associated_skill(user_id, skill_name) 
            exist_skill_with_name = self._neo4j_graph.run(query).data()
            if len(exist_skill_with_name) == 0:
                query = n_h.add_associated_skill(user_id, skill_name, skill_level)
                self._neo4j_graph.run(query)
                mongo_skill = m_h.MongoDbSchema.Skill(skill_name, description)
                new_skill_doc = mongo_skill.create_new_skill_doc()
                self._mongo_db[mongo_skill.table_name].insert(new_skill_doc) 
                print('\tData saved for skill {0} at ... {1}\n'.format(skill_name, datetime.now()))
            else:
                print('\tData associated with skill {0} already present.\n\tSkill data rejected at ... {1}\n'.format(skill_name, datetime.now()))
        else:
            print('\tUser associated with id: {0} does not exist.\n\tSkill data rejected at ... {1}\n'.format(user_id, datetime.now()))


    def add_many_new_project_nodes(self, dataframe):
        for row in dataframe.iterrows():
            index, data = row
            row_items = data.tolist()
            row_items = self._make_list_correct_length(4, row_items)
            self._add_new_project_node('project', row_items[0], row_items[1], row_items[2], row_items[3])

    def _add_new_project_node(self, label, user_id, project_name, role, description): 
        if not role or not description:
            role = 'unknown'
            description = None
        query = n_h.find_node('user', user_id)
        exist_nodes_with_id = self._neo4j_graph.run(query)
        if exist_nodes_with_id.data():
            query = n_h.create_node(label, [project_name])
            self._neo4j_graph.run(query)
            query = n_h.match_project_association(user_id, project_name)  
            exist_project_with_name = self._neo4j_graph.run(query).data()
            if len(exist_project_with_name) == 0:
                query = n_h.add_to_project(user_id, project_name, role)
                self._neo4j_graph.run(query)
                mongo_project = m_h.MongoDbSchema.Project(project_name, description)
                new_project_doc = mongo_project.create_new_project_doc()
                self._mongo_db[mongo_project.table_name].insert(new_project_doc) 
                print('\tData saved for project {0} at ... {1}\n'.format(project_name, datetime.now()))
            else:
                print('\tData associated with project {0} already present.\n\tProject data rejected at ... {1}\n'.format(project_name, datetime.now()))
        else:
            print('\tUser associated with id: {0} does not exist.\n\tProject data rejected at ... {1}\n'.format(user_id, datetime.now()))

    def add_many_new_user_nodes(self, dataframe):
        # Take the dataframe and for each row add a new nor
        for row in dataframe.iterrows():
            index, data = row
            row_items = data.tolist()
            self._add_new_user_node('user', row_items[0], row_items[1], row_items[2], row_items[3])

    def _add_new_user_node(self, label, user_id, first_name, last_name, description):
        query = n_h.find_node(label, user_id) 
        exist_nodes_with_id = self._neo4j_graph.run(query)
        if len(exist_nodes_with_id.data()) == 0: 
            query = n_h.create_node(label, [user_id, first_name, last_name])
            self._neo4j_graph.run(query)
            mongo_user = m_h.MongoDbSchema.User(first_name, last_name, user_id, description)
            #self._mongo_db[mongo_user.table_name].            
            new_user_doc = mongo_user.create_new_user_doc()
            self._mongo_db[mongo_user.table_name].insert(new_user_doc)
            print('\tData saved for user with id {0} at ... {1}\n'.format(user_id, datetime.now()))
        else:
            print('\tData already downloaded for user with id: {0}\n\tNew user rejected at ... {1}\n'.format(user_id, datetime.now()))

    def __delete_all_data(self):
        ans = input('Are you sure you want to delete all data?(Y/N)')
        if ans == 'Y':
            query = 'MATCH (n) DETACH DELETE n;'
            self._neo4j_graph.run(query)
            print('Mongo data not yet deleted')
        else:
            print('Data not deleted. Exiting.')
        

if __name__ == '__main__':
    x = DbService()

