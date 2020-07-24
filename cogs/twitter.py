#特定のメッセージに反応するコグ

from discord.ext import commands, tasks # Bot Commands Frameworkのインポート
import discord
import datetime
from asyncio import sleep
import oauth2
import json
import pprint
import datetime
import asyncio

# Twitter APIのキーとトークン
API_KEY='******************************'
API_SECRET='******************************'
TOKEN_KEY=='******************************'
TOKEN_SECRET=='******************************'

# チャンネルID
CHANNEL_ID_TEST = [******************,******************]
CHANNEL_ID_NEWS = [******************,******************]

# コグとして用いるクラスを定義。
class Twitter(commands.Cog):

    # Twitterクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot
        self.check_tweet.start()

    @tasks.loop(seconds=60.0)
    async def check_tweet(self):
        def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):
            consumer = oauth2.Consumer(key=API_KEY, secret=API_SECRET)
            token = oauth2.Token(key=key, secret=secret)
            client_oauth = oauth2.Client(consumer, token)
            resp, content = client_oauth.request( url, method=http_method, body=post_body.encode('utf-8'), headers=http_headers )
            return content

        with open('./data/timeline_history.json') as f:
           df = json.load(f)
        dt_last_id = df['IIDX_OFFICIAL']
        url='https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=IIDX_OFFICIAL&count=10&include_rts=true&since_id=' + dt_last_id

        tl_data=oauth_req(url, TOKEN_KEY, TOKEN_SECRET)
        timelines=json.loads(tl_data)

        if timelines:
            for line in reversed(timelines):
                channel_list = CHANNEL_ID_NEWS
                for ch in channel_list:
                    try:
                        channel = self.bot.get_channel(int(ch))
                        dt_now = datetime.datetime.now()
                        await channel.send("https://twitter.com/IIDX_OFFICIAL/status/" + str(line['id']))
                        print(str(dt_now) + "sent to " + channel.guild.name + ":https://twitter.com/IIDX_OFFICIAL/status/" + str(line['id']))
                        await sleep(0.5)                        
                    except Exception as e:
                        print("error:", e, flush=True)
            df['IIDX_OFFICIAL'] = str(timelines[0]['id'])
            with open('./data/timeline_history.json','w') as f:
                json.dump(df,f)
        else:
            dt_now = datetime.datetime.now()
            print(str(dt_now) + ":新着ツイートなし")

    #テスト用の関数（未使用）
    @tasks.loop(seconds=10.0)
    async def check_test(self):
        channel_list = CHANNEL_ID_TEST
        for ch in channel_list:
            try:
                channel = self.bot.get_channel(int(ch))
                await channel.send("message")
                print("sent to", channel.guild.name, flush=True)
                await sleep(0.4)
            except Exception as e:
                print("error:", e, flush=True)


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Twitter(bot)) # TwitterにBotを渡してインスタンス化し、Botにコグとして登録する。
