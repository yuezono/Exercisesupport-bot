from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,VideoSendMessage,ImageMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('tGKy95hAL8KYgrU0uAvwOdOK//02hmD6usLNg2ia8QZp6wm0XQqC6pdTLXwPK+5CG8NuKlJwdtxS5UjG+6TCG6ae18yt94x39BfrJ1p9fuUDXgHzdTP3aT03MHWiNXjfAPzdH3EygandYRU+fOvbDQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c6fe756b2202a9b409d98cf51935d592')

@app.route("/")
def test():
    return "hello"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        
        abort(400)

    return 'OK'

from time import time
import random
users = {}
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    userId = event.source.user_id
    movie_list = ["https://youtu.be/fuMOxAZOlLI","https://youtu.be/1fI8eAhd95k","https://youtu.be/qSsUM4Ffi70","https://youtu.be/G6zdi88y95w","https://youtu.be/qkAfmttfW3o","https://youtu.be/LdpVTj1t9M0","https://youtu.be/KxzZJwmB8qc","https://youtu.be/tMS7SWB0H8E"]
    movie_text = "本日のおすすめはこちらです。" + random.choice(movie_list)
    hagemashi = ["今日も体を動かしましょう！","応援しているよ！！","一緒に頑張ろう","負けないで！！"]
    if "開始" in event.message.text:
        replay = "運動を開始します。計測を開始しました。"
        if not userId in users:
            users[userId] = {}
            users[userId]["total"] = 0
        users[userId]["start"] = time()
    elif "終了" in event.message.text:
        end = time()
        difference = int(end - users[userId]["start"])
        users[userId]["total"] += difference
        #時間
        hour = difference // 3600
        minute = (difference % 3600) // 60
        second = difference % 60
        replay = f"本日の運動時間は{hour}時間{minute}分{second}秒です。お疲れ様でした。本日は合計で{users[userId]['total']}秒運動しています。"
    elif "筋トレ" in event.message.text:
        replay = movie_text
    # elif "動画" in event.message.text:
    #     video_message  =  VideoSendMessage(original_content_url=random.choice(movie_list[0]),preview_image_url='https://i2.wp.com/s3-ap-northeast-1.amazonaws.com/media.gamepedia/pokemon-kg/wp-content/uploads/2017/09/20110310/198.png?fit=475%2C475&ssl=1&resize=240%2C240')
    else:
        replay = random.choice(hagemashi)

    # if event.message.text == "動画":
    #     line_bot_api.reply_message(
    #         event.reply_token,video_message)
    line_bot_api.reply_message(
            event.reply_token,TextSendMessage(text=replay))



if __name__ == "__main__":
    app.run()


