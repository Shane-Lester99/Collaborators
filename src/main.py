from plumbum import (cli, local)
from datetime import datetime
import pandas as pd



class CollaboratorDotNet(cli.Application):
    #_read_data = cli.SwitchAttr(
    #    ['--input-data', , mandatory=False, argtype=cli.ExistingFile, 
    #    help="
    #)

    _valid_file_types = ('skill', 'project', 'organization', 'interest', 'distance', 'user')

    _valid_file_structures = {
        'skill': ['User_Id', 'Skill ', 'Skill level']
    }

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
        if file_structure[file_type] != headers:
            print("Failed to match valid proper csv data structure  at ... {0}".format(datetime.now()))
            err_message = 'Invalid file structure at "{0}", exiting'.format(file_path)
            raise TypeError(err_message)

if __name__=='__main__':
    CollaboratorDotNet.run()
