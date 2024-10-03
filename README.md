# Natural Language-to-SQL Project

### Overview
This project integrates a PostgreSQL database with OpenAI's GPT to generate SQL queries from natural language prompts. It evaluates different GPT prompting strategies, such as zero-shot and double-shot learning (taken from this paper https://arxiv.org/pdf/2305.11853), and logs results to JSON files.

The Song Recommendation database stores and manages data related to users, artists, songs, listening history, and song recommendations. It can be queried to analyze user interactions and trends with their listening habits and preferences.

### File Descriptions
- **promptDB.py:** contains the core logic for connecting to the database, executing SQL queries, and integrating GPT to generate SQL based on user questions. It implements multiple prompting strategies like zero-shot and few-shot

- **main.py:** loads configurations, sets up the database, and orchestrates the process of generating, executing, and analyzing GPT-generated SQL queries

- **setup.sql and setupData.sql:** these scripts create the structure for the database and populates database with initial data, which is used for testing GPT's SQL query generation

- **response_zero_shot.json:** Contains the results of running GPT's zero-shot strategy, where SQL is generated based on questions without prior examples. It includes generated SQL queries, results, and errors.

- **response_few_shot.json:** Stores the output of the few-shot strategy, where GPT is given examples before generating SQL. It compares performance to the zero-shot approach with queries, results, and explanations.

- **schema.jpg:** ERD diagram of the initial database schema for reference

- **sample_questions.md**: Contains sample questions that both performed well and didn't. Also includes a discussion of the different strategies used.