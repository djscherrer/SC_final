from openai import OpenAI

client = OpenAI(
    api_key="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" # API key David: Love with love and care, han nume no so 4 bucks
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