#算分

from hoshino import Service
from ..MDgen import *

sv = Service('gkmas_score_caculate')

def score_caculate(score:int):
    if score <= 1500:return int(score/0.3)
    elif score <= 2250:return int((score-1500)/0.15) + 5000
    elif score <= 3050:return int((score-2250)/0.08) + 10000
    elif score <= 3450:return int((score-3050)/0.04) + 20000
    elif score <= 3650:return int((score-3450)/0.02) + 30000
    else:return int((score-3650)/0.01) + 40000

button = [
    {"buttons": [button_gen(False,'算分','算分'),button_gen(False,'逆算分','逆算分'),button_gen(False,'算目标分','算目标分')]},
    {"buttons": [button_gen(False,'算加练','算加练'),button_gen(True,'帮助','学马仕帮助')]}
]

@sv.on_prefix('算分','查分')
async def gkmas_score_caculate(bot,ev):
    texts:str = ev.message.extract_plain_text().strip()
    data = texts.split(' ')[:3]
    if len(data) == 3:
        n = 0
        for i in data:
            if not i.isdigit():await bot.send(ev,'格式错误，应为[算分 vo da vi]');return
            data[n] = int(i)
            if int(i)>1500 or int(i)<1:await bot.send(ev,'属性值不合理，应在1~1500区间内');return
            n += 1
    else: await bot.send(ev,'格式错误，应为[算分 vo da vi]');return
    vo,da,vi = data
    state = vo+da+vi
    flu = 0
    if 1500-vo <=30:flu += vo-1470
    if 1500-da <=30:flu += da-1470
    if 1500-vi <=30:flu += vi-1470
    data = [f'您的面板为{state}→{state+90-flu}(+{90-flu})']
    score = 1700 + int((state+90-flu)*2.3)
    if score < 8200: data.append(f'A评价需要最终试验获得{score_caculate(10000-score)}分  \rA+评价需要最终试验获得{score_caculate(11500-score)}分  \rS评价需要最终试验获得{score_caculate(13000-score)}分  \r')
    elif score < 9250: data.append(f'最终试验1位即可达成A评价  \rA+评价需要最终试验获得{score_caculate(11500-score)}分  \rS评价需要最终试验获得{score_caculate(13000-score)}分  \r')
    elif score < 9700: data.append(f'A+评价需要最终试验获得{score_caculate(11500-score)}分  \rS评价需要最终试验获得{score_caculate(13000-score)}分  \r')
    elif score < 11200: data.append(f'最终试验1位即可达成A+评价  \rS评价需要最终试验获得{score_caculate(13000-score)}分  \r')
    else: data.append(f'最终试验1位即可达成S评价  \r')
    data.append('如果不想更新旧版qq，可以使用[o算分]命令(原命令前加字母o)，可以输出旧版结果')
    msg = MD_gen1(data,button)
    await bot.send(ev,msg)

@sv.on_prefix('o算分','o查分')
async def gkmas_score_caculate(bot,ev):
    texts:str = ev.message.extract_plain_text().strip()
    data = texts.split(' ')[:3]
    if len(data) == 3:
        n = 0
        for i in data:
            if not i.isdigit():await bot.send(ev,'格式错误，应为[算分 vo da vi]');return
            data[n] = int(i)
            if int(i)>1500 or int(i)<1:await bot.send(ev,'属性值不合理，应在1~1500区间内');return
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
    if score < 8200:msg += f'A评价需要最终试验获得{score_caculate(10000-score)}分\nA+评价需要最终试验获得{score_caculate(11500-score)}分\nS评价需要最终试验获得{score_caculate(13000-score)}分'
    elif score < 9250:msg += f'最终试验1位即可达成A评价\nA+评价需要最终试验获得{score_caculate(11500-score)}分\nS评价需要最终试验获得{score_caculate(13000-score)}分'
    elif score < 9700:msg += f'A+评价需要最终试验获得{score_caculate(11500-score)}分\nS评价需要最终试验获得{score_caculate(13000-score)}分'
    elif score < 11200:msg += f'最终试验1位即可达成A+评价\nS评价需要最终试验获得{score_caculate(13000-score)}分'
    else:msg += f'最终试验1位即可达成S评价'
    await bot.send(ev,msg)

#以下假设第一名为7000分(1800)，第二名为5000分(1500)，第三名为2500分(750)
#初：第一名2600分(780)，第二名1600分(480)，第三名800分(240)
rank2score = {1:1700,2:900,3:500,4:0}

@sv.on_prefix('逆算分')
async def gkmas_score_in_caculate(bot,ev):
    texts:str = ev.message.extract_plain_text().strip()
    data = texts.split(' ')[:4]
    if len(data) == 4:
        n = 0
        for i in data:
            if not i.isdigit():await bot.send(ev,f'你输入的第{n+1}个参数不是数字');return
            data[n] = int(i)
            if int(i)>1500 or int(i)<1:
                if n <= 2:await bot.send(ev,f'你输入的第{n+1}个属性值不在1~1500区间内');return
            n += 1
    else: await bot.send(ev,'格式错误，应为[逆算分 vo da vi 最终评价分](无需中括号)');return
    vo,da,vi,score_r = data
    state = vo+da+vi
    score = int(state*2.3)
    diff = score_r - score
    if diff < 0:await bot.send(ev,'最终评价分不合理');return
    elif diff< 750:rank = 4
    elif diff<1500+900:rank = 3
    elif diff<1800+1700:rank = 2
    else:rank = 1
    if score_r < 10000:
        if diff < 240:rank0 =4
        elif diff<480+500:rank0 = 3
        elif diff<780+1700:rank0 = 2
        else:rank0 = 1
        data = [f'您的面板为{state}',f'最终试验取得了:  \r{score_caculate(diff-rank2score[rank])}~{score_caculate(diff+1-rank2score[rank])-1}分({rank}位)(pro模式)  \r',f'{score_caculate(diff-rank2score[rank0])}~{score_caculate(diff+1-rank2score[rank0])-1}分({rank0}位)(regular模式)']
    else:
        data = [f'您的面板为{state}',f'最终试验取得了:  \r{score_caculate(diff-rank2score[rank])}~{score_caculate(diff+1-rank2score[rank])-1}分({rank}位)  \r','仅pro模式适用']
    msg = MD_gen1(data,button)
    await bot.send(ev,msg)

pro_rank_score = {1:7000,2:5000,3:2500,4:0}
regular_rank_score = {1:2600,2:1600,3:800,4:0}

def score_by_rank(rank,vo,da,vi,score_r):
    ex = {1:30,2:20,3:10,4:0}
    ex = ex[rank]
    flu = 0
    if 1500-vo <=ex:flu += vo-(1500-ex)
    if 1500-da <=ex:flu += da-(1500-ex)
    if 1500-vi <=ex:flu += vi-(1500-ex)
    state = vo+da+vi
    state_end = state+ex*3-flu
    score = int(state_end*2.3)
    diff = score_r - score
    return rank,score_caculate(diff-rank2score[rank]),score_caculate(diff+1-rank2score[rank])-1,state,state_end

str_score = {
    'b':6000,
    'b+':8000,
    'a':10000,
    'a+':11500,
    's':13000,
    's+':14500
}

@sv.on_prefix('算目标分')
async def gkmas_score_ta_caculate(bot,ev):
    texts:str = ev.message.extract_plain_text().strip()
    data = texts.split(' ')[:4]
    if len(data) == 4:
        n = 0
        for i in data:
            if not i.isdigit()and n<=2:await bot.send(ev,f'你输入的第{n+1}个参数不是数字');return
            if n == 3 and not i.isdigit():
                if i.lower() not in ['b','b+','a','a+','s','s+']:await bot.send(ev,f'你输入的目标评价分不是数字或B/B+/A/A+/S/S+');return
                else:
                    score_r = str_score[i.lower()]
            else:score_r = int(i)
            if n <= 2:
                data[n] = int(i)
                if int(i)>1500 or int(i)<1:
                    await bot.send(ev,f'你输入的第{n+1}个属性值不在1~1500区间内');return
            n += 1
    else: await bot.send(ev,'格式错误，应为[算目标分 vo da vi 目标评价分]');return
    vo,da,vi = data[:3]
    #把所有排位结果计算出来
    pro_result = {rank:score_by_rank(rank,vo,da,vi,score_r) for rank in range(1,5)}
    result_pro = []
    result_regular = []
    for rank in range(1,5):
        if pro_result[rank][1] > pro_rank_score[rank]:
            result_pro.append(pro_result[rank])
            break
    if score_r < 10000:
        regular_result = {rank:score_by_rank(rank,vo,da,vi,score_r) for rank in range(1,5)}
        for rank in range(1,5):
            if regular_result[rank][1] > regular_rank_score[rank]:
                result_regular.append(regular_result[rank])
                break
        if not result_regular:
            result_regular.append(regular_result[4])
    else:
        if not result_pro:
            result_pro.append(pro_result[4])
    if not result_regular:
        if len(result_pro) == 1:
            result = result_pro[0]
            if result[0]!=1:
                rank = result[0]
                if pro_rank_score[rank-1] < result[1]:
                    data = [f'您的预计面板为{result[3]}→{result[4]}',f'达到目标评价以上需要在最终试验取得{rank-1}位(预计{pro_rank_score[rank-1]}分)  \r',f'仅pro模式适用,注意：你无法精确获得此评价分']
                    await bot.finish(ev,MD_gen1(data,button))
            data = [f'您的预计面板为{result[3]}→{result[4]}',f'达到目标评价需要在最终试验获得:  \r{result[1]}~{result[2]}分({result[0]}位)  \r',f'仅pro模式适用']
            await bot.send(ev,MD_gen1(data,button))
        else:return
    elif not result_pro:
        if len(result_regular) == 1:
            result = result_regular[0]
            if result[0]!=1:
                rank = result[0]
                if regular_rank_score[rank-1] < result[1]:
                    data = [f'您的预计面板为{result[3]}→{result[4]}',f'达到目标评价以上需要在最终试验取得{rank-1}位(预计{regular_rank_score[rank-1]}分)  \r',f'仅regular模式适用,注意：你无法精确获得此评价分']
                    await bot.finish(ev,MD_gen1(data,button))
            data = [f'您的预计面板为{result[3]}→{result[4]}',f'达到目标评价需要在最终试验获得:  \r{result[1]}~{result[2]}分({result[0]}位)  \r',f'仅regular模式适用,如果你是pro模式,说明你的目标评价太低了']
            await bot.send(ev,MD_gen1(data,button))
        else:return
    else:
        data = ['计算结果(pro&regular模式)','','']
        result = result_pro[0]
        if result[0]!=1:
            rank = result[0]
            if pro_rank_score[rank-1] < result[1]:
                data[1] += f'您的预计面板为{result[3]}→{result[4]}(pro模式)({rank-1}位)  \r    达到目标评价以上需要在最终试验取得{rank-1}位(预计{pro_rank_score[rank-1]}分)  \r注意：你无法精确获得此评价分  \r'
            else:
                data[1] +=  f'您的预计面板为{result[3]}→{result[4]}(pro模式)({result[0]}位)  \r    达到目标评价需要在最终试验获得:  \r{result[1]}~{result[2]}分  \r'
        else:
            data[1] +=  f'您的预计面板为{result[3]}→{result[4]}(pro模式)({result[0]}位)  \r    达到目标评价需要在最终试验获得:  \r{result[1]}~{result[2]}分  \r'
        result = result_regular[0]
        if result[0]!=1:
            rank = result[0]
            if regular_rank_score[rank-1] < result[1]:
                data[2] += f'您的预计面板为{result[3]}→{result[4]}(regular模式)({rank-1}位)  \r    达到目标评价以上需要在最终试验取得{rank-1}位(预计{regular_rank_score[rank-1]}分)  \r注意：你无法精确获得此评价分  \r'
            else:
                data[2] +=  f'您的预计面板为{result[3]}→{result[4]}(regular模式)({i[0]}位)  \r    达到目标评价需要在最终试验获得:  \r{result[1]}~{result[2]}分  \r'
        else:
            data[2] +=  f'您的预计面板为{result[3]}→{result[4]}(regular模式)({result[0]}位)  \r    达到目标评价需要在最终试验获得:  \r{result[1]}~{result[2]}分  \r'
        await bot.send(ev,MD_gen1(data,button))

def is_float(self):
    try:
        float(self)
        return True
    except ValueError:
        return False


@sv.on_prefix('算加练')
async def gkmas_oiko_caculate(bot,ev):
    texts:str = ev.message.extract_plain_text().strip()
    data = texts.split(' ')[:6]
    err = """格式错误，正确格式应为
三属性计算：[算加练 vo vo% da da% vi vi%]
单属性计算：[算加练 某一属性 该属性加成%]
无需中括号，百分号可省略"""
    if len(data) == 2:
        if not data[0].isdigit():await bot.send(ev,err);return
        state = int(data[0])
        if data[1].endswith('%'):
            state_p = data[1][:-1]
        elif data[1].endswith('％'):
            state_p = data[1][:-1]
        else:state_p = data[1]
        if not is_float(state_p):await bot.send(ev,err);return
        state_p = float(state_p) + 100
        state_end_1 = state + int(state_p*310/100)
        if state_end_1 > 1500:state_end_1 = 1500
        state_end_2 = state + int(state_p*145/100)
        if state_end_2 > 1500:state_end_2 = 1500
        data = [f'主训练→{state_end_1}',f'副训练→{state_end_2}  \r','未考虑s卡课后加值']
        await bot.finish(ev,MD_gen1(data,button));return
    elif len(data) == 6:
        vo,vo_p,da,da_p,vi,vi_p = data
        for i in data:
            if (i.endswith('%') and not is_float(i[:-1])) or (i.endswith('％') and not is_float(i[:-1])) or not is_float(i):await bot.send(ev,err);return
        if vo_p.endswith('%'):vo_p = vo_p[:-1]
        if vo_p.endswith('％'):vo_p = vo_p[:-1]
        if da_p.endswith('%'):da_p = da_p[:-1]
        if da_p.endswith('％'):da_p = da_p[:-1]
        if vi_p.endswith('%'):vi_p = vi_p[:-1]
        if vi_p.endswith('％'):vi_p = vi_p[:-1]
        vo, vo_p, da, da_p, vi, vi_p = map(float, [vo, vo_p, da, da_p, vi, vi_p])
        vo_p += 100;da_p += 100;vi_p += 100
        f1 = lambda x,y:int(x)+int(y*310/100) if x+int(y*310/100)<1500 else 1500
        f2 = lambda x,y:int(x)+int(y*145/100) if x+int(y*145/100)<1500 else 1500
        f3 = lambda x:int(x+30) if x+30<1500 else 1500
        state_end_vo = f1(vo,vo_p) + f2(da,da_p) + f2(vi,vi_p)
        _state_end_vo = f3(f1(vo,vo_p)) + f3(f2(da,da_p)) + f3(f2(vi,vi_p))
        state_end_da = f2(vo,vo_p) + f1(da,da_p) + f2(vi,vi_p)
        _state_end_da = f3(f2(vo,vo_p)) + f3(f1(da,da_p)) + f3(f2(vi,vi_p))
        state_end_vi = f2(vo,vo_p) + f2(da,da_p) + f1(vi,vi_p)
        _state_end_vi = f3(f2(vo,vo_p)) + f3(f2(da,da_p)) + f3(f1(vi,vi_p))
        state = {"vo":state_end_vo,"da":state_end_da,"vi":state_end_vi}
        _state = {"vo":_state_end_vo,"da":_state_end_da,"vi":_state_end_vi}
        trt = {"vo":[f1,f2,f2],"da":[f2,f1,f2],"vi":[f2,f2,f1]}
        max_state = max(_state,key=_state.get)
        data = [f'建议选择{max_state}训练',f'训练后面板:{state[max_state]}→{_state[max_state]}  \rvo:{int(vo)}→{trt[max_state][0](vo,vo_p)}  \rda:{int(da)}→{trt[max_state][1](da,da_p)}  \rvi:{int(vi)}→{trt[max_state][2](vi,vi_p)}  \r',f'未考虑s卡课后加值']
        await bot.finish(ev,MD_gen1(data,button))
    else: await bot.send(ev,err);return