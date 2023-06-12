from openai import OpenAI, Configuration
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
import azure.functions as func
import json

openaiClient = OpenAI(
    Configuration(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_path=os.getenv("OPENAI_API_URL") + os.getenv("OPENAI_API_MODEL"),
        base_options={
            'headers': {'api-key': os.getenv("OPENAI_API_KEY")},
            'params': {
                'api-version': '2023-03-15-preview'
            }
        }
    )
)

slackClient = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))
GPT_BOT_USER_ID = os.getenv("GPT_BOT_USER_ID")
CHAT_GPT_SYSTEM_PROMPT = os.getenv("CHAT_GPT_SYSTEM_PROMPT")
GPT_THREAD_MAX_COUNT = int(os.getenv("GPT_THREAD_MAX_COUNT"))

async def postMessage(channel, text, threadTs, context):
    try:
        response = slackClient.chat_postMessage(
            channel=channel,
            text=text,
            thread_ts=threadTs
        )
        context.log(text)
    except SlackApiError as e:
        context.log.error(f"Error posting message: {e.response['error']}")

async def createCompletion(messages, context):
    try:
        response = openaiClient.create_chat_completion(
            messages=messages,
            max_tokens=800,
            temperature=0.7,
            frequency_penalty=0,
            presence_penalty=0,
            top_p=0.95,
        )
        return response.choices[0].message.content
    except Exception as e:
        context.log.error(e)
        return str(e)

async def main(context: func.Context, req: func.HttpRequest):
    # Ignore retry requests
    if "x-slack-retry-num" in req.headers:
        context.log("Ignoring Retry request: " + req.headers["x-slack-retry-num"])
        context.log(req.get_body().decode())
        return func.HttpResponse(
            body="No need to resend",
            status_code=200,
        )

    # Response slack challenge requests
    body = json.loads(req.get_body().decode())
    if "challenge" in body:
        context.log("Challenge: " + body["challenge"])
        return func.HttpResponse(
            body=body["challenge"],
            status_code=200,
            mimetype="text/plain"
        )

    # ...

    # The rest of your function goes here.

    return func.HttpResponse(
        body="OK",
        status_code=200
    )
