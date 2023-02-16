###############################################################
# 関数をimportする
import random

from .Phrase import phrase
import commands.MKnita as MK
from .Stamp import stamp
import commands.Login_function as Login

###############################################################


async def slash(word):
    # 文字のみを返すフレーズ呼び出し（動作確認用）
    if word.content == '/neko':
        await word.channel.send('にゃーん')
    
    elif word.content == '/phrase':
        await phrase(word)

    # MK8Dお役立ち機能
    elif word.content == '/mkhyou' or word.content == '/mkhyo':
        MK_object = MK.MKnita(word, 0, 0)
        await MK_object.mkhyou()

    elif word.content[:7] == '/mknita':
        track = str(word.content[8:])
        nita_csv = open('./data/mknita.csv', encoding='utf-8')
        MK_object = MK.MKnita(word, track, nita_csv)
        await MK_object.mknita()

    # VC関連お役立ち機能
    elif word.content[:4] == '/stp' or word.content[:6] == '/stamp':
        await stamp(word)
    
    # ログイン機能/ログインボーナス・ガチャ機能
    elif word.content == '/login':
        userroot = word.author
        login_csv = open('./data/log.csv')
        Login_object = Login.Login(word, userroot, login_csv)
        await Login_object.login()
    
    elif word.content == '/gacha':
        userroot = word.author
        login_csv = open('./data/log.csv')
        Login_object = Login.Login(word, userroot, login_csv)
        await Login_object.gacha()

    elif word.content == '/juren':
        userroot = word.author
        login_csv = open('./data/log.csv')
        Login_object = Login.Login(word,userroot, login_csv)
        await Login_object.juren()
    
    elif word.content == '/status' or word.content == '/stat':
        userroot = word.author
        login_csv = open('./data/log.csv')
        Login_object = Login.Login(word,userroot, login_csv)
        await Login_object.status()

    
    # 例外処理
    elif word.content[0] == '/':
        await word.channel.send('有効なスラッシュコマンドを入力してください。')
    
    # Login_functionに関する、チャットボーナスポイント機能を返す
    else:
        bonuscheck = random.randint(1, 100)
        if bonuscheck <= 10:
            userroot = word.author
            login_csv = open('./data/log.csv')
            Login_object = Login.Login(word, userroot, login_csv)
            await Login_object.bonuspoint()