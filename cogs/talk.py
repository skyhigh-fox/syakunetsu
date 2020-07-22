#灼熱botとの会話関係のコグ

from discord.ext import commands # Bot Commands Frameworkのインポート
from discord import Embed
import random
import discord

# コグとして用いるクラスを定義。
class Talk(commands.Cog):

    # Talkクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。
    @commands.command()
    async def yo(self, ctx):
        await ctx.send('Yo！' + ctx.author.name + 'さん')

    @commands.command()
    async def omikuji(self, ctx):
        # Embedを使ったメッセージ送信 と ランダムで要素を選択
        embed = discord.Embed(title="おみくじ", description=f"{ctx.author.mention}さんの今日の運勢は！",
                              color=0x2ECC69)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name="[運勢] ", value=random.choice(('大吉', '吉', '凶', '大凶')), inline=False)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def dice(self, ctx, *args):
        reply = ""
        if len(args) == 0: #引数がない場合、6面ダイスを一回だけ振る。
            dice_face = 6
            times = 1
            roll_result = random.randrange(dice_face) + 1
            reply = f"{dice_face}面ダイスを{times}回振りました。\n出目は{roll_result}だYO!"
        elif len(args) == 2: #指定した面数のダイスを指定した回数ロールする。
            if args[0].isdigit() == True and args[1].isdigit() == True:
                dice_face = int(args[0])
                times = int(args[1])
                roll_result = []
                for i in range(times):
                    roll_result.append(random.randrange(dice_face) + 1)
                reply = f"{dice_face}面ダイスを{times}回振りました。\n出目は{roll_result}だYO!"
            else:
                reply = "コマンドを正しく入力してください。\nコマンド：!dice [面数] [回数]\n例：!dice 2 3"
        else:
            reply = "コマンドを正しく入力してください。\nコマンド：!dice [面数] [回数]\n例：!dice 2 3"
        await ctx.send(reply)

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Talk(bot)) # TalkにBotを渡してインスタンス化し、Botにコグとして登録する。