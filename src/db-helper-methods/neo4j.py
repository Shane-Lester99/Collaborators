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

def find_user(user_name): 
    query = "MATCH (u: {0} {{ {1} : '{2}' }} ) RETURN u".format(user[0], user[1], user_name );
    return query;

def find_skill(skill_name): 
    query = "MATCH (u: {0} {{ {1} : '{2}' }} ) RETURN u".format(skill[0], skill[1], skill_name );
    return query;

def find_interest(interest_name): 
    query = "MATCH (u: {0} {{ {1} : '{2}' }} ) RETURN u".format(interest[0], interest[1], interest_name );
    return query;

def find_project(project_name): 
    query = "MATCH (u: {0} {{ {1} : '{2}' }} ) RETURN u".format(project[0], project[1], project_name );
    return query;

def find_organization(organization_name): 
    query = "MATCH (u: {0} {{ {1} : '{2}' }} ) RETURN u".format(organization[0], organization[1], organization_name );
    return query;

# Create methods for nodes

def create_user(user_name):
    query = "MERGE (u: {0} {{ {1} : '{2}' }} ) RETURN u".format(user[0], user[1], user_name );
    return query

def create_skill(skill_name):        
    query = "MERGE (u: {0} {{ {1} : '{2}' }} ) RETURN u".format(skill[0], skill[1], skill_name );
    return query

def create_interest(interest_name): 
    query = "MERGE (u: {0} {{ {1} : '{2}' }} ) RETURN u".format(interest[0], interest[1], interest_name );
    return query

def create_project(project_name): 
    query = "MERGE (u: {0} {{ {1} : '{2}' }} ) RETURN u".format(project[0], project[1], project_name );
    return query

def create_organization(organization_name):    
    query = "MERGE (u: {0} {{ {1} : '{2}' }} ) RETURN u".format(organization[0], organization[1], organization_name );
    return query

# Delete methods for nodes
def delete_user(user_name):
    query = "MATCH (u: {0}) WHERE  u.{1} = '{2}' DELETE u".format(user[0], user[1], user_name );
    return query

def delete_skill(skill_name):        
    query = "MATCH (u: {0}) WHERE  u.{1} = '{2}' DELETE u".format(skill[0], skill[1], skill_name );
    return query

def delete_interest(interest_name): 
    query = "MATCH (u: {0}) WHERE  u.{1} = '{2}' DELETE u".format(interest[0], interest[1], interest_name );
    return query

def delete_project(project_name): 
    query = "MATCH (u: {0}) WHERE  u.{1} = '{2}' DELETE u".format(project[0], project[1], project_name );
    return query

def delete_organization(organization_name):    
    query =  "MATCH (u: {0}) WHERE  u.{1} = '{2}' DELETE u".format(organization[0], organization[1], organization_name );
    return query

if __name__ == '__main__':
    print(create_user("Shane"))
    print(create_skill("Cloud Computing"))
    print(create_interest("Bird Watching"))
    print(create_project("Expansion_DB"))
    print(create_organization("Bloomberg")) 
    print(find_user("Shane"))
    print(find_skill("Cloud Computing"))
    print(find_interest("Bird Watching"))
    print(find_project("Expansion_DB"))
    print(find_organization("Bloomberg"))
    print(delete_user("Shane")) 
    print(delete_skill("Cloud Computing"))
    print(delete_interest("Bird Watching"))
    print(delete_project("Expansion_DB"))
    print(delete_organization("Bloomberg"))
