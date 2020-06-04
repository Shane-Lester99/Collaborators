# Six Degrees Of Separation

This command-line tool processes structured social media data. When the data is separated into people, skills, interests, and organizational groups, it can be run through a pipeline designed to process and structure its relationships for queries and analytics. Once the data is in the proper structure (which is discussed in "How to insert data on each load in `instructions.md`), it can be pulled, stored, and analyzed through the data pipeline for insight.

Currently, the commands are basic explanation queries,  like "what kind of relationship does this person have with other entities"), and two more advanced queries. One gives recommendations, like who to reach out to in their network or what skills/ groups to join, and the other is a list of the most trustworthy people in their network based on the degree of connection and other similarities. The algorithms are simple to understand and are both explained in `instructions.md`.

## System Architecture

The interface is a Python command-line tool. It has a similar feel to other Unix tools because of the library Plumbum, which makes it simple to use flags and outputs recognizable structured information similar to all other Unix tools.

Python is used for data processing where the relationship structure of the entities is formed and commands are processed for analysis. The end output for storage commands and the input for queries/ analytics are two databases, Neo4j and MongoDB. Neo4j allows for fast storage and queries on graphs. MongoDB's flexible data structure allows for each entity to store textual data for analysis and extend the structure when necessary.

## Current state of the project

All of the core logic is implemented, but richer queries involving more advanced analytics would be nice. A descriptive statistics interface would make for a much richer experience, especially if they involve a natural language processing library like Textblob. 

The major limitation of this application is the missing software layer to process social media data down into CSV files for input into the pipeline. However, with NLP libraries like Textblob, it should be somewhat straightforward to implement that layer.

Also, some of the input information is not as developed as it should be. For example, the distance is a number from 1-10 when it should be miles or something more intuitive. It was built that way to implement all the core logic rapidly.

Additionally, it could use a frontend. The command-line interface isn't as accessible and a "click and drag" interface would be much easier to use for most people.

No major updates have been made since May 2019.
