#特定のメッセージに反応するコグ

from discord.ext import commands # Bot Commands Frameworkのインポート
import discord
import datetime

# コグとして用いるクラスを定義。
class Listener(commands.Cog):

    # Listenerクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        if '水素水' in message.content:
            return await message.channel.send(file=discord.File('./data/picture/suisosui.jpg'))
        
        elif '勝てません' in message.content or 'かてません' in message.content or '負けました' in message.content or 'まけました' in message.content:
            await message.channel.send(file=discord.File('./data/picture/honda_make_1.png'))
            return await message.channel.send(file=discord.File('./data/picture/honda_make_2.png'))

        elif '何すかコレ' in message.content or 'なんすかコレ' in message.content or '何すかこれ' in message.content or 'なんすかこれ' in message.content:
            await message.channel.send(file=discord.File('./data/picture/Critical Crystal.png'))
            reply = """「何スカコレ」ト言ワレテモ、ソレガ、クリティカルクリスタル。"""
            return await message.channel.send(reply)
        
        elif 'そう！' in message.content or 'ソウ！' in message.content:
            return await message.channel.send(file=discord.File('./data/picture/EDEN.jpg'))
        
        elif 'やったぜ' in message.content:
            now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
            reply = "投稿者：変態糞" + message.author.name + " " + now.strftime("(%m月%d日 (%a) %H時%M分%S秒)")
            return await message.channel.send(reply)
        
        

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Listener(bot)) # ListenerにBotを渡してインスタンス化し、Botにコグとして登録する。