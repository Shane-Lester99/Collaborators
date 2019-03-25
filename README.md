# Collaboraters


## About

Welcome to collaborator. A command line tool to store and query professional
social networking information. This app is in its infancy but is designed and 
built to read in large amounts of data regarding users, projects, organizations
(government, university, or companies), skills, and interests. It can then 
retrieve information and store new information based on each entitiy above. 
It is used at the command line to read, write, store, and query data about 
professionals. Please read the arcitecture page and the rest of this
document for how to use it. Also note this app is currently in its proof of concept, 
and is in its very early stages of development

## How to use/ All Queries:
Make sure to navigate to src directory then execute one of the commands below

## Help Menu:

Will display help menu and all the commands and what they do. Will also display the name of the app and the version number.
`$> python collaborator.py -h` 

Will tell a bit of information about the app
`$>python collaborator.py —about`

Will display the version number
`$> python collaborator.py -v`


### Loading data:
There are two options to download data, one is by a yaml file and the other is to input one file given a file path and file name


This will load all the data from all the file paths in yaml file. To see the correct format, look at how the file structure is formed in mock-data and how the load_all_data.yaml file is configured. It should be self evident
`$> python collaborator.py -m mock-data/load_all_data.yaml`

Also we can load from certain areas of the yaml file with the `-y` switch. By default it loads from load_all_data part of the yaml file. The -y switch is not mandatory. Check the load_all_data.yaml file to see example configuration
`$> python collaborator.py -y user_data_only -m mock-data/load_all_data.yaml `

This one must be of form file_path,file_type. Valid file types are user, skill, project, organization, and interest. Also notice that the yaml file just specifies multiple file paths for data
`$> python collaborator.py -o mock-data/user.csv,user`


### Deletes
Currently the only deletes supported are all the data
`$> python collaborator.py -d`

### Updates
You can update project user, organization, skill, and interest entities as much as you want as long as you don’t modify read only properties. That is the properties that are written when loading data can’t be modified. This allows for complete customization of each entity, while also preserving the integrity of the data.
`$> python collaborator.py -u project,p1`

### Queries

Can query all of any type of entity. That is we can get all the read only properties for user, project, organization, skill, and interest
`$>python collaborator.py -a skill`

Can query more information about a specific entity given its key. Users key are user_id while all other entities are queried by there names (as in project is queried with p1)
`$>python collaborator.py -s user,1`
`
#### Can make two more advanced queries:

##### Recommend People to meet:
Can recommend a specific user to meet by if they share similar interests/ skills and if they work either in the same organization or work within 10 miles of each other. They are then given a weighted score to see who is most strongly recommended. The weighted score is based on a sum of there skills weighted by the original user. Here is an example
Say a User 1 has skills s1 and s2 and interest i1 given a weight 4,6,7 respectively.
Say User 2 has i1 in common at a weight of 10 and user 3 has s1, s2, and i1 at a weight of 1 each. If we run this query for user 1 then user 2 will have a collective score of  7 * 10 = 70 and user 3 of 1 * 4 + 1 * 6 + 1* 7 = 31. So user 2 will be recommended above user 3. Below is how we run this query with user with id 1

`$> python collaborator.py -r 1`

##### Find trusted colleagues:

Can find all the users to a particular user that have at least one shared interest or skill and have worked on the same project. Also note that a command prompt will come up to write if want to query trusted colleagues based on interests or skills. Below is to run the query with user with id 1

`$> python collaborator.py -t 1`

## How to insert data on each load

The format of data to insert at each node is important to make the application work correctly. It can take in data in csv files. The name of the csv file doesn’t matter, but they must have the suffix `.csv` to load.  Also, as shown in the ‘how to use’ section of this README, what type of entity is specified at each load or in the yaml configuration file

Data for different entities is represented in this format. Note that characters, ‘_’, ‘ ‘, any whitespace, and uppercase are all acceptable in column names. So the column name “__ user _ id ” == “userid”. 

user.csv
```
Userid,firstname,lastname
1,F1,L1
2,F2,L2
```
skill.csv (skill level must be from 1 - 10)
```
Userid, skill, skill level
1,s1,10
1,s2,7
2,S3,5
3,S2,10
```
interest.csv (interest level must be from 1 - 10)
```
Userid, interest, interest level
1,s1,10
1,s2,7
2,S3,5
3,S2,10
```
organization.csv (org type must only be U,C, or G)
```
Userid, organization, organizationtype
1,O1,U
2,O2,C
3,O3,G
```
distance.csv:
```
Organization1,organization2,distance
O1,O2,8.3
O2,O3,9
```
Project.csv
```
User_id,Project
1,P1
1,P2
3,P2
```

Also note that all data can be loaded in from a yaml file. To do this match the format in the file load_all_data.yaml and follow the query directions in the ‘how to run’ section

## How to specify database connection information

From root directory, go to `/config/db.yaml` file

In this file fill in the correct information to connect to neo4j and mongodb. Whatever information you place in here will form the uri string for connection. For more information on how to connect, please look at there own documentation. 

## Potential Improvements: - Heavy coupling between collaborator.py file and db_service.py
	- This makes it hard to iterate on and test. The project started with clear separation of roles, but it got blurred as I got further into the project
- Unit and integration tests
    - Never implemented, should be implemented
- Delete specific nodes/ documents
    - Currently can only delete all the data, would like to be able to delete specific nodes
- Cant remove fields in update entity command
    - Currently can only append to mongo documents or update a field. Cant remove a non read only field. 
- Cant specify any data type but strings when updating documents
    - Would like to be able to specify more complex data types on update commands
