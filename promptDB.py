import json
from openai import OpenAI
import os
import psycopg2
from time import time


PROMPT_SQL_ZERO_SHOT = "Give me a Postgres select statement that answers the question. Only respond with Postgres SQL syntax."
PROMPT_SQL_DOUBLE_SHOT = (
                        "\nExample 1: Which user has rated the most songs?" + 
                        "\nSELECT user_id, COUNT(song_id) AS song_count FROM listeninghistory GROUP BY user_id ORDER BY song_count DESC LIMIT 1;\n\n" +
                        "Example 2: Which songs have been rated by more than one user?" + 
                        "\nSELECT song_id, COUNT(user_id) AS user_count FROM listeninghistory GROUP BY song_id HAVING user_count > 1;\n\n"
                        )
QUESTIONS = [
        "What is tony_stark's favorite genre of music?",  # easier questions
        "What are the top-rated songs by john_doe?",
        "Which users have rated 2 or more songs?",
        "What is the average rating for songs in the Jazz genre?",
        "What are the most popular songs by total ratings?",
        "Which artists have the highest average rating?",
        "Which users have rated songs by artists who debuted before 2000?",     # start harder questions
        "For each genre, what is the average rating and the number of users who rated at least one song?",
        "Which users have engaged with the most popular music?"
    ]

    
fdir = os.path.dirname(__file__)
def get_path(fname):
    return os.path.join(fdir, fname)


def get_config_file(path):
    configPath = get_path(path)
    with open(configPath) as file:
        config = json.load(file)

    return config 


def connect_to_db(url):
    pg_conn = psycopg2.connect(url)
    pg_cursor = pg_conn.cursor()

    return pg_conn, pg_cursor


def create_openai_client(api_key):
    openai_client = OpenAI(
        api_key=api_key
    )

    return openai_client


def run_sql_file(cursor, filepath):
    with open(filepath, 'r') as file:
        sql = file.read()
        cursor.execute(sql)


def run_sql_query(conn, cursor, query):
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"SQL Error: {e}")
        conn.rollback()  # Rollback transaction to clear error state
        raise


def get_chat_response(client, content):
    stream = client.chat.completions.create(
        model="gpt-4o-mini",
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


def load_sql_schema(filepath):
    with open(filepath, 'r') as file:
        schema = file.read()
    return schema


def implement_prompt_strategy(client, conn, cursor):
    schema_context = load_sql_schema("setup.sql")
    strategies = {  # try two dif strategies
        "zero_shot": schema_context + "\n\n" + PROMPT_SQL_ZERO_SHOT,
        "single_domain_double_shot": schema_context + "\n\n" + PROMPT_SQL_DOUBLE_SHOT
        }  

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
                queryRawResponse = str(run_sql_query(conn, cursor, sqlSyntaxResponse))
                print("Query Result:", queryRawResponse)

                # get friendly response for query result
                friendlyResultsPrompt = f"I asked the question '{question}' and the result was '{queryRawResponse}'. Please provide a concise and friendly explanation."
                friendlyResponse = get_chat_response(client, friendlyResultsPrompt)
                print(f"Friendly Response: {friendlyResponse}\n")

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
