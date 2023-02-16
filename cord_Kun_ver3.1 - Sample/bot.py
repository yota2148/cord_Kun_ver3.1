##############################################################
# 起動時実行する関数を読み込む
import discord
import csv
from commands.Greet import greet
from commands.Slash_checker import slash

# configを読み取る
config_csv = open('data/config.csv', encoding='utf-8')
for row in csv.reader(config_csv):
    name, ids = row
    if name == 'TOKEN':
        TOKEN = str(ids)
    elif name == 'greet_channel':
        greet_channel = int(ids)

client = discord.Client(intents=discord.Intents.all())

###############################################################


# 起動確認
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')
    await greet(client, greet_channel)

# 関数を発生させていく場所
@client.event
async def on_message(message):
    try:
        # メッセージ送信者がBotだった場合は無視する
        if message.author.bot:
            return
        # message_Tell機能は廃止する
        else:
            await slash(message)
    except IndexError as e:
        print('========================\nERROR:'+str(e)+'\n========================')
    except KeyboardInterrupt as e:
        print('========================\nERROR:'+str(e)+'\n========================')
    except Exception as e:
        await message.channel.send('(´・ω・｀)エラーが発生したみたいよー\n(´・ω・｀)そんなー')
        print('========================\nUNKNOWN ERROR:'+str(e)+'\n========================')

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
        