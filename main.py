import re
import time
import datetime
import json
import copy
import random
import os
import importlib
import inspect
import pathlib

from amiyabot import PluginInstance
from amiyabot.util import temp_sys_path, extract_zip
from amiyabot.adapters.mirai.payload import WebsocketAdapter
from amiyabot.adapters.mirai import MiraiBotInstance
from core.util import read_yaml
from core import log, Message, Chain
from core.database.user import User, UserInfo
from core.database.bot import OperatorConfig
from core.resource.arknightsGameData import ArknightsGameData, ArknightsGameDataResource, Operator

curr_dir = os.path.dirname(__file__)

class DuelPluginInstance(PluginInstance):
    def install(self):
        pass

bot = DuelPluginInstance(
    name='决斗游戏',
    version='1.0',
    plugin_id='amiyabot-game-hsyhhssyy-duel',
    plugin_type='',
    description='让兔兔可以公平的裁判一场决斗',
    document=f'{curr_dir}/README.md'
)

async def mute(data: Message,target_id:int, mute_time:int ):
    #只支持Mirai，别的没法禁言
    if type(data.instance) is MiraiBotInstance:
        log.info(f'MiraiBot mute {target_id}')
        await data.instance.connection.send(WebsocketAdapter.mute(data.instance.session, data.channel_id, target_id, int(mute_time)))

@bot.on_message(keywords=['决斗'])
async def _(data: Message):

    if len(data.at_target)<1:
        return Chain(data).text('发起决斗时请at对方哦')
    
    duel_starter = data.user_id
    duel_victim = data.at_target[0]
    start_time = datetime.datetime.now()
    time_delta = datetime.timedelta(milliseconds=1)

    await data.send(Chain(data,at=False).text(f'博士{data.nickname}发起了一场决斗，请').at(duel_victim).text('确认是否参与决斗，如果参与请回复同意，否则将自动取消'))

    agree = False
    while time_delta < datetime.timedelta(seconds=30):
        event = await data.wait_channel(force=True,clean=False,max_time = 30)

        now = datetime.datetime.now()
        time_delta = now - start_time
        log.info(f'{time_delta}')

        if event:
            choice = event.message
            event.close_event()
        else:
            continue

        if choice:
            if choice.user_id != duel_victim:
                continue
            if choice.text !='同意':
                return Chain(choice,at=False).text('对方没有同意')            
            agree = True
            break
        else:
            return Chain(data,at=False).text('对方30秒内未响应同意')
    
    if not agree:
        return Chain(choice,at=False).text('对方30秒内未响应同意')

    await data.send( Chain(data,at=False).at(duel_starter).at(duel_victim).text('接下来，阿米娅会在60秒内喊出开始，在这之后最先发送“开枪”的博士胜出，在喊开始之前发送的博士会被视为犯规，输的人会被禁言哦。') )

    duel_second = random.randint(1,60)
    
    log.info(f'duel start ,set time: {duel_second}')

    start_time = datetime.datetime.now()
    time_delta = datetime.timedelta(milliseconds=1)

    while time_delta < datetime.timedelta(seconds=duel_second):

        event = await data.wait_channel(force=True, clean=False, max_time = 1)

        now = datetime.datetime.now()
        time_delta = now -start_time
        log.info(f'{time_delta}')

        if event:
            choice = event.message
            event.close_event()
        else:
            continue

        if choice:
            if choice.user_id != duel_victim and choice.user_id != duel_starter:
                continue

            if choice.text !='开枪':
                continue

            if choice.user_id == duel_victim:
                await mute(data,duel_victim,60*10)
                await mute(data,duel_starter,60)
            if choice.user_id == duel_starter:
                await mute(data,duel_starter,60*10)
                await mute(data,duel_victim,60)
                
            return Chain(choice,at=False).text(f'玩家{choice.nickname}抢跑犯规，被禁言10分钟，对方被击毙，禁言1分钟')
        else:
            continue

    log.info(f'duel start fire')

    await data.send(Chain(data,at=False).text('开始') )
    start_time = datetime.datetime.now()
    time_delta = datetime.timedelta(milliseconds=1)

    while time_delta < datetime.timedelta(seconds=10):

        event = await data.wait_channel(force=True,clean=False,max_time = 10)

        now = datetime.datetime.now()
        time_delta = now -start_time
        log.info(f'{time_delta}')

        if event:
            choice = event.message
            event.close_event()
        else:
            continue

        if choice:
            if choice.user_id != duel_victim and choice.user_id != duel_starter:
                continue    

            if choice.text !='开枪':
                continue
            #    await mute(data,choice.user_id,10)
            #    return Chain(choice).text(f'玩家{choice.nickname}敲错了字')
            
            if choice.user_id == duel_victim:
                await mute(data,duel_starter,60*3)
            if choice.user_id == duel_starter:
                await mute(data,duel_victim,60*3)

            return Chain(choice).text(f'玩家{choice.nickname}胜出，对方被禁言3分钟')
        else:
            continue

    await mute(data,duel_starter,60*5)
    await mute(data,duel_victim,60*5)
    return Chain(data,at=False).text('双方10秒内都没有回应，一起被禁言5分钟')