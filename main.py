# make an API request to openai
from openai import OpenAI
from dotenv import load_dotenv
import os
from mydb import run_query, get_schema

load_dotenv()
my_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=my_key)

schema = get_schema('orders')

while True:
        user_input = input("Ask your question: ")
        if user_input.lower() == 'exit':
            break

        final_prompt = f'''
                Generate a MS SQL Server SQL based on the below schema
                {schema}
                Question : {user_input}

                Provide limit your respose to SQL Only
                '''
        #print(final_prompt)
        response = client.responses.create(model='gpt-5.6-sol',
                                input = final_prompt)


        query = response.output_text
        print(query)
        result = run_query(query)
        print(result)



