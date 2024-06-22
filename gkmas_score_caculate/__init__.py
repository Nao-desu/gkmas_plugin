#算分

from hoshino import Service
sv = Service('gkmas_score_caculate')

def score_caculate(score:int):
    if score <= 1500:return int(score/0.3)
    elif score <= 2250:return int((score-1500)/0.15) + 5000
    elif score <= 3050:return int((score-2250)/0.08) + 10000
    elif score <= 3450:return int((score-3050)/0.04) + 20000
    elif score <= 3650:return int((score-3450)/0.02) + 30000
    else:return int((score-3650)/0.01) + 40000

@sv.on_prefix('算分','查分')
async def gkmas_score_caculate(bot,ev):
    texts:str = ev.message.extract_plain_text().strip()
    data = texts.split(' ')
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

#以下假设第一名为7000分(1800)，第二名为5000分(1500)，第三名为2500(750)分

rank2score = {1:1700,2:900,3:500,4:0}

@sv.on_prefix('逆算分')
async def gkmas_score_in_caculate(bot,ev):
    texts:str = ev.message.extract_plain_text().strip()
    data = texts.split(' ')
    if len(data) == 4:
        n = 0
        for i in data:
            if not i.isdigit():await bot.send(ev,'格式错误，应为[逆算分 vo da vi 最终评价分]');return
            data[n] = int(i)
            if int(i)>1500 or int(i)<1:
                if n <= 2:await bot.send(ev,'属性值不合理，应在1~1500区间内');return
            n += 1
    else: await bot.send(ev,'格式错误，应为[逆算分 vo da vi 最终评价分]');return
    vo,da,vi,score_r = data
    state = vo+da+vi
    score = int(state*2.3)
    diff = score_r - score
    if diff < 0:await bot.send(ev,'最终评价分不合理');return
    elif diff< 750:rank = 4
    elif diff<1500:rank = 3
    elif diff<1800:rank = 2
    else:rank = 1
    msg = f'您的面板为{state}\n最终试验取得了:\n    {score_caculate(diff+rank2score[rank-1])}~{score_caculate(diff+1+rank2score[rank-1])-1}分({rank}位)\n(pro模式适用)'
    await bot.send(ev,msg)

@sv.on_prefix('算目标分')
async def gkmas_score_ta_caculate(bot,ev):
    texts:str = ev.message.extract_plain_text().strip()
    data = texts.split(' ')
    if len(data) == 4:
        n = 0
        for i in data:
            if not i.isdigit():await bot.send(ev,'格式错误，应为[算目标分 vo da vi 最终评价分]');return
            data[n] = int(i)
            if int(i)>1500 or int(i)<1:
                if n <= 2:await bot.send(ev,'属性值不合理，应在1~1500区间内');return
            n += 1
    else: await bot.send(ev,'格式错误，应为[算目标分 vo da vi 最终评价分]');return
    vo,da,vi,score_r = data
    state = vo+da+vi
    flu = 0
    if 1500-vo <=30:flu += vo-1470
    if 1500-da <=30:flu += da-1470
    if 1500-vi <=30:flu += vi-1470
    msg = f'您的面板为{state}→{state+90-flu}(+{90-flu})\n'
    score = int((state+90-flu)*2.3)
    diff = score_r - score
    if diff < 0:await bot.send(ev,'已达到目标评价！\n(仅pro模式适用)');return
    elif diff< 750:rank = 4
    elif diff<1500:rank = 3
    elif diff<1800:rank = 2
    else:rank = 1
    msg = f'达到目标评价需要在最终试验获得:\n    {score_caculate(diff+rank2score[rank-1])}~{score_caculate(diff+1+rank2score[rank-1])-1}分({rank}位)\n(仅pro模式适用)'
    await bot.send(ev,msg)

@sv.on_prefix('算加练')
async def gkmas_oiko_caculate(bot,ev):
    texts:str = ev.message.extract_plain_text().strip()
    data = texts.split(' ')
    err = '格式错误，应为[算加练 vo vo% da da% vi vi%]\n或[算加练 某一属性 该属性加成%](%可省略)'
    if len(data) == 2:
        if not data[0].isdigit():await bot.send(ev,err);return
        state = int(data[0])
        if data[1].endswith('%'):
            state_p = data[1][:-1]
        else:state_p = data[1]
        if not state_p.isdigit():await bot.send(ev,err);return
        state_p = int(state_p) + 1
        state_end_1 = state + int(state_p*310/100)
        if state_end_1 > 1500:state_end_1 = 1500
        state_end_2 = state + int(state_p*145/100)
        if state_end_2 > 1500:state_end_2 = 1500
        await bot.finish(ev,f'\n主训练→{state_end_1}\n副训练→{state_end_2}');return
    elif len(data) == 6:
        vo,vo_p,da,da_p,vi,vi_p = data
        for i in data:
            if not i.isdigit() or (i.endswith('%') and not i[:-1].isdigit()):await bot.send(ev,err);return
        if vo_p.endswith('%'):vo_p = vo_p[:-1]
        if da_p.endswith('%'):da_p = da_p[:-1]
        if vi_p.endswith('%'):vi_p = vi_p[:-1]
        vo, vo_p, da, da_p, vi, vi_p = map(int, [vo, vo_p, da, da_p, vi, vi_p])
        vo_p += 1
        da_p += 1
        vi_p += 1
        f1 = lambda x,y:x+int(y*310/100) if x+int(y*310/100)<1500 else 1500
        f2 = lambda x,y:x+int(y*145/100) if x+int(y*145/100)<1500 else 1500
        f3 = lambda x:x+30 if x+30<1500 else 1500
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
        msg = f'建议选择{max_state}训练\n训练后面板:{state[max_state]}→{_state[max_state]}\nvo:{vo}→{trt[max_state][0](vo,vo_p)}\nda:{da}→{trt[max_state][1](da,da_p)}\nvi:{vi}→{trt[max_state][2](vi,vi_p)}\n(未考虑s卡加值)'
        await bot.finish(ev,msg)
    else: await bot.send(ev,err);return