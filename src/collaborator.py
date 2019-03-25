from plumbum import (cli, local)
from datetime import datetime
from collections import OrderedDict
import pandas as pd
import yaml
import os
import sys
sys.path.append(os.path.join(local.path(__file__).dirname, 'db'))

from db.db_service import DbService
class Collaborator(cli.Application):
    PROGNAME = "Collaborator"
    VERSION = "1.0"
    DESCRIPTION = "This is a command line tool to store and query professional social networking information."
    # ********************************* read interface ********************************************

    # Types of acceptable files at command line (friend not implemented)
    _valid_file_types = ('skill', 'project', 'organization', 'interest', 'distance', 'user', 'friend')
    # Structure of csv columns 
    _valid_file_structures = {
            _valid_file_types[0] : OrderedDict({'userid': int, 'skill': str, 'skilllevel': int}),
            _valid_file_types[1] : OrderedDict({'userid': int, 'project': str}),
            _valid_file_types[2] : OrderedDict({'userid': int, 'organization': str, 'organizationtype': str}),
            _valid_file_types[3] : OrderedDict({'userid': int, 'interest': str, 'interestlevel': int}),
            _valid_file_types[4] : OrderedDict({"organization1": str, "organization2": str, "distance": int}),
            _valid_file_types[5] : OrderedDict({'userid': int, 'firstname': str, 'lastname': str}),
            # Not implemented
            _valid_file_types[6] : OrderedDict({'userid1': int, 'userid2':int})
    } 

    _yaml_option = cli.SwitchAttr(
        ['-y', '--yaml-file'], mandatory=False, default='load_all_data',
        help='In the yaml file specified at path from --input-many switch, can specify which attribue of yaml file you want to download. load_all_data is used by default. Must be used before the --input-many switch to work.'
    )

    _db_service = None

    def connect_to_db(self):
        if not self._db_service:
            print('Connecting to databases at ... {0}\n'.format(datetime.now()))
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
        for i in yaml_file[self._yaml_option]:
            self.input_data(i)
        print('All data loaded at ... {0}'.format(datetime.now()))
        
    # will input a file named file_name that is input data of file_type
   
    @cli.switch(['-o', '--input-one'], str)
    def input_data(self, file_path_and_type):
        """         
        Input data, enter a string of form file_type,file_path  
        """
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
        if list(file_structure[file_type].keys()) != headers: 
            print("Failed to match valid proper csv data structure  at ... {0}".format(datetime.now()))
            err_message = 'Invalid file structure at "{0}", exiting'.format(file_path)
            raise TypeError(err_message)

    @cli.switch(['-d', '--delete-all-data'])
    def delete_all_data(self):
        """
        deletes all data in both databases. Warning provided before deletion.
        """
        self.connect_to_db()
        self._db_service.delete_all_data()

    @cli.switch(['-u','--update-specific-entity' ], str)
    def update_entity(self, raw_info_string):
        """
        Updates documents based on project, user, skill, interest, or organization.
        Can store any type of information, but it cannot modify read only properties.
        Read only properties are the ones that were read in on entity creation from the
        dataset provided. Input is of form entity-type,key
        """
        self.connect_to_db()
        label, key = raw_info_string.split(',')
        if label not in ('user', 'project', 'skill', 'interest', 'organization'):
            print('Label {0} not found. Exiting'.format(label))
            sys.exit(1)
        if label == 'user':
            try:
                key = int(key)
            except ValueError as err:
                raise err
        self._db_service.update_specific_info(label, key)

    #******************* read interface: *********************************
    @cli.switch(["--about"])
    def about(self):
        """    
        A little bit of information about collaborator 
        """
        print()
        print("Welcome to collaborator. A command line tool to store and query professional")
        print("social networking information. Please read the README.md document attached for details")
        print("on how to use the application.")
        print()
     
    @cli.switch(['-a', '--get-all'], str)
    def get_all_of_node_type(self, node_type):
        """ 
        Flag to retrieve nodes of a particular type. Valid input types are interest,
        skill, project, user, and organization. 
        Output will be all nodes of that type and there data outputted to terminal.
        """
        self.connect_to_db()
        print('Searching for data of type {0} at ... {1}\n'.format(node_type, datetime.now()))
        valid_node_types = self._valid_file_types[:4] + (self._valid_file_types[5],) 
        if node_type in (valid_node_types):
            self._db_service.get_all_of_node_type(node_type)
        else:
            print('Node type {0} is not a valid type.\nExiting at {1}'.format(node_type, datetime.now()))

    @cli.switch(['-s', '--get-specific-information'], str)
    def get_specific_information(self, raw_info_string):
        """
        This switch will allow retrieval of specific information based on the key of a node type.
        The input options are: (user,some_user_id_integer), (project,some_project_str), 
        (organization,some_org, (skill,some_skill_str) , (interest,some_interest_str).
        """
        self.connect_to_db()
        label, key = raw_info_string.split(',')
        if label not in ('user', 'project', 'skill', 'interest', 'organization'):
            print('Label {0} not found. Exiting'.format(label))
            sys.exit(1)
        if label == 'user':
            try:
                key = int(key)
            except ValueError as err:
                raise err
        print('Retrieving information about {0} with key {1} at ... {2}\n'.format(label, key, datetime.now()))
        info_list = self._db_service.get_specific_info(label, key)
        if info_list:
            print('Information found about {0} with key {1} at ... {2}\n'.format(label, key, datetime.now()))
            for node in info_list:
                print_value = ''
                for (key, value) in node.items():
                    if (key != '_id'):
                        print("\t" + key + ": " + str(value) + ";")
            print('\nInformation Retrieval finished at ... {0}\n'.format(datetime.now()))
        else:
            print('No information found about {0} with key {1}. at ... {2}'.format(label, key, datetime.now()))

    @cli.switch(['-t','--trusted-collegues'], int)
    def trusted_collegues(self, user_id):
        """
        Based off of network, this shows people who are trusted collegues of your collegues.
        These include people who have similar interests and have worked on the same projects
        """
        self.connect_to_db()
        raw_input_string = input('Please enter if you would like to match by skill or interest (s/i): ')
        while raw_input_string not in ('i', 's'):
            raw_input_string = input('Incorrect input. Please enter if you would like to match by skill or interest (s/i) : ')
        print()
        is_skill = False
        if raw_input_string == 's':
            is_skill = True
        print('Fetching trusted collegues of collegues at ... {0}'.format(datetime.now()))
        rec = list(self._db_service.get_trusted_c_of_c(user_id, is_skill))
        if not rec:
            print('Fetch retrieved no results at ... {0}.\nExiting'.format(datetime.now()))
            sys.exit(0)        
        rec = [dict(i) for i in rec] 
        print('Fetch retrieved at ... {0}\n'.format(datetime.now()))
        for result in rec:
            #main_user, other_user, role, project, level, interest = result
            main_user = dict(result['main_user'])
            other_user = dict(result['other_users'])
            role = dict(result['role'])
            project = dict(result['projects'])
            level = dict(result['level'])
            i_or_s = None
            if is_skill:
                i_or_s = dict(result['skills'])
            else:
                i_or_s = dict(result['interests'])
            print('\tUser {0} with id {1} is recommended to trust {2} with id {3}'
                    .format(' '.join([main_user['first_name'], main_user['last_name']]),
                        main_user['user_id'],
                        ' '.join([other_user['first_name'], other_user['last_name']]),
                        other_user['user_id']))
            print('\tThis is based on both working on project {0} and having similar',
                  '{1} {2}'.format(project['project_name'], 'skill' if is_skill else 'interest',
                  i_or_s.get('skill_name') if is_skill else i_or_s.get('interest_name')))
            print()
        print('Retrieved and outputted at ... {0}.\nExiting'.format(datetime.now()))

    @cli.switch(['-r', '--rec-to-meet'], int)
    def people_on_path_of(self, user_id):
        """
        Based off of network, recommends people you may have met or that you may want to meet.
        It bases it off of similar interest or skills, and people who either work at the same
        company or work at a company within a close distance (under 10 miles)
        """
        self.connect_to_db()
        print('Looking for recommendations for user {0} at ... {1}'.format(user_id, datetime.now()))
        #retrieve_recommendations
        rec_list = list(self._db_service.retrieve_recommendations(user_id))
        print('Fetch finished at ... {0}'.format(datetime.now()))
        print('Sorting recommendation at .. {0}'.format(datetime.now()))
        sorted_rec_dict = OrderedDict()
        for rec in rec_list:
            items = list(rec) 
            for i in range(0, len(items), 1): 
                if items[i]: 
                    items[i] = dict(items[i])
                else: 
                    items[i] = None
            main_user, interest_skill, other_user, organization_of_main, dist, organization_of_other, i_lvl_1, i_lvl_2  = items
            main_user_info = None
            if not sorted_rec_dict.get('main_user'):
                 main_user_info = (main_user['first_name'] + ' ' + main_user['last_name'], main_user['user_id'])
            if not dist:
                if not organization_of_main['organization_name'] == organization_of_other['organization_name']:
                    continue
            skill_or_interest_prop = None 
            if i_lvl_1.get('skill_level'):
                skill_or_interest_prop = 'skill_level'
            else:
                skill_or_interest_prop = 'interest_level'
            if sorted_rec_dict.get(other_user['user_id']):
                sorted_rec_dict[other_user['user_id']][0] += i_lvl_1[skill_or_interest_prop] * i_lvl_2[skill_or_interest_prop]
                sorted_rec_dict[other_user['user_id']][5].append(interest_skill[skill_or_interest_prop.replace('level', 'name')])
            else:
                sorted_rec_dict[other_user['user_id']] = [
                                                      i_lvl_1[skill_or_interest_prop] * i_lvl_2[skill_or_interest_prop],
                                                      (other_user['first_name'] + ' ' + other_user['last_name'], other_user['user_id']), 
                                                      organization_of_main['organization_name'],
                                                      organization_of_other['organization_name'],
                                                      dist,
                                                      [interest_skill[skill_or_interest_prop.replace('level', 'name')]]
                                                      ]

        sorted_rec_dict = OrderedDict(sorted(sorted_rec_dict.items(), key= lambda x: x[1][0], reverse=True))   
        print('Finished sorting at ... {0}\n'.format(datetime.now()))
        print('Displaying results at ... {0}\n'.format(datetime.now()))
        for final_rec in sorted_rec_dict.values():
            print('\tWe recommend user {0} with id {1} to meet user {2} with id {3}'
                    .format(main_user_info[0], main_user_info[1],
                            final_rec[1][0], final_rec[1][1]))
            s_i_key = ('interest', 'interest_name')
            if 'skill_name' in interest_skill:
                s_i_key = ('skill', 'skill_name')
            print("\tThis is based on shared interest or skills {0} with collective weight {1}".format(', '.join(final_rec[5]), final_rec[0])) 
            if final_rec[4]:
                print("\tThis is based on organization {0} and {1} being only {2} miles apart"
                        .format(final_rec[2], final_rec[3], final_rec[4]['distance']))
            else:
                print("\tThis is based on both people working at {0}".format(final_rec[2]))
            print()
        print('Recommendation finished at ... {0}'.format(datetime.now()))

    def main(self):
        pass

if __name__=='__main__':
    Collaborator.run()
