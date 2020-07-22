#画像処理関連のCog

from discord.ext import commands # Bot Commands Frameworkのインポート
from base64 import b64encode
import discord
import datetime
import requests
import urllib.error
import urllib.request
import json

API_KEY = "******************"
ENDPOINT_URL = 'https://vision.googleapis.com/v1/images:annotate'

# コグとして用いるクラスを定義。
class Image(commands.Cog):

    # Listenerクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot
   
    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。
    @commands.command()
    async def ocr(self, ctx):
        if not ctx.message.attachments:
                await ctx.send(ctx.author.name + 'さん：文字検出したい画像を添付してYo')
                return
        
        #画像ファイルの取得と構造化
        img_url = ctx.message.attachments[0].url
        img_requests = []

        # ヘッダーをFireFoxに偽装して正常にアクセス可能にする
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"
        }
        request = urllib.request.Request(img_url, headers=headers)
        attached_data = urllib.request.urlopen(request).read()
        ctxt = b64encode(attached_data).decode()
        img_requests.append({
                'image': {'content': ctxt},
                'features': [{
                    'type': 'TEXT_DETECTION',
                    'maxResults': 1
                }]
        })
        
        #CloudVision APIによる文字検出
        response = requests.post(ENDPOINT_URL,
                            data=json.dumps({"requests": img_requests}).encode(),
                            params={'key': API_KEY},
                            headers={'Content-Type': 'application/json'})
        if response.status_code != 200 or response.json().get('error'):
            await  ctx.send(response.text)
        else:
            str = ""
            embed = discord.Embed(title="文章検出(OCR)", description="", color=0x00ffff)
            for idx, resp in enumerate(response.json()['responses']):
                str = str + "\n" + resp['textAnnotations'][0]['description']
            embed.add_field(name ="結果" ,value=str)    
            await ctx.send(embed=embed)
    
    @commands.command(name='label_detection', aliases=['ld'])
    async def label_detection(self, ctx):
        if not ctx.message.attachments:
                await ctx.send(ctx.author.name + 'さん：文字検出したい画像を添付してYo')
                return
        
        #画像ファイルの取得と構造化
        img_url = ctx.message.attachments[0].url
        img_requests = []

        # ヘッダーをFireFoxに偽装して正常にアクセス可能にする
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"
        }
        request = urllib.request.Request(img_url, headers=headers)
        attached_data = urllib.request.urlopen(request).read()
        ctxt = b64encode(attached_data).decode()
        img_requests.append({
                'image': {'content': ctxt},
                'features': [{
                    'type': 'LABEL_DETECTION',
                    'maxResults': 10
                }]
        })

        #CloudVision APIによる文字検出
        response = requests.post(ENDPOINT_URL,
                            data=json.dumps({"requests": img_requests}).encode(),
                            params={'key': API_KEY},
                            headers={'Content-Type': 'application/json'})
        if response.status_code != 200 or response.json().get('error'):
            await  ctx.send(response.text)
        else:
            str = ""
            embed = discord.Embed(title="物体検出(Label detection)", description="", color=0x00ffff)
            for idx, resp in enumerate(response.json()['responses']):
                for index in range(len(resp['labelAnnotations'])):
                    str = str + "\n" + resp['labelAnnotations'][index]['description']
            embed.add_field(name ="結果" ,value=str)    
            await ctx.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        elif message.attachments:
             #画像ファイルの取得と構造化
            img_url = message.attachments[0].url
            img_requests = []

            # ヘッダーをFireFoxに偽装して正常にアクセス可能にする
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"
            }
            request = urllib.request.Request(img_url, headers=headers)
            attached_data = urllib.request.urlopen(request).read()
            ctxt = b64encode(attached_data).decode()
            img_requests.append({
                    'image': {'content': ctxt},
                    'features': [{
                        'type': 'LABEL_DETECTION',
                        'maxResults': 10
                    }]
            })

            #CloudVision APIによる文字検出
            response = requests.post(ENDPOINT_URL,
                                data=json.dumps({"requests": img_requests}).encode(),
                                params={'key': API_KEY},
                                headers={'Content-Type': 'application/json'})
            if response.status_code != 200 or response.json().get('error'):
                await  message.channel.send(response.text)
            else:
                desc_list = []
                for idx, resp in enumerate(response.json()['responses']):
                    for index in range(len(resp['labelAnnotations'])):
                        desc_list.append(resp['labelAnnotations'][index]['description'])

                if ('Screenshot' in desc_list or 'Screen' in desc_list) and 'Games' in desc_list:
                    reply = message.author.name + "さん、ナイスリザルトだYo！"
                    return await message.channel.send(reply)
                elif 'Green tea' in desc_list or 'Hojicha' in desc_list or 'Oolong' in desc_list or 'Gyokuro' in desc_list or 'Sencha' in desc_list:
                    reply = message.author.name + "さんからお茶の差し入れです( ^^) _旦~~"
                    return await message.channel.send(reply)
                elif 'Frozen dessert' in desc_list or 'Ice cream' in desc_list:
                    reply = "僕を殺すきか？"
                    return await message.channel.send(reply)
                elif 'Dessert' in desc_list or 'Gelato' in desc_list:
                    reply = "甘いものを上手に摂取することは、脳の活性化につながるYo！\nつまり地力アップ！！！"
                    return await message.channel.send(reply)
                elif 'Kabayaki' in desc_list or 'Unagi' in desc_list or 'Unadon' in desc_list:
                    reply = "うなぎ食ってんじゃねーYo！"
                    return await message.channel.send(reply)
                elif 'Karaage' in desc_list:
                    reply = "からあげ食べて、鳥は乗りましたか？？？"
                    return await message.channel.send(reply)
                elif 'Ramen' in desc_list:
                    reply = "ラーメン食べて地力アップ！！！"
                    return await message.channel.send(reply)
                elif 'Steak' in desc_list or 'Meat' in desc_list:
                    reply = "肉🍖ニクニ国苦肉🍖"
                    return await message.channel.send(reply)
                elif 'Sushi' in desc_list:
                    reply = "🍣🍣🍣🍣🍣へいお待ち！"
                    return await message.channel.send(reply)


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Image(bot)) # ImageにBotを渡してインスタンス化し、Botにコグとして登録する。
