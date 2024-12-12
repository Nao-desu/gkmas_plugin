from hoshino import Service
from .config import *
from hoshino.MD import *
from ...groupmaster.switch import check_status
from .caculate import *

sv = Service('gkmas_score_caculate')

b = button_gen
button = [
    [b('算分','算分'),b('逆算分','逆算分'),b('算目标分','算目标分')],
    [b('算加练','算加练'),b('帮助','https://www.koharu.cn:8149/docs/gkmas/gkmas.html#%E7%AE%97%E5%88%86',type_int=0)]
]
button = generate_buttons(button)

def err_msg(hint_msg):
    return generate_md(3,["发生错误",hint_msg+'\r',"请点击帮助按扭查看具体使用方法"],button)

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def check_parameter(data,type):
    if len(data) != 3 and type == 1:
        return False,"格式错误，应为[算分 vo da vi](无需中括号)"
    elif len(data)!= 4 and type == 2:
        return False,"格式错误，应为[逆算分 vo da vi 评价分](无需中括号)"
    elif len(data)!= 4 and type == 3:
        return False,"格式错误，应为[算目标分 vo da vi 目标分](无需中括号)"
    if len(data) not in [2,6] and type == 4:
        return False,"格式错误，应为\r三属性计算：[算加练 vo vo% da da% vi vi%]\r单属性计算：[算加练 某一属性 该属性加成%]\r无需中括号和百分号"
    
    for i in range(len(data)):
        if type in [1,2,3] and not data[i].isdigit():
            return False,"参数错误"
        if type in [1,2,3] and i in range(0,2) and int(data[i]) not in range(0,1801):
            return False,"属性值应在0~1800之间"
        if type == 4 and i in [0,2,4] and int(data[i]) not in range(0,1801):
            return False,"属性值应在0~1800之间"
        if type == 4 and i in [1,3,5] and not is_float(data[i]):
            return False,"参数错误"
        
    return True,""

@sv.on_prefix("算分","查分")
@check_status("算分")
async def score_caculate(bot, ev):
    texts:str = ev.message.extract_plain_text().strip()
    data = [i for i in texts.split(' ') if i][:3]
    status,hint_msg = check_parameter(data,1)
    if not status:
        await bot.send(ev,err_msg(hint_msg))
        return
    data = [int(i) for i in data]
    mode_list = [mode for mode in MAX_PANEL if max(data) <= MAX_PANEL[mode]]
    msg_data = [f"您的面板为{sum(data)}","","使用o算分命令,可以输出纯文字结果"]
    for mode in mode_list:
        msg_data[1] += caculate_by_mode(mode,data).replace('\n','\r')
    msg = generate_md(3,msg_data,button)
    await bot.send(ev,msg)

@sv.on_prefix("o算分","o查分")
@check_status("算分")
async def score_caculate_o(bot, ev):
    texts:str = ev.message.extract_plain_text().strip()
    data = [i for i in texts.split(' ') if i][:3]
    status,hint_msg = check_parameter(data,1)
    if not status:
        await bot.send(ev,f'{hint_msg}')
        return
    data = [int(i) for i in data]
    mode_list = [mode for mode in MAX_PANEL if max(data) <= MAX_PANEL[mode]]
    msg = f"您的面板为{sum(data)}\n"
    for mode in mode_list:
        msg += caculate_by_mode(mode,data)
    await bot.send(ev,msg)
    
@sv.on_prefix("逆算分")
@check_status("算分")
async def score_reverse_caculate(bot, ev):
    texts:str = ev.message.extract_plain_text().strip()
    data = [i for i in texts.split(' ') if i][:4]
    status,hint_msg = check_parameter(data,2)
    if not status:
        await bot.send(ev,err_msg(hint_msg))
        return
    data = [int(i) for i in data[:4]]
    mode_list = [mode for mode in MAX_PANEL if max(data[:3]) <= MAX_PANEL[mode]]
    msg_data = [f"您的面板为{sum(data)},最终试验取得了","","得分与排名关系仅供参考"]
    for mode in mode_list:
        status,result = reverse_caculate_by_mode(mode,data)
        if not status:
            await bot.send(ev,err_msg("评价分过低,请检查输入"))
            return
        msg_data[1] += result
    msg = generate_md(3,msg_data,button)
    await bot.send(ev,msg)

@sv.on_prefix("算目标分")
@check_status("算分")
async def score_target_caculate(bot, ev):
    texts:str = ev.message.extract_plain_text().strip()
    data = [i for i in texts.split(' ') if i][:4]
    if data[-1].upper() in RANK_2_EVALUATION.keys():
        data[-1] = RANK_2_EVALUATION[data[-1].upper()]
    status,hint_msg = check_parameter(data,3)
    if not status:
        await bot.send(ev,err_msg(hint_msg))
        return
    data = [int(i) for i in data[:4]]
    mode_list = [mode for mode in MAX_PANEL if max(data[:3]) <= MAX_PANEL[mode]]
    msg_data = [f"您的面板为{sum(data[:3])},","达到目标评价需要取得的分数\名次为:\r","得分与排名关系仅供参考"]
    for mode in mode_list:
        msg_data[1] += target_caculate_by_mode(mode,data)
    msg = generate_md(3,msg_data,button)
    await bot.send(ev,msg)

@sv.on_prefix("算加练")
@check_status("算分")
async def oikomi_caculate(bot, ev):
    texts:str = ev.message.extract_plain_text().strip()
    data = [i.strip('%').strip('％') for i in texts.split(' ') if i][:6]
    if len(data) != 6:
        data = data[:2]
    status,hint_msg = check_parameter(data,4)
    if not status:
        await bot.send(ev,err_msg(hint_msg))
        return
    data = [float(i) for i in data]
    msg_data = [f"计算结果","","已包含期末考试后加成,未考虑s卡课后加成"]
    if len(data) == 2:
        mode_list = [mode for mode in MAX_PANEL if data[0] <= MAX_PANEL[mode]]
        for mode in mode_list:
            result = oikomi_caculate_1_by_mode(mode,data)
            msg_data[1] += result
        msg = generate_md(3,msg_data,button)
        await bot.send(ev,msg)
    if len(data) == 6:
        mode_list = [mode for mode in MAX_PANEL if max([data[0],data[2],data[4]]) <= MAX_PANEL[mode]]
        for mode in mode_list:
            result = oikomi_caculate_3_by_mode(mode,data)
            msg_data[1] += result
        msg = generate_md(3,msg_data,button)
        await bot.send(ev,msg)