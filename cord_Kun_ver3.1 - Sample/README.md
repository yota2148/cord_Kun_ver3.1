# 初めまして、「cord_Kun_ver3.1」です。
チャットサービス「Discord」における、yota2148の身内向けの多機能botです。
Nintendo Switchのゲーム、マリオカート8DXにおけるタイムアタックの世界上位記録を参照したり、ログインを行ってガチャを引くことができます。
まだまだ鋭意製作中の部分も多く、今後、Discordのメッセージピン止め機能や、ボイスチャンネルで喋りすぎている人を強制的にミュートにする「自習室の先生」機能などをリリース予定です。

This is a multifunctional bot for yota2148's family members on the Discord chat service.
You can refer to the world's top time attack record in the Nintendo Switch game Mario Kart 8DX, or log in to pull down gachas.
We are still working on many aspects of the bot, and plan to release a Discord message pinning function and a "study room teacher" function that will forcibly mute people who are talking too much on the voice channel.

# Requirement，使用技術
- Python 3.10
    - discordpy

# セットアップ
- data/config.csvにアクセストークンと、起動時に挨拶を行うチャンネルIDを入力する
- data/log.csvに、「Username, Userid, 最終ログイン日を八桁の数字（例：20230216）,0,0,0」をサーバーの人数分入力する

以下、アイテムを自分で作り替えたい方のみ
- data/gacha_logs.csvに、「Username, Userid, 0」を入力する
- data/gacha_items.csvは「Itemid, rarerity, Itemname」の順で入力する


# 機能
**マリオカート8DX関連機能：commands/MKnita.py**
- */mknita コース名*
・ノーアイテムタイムアタックの世界上位記録,目標記録,難易度を表示する機能
- */mkhyou*
・それらの上位記録一覧の表を画像形式で表示する機能
**ログイン機能：commands/Login_function**
- */login*
・サーバー内でログインを行う機能。（log.csvに事前にアカウント情報を登録しておく必要があります）
- */gacha*
・loginで手に入れたユーザーポイントを利用してガチャを引くことができます。
- */juren*
・ガチャを１０回連続で行います。
- */status*
・ユーザーネーム、最終ログイン日、総ログイン回数、保有ユーザーポイントなどを教えてくれます。
- **名言フレーズ機能：commands/Phrase.py**
- */phrase*
・data/phrase.txtに登録されている名言をランダムに出力します。サンプルとして現在名言を登録してありますが、自由に改変可能です。
- **起動時挨拶**
スラッシュコマンド無しで、起動時に自動でメッセージを送信します。（起動時発言を行うチャンネルのIDを事前に入れておく必要があります）