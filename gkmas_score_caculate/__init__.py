#算分

from hoshino import Service

sv_help = """
学马仕功能
通过面板计算达到对应评价需要的分数
格式为：算分 vo da vi
(注意：这里的面板为进入最终试验之前的面板)
"""

sv = Service('gkmas_score_caculate',help_=sv_help)

def score_caculate(score:int):
    if score <= 1500:return int(score/0.3)
    elif score <= 2250:return int((score-1500)/0.15) + 5000
    elif score <= 3050:return int((score-2250)/0.08) + 10000
    elif score <= 3450:return int((score-3050)/0.04) + 20000
    elif score <= 3650:return int((score-3450)/0.02) + 30000
    elif score <= 3750:return int((score-3650)/0.01) + 40000

@sv.on_prefix('算分','查分')
async def gkmas_score_caculate(bot,ev):
    texts:str = ev.message.extract_plain_text().strip()
    data = texts.split(' ')
    if len(data) == 3:
        n = 0
        for i in data:
            if not i.isdigit():await bot.send(ev,'格式错误，应为[算分 vo da vi]');return
            data[n] = int(i)
            if int(i)>1500 or int(i)<0:await bot.send(ev,'属性值不合理，应在1~1500区间内');return
            n += 1
    else: await bot.send(ev,'格式错误，应为[算分 vo da vi]');return
    vo,da,vi = data
    state = vo+da+vi
    flu = 0
    if 1500-vo <=30:flu += vo-1470
    if 1500-da <=30:flu += da-1470
    if 1500-vi <=30:flu += vi-1470
    msg = f'您的面板为{state}→{state+90-flu}(+{90-flu})\n'
    score = 1700 + int((state+90-flu)*2.3)
    if score < 6250:msg += '离A还很遥远哦，再接再厉吧！'
    elif score < 7750:msg += f'A评价需要最终试验获得{score_caculate(10000-score)}分\n离A+还很遥远哦，再接再厉吧！'
    elif score < 8200:msg += f'A评价需要最终试验获得{score_caculate(10000-score)}分\nA+评价需要最终试验获得{score_caculate(11500-score)}分\n离S还很遥远哦，再接再厉吧！'
    elif score < 9250:msg += f'最终试验1位即可达成A评价\nA+评价需要最终试验获得{score_caculate(11500-score)}分\n离S还很遥远哦，再接再厉吧！'
    elif score < 9700:msg += f'A+评价需要最终试验获得{score_caculate(11500-score)}分\nS评价需要最终试验获得{score_caculate(13000-score)}分'
    elif score < 11200:msg += f'最终试验1位即可达成A+评价\nS评价需要最终试验获得{score_caculate(13000-score)}分'
    else:msg += f'最终试验1位即可达成S评价'
    await bot.send(ev,msg)