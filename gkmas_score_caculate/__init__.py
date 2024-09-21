#算分

from hoshino import Service
from ..MDgen import *
from ...groupmaster.switch import sdb

sv = Service('gkmas_score_caculate')

def score_caculate(score:int):
    if score <= 1500:return int(score/0.3)
    elif score <= 2250:return int((score-1500)/0.15) + 5000
    elif score <= 3050:return int((score-2250)/0.08) + 10000
    elif score <= 3450:return int((score-3050)/0.04) + 20000
    elif score <= 3650:return int((score-3450)/0.02) + 30000
    else:return int((score-3650)/0.01) + 40000

def r_score_caculate(score:int):
    s = 0
    if score <= 5000:return int(score*0.3)
    s += 1500;score -= 5000
    if score <= 5000:return int(s + score*0.15)
    s += 750;score -= 5000
    if score <= 10000:return int(s + score*0.08)
    s += 800;score -= 10000
    if score <= 10000:return int(s + score*0.04)
    s += 400;score -= 10000
    if score <= 10000:return int(s + score*0.02)
    s += 200;score -= 10000
    return int(s + score*0.01)

def cacu_pro(vo,da,vi):
    msg = 'pro模式:\r'
    state = vo+da+vi
    flu = 0
    if 1500-vo <=30:flu += vo-1470
    if 1500-da <=30:flu += da-1470
    if 1500-vi <=30:flu += vi-1470
    score = 1700 + int((state+90-flu)*2.3)
    if score < 8200:msg += f'A评价需要最终试验获得{score_caculate(10000-score)}分\rA+评价需要最终试验获得{score_caculate(11500-score)}分\rS评价需要最终试验获得{score_caculate(13000-score)}分'
    elif score < 9250:msg += f'最终试验1位即可达成A评价\rA+评价需要最终试验获得{score_caculate(11500-score)}分\rS评价需要最终试验获得{score_caculate(13000-score)}分'
    elif score < 9700:msg += f'A+评价需要最终试验获得{score_caculate(11500-score)}分\rS评价需要最终试验获得{score_caculate(13000-score)}分'
    elif score < 11200:msg += f'最终试验1位即可达成A+评价\rS评价需要最终试验获得{score_caculate(13000-score)}分'
    else:msg += f'最终试验1位即可达成S评价'
    return msg

def cacu_master(vo,da,vi):
    msg = 'master模式:\r'
    state = vo+da+vi
    #1位20000分,2位12000,3位7000
    flu1 = 0
    flu2 = 0
    flu3 = 0
    if 1800 - vo <= 30:flu1 += vo - 1770
    if 1800 - da <= 30:flu1 += da - 1770
    if 1800 - vi <= 30:flu1 += vi - 1770
    if 1800 - vo <= 20:flu2 += vo - 1780
    if 1800 - da <= 20:flu2 += da - 1780
    if 1800 - vi <= 20:flu2 += vi - 1780
    if 1800 - vo <= 10:flu3 += vo - 1790
    if 1800 - da <= 10:flu3 += da - 1790
    if 1800 - vi <= 10:flu3 += vi - 1790
    score1 = 1700 + int((state+90-flu1)*2.3)
    score2 = 900 + int((state+90-flu2)*2.3)
    score3 = 500 + int((state+90-flu3)*2.3)
    if score_caculate(11500-score1) < 15000:
        if score_caculate(11500-score2) > 20000:
            msg += '最终试验1位即可达成A+评价\r'
        else:
            if score_caculate(11500-score2) < 12000:
                if score_caculate(11500-score3) > 12000:
                    msg += '最终试验2位即可达成A+评价\r'
                elif score_caculate(11500-score2) > 15000:
                    msg += f'A+评价需要最终试验1位或获得{score_caculate(11500-score2)}分(2位)\r'
                else:
                    if score_caculate(11500-score3) < 7000:
                        msg += '最终试验3位即可达成A+评价\r'
                    else:
                        msg += f'A+评价需要最终试验获得{score_caculate(11500-score3)}分(3位)\r'
            else:
                msg += f'A+评价需要最终试验获得{score_caculate(11500-score2)}分(2位)\r'
    else:
        if score_caculate(11500-score1) < 20000:
            if score_caculate(11500-score2) < 20000:
                msg += f'A+评价需要最终试验获得{score_caculate(11500-score1)}分(1位)/{score_caculate(11500-score2)}分(2位)\r'
            else:
                msg += f'A+评价需要最终试验获得{score_caculate(11500-score1)}分(1位)\r'
        else:
            msg += f'A+评价需要最终试验获得{score_caculate(11500-score1)}分\r'
    if score_caculate(13000-score1) < 15000:
        if score_caculate(13000-score2) > 20000:
            msg += '最终试验1位即可达成S评价\r'
        elif score_caculate(13000-score2) > 15000:
            msg += f'S评价需要最终试验1位或获得{score_caculate(13000-score2)}分(2位)\r'
        else:
            if score_caculate(13000-score2) < 12000:
                if score_caculate(13000-score3) > 12000:
                    msg += '最终试验2位即可达成S评价\r'
                else:
                    if score_caculate(13000-score3) < 7000:
                        msg += '最终试验3位即可达成S评价\r'
                    else:
                        msg += f'S评价需要最终试验获得{score_caculate(13000-score3)}分(3位)\r'
            else:
                msg += f'S评价需要最终试验获得{score_caculate(13000-score2)}分(2位)\r'
    else:
        if score_caculate(13000-score1) < 20000:
            if score_caculate(13000-score2) < 20000:
                msg += f'S评价需要最终试验获得{score_caculate(13000-score1)}分(1位)/{score_caculate(13000-score2)}分(2位)\r'
            else:
                msg += f'S评价需要最终试验获得{score_caculate(13000-score1)}分(1位)\r'
        else:
            msg += f'S评价需要最终试验获得{score_caculate(13000-score1)}分\r'
    if score_caculate(14500 - score1) < 20000:
        if score_caculate(14500 - score2) > 20000:
            msg += '最终试验1位即可达成S+评价\r'
        else:
            if score_caculate(14500 - score2) < 12000:
                if score_caculate(14500 - score3) > 12000:
                    msg += '最终试验2位即可达成S+评价\r'
                else:
                    if score_caculate(14500 - score3) < 7000:
                        msg += '最终试验3位即可达成S+评价\r'
                    else:
                        msg += f'S+评价需要最终试验获得{score_caculate(14500 - score3)}分(3位)\r'
            else:
                msg += f'S+评价需要最终试验获得{score_caculate(14500 - score2)}分(2位)\r'
    else:
        msg += f'S+评价需要最终试验获得{score_caculate(14500 - score1)}分\r'
    return msg

button = [
    {"buttons": [button_gen(False,'算分','算分'),button_gen(False,'逆算分','逆算分'),button_gen(False,'算目标分','算目标分')]},
    {"buttons": [button_gen(False,'算加练','算加练'),button_gen(True,'帮助','学马仕帮助')]}
]

@sv.on_prefix('算分','查分')
async def gkmas_score_caculate(bot,ev):
    status = sdb.get_status(ev.real_group_id,'算分')
    if not status:
        return
    texts:str = ev.message.extract_plain_text().strip()
    data = texts.split(' ')[:4]
    if len(data) == 3:
        n = 0
        for i in data:
            if not i.isdigit():await bot.send(ev,'格式错误，应为[算分 vo da vi 试验得分(可选)]');return
            data[n] = int(i)
            if int(i)>1800 or int(i)<1:await bot.send(ev,'属性值不合理，应在1~1800区间内');return
            n += 1
    elif len(data) == 4:
        n = 0
        for i in data:
            if not i.isdigit():await bot.send(ev,'格式错误，应为[算分 vo da vi 试验得分(可选)]');return
        vo,da,vi,score = data
        vo = int(vo)
        da = int(da)
        vi = int(vi)
        score = int(score)
        if int(vo)>1800 or int(vo)<1 or int(da)>1800 or int(da)<1 or int(vi)>1800 or int(vi)<1 :await bot.send(ev,'属性值不合理，应在1~1800区间内');return
        if int(score)<0:await bot.send(ev,'试验得分应为正数');return
        m = max(vo,da,vi)
        state = vo+da+vi
        data = [f'最终得分']
        if score > 20000:
            flu = 0
            if 1800 - vo <= 30: flu += vo - 1770
            if 1800 - da <= 30: flu += da - 1770
            if 1800 - vi <= 30: flu += vi - 1770
            m_score = 1700 + int((state + 90 - flu) * 2.3)
        elif score in range(12000,20000):
            flu = 0
            if 1800 - vo <= 20: flu += vo - 1780
            if 1800 - da <= 20: flu += da - 1780
            if 1800 - vi <= 20: flu += vi - 1780
            m_score = 900 + int((state + 60 - flu) * 2.3)
        elif score in range(7000,12000):
            flu = 0
            if 1800 - vo <= 10: flu += vo - 1790
            if 1800 - da <= 10: flu += da - 1790
            if 1800 - vi <= 10: flu += vi - 1790
            m_score = 500 + int((state + 30 - flu) * 2.3)
        else:
            m_score = 1700 + int((state)*2.3)
        data.append(f'master模式:{m_score + r_score_caculate(score)}')
        if m < 1500:
            if score > 7000:
                flu = 0
                if 1500 - vo <= 30: flu += vo - 1470
                if 1500 - da <= 30: flu += da - 1470
                if 1500 - vi <= 30: flu += vi - 1470
                m_score = 1700 + int((state + 90 - flu) * 2.3)
            elif score in range(5000,7000):
                flu = 0
                if 1500 - vo <= 20: flu += vo - 1480
                if 1500 - da <= 20: flu += da - 1480
                if 1500 - vi <= 20: flu += vi - 1480
                m_score = 900 + int((state + 60 - flu) * 2.3)
            elif score in range(2500,5000):
                flu = 0
                if 1500 - vo <= 10: flu += vo - 1490
                if 1500 - da <= 10: flu += da - 1490
                if 1500 - vi <= 10: flu += vi - 1490
                m_score = 500 + int((state + 30 - flu) * 2.3)
            else:
                m_score = int((state)*2.3)
            data[1] += f'\rpro模式:{m_score + r_score_caculate(score)}'
        data.append('如果不想更新旧版qq，可以使用[o算分]命令(原命令前加字母o)，可以输出旧版结果')
        msg = MD_gen1(data,button)
        await bot.send(ev,msg)
        return
    else: await bot.send(ev,'格式错误，应为[算分 vo da vi 试验得分(可选)]');return
    vo,da,vi = data
    m = max(vo,da,vi)
    data = [f'您的面板为{vo + da + vi}']
    if m > 1500:
        data.append(cacu_master(vo,da,vi))
    else:
        data.append(cacu_pro(vo,da,vi) + '\r' + cacu_master(vo,da,vi))
    data.append('如果不想更新旧版qq，可以使用[o算分]命令(原命令前加字母o)，可以输出旧版结果')
    msg = MD_gen1(data,button)
    await bot.send(ev,msg)

@sv.on_prefix('o算分','o查分')
async def gkmas_score_caculate(bot,ev):
    status = sdb.get_status(ev.real_group_id,'算分')
    if not status:
        return
    texts:str = ev.message.extract_plain_text().strip()
    data = texts.split(' ')[:3]
    if len(data) == 3:
        n = 0
        for i in data:
            if not i.isdigit():await bot.send(ev,'格式错误，应为[算分 vo da vi 试验得分(可选)]');return
            data[n] = int(i)
            if int(i)>1800 or int(i)<1:await bot.send(ev,'属性值不合理，应在1~1800区间内');return
            n += 1
    elif len(data) == 4:
        n = 0
        for i in data:
            if not i.isdigit():await bot.send(ev,'格式错误，应为[算分 vo da vi 试验得分(可选)]');return
        vo,da,vi,score = data
        vo = int(vo)
        da = int(da)
        vi = int(vi)
        score = int(score)
        if int(vo)>1800 or int(vo)<1 or int(da)>1800 or int(da)<1 or int(vi)>1800 or int(vi)<1 :await bot.send(ev,'属性值不合理，应在1~1800区间内');return
        if int(score)<0:await bot.send(ev,'试验得分应为正数');return
        m = max(vo,da,vi)
        state = vo+da+vi
        msg = f'最终得分\r'
        if score > 20000:
            flu = 0
            if 1800 - vo <= 30: flu += vo - 1770
            if 1800 - da <= 30: flu += da - 1770
            if 1800 - vi <= 30: flu += vi - 1770
            m_score = 1700 + int((state + 90 - flu) * 2.3)
        elif score in range(12000,20000):
            flu = 0
            if 1800 - vo <= 20: flu += vo - 1780
            if 1800 - da <= 20: flu += da - 1780
            if 1800 - vi <= 20: flu += vi - 1780
            m_score = 900 + int((state + 60 - flu) * 2.3)
        elif score in range(7000,12000):
            flu = 0
            if 1800 - vo <= 10: flu += vo - 1790
            if 1800 - da <= 10: flu += da - 1790
            if 1800 - vi <= 10: flu += vi - 1790
            m_score = 500 + int((state + 30 - flu) * 2.3)
        else:
            m_score = 0 + int((state)*2.3)
        msg += f'master模式:{m_score + r_score_caculate(score)}'
        if m < 1500:
            if score > 7000:
                flu = 0
                if 1500 - vo <= 30: flu += vo - 1470
                if 1500 - da <= 30: flu += da - 1470
                if 1500 - vi <= 30: flu += vi - 1470
                m_score = 1700 + int((state + 90 - flu) * 2.3)
            elif score in range(5000,7000):
                flu = 0
                if 1500 - vo <= 20: flu += vo - 1480
                if 1500 - da <= 20: flu += da - 1480
                if 1500 - vi <= 20: flu += vi - 1480
                m_score = 900 + int((state + 60 - flu) * 2.3)
            elif score in range(2500,5000):
                flu = 0
                if 1500 - vo <= 10: flu += vo - 1490
                if 1500 - da <= 10: flu += da - 1490
                if 1500 - vi <= 10: flu += vi - 1490
                m_score = 500 + int((state + 30 - flu) * 2.3)
            else:
                m_score = int((state)*2.3)
            msg += f'\rpro模式:{m_score + r_score_caculate(score)}'
        await bot.send(ev,msg)
        return
    else: await bot.send(ev,'格式错误，应为[算分 vo da vi 试验得分(可选)]');return
    vo,da,vi = data
    m = max(vo,da,vi)
    state = vo+da+vi
    msg = f'您的面板为{state}\r'
    if m > 1500:
        msg += cacu_master(vo,da,vi)
    else:
        msg += cacu_pro(vo,da,vi) + '\r' + cacu_master(vo,da,vi)
    await bot.send(ev,msg)

#假设master第一名为20000分(3050),第二名为12000分(2410),第三名为7000分(1800)
# 假设pro第一名为7000分(1800)，第二名为5000分(1500)，第三名为2500分(750)
#初：第一名2600分(780)，第二名1600分(480)，第三名800分(240)
rank2score = {1:1700,2:900,3:500,4:0}

@sv.on_prefix('逆算分')
async def gkmas_score_in_caculate(bot,ev):
    status = sdb.get_status(ev.real_group_id,'算分')
    if not status:
        return
    texts:str = ev.message.extract_plain_text().strip()
    data = texts.split(' ')[:4]
    if len(data) == 4:
        n = 0
        for i in data:
            if not i.isdigit():await bot.send(ev,f'你输入的第{n+1}个参数不是数字');return
            data[n] = int(i)
            if int(i)>1800 or int(i)<1:
                if n <= 2:await bot.send(ev,f'你输入的第{n+1}个属性值不在1~1800区间内');return
            n += 1
    else: await bot.send(ev,'格式错误，应为[逆算分 vo da vi 最终评价分](无需中括号)');return
    vo,da,vi,score_r = data
    data = [f'您的面板为{vo + da + vi}']
    state = vo+da+vi
    score = int(state*2.3)
    m = max(vo,da,vi)
    diff = score_r - score
    if diff < 0:await bot.send(ev,'最终评价分不合理');return
    msg = ''
    if diff < 1800 + 500:rank = 4
    elif diff< 2410 + 900:rank = 3
    elif diff< 3050 + 1700:rank = 2
    else:rank = 1
    msg += f'最终试验取得了:  \rmaster模式:{score_caculate(diff-rank2score[rank])}~{score_caculate(diff+1-rank2score[rank])-1}分({rank}位)\r'
    if m < 1500:
        if diff< 750+500:rank = 4
        elif diff<1500+900:rank = 3
        elif diff<1800+1700:rank = 2
        else:rank = 1
        msg += f'\rpro模式:{score_caculate(diff-rank2score[rank])}~{score_caculate(diff+1-rank2score[rank])-1}分({rank}位)\r'
    if m < 1000 and score_r < 10000:
        if diff< 240+500:rank = 4
        elif diff<480+900:rank = 3
        elif diff<780+1700:rank = 2
        else:rank = 1
        msg += f'\rregular模式:{score_caculate(diff-rank2score[rank])}~{score_caculate(diff+1-rank2score[rank])-1}分({rank}位)\r'
    data.append(msg)
    data.append('得分与排名关系仅供参考')
    msg = MD_gen1(data,button)
    await bot.send(ev,msg)

master_rank_score = {1:20000,2:12000,3:7000,4:0}
pro_rank_score = {1:7000,2:5000,3:2500,4:0}
regular_rank_score = {1:2600,2:1600,3:800,4:0}

def score_by_rank(rank,vo,da,vi,score_r,max):
    ex = {1:30,2:20,3:10,4:0}
    ex = ex[rank]
    flu = 0
    if max-vo <=ex:flu += vo-(max-ex)
    if max-da <=ex:flu += da-(max-ex)
    if max-vi <=ex:flu += vi-(max-ex)
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
    status = sdb.get_status(ev.real_group_id,'算分')
    if not status:
        return
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
                if int(i)>1800 or int(i)<1:
                    await bot.send(ev,f'你输入的第{n+1}个属性值不在1~1800区间内');return
            n += 1
    else: await bot.send(ev,'格式错误，应为[算目标分 vo da vi 目标评价分]');return
    vo,da,vi = data[:3]
    #把所有排位结果计算出来
    master_result = {rank:score_by_rank(rank,vo,da,vi,score_r,1800) for rank in range(1,5)}
    pro_result = {rank:score_by_rank(rank,vo,da,vi,score_r,1500) for rank in range(1,5)}
    regular_result = {rank:score_by_rank(rank,vo,da,vi,score_r,1000) for rank in range(1,5)}
    result_master = []
    result_pro = []
    result_regular = []
    for rank in range(1,5):
        if master_result[rank][1] > master_rank_score[rank]:
            result_master.append(master_result[rank])
            break
    for rank in range(1,5):
        if pro_result[rank][1] > pro_rank_score[rank]:
            result_pro.append(pro_result[rank])
            break
    for rank in range(1,5):
        if regular_result[rank][1] > regular_rank_score[rank]:
            result_regular.append(regular_result[rank])
            break
    if not result_master:
        result_master.append(master_result[4])
    if not result_pro:
        result_pro.append(pro_result[4])
    if not result_regular:
        result_regular.append(regular_result[4])
    m = max(vo,da,vi)
    data = ['计算结果']
    msg = ''
    result = result_master[0]
    rank = result[0]
    if rank == 1:
        msg += f'您的预计面板为{result[3]}→{result[4]}(master模式)\r   达到目标评价需要在最终试验获得:\r   {result[1]}~{result[2]}分\r'
    elif master_rank_score[rank-1] < result[1]:
        msg += f'您的预计面板为{result[3]}→{result[4]}(master模式)({rank}位)\r   达到目标评价以上需要在最终试验取得{rank-1}位(预计{master_rank_score[rank-1]}分)\r   注意：目标评价分过低，你无法精确获得此评价分\r'
    else:
        msg += f'您的预计面板为{result[3]}→{result[4]}(master模式)({rank}位)\r   达到目标评价需要在最终试验获得:\r   {result[1]}~{result[2]}分({rank}位)\r'
    if m < 1500:
        result = result_pro[0]
        rank = result[0]    
        if rank == 1:
            msg += f'您的预计面板为{result[3]}→{result[4]}(pro模式)\r   达到目标评价需要在最终试验获得:\r   {result[1]}~{result[2]}分\r'
        elif pro_rank_score[rank-1] < result[1]:
            msg += f'您的预计面板为{result[3]}→{result[4]}(pro模式)({rank}位)\r   达到目标评价以上需要在最终试验取得{rank-1}位(预计{pro_rank_score[rank-1]}分)\r   注意：目标评价分过低，你无法精确获得此评价分\r'
        else:
            msg += f'您的预计面板为{result[3]}→{result[4]}(pro模式)({rank}位)\r   达到目标评价需要在最终试验获得:\r   {result[1]}~{result[2]}分({rank}位)\r'
    if m < 1000 and score_r < 10000:
        result = result_regular[0]
        rank = result[0]
        if rank == 1:
            msg += f'您的预计面板为{result[3]}→{result[4]}(regular模式)\r   达到目标评价需要在最终试验获得:\r   {result[1]}~{result[2]}分\r'
        elif regular_rank_score[rank-1] < result[1]:
            msg += f'您的预计面板为{result[3]}→{result[4]}(regular模式)({rank}位)\r   达到目标评价以上需要在最终试验取得{rank-1}位(预计{regular_rank_score[rank-1]}分)\r   注意：目标评价分过低，你无法精确获得此评价分\r'
        else:
            msg += f'您的预计面板为{result[3]}→{result[4]}(regular模式)({rank}位)\r   达到目标评价需要在最终试验获得:\r   {result[1]}~{result[2]}分({rank}位)\r'
    data.append(msg)
    data.append('得分与排名关系仅供参考')
    msg = MD_gen1(data,button)
    await bot.send(ev,msg)

def is_float(self):
    try:
        float(self)
        return True
    except ValueError:
        return False


@sv.on_prefix('算加练')
async def gkmas_oiko_caculate(bot,ev):
    status = sdb.get_status(ev.real_group_id,'算分')
    if not status:
        return
    texts:str = ev.message.extract_plain_text().strip()
    data = texts.split(' ')[:6]
    err = """格式错误，正确格式应为
三属性计算：[算加练 vo vo% da da% vi vi%]
单属性计算：[算加练 某一属性 该属性加成%]
无需中括号和百分号"""
    if len(data) == 2:
        if not data[0].isdigit():await bot.send(ev,err);return
        state = int(data[0])
        state_p = data[1]
        if not is_float(state_p):await bot.send(ev,err);return
        state_p = float(state_p) + 100
        state_end_1 = state + int(state_p*310/100)
        if state_end_1 > 1800:state_end_1 = 1800
        state_end_2 = state + int(state_p*145/100)
        if state_end_2 > 1800:state_end_2 = 1800
        if state_end_1 <= 1500 and state_end_2 <= 1500:
            data = [f'计算结果',f'主训练→{state_end_1}  \r副训练→{state_end_2}  \r','未考虑s卡课后加值']
        else:
            data = [f'计算结果',f'master模式：\r  主训练→{state_end_1}  \r  副训练→{state_end_2}  \r','未考虑s卡课后加值']
            if state_end_1 > 1500:state_end_1 = 1500
            if state_end_2 > 1500:state_end_2 = 1500
            data[1] += f'pro模式：\r  主训练→{state_end_1}  \r  副训练→{state_end_2}  \r'
        await bot.finish(ev,MD_gen1(data,button));return
    elif len(data) == 6:
        _vo,vo_p,_da,da_p,_vi,vi_p = data.copy()
        for i in data:
            if not is_float(i):await bot.send(ev,err);return
        vo = float(_vo);vo_p = float(vo_p);da = float(_da);da_p = float(da_p);vi = float(_vi);vi_p = float(vi_p)
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
        _data = [f'建议选择{max_state}训练(pro模式)',f'训练后面板:{state[max_state]}→{_state[max_state]}(+{_state[max_state]-state[max_state]})  \rvo:{int(vo)}→{trt[max_state][0](vo,vo_p)}  \rda:{int(da)}→{trt[max_state][1](da,da_p)}  \rvi:{int(vi)}→{trt[max_state][2](vi,vi_p)}  \r',f'未考虑s卡课后加值']
        await bot.send(ev,MD_gen1(_data,button))
        _vo,vo_p,_da,da_p,_vi,vi_p = data.copy()
        vo = float(_vo);vo_p = float(vo_p);da = float(_da);da_p = float(da_p);vi = float(_vi);vi_p = float(vi_p)
        vo_p += 100;da_p += 100;vi_p += 100
        f1 = lambda x,y:int(x)+int(y*310/100) if x+int(y*310/100)<1800 else 1800
        f2 = lambda x,y:int(x)+int(y*145/100) if x+int(y*145/100)<1800 else 1800
        f3 = lambda x:int(x+30) if x+30<1800 else 1800
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
        _data = [f'建议选择{max_state}训练(master模式)',f'训练后面板:{state[max_state]}→{_state[max_state]}(+{_state[max_state]-state[max_state]})  \rvo:{int(vo)}→{trt[max_state][0](vo,vo_p)}  \rda:{int(da)}→{trt[max_state][1](da,da_p)}  \rvi:{int(vi)}→{trt[max_state][2](vi,vi_p)}  \r',f'未考虑s卡课后加值']
        await bot.send(ev,MD_gen1(_data,button))
    else: await bot.send(ev,err);return