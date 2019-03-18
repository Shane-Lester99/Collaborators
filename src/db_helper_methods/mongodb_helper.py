class MongoDbSchema(object):
    class User(object):
        _first_name = None
        _last_name = None
        _user_id = None
        _description = None
        table_name = 'user'
        def __init__(self, first_name, last_name, user_id, description):
            self._first_name = first_name
            self._last_name = last_name
            self._user_id = user_id
            self._description = description
        def _make_usable(self):
            if not all(self._first_name, self._last_name, self._user_id):
                return False
            if not self._description:
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
            print('User document not usable. Error in code. Exiting')
            sys.exit(1)
    class Skill(object):
        _skill_name = None
        _description = None
        table_name = 'skill'
        def __init__(self, name, description):
            self._skill_name = name
            self._description = description
        def _make_usable(self):
            if not self._skill_name:
                return False
            if not self._description:
                self._description = 'Fill in information about this skill'
        def create_new_skill_doc(self):
            if self._make_usable:
                skill_doc = {
                    'skill': self._skill_name,
                    'description': self._description
                }
                return skill_doc
            print('Skill document not usable. Error in code. Exiting.')
            sys.exit(1)

