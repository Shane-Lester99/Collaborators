import sys

class MongoDbSchema(object):
    def look_up(self, table_name, key):
        if isinstance(key, str):
            key = key.lower()
        if table_name == 'user':
            try:
                key = int(key)
            except ValueError as err:
                raise err
            return { self.User.key : key }

        elif table_name == 'project':
            return { self.Project.key : str(key) }

        elif table_name == 'skill':
            return { self.Skill.key : str(key) }

        elif table_name == 'interest':
            return {self.Interest.key : str(key) }

        elif table_name == 'organization':
            return { self.Organization.key :  str(key) }
        else:
            print('Table does not exist. Mongo schema error. Exiting.')
            sys.exit(1)

    all_table_names = ('user', 'project', 'skill', 'interest', 'organization')
    class User(object):
        _first_name = None
        _last_name = None
        _user_id = None
        _description = None
        key = 'userid'
        table_name = 'user'
        def __init__(self, first_name, last_name, user_id, description):
            self._first_name = first_name
            self._last_name = last_name
            self._user_id = user_id
            self._description = description
        def _make_usable(self):
            if not all(self._first_name, self._last_name, self._user_id):
                return False
            if not self._description():
                self._description = 'Fill in text here describing yourself'
            return True
        def create_new_user_doc(self):
            if self._make_usable:
                user_doc = {
                    'userid': self._user_id,
                    'firstname': self._first_name,
                    'lastname': self._last_name,
                    'description' : self._description 
                }
                return user_doc
            print('User document not usable. Mongo schema error. Exiting')
            sys.exit(1)
        def update_document(self, description):
            self._description = str(description)
    class Skill(object):
        _skill_name = None
        _description = None
        table_name = 'skill'
        key = 'skill'
        def __init__(self, name, description):
            self._skill_name = name
            self._description = description
        def _make_usable(self):
            if not self._skill_name:
                return False
            if not self._description:
                self._description = 'Fill in information about this skill'
            return True
        def create_new_skill_doc(self):
            if self._make_usable():
                skill_doc = {
                    'skill': self._skill_name.lower(),
                    'description': self._description
                }
                return skill_doc
            print('Skill document not usable. Mongo schema error. Exiting.')
            sys.exit(1)
        def update_document(self, description):
            self._description = str(description)
    class Interest(object):
        _interest_name = None
        _description = None
        table_name = 'interest'
        key = 'interest'
        def __init__(self, name, description):
            self._interest_name = name
            self._description = description
        def _make_usable(self):
            if not self._interest_name:
                return False
            if not self._description:
                self._description = 'Fill in information about this interest'
            return True
        def create_new_interest_doc(self):
            if self._make_usable():
                interest_doc = {
                    'interest': self._interest_name.lower(),
                    'description': self._description
                }
                return interest_doc
            print('Interest document not usable. Mongo schema error. Exiting.')
            sys.exit(1)
        def update_document(self, description):
            self._description = str(description)
    class Project(object):
        _project_name = None
        _description = None
        table_name = 'project'
        key = 'project'
        def __init__(self, name, description):
            self._project_name = name
            self._description = description
        def _make_usable(self):
            if not self._project_name:
                return False
            if not self._description:
                self._description = 'Fill in information about this project'
            return True
        def create_new_project_doc(self):
            if self._make_usable():
                project_doc = {
                    'project': self._project_name.lower(),
                    'description': self._description
                }
                return project_doc
            print('Project document not usable. Mongo schema error. Exiting.')
            sys.exit(1)
        def update_document(self, description):
            self._description = str(description)
    class Organization(object):
        _organization_name = None
        _sector = None
        _description = None
        table_name = 'organization'
        key = 'organization'
        def __init__(self, name, sector, description):
            self._organization_name = name
            self._sector = sector
            self._description = description
        def _make_usable(self): 
            if not all([self._organization_name, self._sector]): 
                return False
            if not self._description:
                self._description = 'Fill in information about this organization'
            return True
        def create_new_organization_doc(self):
            if self._make_usable():
                organization_doc = {
                    'organization': self._organization_name.lower(),
                    'sector': self._sector,
                    'description': self._description
                }
                return organization_doc
            print('Organization document not usable. Mongo schema error. Exiting.')
            sys.exit(1)
        def update_document(self, description):
            self._description = str(description)
