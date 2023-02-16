import discord
import csv

class MKnita:
    def __init__(self, word, track, nita_csv):
        self.nita_csv = nita_csv
        self.word = word
        self.track = track
    
    async def mkhyou(self):
        await self.word.channel.send(file=discord.File('./pic/MKNITA.png'))

    async def mknita(self):
        flag = 1
        for row in csv.reader(self.nita_csv):
            name, time, difficulty = row
            if name in self.track:
                t_min, t_sec, t_nsec = map(int, [time[0], time[1:3], time[3:]])
                # intの型変換によってズレたコンマ以下の秒数の桁合わせを行います
                if t_nsec <= 99:
                    t_nsec = '0'+str(t_nsec)
                
                # ここから目標タイム（g_*）を計算する。目標タイムは、参考記録（time, t_*）にプラス５秒した記録になります。
                g_min, g_sec, g_nsec = t_min, t_sec+5, t_nsec

                # 繰り上がりの処理などを行います
                if g_sec >= 60:
                    g_min += 1
                    g_sec -= 60
                # 秒数の桁合わせを行います
                if 0 <= g_sec <= 9:
                    g_sec = '0'+str(g_sec)
                if 0 <= t_sec <= 9:
                    t_sec = '0'+str(t_sec)
                
                # 計算が終わったので記録を出力します。
                await self.word.channel.send('参考記録＊%s:%s.%s\n目標記録＊%s:%s.%s\n難易度　＊%s' %(t_min, t_sec, t_nsec,g_min, g_sec, g_nsec,int(difficulty)*'★'))
                flag = 0
                break
        if flag:
            await self.word.channel.send('コース名を入力するか、正しいコース名を入力してください。\n'\
                'ヒント：SFCやGBAなど、過去作からの移植名が抜けている可能性があります。')