import json
from openai import OpenAI
import os
import psycopg2
from time import time


PROMPT_SQL_ZERO_SHOT = "Give me a Postgres select statement that answers the question. Only respond with Postgres SQL syntax."
QUESTIONS = [
        "What songs should I listen to based on my favorite genres?",
        "What are the top-rated songs by john_doe?",
        "Which users have rated more than 3 songs?",
        "What is the average rating for songs in the Jazz genre?",
        "What are the most popular songs by total ratings?",
        "Which users have the highest average rating?"
    ]

########################    
### helper functions ###
########################
    
fdir = os.path.dirname(__file__)
def get_path(fname):
    return os.path.join(fdir, fname)


def get_config_file(path):
    configPath = get_path(path)
    with open(configPath) as file:
        config = json.loan(file)

    return config 


def connect_to_db(url):
    pg_conn = psycopg2.connect(url)
    pg_cursor = pg_conn.cursor()

    return pg_conn, pg_cursor


def create_openai_client(api_key, orgId):
    openai_client = OpenAI(
        api_key=api_key,
        organization=orgId
    )

    return openai_client


def run_sql_file(cursor, filepath):
    with open(filepath, 'r') as file:
        sql = file.read()
        cursor.execute(sql)


def run_sql_query(cursor, query):
    cursor.execute(query)
    result = cursor.fetchall()
    return result


def get_chat_response(client, content):
    stream = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{"role": "user", "content": content}],
        stream=True,
    )

    response_list = []
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            response_list.append(chunk.choices[0].delta.content)

    result = "".join(response_list)
    return result


def sql_setup(conn, cursor):
    setup_sql_path = get_path("setup.sql")
    setup_sql_data_path = get_path("setupData.sql")

    print("Setting up Song Rec Tables...")
    run_sql_file(cursor, setup_sql_path)

    print("Inserting Data into Song Rec Tables...")
    run_sql_file(cursor, setup_sql_data_path)

    conn.commit()


def sanitize_sql(value):
    gptStartSqlMarker = "```sql"
    gptEndSqlMarker = "```"
    if gptStartSqlMarker in value:
        value = value.split(gptStartSqlMarker)[1]
    if gptEndSqlMarker in value:
        value = value.split(gptEndSqlMarker)[0]
    return value


def implement_prompt_strategy(client, cursor):
    strategies = {"zero_shot": PROMPT_SQL_ZERO_SHOT}

    for strategy in strategies:
        responses = {"strategy": strategy, "prompt_prefix": strategies[strategy]}
        questionResults = []
        for question in QUESTIONS:
            print("Asking question:", question)
            error = "None"
            try:
                # sql response from chat
                sqlSyntaxResponse = get_chat_response(client, strategies[strategy] + " " + question)
                sqlSyntaxResponse = sanitize_sql(sqlSyntaxResponse)
                print("Generated SQL:", sqlSyntaxResponse)

                # run generated query on database
                queryRawResponse = str(run_sql_query(cursor, sqlSyntaxResponse))
                print("Query Result:", queryRawResponse)

                # get friendly response for query result
                friendlyResultsPrompt = f"I asked the question '{question}' and the result was '{queryRawResponse}'. Please provide a concise and friendly explanation."
                friendlyResponse = get_chat_response(client, friendlyResultsPrompt)
                print("Friendly Response:", friendlyResponse)

            except Exception as err:
                error = str(err)
                print(f"Error: {err}")

            questionResults.append({
                "question": question, 
                "sql": sqlSyntaxResponse, 
                "queryRawResponse": queryRawResponse,
                "friendlyResponse": friendlyResponse,
                "error": error
            })

        # save results for each strat
        responses["questionResults"] = questionResults
        with open(get_path(f"response_{strategy}_{time()}.json"), "w") as outFile:
            json.dump(responses, outFile, indent=2)
    


#####################
### main function ###
#####################
def main():
    print(f"Starting promptDB script...")

    config_file = get_config_file("config.json")
    conn, cursor = connect_to_db(config_file["dbServiceUrl"])

    sql_setup(conn, cursor)

    client = create_openai_client(config_file["openaiKey"], config_file["orgId"])
    implement_prompt_strategy(client, cursor)

    cursor.close()
    conn.close()
    print("PromptDB script finished.")


if __name__ == "__main__":
    main()
