from plumbum import (cli, local)
from datetime import datetime
from collections import OrderedDict
import pandas as pd
import yaml


class CollaboratorDotNet(cli.Application):
    # Types of acceptable files at command line
    _valid_file_types = ('skill', 'project', 'organization', 'interest', 'distance', 'user')
    # Structure of csv columns
    _valid_file_structures = {
            _valid_file_types[0] : OrderedDict({'User_Id': int, 'Skill ': str, 'Skill level': int}),
            _valid_file_types[1] : OrderedDict({'User_id': int, 'Project': str}),
            _valid_file_types[2] : OrderedDict({'User_id': int, 'organization': str, 'organization type': str}),
            _valid_file_types[3] : OrderedDict({'User_id': int, 'Interest': str, 'Interest level': int}),
            _valid_file_types[4] : OrderedDict({"Organization 1": str, "Organization 2": str, "Distance": int}),
            _valid_file_types[5] : OrderedDict({'User_id': int, 'First name': str, 'Last name': str})
    }

    @cli.switch(['-m', '--input-many'], str)
    def input_many_data(self, file_path_to_yaml):
        """ Input a list of csv files to input input_data """
        yaml_file = None
        with open(file_path_to_yaml) as raw_config_file:
            try:
                yaml_file  = yaml.load(raw_config_file, yaml.FullLoader)
            except yaml.YAMLError as err:
                raise err
        for i in yaml_file['load_all_data']:
            self.input_data(i)
        

    # will input a file named file_name that is input data of file_type
    @cli.switch(['-i', '--input'], str)
    def input_data(self, file_path_and_type):
        """ Input data, enter a string of form file_type,file_path  """
        file_path, file_type = file_path_and_type.split(',')
        print('Check if input is valid at ... {0}'.format(datetime.now()))
        # Error validation
        self.is_file(file_path)
        self.is_csv(file_path)
        self.is_valid_file_type(file_type, self._valid_file_types, self._valid_file_structures, file_path)
        print('Input validated at ... {0}\n'.format(datetime.now()))
        print('Attempting to read data from {0} at ... {1}'.format(file_path, datetime.now())) 
        input_data = self.read_data(file_path, file_type)
        print('Data read and cleaned at ... {0}'.format(datetime.now()))
        print(input_data)
        print()
        # TODO: Load the data according to the appropriate file
    def read_data(self, file_path, file_type):
        data_to_load = pd.read_csv(file_path)
        #print(data_to_load, data_to_load.dtypes)
        #print()
        #for (key, value) in self._valid_file_structures[file_type].items():
        #    print(data_to_load[key].astype(value))
        types_to_convert = []
        for (key, value) in self._valid_file_structures[file_type].items():
            if value ==  int:
                types_to_convert.append(key)
        for data_type in types_to_convert:
            data_to_load[data_type] = pd.to_numeric(data_to_load[data_type], errors='coerce')
            data_to_load = data_to_load.dropna()
            data_to_load[data_type] = data_to_load[data_type].astype(int)
        return data_to_load

    def main(self):
        #print('Command line application starting...')
        pass

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
        headers = list(pd.read_csv(file_path).columns)
        if list(file_structure[file_type].keys()) != headers:
            print("Failed to match valid proper csv data structure  at ... {0}".format(datetime.now()))
            err_message = 'Invalid file structure at "{0}", exiting'.format(file_path)
            raise TypeError(err_message)

if __name__=='__main__':
    CollaboratorDotNet.run()
