# File to enforce strict schema for neo4j. Neo4j will
# only be accessed via helper methods so the schema
# can not be corrupted with strange data

#from py2neo import Graph

# constants for entity types
user = ("User", "user_name")
organization = ("Organization", "organization_name")
project = ("Project", "project_name")
skill = ("Skill", "skill_name")
interest = ("Interest", "interest_name")


#graph = Graph()

# Getter methods for nodes

def find_node(label, node_name):
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
    query = "MATCH (u: {0}) WHERE  u.{1} = '{2}' DELETE u".format(node_type[0], node_type[1], node_name );
    return query

if __name__ == '__main__':
    #print(create_user("Shane"))
    #print(create_skill("Cloud Computing"))
   # print(create_interest("Bird Watching"))
   # print(create_project("Expansion_DB"))
   # print(create_organization("Bloomberg")) 
    #print(find_user("Shane"))
    print("New method")
    print(delete_node("User", "Shane"))
    print(delete_node("Skill", "Cloud Computing"))
    print(delete_node("Interest", "Bird Watching"))
    print(delete_node("Project", "Expansion_DB"))
    print(delete_node("Organization", "Bloomberg"))
    print("Old method")
    print(delete_user("Shane"))
    print(delete_skill("Cloud Computing"))
    print(delete_interest("Bird Watching"))
    print(delete_project("Expansion_DB"))
    print(delete_organization("Bloomberg"))
   # print(delete_user("Shane")) 
   # print(delete_skill("Cloud Computing"))
   # print(delete_interest("Bird Watching"))
   # print(delete_project("Expansion_DB"))
   # print(delete_organization("Bloomberg"))
