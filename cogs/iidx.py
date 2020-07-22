#IIDXに関するコマンドに関するコグ

from discord.ext import commands # Bot Commands Frameworkのインポート
from discord import Embed
import discord
import pandas as pd
import random

# コグとして用いるクラスを定義。
class IIDX(commands.Cog):

    # IIDXクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。
    @commands.command()
    async def kadai(self, ctx, *args):
        #課題曲の検索
        if len(args) == 0: #引数がない場合、1曲だけランダムで選曲する
            df = pd.read_csv(filepath_or_buffer="./data/beatmania_musiclist.csv",encoding="utf_8",sep=",")
            row_number = random.randrange(len(df))
            embed = discord.Embed(title="課題曲", description="", color=0x00ffff)
            embed.add_field(name="バージョン", value=df.iat[row_number,0])
            embed.add_field(name="タイトル", value=df.iat[row_number,1])
            embed.add_field(name="ジャンル", value=df.iat[row_number,2])
            embed.add_field(name="アーティスト", value=df.iat[row_number,3])
            await ctx.send(embed=embed)
        elif len(args) == 1: #指定されたレベルの曲を1曲だけランダムで選曲する
            if args[0].isdigit() == True:
                df = pd.read_csv(filepath_or_buffer="./data/beatmania_musiclist.csv",encoding="utf_8",sep=",")
                df = df[(df['BEGINNER 難易度'] == int(args[0])) | (df['NORMAL 難易度'] == int(args[0])) | (df['HYPER 難易度'] == int(args[0])) | (df['ANOTHER 難易度'] == int(args[0])) | (df['LEGGENDARIA 難易度'] == int(args[0]))]
                row_number = random.randrange(len(df))
                embed = discord.Embed(title="課題曲", description="", color=0x00ffff)
                embed.add_field(name="バージョン", value=df.iat[row_number,0])
                embed.add_field(name="タイトル", value=df.iat[row_number,1])
                embed.add_field(name="ジャンル", value=df.iat[row_number,2])
                embed.add_field(name="アーティスト", value=df.iat[row_number,3])
                await ctx.send(embed=embed)
            else:
                await ctx.send("コマンドを正しく入力してください。\nコマンド：!kadai [難易度] [曲数] [バージョン(省略可)]\n例：!kadai 12 5") 
        elif len(args) == 2: #指定されたレベルの曲を指定した曲だけランダムで選曲する
            if args[0].isdigit() == True and args[1].isdigit() == True:
                df = pd.read_csv(filepath_or_buffer="./data/beatmania_musiclist.csv",encoding="utf_8",sep=",")
                df = df[(df['BEGINNER 難易度'] == int(args[0])) | (df['NORMAL 難易度'] == int(args[0])) | (df['HYPER 難易度'] == int(args[0])) | (df['ANOTHER 難易度'] == int(args[0])) | (df['LEGGENDARIA 難易度'] == int(args[0]))]
                reply = "ID    " + str(df.loc[:,["バージョン","タイトル"]].sample(n=int(args[1])))
                await ctx.send(reply)
            else:
                await ctx.send("コマンドを正しく入力してください。\nコマンド：!kadai [難易度] [曲数] [バージョン(省略可)]\n例：!kadai 12 5") 
        elif len(args) == 3: #指定されたレベル、指定した曲数、指定したバージョンでランダム選曲する
            if args[0].isdigit() == True and args[1].isdigit() == True and args[2].isdigit() == True:
                version = ""
                if args[2] == '1':
                    version = "1st&substream"
                elif args[2] == '2':
                    version = "2nd style"
                elif args[2] == '3':
                    version = "3rd style"
                elif args[2] == '4':
                    version = "4th style"
                elif args[2] == '5':
                    version = "5th style"
                elif args[2] == '6':
                    version = "6th style"
                elif args[2] == '7':
                    version = "7th style"
                elif args[2] == '8':
                    version = "8th style"
                elif args[2] == '9':
                    version = "9th style"
                elif args[2] == '10':
                    version = "10th style"
                elif args[2] == '11':
                    version = "IIDX RED"
                elif args[2] == '12':
                    version = "HAPPY SKY"
                elif args[2] == '13':
                    version = "DistorteD"
                elif args[2] == '14':
                    version = "GOLD"
                elif args[2] == '15':
                    version = "DJ TROOPERS"
                elif args[2] == '16':
                    version = "EMPRESS"
                elif args[2] == '17':
                    version = "SIRIUS"
                elif args[2] == '18':
                    version = "Resort Anthem"
                elif args[2] == '19':
                    version = "Lincle"
                elif args[2] == '20':
                    version = "tricoro"
                elif args[2] == '21':
                    version = "SPADA"
                elif args[2] == '22':
                    version = "PENDUAL"
                elif args[2] == '23':
                    version = "copula"
                elif args[2] == '24':
                    version = "SINOBUZ"
                elif args[2] == '25':
                    version = "CANNON BALLERS"
                elif args[2] == '26':
                    version = "Rootage"
                elif args[2] == '27':
                    version = "HEROIC VERSE"
                else:
                    return await ctx.send("指定したバージョンが正しくありません")
                df = pd.read_csv(filepath_or_buffer="./data/beatmania_musiclist.csv",encoding="utf_8",sep=",")
                df= df[((df['BEGINNER 難易度'] == int(args[0])) | (df['NORMAL 難易度'] == int(args[0])) | (df['HYPER 難易度'] == int(args[0])) | (df['ANOTHER 難易度'] == int(args[0])) | (df['LEGGENDARIA 難易度'] == int(args[0]))) & (df['バージョン'] == version)]
                reply = "ID    " + str(df.loc[:,["バージョン","タイトル"]].sample(n=int(args[1])))
                await ctx.send(reply)
            else:
                await ctx.send("コマンドを正しく入力してください。\nコマンド：!kadai [難易度] [曲数] [バージョン(省略可)]\n例：!kadai 12 5")   


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(IIDX(bot)) # TalkにBotを渡してインスタンス化し、Botにコグとして登録する。