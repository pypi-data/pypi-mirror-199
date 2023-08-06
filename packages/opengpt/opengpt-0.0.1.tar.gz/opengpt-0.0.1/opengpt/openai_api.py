import openai
import os

def ask_openai(prompt, config):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    message = None

    try:
        response = openai.ChatCompletion.create(
            model = config.openai.model,
            messages = [
                {"role": "user", "content": prompt},
            ]
        )

        message = None
        if response['choices'][0]['finish_reason'] == 'stop':
            message = response['choices'][0]['message']['content']
    except Exception as e:
        print(e)
        print("An example failed, it will be skipped. You can re-run the script and the missed examples will be tried again.")

    return message