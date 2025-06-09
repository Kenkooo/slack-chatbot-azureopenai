import os
import json
from azure.functions import HttpRequest, HttpResponse
import azure.functions as func
from slack_sdk import WebClient
from slack_sdk.signature import SignatureVerifier

# Slackのトークンと署名の秘密鍵を環境変数から取得
slack_bot_token = os.getenv("SLACK_BOT_TOKEN")
signing_secret = os.getenv("SLACK_SIGNING_SECRET")

slack_client = WebClient(token=slack_bot_token)
signature_verifier = SignatureVerifier(signing_secret)

def main(req: HttpRequest) -> HttpResponse:
    # Slackからのリクエストが正しい署名を持っていることを検証
    if not signature_verifier.is_valid_request(req.get_body(), req.headers):
        return func.HttpResponse(status_code=401)

    payload = json.loads(req.get_body())
    
    # メンションイベントが発生したときにメッセージを送る
    if "event" in payload and payload["event"]["type"] == "app_mention":
        channel_id = payload["event"]["channel"]
        slack_client.chat_postMessage(channel=channel_id, text="こんにちは。")

    return func.HttpResponse(status_code=200)
