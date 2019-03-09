# File to enforce strict schema for neo4j. Neo4j will
# only be accessed via helper methods so the schema
# can not be corrupted with strange data

from datetime import datetime

#from py2neo import Graph

# constants for entity types
user = ("User", "user_name")
organization = ("Organization", "organization_name")
project = ("Project", "project_name")
skill = ("Skill", "skill_name")
interest = ("Interest", "interest_name")

# constants for labels:
friendship = ("is_friends_with", "added_on")


#graph = Graph()

# Getter methods for nodes

def find_node(label, node_name):
    # TODO: Would like a reason for failure here
    node_type = None
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
    query = "MATCH (u: {0} {{ {1} : '{2}' }} ) RETURN u".format(node_type[0], node_type[1], node_name )
    return query;

# Create methods for nodes

def create_node(label, node_name):
    # TODO: Would like a boolean here indicating whether it was successful or not
    node_type = None
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
        errorMessage = "Incorrect label used when trying to create node: {0} with name: {1}".format(label, node_name)
        raise ValueError(errorMessage)
    query = "MERGE (u: {0} {{ {1} : '{2}' }} ) RETURN u".format(node_type[0], node_type[1], node_name )
    return query

# Delete methods for nodes


def delete_node(label, node_name):
    # TODO: Would like a boolean here indicating whether it was successful or not and give info back
    node_type = None
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
    # TODO: Would like a boolean here indicating whether it was created and returning the nodes/ rel
    query = """MATCH (u1: {0} {{ {1}: '{2}' }}), (u2: {0} {{ {1}: '{3}' }})
                MERGE(u1) - [ :{4} {{ {5} : '{6}' }}] -> (u2)
                MERGE (u1) <- [:{4} {{ {5}: '{6}' }}] - (u2)
                RETURN u1, u2""".format(user[0], user[1], user1, user2, friendship[0], friendship[1], str(datetime.now()) )
    return query

def delete_friendship(user1, user2):
    # TODO: Would like some indication of what happened to caller returned here
    query = """MATCH (u1: {0} {{ {1}: '{2}' }}) -[f: {4}] - (u2: {0} {{ {1}: '{3}' }} )
                DELETE f""".format(user[0], user[1], user1, user2, friendship[0] )
    return query



if __name__ == '__main__':
    print(create_friendship('Jessica', 'Amanda'))
    print(delete_friendship('Jessica','Amanda'))

   # print("New method")
    #print(delete_node("User", "Shane"))
    #print(delete_node("Skill", "Cloud Computing"))
   # print(delete_node("Interest", "Bird Watching"))
   # print(delete_node("Project", "Expansion_DB"))
   # print(delete_node("Organization", "Bloomberg"))
