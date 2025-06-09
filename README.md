# slack-chatbot-azureopenai

このリポジトリは、SlackのApp Mentionイベントに応答するチャットボットのサンプルコードです。Azure OpenAI Service を利用してメッセージを生成し、Flask アプリケーションとして動作します。

## ディレクトリ構成

- `__init__.py` - Flask を用いた Slack イベントハンドラー。`/slack/events` エンドポイントでメンションを受け取り、OpenAI の ChatCompletion API に投げて返信します。
- `csvconvert` - Pandas を使用した簡易 CSV 変換スクリプト。
- `test.py` - Azure Functions で動作する Slack ハンドラーのサンプル。

## 環境変数

Slack と OpenAI にアクセスするため、以下の環境変数を設定します。

- `SLACK_BOT_TOKEN` – Bot の OAuth Token
- `SLACK_SIGNING_SECRET` – Slack 署名検証用シークレット
- `OPENAI_API_KEY` – Azure OpenAI の API キー
- `OPENAI_API_URL` – API のエンドポイント URL
- `OPENAI_API_MODEL` – 利用するモデル名
- `GPT_BOT_USER_ID` – ボットユーザー ID
- `CHAT_GPT_SYSTEM_PROMPT` – システムプロンプト
- `GPT_THREAD_MAX_COUNT` – スレッド内メッセージの最大数

## ローカルでのクローン方法

```bash
git clone <repository_url>
cd slack-chatbot-azureopenai
```

## 開発環境の構築方法

1. Python 3.9 以降をインストールします。
2. 仮想環境を作成して必要なパッケージをインストールします。

```bash
python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install flask slack_sdk openai pandas azure-functions
```

## アプリケーションの起動例

環境変数を設定したうえで、以下のように実行できます。

```bash
python __init__.py
```

Flask サーバーが起動し、`/slack/events` で Slack からのリクエストを受け付けます。

