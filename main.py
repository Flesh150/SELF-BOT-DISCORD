#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Создатель: Flesh
Донаты: https://www.donationalerts.com/r/flesh150
GitHub: https://github.com/Flesh150
Канал в тг: https://t.me/flesh_150
'''

import discord
import requests
import asyncio
import json

from discord.ext import commands
from config import *

client = commands.Bot( command_prefix = PREFIX,help_command = None, self_bot = True)

#================================================================
# ЕВЕНТЫ
#================================================================

@client.event
async def on_ready():
    print('Селф Бот готов к работе!')

#================================================================
# КОМАНДЫ 
#================================================================

@client.command()
async def help(ctx):
    await ctx.send(f'`{client.command_prefix}ping` - выводит пинг селф бота\n`{client.command_prefix}hypesquad` <от 1 до 3 delete удалит значёк> - меняет значек hypesquad\n`{client.command_prefix}block` <айди пользователя> - заблокировать пользователя\n`{client.command_prefix}unblock` <айди пользователя> - разблокировать пользователя\n`{client.command_prefix}bio` <текст> - изменить информацию о себе\n`{client.command_prefix}clear_bio` - удалить информацию о себе\n`{client.command_prefix}confidentiality` <от 1 до 3> - меняет безопасность личных данных\n`{client.command_prefix}leave_guild` <айди гилдии>- выйти из определеной гилдии\n`{client.command_prefix}theme` <light/dark> - меняет тему дискорда\n`{client.command_prefix}spam` <количество сообщений> <айди канала> <текст> - спам сообщениями в гилдии\n`{client.command_prefix}invite_link` <количество от 1 до 101> <айди канала> - создаёт инвайт ссылки на сервере\n`{client.command_prefix}username_local` <текст> - изменить ник на сервере где использовал команду\n`{client.command_prefix}username_global` <айди гилдии> <текст> - изменить ник на определеном сервере\n`{client.command_prefix}close_ls` - закрывает все личные переписки с другими пользователями и выходит из групп\n`{client.command_prefix}note` <айди пользователя> <текст> - поставить заметку на пользователе\n`{client.command_prefix}clear_note` <айди пользователя> - удаление заметки с пользователя')

@client.command()
async def ping(ctx):
    await ctx.send(f'Пинг: `{int(client.latency * 1000)}` ms')

@client.command()
async def hypesquad(ctx,hs_id):
    if str(hs_id) == 'delete':
        requests.delete('https://discord.com/api/v9/hypesquad/online',headers={'authorization':TOKEN})
        await ctx.send('HypeSquad удален.')
    elif int(hs_id) > 3:
        pass
    elif int(hs_id) < 1:
        pass
    else:
        requests.post('https://discord.com/api/v9/hypesquad/online',headers={'authorization':TOKEN},json={"house_id":hs_id})
        await ctx.send('HypeSquad изменен.')

@client.command()
async def block(ctx,user_id: int):
    find_user = await client.fetch_user(user_id)
    requests.put(f'https://discord.com/api/v9/users/@me/relationships/{find_user.id}',headers={'authorization':TOKEN},json={"type":2})
    await ctx.send('Добавлен в чс.')

@client.command()
async def unblock(ctx,user_id: int):
    find_user = await client.fetch_user(user_id)
    requests.delete(f'https://discord.com/api/v9/users/@me/relationships/{find_user.id}',headers={'authorization':TOKEN})
    await ctx.send('Удален из чс.')

@client.command()
async def bio(ctx,*,text):
    requests.patch("https://discord.com/api/v9/users/@me",headers={'authorization':TOKEN},json={"bio":text})
    await ctx.send('Информация обо мне изменена.')

@client.command()
async def clear_bio(ctx):
    requests.patch("https://discord.com/api/v9/users/@me",headers={'authorization':TOKEN},json={"bio":''})
    await ctx.send('Информация обо мне удалена')

@client.command()
async def confidentiality(ctx, conf_id: int):
    if conf_id == 1:
        requests.patch('https://discord.com/api/v9/users/@me/settings-proto/1',headers={'authorization':TOKEN},json={"settings":"Mi1KAggBUgIIAVoCCAFiAggBagIIAXICCAF6AIIBAggBigEAmgEAogEAqgECCAE="})
        await ctx.send('Конфидециальность низкая.')
    elif conf_id == 2:
        requests.patch('https://discord.com/api/v9/users/@me/settings-proto/1',headers={'authorization':TOKEN},json={"settings":"Mi9KAggBUgIIAVoCCAFiAggBagIIAXICCAF6AIIBAggBigEAmgECCAGiAQCqAQIIAQ=="})
        await ctx.send('Конфидециальность средняя.')
    elif conf_id == 3:
        requests.patch('https://discord.com/api/v9/users/@me/settings-proto/1',headers={'authorization':TOKEN},json={"settings":"Mi9KAggBUgIIAVoCCAFiAggBagIIAXICCAF6AIIBAggBigEAmgECCAKiAQCqAQIIAQ=="})
        await ctx.send('Конфидециальность высокая.')
    else:
        pass

@client.command()
async def leave_guild(ctx, guild_id=None):
    if guild_id == None:
        requests.delete(f'https://discord.com/api/v9/users/@me/guilds/{ctx.guild.id}',headers={'authorization':TOKEN},json={"lurking":'false'})
    else:
        requests.delete(f'https://discord.com/api/v9/users/@me/guilds/{guild_id}',headers={'authorization':TOKEN},json={"lurking":'false'})

@client.command()
async def theme(ctx,theme):
    if theme == 'dark':
        requests.patch('https://discord.com/api/v9/users/@me/settings',headers={'authorization':TOKEN},json={"theme":"dark"})
        await ctx.send('Установлена темная тема.')
    elif theme == 'light':
        requests.patch('https://discord.com/api/v9/users/@me/settings',headers={'authorization':TOKEN},json={"theme":"light"})
        await ctx.send('Установлена светлая тема.')
    else:
        pass

@client.command()
async def spam(ctx,count: int,channel_id,*,message):
    for i in range(count):
        requests.get(f'https://discord.com/api/v9/channels/{channel_id}/messages?limit=50',headers={'authorization':TOKEN})
        requests.post(f'https://discord.com/api/v9/channels/{channel_id}/messages',headers={'authorization':TOKEN},json={"content":message,"nonce":"","tts":'false'})

@client.command()
async def invite_link(ctx,count,channel_id:int):
    #max 604800 min 1
    if count > 101:
        pass
    elif count < 1:
        pass
    else:
        for i in range(count):
            invite = requests.post(f'https://discord.com/api/v9/channels/{channel_id}/invites',headers={'authorization':TOKEN},json={"max_age":0,"max_uses":i,"temporary":'false'})
            print(invite)
            await asyncio.sleep(3)

@client.command()
async def username_local(ctx,*,username: str):
    requests.patch(f'https://discord.com/api/v9/guilds/{ctx.guild.id}/members/@me',headers={'authorization':TOKEN},json={"nick":username})
    await ctx.send(f'Ник на сервере {ctx.guild.id} изменен.')

@client.command()
async def username_global(ctx,server_id: int,*,username: str):
    requests.patch(f'https://discord.com/api/v9/guilds/{server_id}/members/@me',headers={'authorization':TOKEN},json={"nick":username})
    await ctx.send(f'Ник на сервере {server_id} изменен.')

@client.command()
async def close_ls(ctx):
    rs = requests.get(f'https://discord.com/api/v9/users/@me/channels',headers={'authorization':TOKEN})
    g = json.loads(rs.text)
    for i in g:
        id_channel = i['id']
        rs1 = requests.delete(f'https://discord.com/api/v9/channels/{id_channel}',headers={'authorization':TOKEN})

@client.command()
async def note(ctx,user_id: int,*,message: str):
    requests.put(f'https://discord.com/api/v9/users/@me/notes/{user_id}',headers={'authorization':TOKEN},json={"note":message})
    await ctx.send(f'Заметка на {user_id} поставлена.')

@client.command()
async def clear_note(ctx,user_id: int):
    requests.put(f'https://discord.com/api/v9/users/@me/notes/{user_id}',headers={'authorization':TOKEN},json={"note":''})
    await ctx.send(f'Заметка на {user_id} удалена.')

client.run(TOKEN,bot = False)
