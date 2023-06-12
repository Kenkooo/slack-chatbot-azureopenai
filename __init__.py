import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from openai import OpenAI, ChatCompletion, Configuration

# 環境変数から情報を取得
openai_api_key = os.getenv('OPENAI_API_KEY')
openai_api_url = os.getenv('OPENAI_API_URL')
openai_api_model = os.getenv('OPENAI_API_MODEL')
slack_bot_token = os.getenv('SLACK_BOT_TOKEN')
gpt_bot_user_id = os.getenv('GPT_BOT_USER_ID')
chat_gpt_system_prompt = os.getenv('CHAT_GPT_SYSTEM_PROMPT')
gpt_thread_max_count = int(os.getenv('GPT_THREAD_MAX_COUNT'))

# OpenAIクライアントの設定
openai_client = OpenAI(api_key=openai_api_key, api_base=openai_api_url + openai_api_model)

# Slackクライアントの設定
slack_client = WebClient(token=slack_bot_token)

def post_message(channel, text, thread_ts):
    try:
        slack_client.chat_postMessage(channel=channel, text=text, thread_ts=thread_ts)
    except SlackApiError as e:
        print(f"Error posting message: {e}")

def create_completion(messages):
    try:
        response = openai_client.chat_completions.create(
            model=openai_api_model,
            messages=messages,
            max_tokens=800,
            temperature=0.7,
            frequency_penalty=0,
            presence_penalty=0,
            top_p=0.95
        )
        return response.choices[0].message['content']
    except Exception as e:
        print(f"Error creating completion: {e}")
        return str(e)

def handle_request(context, req):
    if 'x-slack-retry-num' in req.headers:
        print(f"Ignoring Retry request: {req.headers['x-slack-retry-num']}")
        return {
            "statusCode": 200,
            "body": {"message": "No need to resend"}
        }
    
    body = eval(req.body)
    if 'challenge' in body:
        print(f"Challenge: {body['challenge']}")
        return {
            "body": body['challenge'],
        }

    # 以下の部分はAzure Functions特有の処理であり、Pythonでの適切な実装方法がないため省略しています。
    # 具体的な実装は、使用しているWebフレームワークや環境によります。

# Azure Functionsのエントリーポイント
def main(context, req):
    return handle_request(context, req)
