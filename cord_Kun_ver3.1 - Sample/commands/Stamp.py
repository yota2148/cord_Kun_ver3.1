import discord

async def stamp(word):
    kind = word.content
    if kind[:4] == '/stp':
        if kind == '/stp' or kind[5] in {'タ', 'た', '離'} or kind[5] in {'t', 'T'}:
            await word.channel.send(file=discord.File('./pic/TIME_OUT.png'))
        if kind[5] in {'ね', 'ネ', '寝', '就'} or kind[5:7] in {'Ne', 'NE', 'ne'}:
            await word.channel.send(file=discord.File('./pic/NE_RU.png'))
        if kind[5] in {'の', 'ノ', '飲','D','d'} or kind[5:7] in {'No', 'NO', 'no'}:
            await word.channel.send(file=discord.File('./pic/DRINK.png'))
        if kind[5] in {'ト', 'と','便'} or kind[5] in {'W', 'w'}:
            await word.channel.send(file=discord.File('./pic/WC.png'))

    elif kind[:6] == '/stamp':
        if kind == '/stamp' or kind[7] in {'タ', 'た', '離'} or kind[7] in {'t', 'T'}:
            await word.channel.send(file=discord.File('./pic/TIME_OUT.png'))
        if kind[7] in {'ね', 'ネ', '寝', '就'} or kind[7:9] in {'Ne', 'NE', 'ne'}:
            await word.channel.send(file=discord.File('./pic/NE_RU.png'))
        if kind[7] in {'の', 'ノ', '飲','D','d'} or kind[7:9] in {'No', 'NO', 'no'}:
            await word.channel.send(file=discord.File('./pic/DRINK.png'))
        if kind[7] in {'ト', 'と','便'} or kind[7] in {'W', 'w'}:
            await word.channel.send(file=discord.File('./pic/WC.png'))