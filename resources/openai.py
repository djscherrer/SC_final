from openai import OpenAI

client = OpenAI(
    api_key="sk-proj-bPS780Pz5xszPidKyKDAT3BlbkFJBq6lBmV3DwWr9MmlFNl0" # API key David: Use with love and care, han nume no so 4 bucks
)

def generate_answer(prompt):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )

    print(chat_completion)

    return chat_completion.choices[0].message.content