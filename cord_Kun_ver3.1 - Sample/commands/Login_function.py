import datetime
import csv
import random

class Login:
    def __init__(self, word, userroot, login_csv):
        self.word = word
        self.userroot = userroot
        self.login_csv = login_csv
    
    async def login(self):
        userid = self.userroot.id

        today_date = datetime.date.today()
        today_date_int = int(str(today_date).replace('-', ''))

        write_data_set = []

        # 時刻を取得して挨拶を変更
        today_now = datetime.datetime.now()
        today_now_hour = today_now.hour
        if 4 <= today_now_hour <= 10:
            aisatsu = 'おはようございます'
        elif 10 <= today_now_hour <= 18:
            aisatsu = 'こんにちは'
        elif 19 <= today_now_hour <= 24 or 0 <= today_now_hour <= 3:
            aisatsu = 'こんばんは'
        
        for row in csv.reader(self.login_csv):
            username, userid_incsv, last_login_date, login_count, userpoints, earned_itemcount = row
            userid_incsv, login_count, userpoints = map(int, [userid_incsv, login_count, userpoints])

            if int(userid) == userid_incsv:
                # login時処理をしていきます。
                # まずは日付を確認してログイン可能かを判定します。
                if today_date_int != int(last_login_date):
                    login_timedelta = today_date - datetime.date(int(last_login_date[:4]), int(last_login_date[4:6]), int(last_login_date[6:8]))
                    login_timedelta = login_timedelta.days

                    login_count += 1

                    aisatsu2 = ''
                    if int(login_timedelta) >= 5:
                        aisatsu2 = 'お久しぶりですね。'
                    
                    userpoints += 1000
                    last_login_date = today_date_int

                    # discordにメッセージを送信
                    await self.word.channel.send('%s、%s。計%d回目のログインです。\n前回のログインから%d日が経過しています。%s\n現在のユーザーポイント：%dpts' %(aisatsu, username, login_count,login_timedelta, aisatsu2,userpoints))

                else:
                    await self.word.channel.send('今日はもうログインしています。ログインは一日一度です。')
            
            # 書き込み用のデータを格納
            write_data_set.append([username, userid_incsv, last_login_date, login_count, userpoints, earned_itemcount])

        # write_data_setをもとにcsvファイルを更新する
        f = open('./data/log.csv', 'w', encoding='utf-8')
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(write_data_set)
        f.close()



    async def gacha(self):
        # gacha_items.csvを更新した際、gacha_logs.csvの列を更新数に合わせて追加する
        gacha_items_csv = open('./data/gacha_items.csv')
        item_count = 0
        for row in csv.reader(gacha_items_csv):
            item_count += 1

        write_data_set = []
        
        gacha_logs_csv = open('./data/gacha_logs.csv')
        for row in csv.reader(gacha_logs_csv):
            username, userid = row[:2]
            item_log_countlist = row[2:]
            item_log_count = int(len(item_log_countlist))
            write_data_set.append([username, userid]+item_log_countlist+[0]*(item_count-item_log_count))

        # gacha_logs.csvの更新（書き換え）
        f = open('./data/gacha_logs.csv', 'w')
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(write_data_set)
        f.close()

        
        # 準備OK ################################################

        # ここからはgacha機能の本編を実装していきます。
        # 誰がガチャを引くのかを判定する。同時に値を初期化していく
        userid = self.userroot.id
        write_data_set = []

        for row in csv.reader(self.login_csv):
            username, userid_incsv, last_login_date, login_count, userpoints, earned_itemcount = row
            userid_incsv, login_count, userpoints, earned_itemcount = map(int, [userid_incsv, login_count, userpoints, earned_itemcount])


            if int(userid) == userid_incsv:
                # Pointが足りているかの判定
                if userpoints <300:
                    await self.word.channel.send('ポイントが不足しているため、ガチャを引くことができません。\n現在保有ポイント：%dpts （必要ポイント：300pts）' %userpoints)
                else:
                    # ガチャ代の演算
                    userpoints -= 300

                    # 以下、アイテム獲得処理
                    get_number = int(random.randint(1, item_count))

                    # 手に入れたIDに合致するアイテムのアイテム名とレアリティを取得
                    itemlist = open('./data/gacha_items.csv')
                    for itemrow in csv.reader(itemlist):
                        item_no, item_rarerity, item_name = itemrow
                        if int(item_no) == get_number:
                            break
                    
                    # 手に入れたアイテムに応じて、所持アイテム数を追加する
                    # アイテム数が0→1ならば、NEWを表示したい
                    # アイテム数が0でないアイテム（取得済みアイテム数）を取得
                    loglist = open('./data/gacha_logs.csv')
                    write_data_set_gachalog = []
                    for logrow in csv.reader(loglist):
                        username_ingachalog, userid_ingachalog = logrow[:2]
                        gacha_logs_list = logrow[2:]
                        gacha_logs_list = list(map(int, gacha_logs_list))

                        if int(userid_ingachalog) == int(userid): 
                            gacha_logs_list[get_number-1] += 1

                        write_data_set_gachalog.append([username_ingachalog, userid_ingachalog]+gacha_logs_list)

                        newprint = ''
                        if gacha_logs_list[get_number-1] == 1:
                            newprint = '【NEW!!】'
                            earned_itemcount += 1
                        
                    f = open('./data/gacha_logs.csv', 'w')
                    writer = csv.writer(f, lineterminator='\n')
                    writer.writerows(write_data_set_gachalog)
                    f.close()

                    await self.word.channel.send('・・・NOW LOADING・・・')
                    await self.word.channel.send('『【No.%d】%s【★%s】』%sを手に入れた。\n残りポイント：%dpts' %(get_number,item_name,item_rarerity,newprint,userpoints))
                    await self.word.channel.send('コンプリート率：%d/%d' %(earned_itemcount, item_count))

            
            else:
                pass
            
            # 書き込み用のデータを格納
            write_data_set.append([username, userid_incsv, last_login_date, login_count, userpoints, earned_itemcount])
        
        # write_data_setをもとにcsvファイルを更新する
        f = open('./data/log.csv', 'w')
        writer = csv.writer(f,lineterminator='\n')
        writer.writerows(write_data_set)
        f.close()
    


    async def juren(self):
        # gacha_items.csvを更新した際、gacha_logs.csvの列を更新数に合わせて追加する
        gacha_items_csv = open('./data/gacha_items.csv')
        item_count = 0
        for row in csv.reader(gacha_items_csv):
            item_count += 1

        write_data_set = []
        
        gacha_logs_csv = open('./data/gacha_logs.csv')
        for row in csv.reader(gacha_logs_csv):
            username, userid = row[:2]
            item_log_countlist = row[2:]
            item_log_count = int(len(item_log_countlist))
            write_data_set.append([username, userid]+item_log_countlist+[0]*(item_count-item_log_count))

        # gacha_logs.csvの更新（書き換え）
        f = open('./data/gacha_logs.csv', 'w')
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(write_data_set)
        f.close()

        # 準備OK ################################################

        # ここからはjuren機能の本編を実装していきます。
        # 誰がガチャを引くのかを判定する。同時に値を初期化していく
        userid = self.userroot.id
        write_data_set = []

        for row in csv.reader(self.login_csv):
            username, userid_incsv, last_login_date, login_count, userpoints, earned_itemcount = row
            userid_incsv, login_count, userpoints, earned_itemcount = map(int, [userid_incsv, login_count, userpoints, earned_itemcount])

            if int(userid) == userid_incsv:
                # Pointが足りているかの判定
                if userpoints <3000:
                    await self.word.channel.send('ポイントが不足しているため、ガチャを引くことができません。\n現在保有ポイント：%dpts （必要ポイント：3000pts）' %userpoints)
                else:
                    # ガチャ代の演算
                    userpoints -= 3000
                    # ↓十連ガチャで排出するアイテムid群を保存するlist
                    get_numbers = []

                    await self.word.channel.send('====連続召喚魔法陣生成システム[J.U.R.E.N.]を起動します====')
                    for i in range(10):
                        # 以下、アイテム獲得処理→listに保存
                        get_number = int(random.randint(1, item_count))
                        get_numbers.append(get_number)

                        # Now loading部分の出力
                        await self.word.channel.send('・・・NOW LOADING（%d/10）・・・' %(i+1))
                        
                    await self.word.channel.send('====生成完了.以下に結果を出力します====')
                    for j in get_numbers:
                        # itemのデータを取得（get_number -> jが獲得アイテムのID）
                        itemlist = open('./data/gacha_items.csv')
                        for itemrow in csv.reader(itemlist):
                            item_no, item_rarerity, item_name = itemrow
                            if int(item_no) == j:
                                break
                        
                        # Userの取得アイテム数を更新
                        loglist = open('./data/gacha_logs.csv')
                        write_data_set_gachalog = []
                        for logrow in csv.reader(loglist):
                            username_ingachalog, userid_ingachalog = logrow[:2]
                            gacha_logs_list = logrow[2:]
                            gacha_logs_list = list(map(int, gacha_logs_list))

                            if int(userid_ingachalog) == int(userid): 
                                gacha_logs_list[j-1] += 1

                            write_data_set_gachalog.append([username_ingachalog, userid_ingachalog]+gacha_logs_list)

                            newprint = ''
                            if gacha_logs_list[j-1] == 1:
                                newprint = '【NEW!!】'
                                earned_itemcount += 1

                        f = open('./data/gacha_logs.csv', 'w')
                        writer = csv.writer(f, lineterminator='\n')
                        writer.writerows(write_data_set_gachalog)
                        f.close()

                        await self.word.channel.send('〇【No.%d】%s【★%s】%s' %(j,item_name,item_rarerity,newprint))
                    await self.word.channel.send('残りポイント：%d' %userpoints)
                    await self.word.channel.send('コンプリート率：%d/%d' %(earned_itemcount, item_count))
                    
            else:
                pass
            
            # 書き込み用のデータを格納
            write_data_set.append([username, userid_incsv, last_login_date, login_count, userpoints, earned_itemcount])
        
        # write_data_setをもとにcsvファイルを更新する
        f = open('./data/log.csv', 'w')
        writer = csv.writer(f,lineterminator='\n')
        writer.writerows(write_data_set)
        f.close()
    


    async def status(self):
        gacha_items_csv = open('./data/gacha_items.csv')
        item_count = 0
        for row in csv.reader(gacha_items_csv):
            item_count += 1
        userid = self.userroot.id

        for row in csv.reader(self.login_csv):
            username, userid_incsv, last_login_date, login_count, userpoints, earned_itemcount = row
            userid_incsv, login_count, userpoints,earned_itemcount = map(int, [userid_incsv, login_count, userpoints,earned_itemcount])
            if int(userid) == userid_incsv:
                await self.word.channel.send(
                    '=STATUS=============================\nUSERNAME: %s\nLAST LOGIN DATE: %d年%d月%d日\n'\
                    'TOTAL LOGIN: %d回\nUSER POINTS: %dpts\nCOMPLETE RATE: %d/%d\n=====================================' %(username,int(last_login_date[:4]), int(last_login_date[4:6]), int(last_login_date[6:8]),login_count,userpoints,earned_itemcount,item_count))
                break
            else:
                pass



    
    async def bonuspoint(self):
        # 誰にbonus pointを付与するか検知する
        userid = self.userroot.id

        write_data_set = []
        bonuspts = random.randint(50, 400)

        for row in csv.reader(self.login_csv):
            username, userid_incsv, last_login_date, login_count, userpoints, earned_itemcount = row
            userid_incsv, login_count, userpoints = map(int, [userid_incsv, login_count, userpoints])
            
            # bonuspts獲得者を検索
            if int(userid) == userid_incsv:
                
                userpoints += bonuspts
                # bonusptsごとにメッセージを設定
                if 300<= bonuspts:
                    bonusmsg = 'やったね！これでガチャが引ける！'
                else:
                    if bonuspts%3 == 0:
                        bonusmsg = '日頃の徳の賜物だ。'
                    elif bonuspts%3 == 1:
                        bonusmsg = '良い気分だ。'
                    else:
                        bonusmsg = '君はラッキー、僕はニャンチー。'


                await self.word.channel.send('謎の力によって、%sはユーザーポイントを%dpts獲得した。%s\n現在保有ポイント：%dpts' %(username, bonuspts, bonusmsg, userpoints))
            else:
                pass
            
            # 書き込み用のデータを格納
            write_data_set.append([username, userid_incsv, last_login_date, login_count, userpoints, earned_itemcount])
        

        # write_data_setをもとにcsvファイルを更新する
        f = open('./data/log.csv', 'w')
        writer = csv.writer(f,lineterminator='\n')
        writer.writerows(write_data_set)
        f.close()