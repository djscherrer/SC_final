import time
import concurrent.futures
from resources import clients
from importlib import reload
from openai import OpenAI
from concurrent.futures import as_completed
import re
import numpy as np

keys = clients.api_keys

gpt_clients = [OpenAI(api_key=key) for key in keys]

def is_valid_response(response):
    # Define all required fields with their regex patterns
    required_fields = {
        'Originality': r'Originality:? (\d+)',
        'Method': r'Method:? (\d+)',
        'Credibility': r'Credibility:? (\d+)',
        'Understandability': r'Understandability:? (\d+)',
        'Relevance': r'Relevance:? (\d+)',
        'Quality of Citations': r'Quality of Citations:? (\d+)',
        'Linguistic style and soundness of grammar': r'Linguistic style and soundness of grammar:? (\d+)',
        'Overall score': r'Overall score:? (\d+\.?\d*)',
    }
    
    # Check each field in the response
    for field, pattern in required_fields.items():
        if not re.search(pattern, response):
            print(f"Field {field} not found in response")
            return False
    return True



def prompt_gpt(prompt, title, uni, client):
    attempts = 0
    while attempts < 2:
        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="gpt-3.5-turbo"
            )
            time.sleep(5)
            response = chat_completion.choices[0].message.content
            if not is_valid_response(response):
                raise ValueError("Invalid response")
            return response
        except Exception as e:
            print(f"Error with generating answer for title {title} and uni {uni} with client {client}: {e}")
            if attempts == 0:
                time.sleep(10)
            else:
                time.sleep(30)
            attempts += 1
    return f"Failed to generate answer for title: {title} and university: {uni}"



def generate_judgments(rows):
    reload(clients)
    print(f"Generating answers for {len(rows)} prompts")
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(gpt_clients)) as executor:
        # Initial submission of all prompts
        futures = {executor.submit(prompt_gpt, row['rating_prompt'], row['title'], row['university_association'], gpt_clients[i % len(gpt_clients)]): i for i, row in rows.iterrows()}
        
        # Handling completed tasks and re-executing if necessary
        for future in as_completed(futures):
            index = futures[future]
            try:
                rows.loc[index, "rating_answer"] = future.result()
            except Exception as e:
                print(f"Error with future {index}: {e}")
                rows.loc[index, "rating_answer"] = np.nan  # Set response to np.nan if all attempts fail
    print(f"Generated answers for {len(rows)} prompts")