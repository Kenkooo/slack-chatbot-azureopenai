import os
import slack_sdk
import openai
from flask import Flask, request, Response
from slack_sdk.web import WebClient
from slack_sdk.signature import SignatureVerifier

app = Flask(__name__)

slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
openai_api_key = os.environ.get("OPENAI_API_KEY")
openai_api_url = os.environ.get("OPENAI_API_URL")
openai_api_model = os.environ.get("OPENAI_API_MODEL")
gpt_bot_user_id = os.environ.get("GPT_BOT_USER_ID")
chat_gpt_system_prompt = os.environ.get("CHAT_GPT_SYSTEM_PROMPT")
gpt_thread_max_count = int(os.environ.get("GPT_THREAD_MAX_COUNT"))

slack_client = WebClient(token=slack_bot_token)
openai.api_key = openai_api_key
openai.api_base = openai_api_url

def post_message(channel, text, thread_ts):
    slack_client.chat_postMessage(channel=channel, text=text, thread_ts=thread_ts)
    print(text)

def create_completion(messages):
    try:
        response = openai.ChatCompletion.create(
          model=openai_api_model,
          messages=messages,
          max_tokens=800,
          temperature=0.7,
          frequency_penalty=0,
          presence_penalty=0,
          top_p=0.95,
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        print(f"Error: {e}")
        return str(e)

@app.route('/slack/events', methods=['POST'])
def slack_events():
    request_body = request.get_data(as_text=True)
    print(request_body)
    if not SignatureVerifier(os.environ.get("SLACK_SIGNING_SECRET")).is_valid_body(request_body, request.headers):
        return Response(status=401)

    event = request.json['event']
    thread_ts = event.get('thread_ts', event.get('ts'))
    if event.get('type') == 'app_mention':
        user_text = event.get('text', '')
        messages = [
            {"role": "system", "content": chat_gpt_system_prompt},
            {"role": "user", "content": user_text},
        ]
        completion = create_completion(messages)
        post_message(event['channel'], completion, thread_ts)
    return Response(status=200)
