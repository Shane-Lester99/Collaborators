# File to enforce strict schema for neo4j. Neo4j will
# only be accessed via helper methods so the schema
# can not be corrupted with strange data

from datetime import datetime
import sys 
import os
from plumbum import local
#sys.path.append('./..')
#from db_service import DbService


# TODO: Connect to neo4j
# TODO: Add some sort of statuses and return values for each query to give feedback of how the query went
# TODO: Seperate schema from query functions

#from py2neo import Graph

# constants for entity types
user = ("user", "userid", "firstname", "lastname")
# TODO: VERY IMPORTANT: need to only allow three organizations (G, C, U)
organization = ("Organization", "organization_name")
project = ("Project", "project_name")
skill = ("skill", "skill")
interest = ("Interest", "interest_name")

# constants for labels:
friendship_rel = ("is_friends_with", "added_on")
skill_rel = ("is_skilled_at","skill_level")
interest_rel = ("is_interested_in","interest_level")
project_rel = ("works_on", "role")
organization_rel = ("works_for", "address", "location")
organization_to_project_rel = ("owns","priority")

# Getter methods for nodes
def find_node(label, node_name):
    # TODO: Would like a reason for failure here
    node_type = None
    if isinstance(node_name, str):
        node_name = ' '.join(node_name.lower().split())
    if label is user[0]:
        node_type = user
    elif label is skill[0]:
        node_type = skill
    elif label is interest[0]:
        node_type = interest
    elif label is organization[0]:
        node_type = organization
    elif label is project[0]:
        node_type = project
    else:
        errorMessage = "Incorrect label used when trying to find node type: {0} with name: {1}".format(label, node_name)
        raise ValueError(errorMessage)
    if node_type[0] == 'user':         
        query = "MATCH (u: {0} {{ {1} : {2} }} ) RETURN u".format(node_type[0], node_type[1], node_name )
    else:
        query = "MATCH (u: {0} {{ {1} : '{2}' }} ) RETURN u".format(node_type[0], node_type[1], node_name )
    return query;

# Create methods for nodes

def create_node(label, node_data):
    # TODO: Would like a boolean here indicating whether it was successful or not
    node_type = None 
    for i in range(0,len(node_data),1):
        if type(node_data[i]) == str:
            node_data[i] = ' '.join(node_data[i].lower().split())
    if label is user[0]:
        node_type = user
    elif label is skill[0]:
        node_type = skill
    elif label is interest[0]:
        node_type = interest
    elif label is organization[0]:
        node_type = organization
    elif label is project[0]:
        node_type = project
    else:
        errorMessage = "Incorrect label used when trying to create node: {0} with data: {1}".format(label, node_data)
        raise ValueError(errorMessage)
    if node_type[0] == 'user': 
        query = """MERGE (u: {0} {{ {1} : {4} }})
            ON CREATE SET u.{1} = {4}
            ON CREATE SET u.{2} ='{5}'
            ON CREATE SET u.{3}  ='{6}'
            RETURN u""".format(node_type[0], node_type[1], node_type[2], node_type[3], node_data[0], node_data[1], node_data[2] )
    else: 
        query = "MERGE (u: {0} {{ {1} : '{2}' }} ) RETURN u".format(node_type[0], node_type[1], node_data[0]  )
    return query

# Delete methods for nodes


def delete_node(label, node_name):
    # TODO: Would like a boolean here indicating whether it was successful or not and give info back
    node_type = None
    node_name = ' '.join(node_name.lower().split())
    if label is user[0]:
        node_type = user
    elif label is skill[0]:
        node_type = skill
    elif label is interest[0]:
        node_type = interest
    elif label is organization[0]:
        node_type = organization
    elif label is project[0]:
        node_type = project
    else:
        errorMessage = "Incorrect label used when trying to delete node: {0} with name: {1}".format(label, node_name)
        raise ValueError(errorMessage)
    query = "MATCH (u: {0}) WHERE  u.{1} = '{2}' DETACH DELETE u".format(node_type[0], node_type[1], node_name );
    return query

# Methods for relationships

# Friendships between users
def create_friendship(user1, user2):
    user1 = ' '.join(user1.lower().split())
    user2 = ' '.join(user2.lower().split())
    # TODO: Would like a boolean here indicating whether it was created and returning the nodes/ rel
    query = """MATCH (u1: {0} {{ {1}: '{2}' }}), (u2: {0} {{ {1}: '{3}' }})
                MERGE(u1) - [ :{4} {{ {5} : '{6}' }}] -> (u2)
                MERGE (u1) <- [:{4} {{ {5}: '{6}' }}] - (u2)
                RETURN u1, u2""".format(user[0], user[1], user1, user2, friendship_rel[0], friendship_rel[1], str(datetime.now()) )
    return query

def delete_friendship(user1, user2):
    user1 = ' '.join(user1.lower().split())
    user2 = ' '.join(user2.lower().split())
    # TODO: Would like some indication of what happened to caller returned here
    query = """MATCH (u1: {0} {{ {1}: '{2}' }}) -[f: {4}] - (u2: {0} {{ {1}: '{3}' }} )
                DELETE f""".format(user[0], user[1], user1, user2, friendship_rel[0] )
    return query


def add_associated_skill(user_id, skill_name, skill_level):  
    skill_name = ' '.join(skill_name.lower().split()) 
    if not 1 <= skill_level <= 10:
        return
    query = """MATCH (u1: {0} {{ {1} : {4} }}), (u2: {2}  {{ {3} : '{5}' }})
                MERGE(u1) - [s : {6} {{ {7} : {8} }}] -> (u2)
                RETURN u1, s,  u2""".format(user[0], user[1], skill[0], skill[1], user_id, skill_name, skill_rel[0], skill_rel[1], skill_level)
    return query


def match_associated_skill(user_id, skill_name): 
    skill_name = ' '.join(skill_name.lower().split())
    # TODO: Would like some indication of what happened to caller returned here
    query = """MATCH (u1: {0} {{ {1}: {5} }}) -[v: {4}] - (u2: {2} {{ {3}: '{6}' }} )
                RETURN v""".format(user[0], user[1], skill[0], skill[1], skill_rel[0], user_id, skill_name )
    return query

def delete_associated_skill(user_name, skill_name):
    user_name = ' '.join(user_name.lower().split())
    skill_name = ' '.join(skill_name.lower().split())
    # TODO: Would like some indication of what happened to caller returned here
    query = """MATCH (u1: {0} {{ {1}: '{5}' }}) -[v: {4}] - (u2: {2} {{ {3}: '{6}' }} )
                DELETE v""".format(user[0], user[1], skill[0], skill[1], skill_rel[0], user_name, skill_name )
    return query


def add_associated_interest(user_name, interest_name, interest_level): 
    user_name = ' '.join(user_name.lower().split())
    interest_name = ' '.join(interest_name.lower().split()) 
    if not 1 <= interest_level <= 10:
        return
    query = """MATCH (u1: {0} {{ {1} : '{4}' }}), (u2: {2}  {{ {3} : '{5}' }})
                MERGE(u1) - [s : {6} {{ {7} : {8} }}] -> (u2)
                RETURN u1, s,  u2""".format(user[0], user[1], interest[0], interest[1], user_name, interest_name, interest_rel[0], interest_rel[1], interest_level)

    return query

def delete_associated_interest(user_name, interest_name):
    user_name = ' '.join(user_name.lower().split())
    interest_name = ' '.join(interest_name.lower().split())
    # TODO: Would like some indication of what happened to caller returned here
    query = """MATCH (u1: {0} {{ {1}: '{5}' }}) -[v: {4}] - (u2: {2} {{ {3}: '{6}' }} )
                DELETE v""".format(user[0], user[1], interest[0], interest[1], interest_rel[0], user_name, interest_name )
    return query


def add_to_project(user_name, project_name, role): 
    user_name = ' '.join(user_name.lower().split())
    project_name = ' '.join(project_name.lower().split()) 
    role = ' '.join(role.lower().split())    
    query = """MATCH (u1: {0} {{ {1} : '{4}' }}), (u2: {2}  {{ {3} : '{5}' }})
                MERGE(u1) - [s : {6} {{ {7} : '{8}' }}] -> (u2)
                RETURN u1, s,  u2""".format(user[0], user[1], project[0], project[1], user_name, project_name, project_rel[0], project_rel[1], role)
    return query

def delete_from_project(user_name, project_name):
    user_name = ' '.join(user_name.lower().split())
    project_name = ' '.join(project_name.lower().split())
    # TODO: Would like some indication of what happened to caller returned here
    query = """MATCH (u1: {0} {{ {1}: '{5}' }}) -[v: {4}] - (u2: {2} {{ {3}: '{6}' }} )
                DELETE v""".format(user[0], user[1], project[0], project[1], project_rel[0], user_name, project_name )
    return query

def add_project_to_organization(organization_name, project_name, priority): 
    project_name = ' '.join(project_name.lower().split())
    organization_name = ' '.join(organization_name.lower().split())
    if not 1 <= priority <= 10:
        return
    query = """MATCH (u1: {0} {{ {1} : '{6}' }}), 
                     (u2: {2} {{ {3}: '{7}' }})
                     MERGE (u1) - [o : {4} {{ {5}: {8} }}] -> (u2)
                     return u1, o, u2 """.format(organization[0], organization[1], project[0], project[1], organization_to_project_rel[0], organization_to_project_rel[1], organization_name, project_name, priority  )
    return query

def remove_project_from_organization(organization_name, project_name):
    project_name = ' '.join(project_name.lower().split())
    organization_name = ' '.join(organization_name.lower().split())
    query = """MATCH (u1: {0} {{ {1} : '{5}' }}) 
                - [o: {4} ] ->  
                (u2: {2} {{ {3}: '{6}' }})
                DELETE o""".format(user[0], user[1], project[0], project[1], organization_to_project_rel[0], organization_name, project_name )
    return query


if __name__ == '__main__':
    #print(create_friendship('Jessica', 'Amanda'))
    #print(delete_friendship('Jessica','Amanda'))

   # print("New method")
    #print(delete_node("User", "Shane"))
    print(create_node('user', [5,'Helena','Jacoba']))
    #print(create_node('User', 'Jessica Ambers'))
    #print(create_node("Skill", "Cloud Computing"))
    #print(create_node('Skill', "Programming"))
    #print(create_node('Skill', 'programming'))
    #print(create_node('Interest', 'Ping   pong'))
    #print(create_node('Project', "Project Sunshine"))
    #print(create_node('Organization', 'Red Cross' ))
    #print(create_node('Organization', 'Bloomberg'))
    #print(create_node('Project', 'Stock Widget'))
    #print(remove_project_from_organization('Bloomberg', 'Stock Widget'))
    #print(create_node('Organization', 'Apache'))
    #print(add_project_to_organization('Apache', 'Stock Widget', 7))
    #print(add_project_to_organization('Red Cross', 'Project Sunshine', 6))
    #print(add_project_to_organization('Bloomberg', 'Stock Widget', 3))
    #print(create_friendship('Jessica Ambers','shane lester  '))
    #print(delete_friendship('Jessica Ambers', 'Shane lester'))
   # print(add_associated_skill("Shane Lester", "programming ", 10))
   # print(delete_associated_skill("Shane Lester", "programming"))
  #  print(add_associated_interest("Shane Lester", "Ping Pong", 2))
  #  print(delete_associated_interest("Shane Lester", "Ping Pong"))
  #  print(add_to_project('Jessica Ambers', 'Project Sunshine', 'coordinator'))
  #  print(delete_from_project('Jessica Ambers', 'Project Sunshine'))

   # print(delete_node("Interest", "Bird Watching"))
   # print(delete_node("Project", "Expansion_DB"))
   # print(delete_node("Organization", "Bloomberg"))
