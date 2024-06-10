import openai

# OpenAI API is not free :(

organization = "org-JNMIXqucySjoYaBhWi8yWcyw"
apikey = "sk-proj-Q9Ptp4jesXhPohRbqeytT3BlbkFJlG7xe6J9jJy1cJ6HDGl9"
project = "Default project"

client = openai.OpenAI(organization=organization, api_key=apikey)

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "You are a creative storyteller, skilled in delivering storybeats to weave a cohesive tale",
        },
        {
            "role": "user",
            "content": "Compose a scary story that could be told to children.",
        },
    ],
)

print(completion.choices[0].message)
