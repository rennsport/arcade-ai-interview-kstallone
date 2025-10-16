"""
Summarize user actions using LangChain and OpenAI.

Included agentic and non-agentic options. Non-agentic chain seems to perform better.
LangChain csv agent is still experimental.
"""

import os
from dotenv import load_dotenv

from arcade_flow_analyzer.analysis.csv_preprocessor import preprocess_csv

from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.llm import LLMChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document

load_dotenv()

BASE_PROMPT = """You are an AI assistant that summarizes user actions in detail
from a CSV file. The CSV file now has columns including 'action_description'
to help you understand the user's journey. Your task is to provide a clear,
step-by-step list of the user's journey. No need to include time stamps or other metadata."""


def summarize_actions(force_regenerate=False, agent=False):
    if not os.getenv('OPENAI_API_KEY'):
        print("Please create a .env file with: 'OPENAI_API_KEY=your_api_key_here'")
        return

    # Preprocess the CSV
    input_csv = 'cache/actions.csv'
    processed_csv = 'cache/processed_actions.csv'
    
    # Separate cache files for agentic vs non-agentic approaches
    if agent:
        summary_cache = 'cache/ai-summary-agentic.txt'
    else:
        steps_cache = 'cache/ai-steps-chain.txt'
        summary_cache = 'cache/ai-summary-chain.txt'

    if not os.path.exists(input_csv):
        print(f"CSV file not found: {input_csv}")
        return

    preprocess_csv(input_csv, processed_csv)
    approach = "Agentic" if agent else "Chain"

    # Check for cached files
    if agent:
        if not force_regenerate and os.path.exists(summary_cache):
            print(f"Using cached AI summary ({approach} approach):")
            with open(summary_cache, 'r') as f:
                cached_summary = f.read()
            print("=" * 60)
            print(cached_summary)
            print("=" * 60)
            return
    else:
        if not force_regenerate and os.path.exists(steps_cache) and os.path.exists(summary_cache):
            print(f"Using cached AI analysis ({approach} approach):")
            with open(steps_cache, 'r') as f:
                cached_steps = f.read()
            with open(summary_cache, 'r') as f:
                cached_summary = f.read()
            print("=" * 60)
            print("STEPS:")
            print(cached_steps)
            print("\nSUMMARY:")
            print(cached_summary)
            print("=" * 60)
            return

    llm = ChatOpenAI(temperature=0.60)

    if agent:
        # LangChain agent
        print("Generating new AI summary (Agentic approach):")

        agent_executer = create_csv_agent(
            llm, processed_csv, verbose=True,
            allow_dangerous_code=True,
            handle_parsing_errors=True
        )

        result = agent_executer.invoke(BASE_PROMPT)

        print(result)

    else:
        print("Generating new AI summary (Chain approach):")
        loader = CSVLoader(file_path=processed_csv)
        docs = loader.load()

        # First chain: Generate steps
        steps_prompt = ChatPromptTemplate.from_messages([
            ("system", f"{BASE_PROMPT} Here is the data:\n\n{{context}}")
        ])
        steps_chain = create_stuff_documents_chain(llm, steps_prompt)
        steps_result = steps_chain.invoke({"context": docs})

        # Second chain: Generate summary from steps
        # Convert steps_result to a document for the second chain
        steps_doc = Document(page_content=str(steps_result))
        
        summary_prompt = ChatPromptTemplate.from_messages([
            ("system", "Based on the following step-by-step list of user actions, "
             "provide a clear narrative summary of the user's journey. The steps are in order and should be summarized in a way that is easy to understand and follow:\n\n{context}")
        ])
        
        summary_chain = create_stuff_documents_chain(llm, summary_prompt)
        summary_result = summary_chain.invoke({"context": [steps_doc]})

        print("=" * 60)
        print("STEPS:")
        print(steps_result)
        print("\nSUMMARY:")
        print(summary_result)
        print("=" * 60)

    # Save the result to cache
    if agent:
        with open(summary_cache, 'w') as f:
            f.write(str(result))
        print(f"Summary saved to {summary_cache} ({approach} approach)")
    else:
        with open(steps_cache, 'w') as f:
            f.write(str(steps_result))
        with open(summary_cache, 'w') as f:
            f.write(str(summary_result))
        print(f"Steps saved to {steps_cache} ({approach} approach)")
        print(f"Summary saved to {summary_cache} ({approach} approach)")


if __name__ == "__main__":
    summarize_actions()
