"""
Summarize user actions using LangChain and OpenAI.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from csv_preprocessor import preprocess_csv

load_dotenv()


def main():
    # Check if API key is available
    if not os.getenv('OPENAI_API_KEY'):
        print("Please create a .env file with: "
              "OPENAI_API_KEY=your_api_key_here")
        return

    # Preprocess the CSV
    input_csv = 'cache/actions.csv'
    processed_csv = 'cache/processed_actions.csv'

    if not os.path.exists(input_csv):
        print(f"CSV file not found: {input_csv}")
        return

    preprocess_csv(input_csv, processed_csv)


    llm = ChatOpenAI(temperature=0.75)
    agent_executer = create_csv_agent(llm, processed_csv, verbose=True, allow_dangerous_code=True, handle_parsing_errors=True)

    agent_executer.invoke("""You are an AI assistant that summarizes user actions in detail from a CSV file. The CSV file now has columns including 'action_description' to help you understand the user's journey. Your task is to provide a clear, step-by-step list of the user's journey. After the list, provide a summary of the user's journey in a narrative format.""")


if __name__ == "__main__":
    main()