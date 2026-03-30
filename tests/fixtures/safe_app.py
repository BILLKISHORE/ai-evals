# Test fixture: safe AI application code
# This demonstrates proper patterns that should NOT trigger scanner findings

import openai

# Safe: user input only in user role
def chat_safe(user_input):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_input},
    ]
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=messages,
        max_tokens=1000,
    )
    return response.choices[0].message.content

# Safe: output used as text only
def display_response(prompt):
    response = chat_safe(prompt)
    print(response)  # textContent equivalent
