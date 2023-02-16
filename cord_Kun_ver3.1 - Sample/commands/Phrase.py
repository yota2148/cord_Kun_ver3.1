import random

async def phrase(word):
    with open('./data/phrase.txt', encoding='utf-8') as ph_set:
        ph_list = [line.rstrip('\n') for line in ph_set.readlines()]
        ph_linessum = len(ph_list)
        ph_num = int(random.randint(1, ph_linessum))
        today_ph = ph_list[ph_num-1]
    await word.channel.send('今日あなたに贈りたい名言は『%s』です。\n今日も一日頑張っていきましょう。' %today_ph)