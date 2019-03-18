from plumbum import (cli, local)
from datetime import datetime
from collections import OrderedDict
import pandas as pd
import yaml
from db_service import DbService

class CollaboratorDotNet(cli.Application):
    # Types of acceptable files at command line
    _valid_file_types = ('skill', 'project', 'organization', 'interest', 'distance', 'user', 'friend')
    # Structure of csv columns 
    _valid_file_structures = {
            _valid_file_types[0] : OrderedDict({'userid': int, 'skill': str, 'skilllevel': int, 'description': str}),
            _valid_file_types[1] : OrderedDict({'userid': int, 'project': str, 'role' : str, 'description': str}),
            _valid_file_types[2] : OrderedDict({'userid': int, 'organization': str, 'organizationtype': str, 'description': str}),
            _valid_file_types[3] : OrderedDict({'userid': int, 'interest': str, 'interestlevel': int, 'description':str}),
            _valid_file_types[4] : OrderedDict({"organization1": str, "organization2": str, "distance": int}),
            _valid_file_types[5] : OrderedDict({'userid': int, 'firstname': str, 'lastname': str, 'description': str}),
            # Not implemented
            _valid_file_types[6] : OrderedDict({'userid1': int, 'userid2':int})
    } 

    _yaml_option = cli.SwitchAttr(
        ['-y', '--yaml-option'], mandatory=False, default='load_all_data',
        help='In the yaml file specified at path from --input-many switch, can specify which attribue of yaml file you want to download. load_all_data is used by default. Must be used before the --input-many switch to work.'
    )

    _db_service = None

    def connect_to_db(self):
        if not self._db_service:
            print('Connecting to databases at ... {0}'.format(datetime.now()))
            self._db_service = DbService()



    @cli.switch(['-m', '--input-many'], str)
    def input_lots_of_data(self, file_path_to_yaml):
        """ Input a list of csv files to input into input_data """
        self.connect_to_db()
        yaml_file = None
        with open(file_path_to_yaml) as raw_config_file:
            try:
                yaml_file  = yaml.load(raw_config_file, yaml.FullLoader)
            except yaml.YAMLError as err:
                raise err
        print(self._yaml_option)
        for i in yaml_file[self._yaml_option]:
            self.input_data(i)
        

    # will input a file named file_name that is input data of file_type
   
    @cli.switch(['-i', '--input'], str)
    def input_data(self, file_path_and_type):
        """ Input data, enter a string of form file_type,file_path  """
        self.connect_to_db()
        file_path, file_type = file_path_and_type.split(',')
        print('Reading file of type {0} from {1} at ... {2}'.format(file_type, file_path, datetime.now())) 
        print('Check if input is valid at ... {0}'.format(datetime.now()))
        # Error validation
        self.is_file(file_path)
        self.is_csv(file_path)
        self.is_valid_file_type(file_type, self._valid_file_types, self._valid_file_structures, file_path)
        print('Input validated at ... {0}\n'.format(datetime.now()))
        print('Attempting to read data from {0} at ... {1}'.format(file_path, datetime.now())) 
        input_data = self.read_data(file_path, file_type)
        print('Data read and cleaned at ... {0}\n'.format(datetime.now()))
        if file_type == self._valid_file_types[0]:
            # Skill switch
            print("Loading {0} data at ... {1}\n\n".format(self._valid_file_types[0].upper(), datetime.now()))
            self._db_service.add_many_new_skill_nodes(input_data)
        elif file_type == self._valid_file_types[1]:
            # Project switch
            print("Loading {0} data at ... {1}\n\n".format(self._valid_file_types[1].upper(), datetime.now()))
            self._db_service.add_many_new_project_nodes(input_data)
        elif file_type == self._valid_file_types[2]:
            # Organization switch 
            print("Loading {0} data at ... {1}\n\n".format(self._valid_file_types[2].upper(), datetime.now()))
            self._db_service.add_many_new_organization_nodes(input_data)
        elif file_type == self._valid_file_types[3]: 
            # Interest switch
            print("Loading {0} data at ... {1}\n\n".format(self._valid_file_types[3].upper(), datetime.now()))
            self._db_service.add_many_new_interest_nodes(input_data)
        elif file_type == self._valid_file_types[4]:
            # Distance switch 
            print("Loading {0} data at ... {1}\n\n".format(self._valid_file_types[4].upper(), datetime.now()))
            self._db_service.add_many_new_distance_rels(input_data)
        elif file_type == self._valid_file_types[5]:
            # Skill associated with user switch
            print('Loading {0} data at  ... {1}\n\n'.format(self._valid_file_types[5].upper(), datetime.now()))
            self._db_service.add_many_new_user_nodes(input_data)
     

    def read_data(self, file_path, file_type):
        data_to_load = pd.read_csv(file_path)
        data_to_load = self.normalize_headers(data_to_load) 
        types_to_convert = []
        for (key, value) in self._valid_file_structures[file_type].items():
            if value ==  int:
                types_to_convert.append(key)
        for data_type in types_to_convert:
            data_to_load[data_type] = pd.to_numeric(data_to_load[data_type], errors='coerce')
            data_to_load = data_to_load.dropna()
            data_to_load[data_type] = data_to_load[data_type].astype(int)
        return data_to_load 

    def normalize_headers(self, data_frame): 
        data_frame.columns = list(map(lambda x : x.replace('_','').replace(' ','').lower(), list(data_frame.columns.values)))
        return data_frame

    def is_file(self, file_path):
        if local.path(file_path).is_file():
            pass
        else:
            print("Failed to find file path at ... {0}".format(datetime.now()))
            err_message = "{0} is not a file, exiting".format(file_path)
            raise TypeError(err_message)

    def is_csv(self, file_path):
        if local.path(file_path).suffix != '.csv':
            print("Failure: not a csv file at ... {0}".format(datetime.now()))
            err_message = 'Invalid file format for {0}, must be a csv file, exiting'.format(file_path)
            raise TypeError(err_message)

    def is_valid_file_type(self, file_type, file_types, file_structure, file_path): 
        if file_type not in file_types:
            print("Failed to match valid data input types at ... {0}".format(datetime.now()))
            err_message = 'Invalid file input type "{0}", exiting'.format(file_type)
            raise TypeError(err_message)
        data_to_load = self.normalize_headers(pd.read_csv(file_path))
        headers = list(data_to_load.columns)
       # headers = list(pd.read_csv(file_path).columns)
        if list(file_structure[file_type].keys()) != headers:
            print("Failed to match valid proper csv data structure  at ... {0}".format(datetime.now()))
            err_message = 'Invalid file structure at "{0}", exiting'.format(file_path)
            raise TypeError(err_message)
    def main(self):
        pass

if __name__=='__main__':
    CollaboratorDotNet.run()
