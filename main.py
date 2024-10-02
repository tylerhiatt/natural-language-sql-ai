from promptDB import *


def main():
    print(f"Starting promptDB script...")

    try:
        config_file = get_config_file("config.json")
        conn, cursor = connect_to_db(config_file["dbServiceUrl"])

        sql_setup(conn, cursor)

        client = create_openai_client(config_file["openaiKey"])
        print("Successfully connected to OpenAI Client")
        implement_prompt_strategy(client, conn, cursor)

        cursor.close()
        conn.close()
        print("PromptDB script finished.")
    
    except Exception as e:
        print(f"Error: {e}")
        print("PromptDB script finished with error.")


if __name__ == "__main__":
    main()