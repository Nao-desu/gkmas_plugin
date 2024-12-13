try:
    from .config import *
except:
    from  config import *

def evaluation2score(evaluation:int) -> int:
    if evaluation <= 1500:return int(evaluation/0.3)
    elif evaluation <= 2250:return int((evaluation-1500)/0.15) + 5000
    elif evaluation <= 3050:return int((evaluation-2250)/0.08) + 10000
    elif evaluation <= 3450:return int((evaluation-3050)/0.04) + 20000
    elif evaluation <= 3650:return int((evaluation-3450)/0.02) + 30000
    else:return int((evaluation-3650)/0.01) + 40000
    
def score2evaluation(score:int) -> int:
    if score <= 5000:return int(score*0.3)
    elif score <= 10000:return int((score-5000)*0.15) + 1500
    elif score <= 20000:return int((score-10000)*0.08) + 2250
    elif score <= 30000:return int((score-20000)*0.04) + 3050
    elif score <= 40000:return int((score-30000)*0.02) + 3450
    else:return int((score-40000)*0.01) + 3650

def final_panel(data:list, mode:str, order:int) -> int:
    max_panel = MAX_PANEL[mode]
    return sum(min(max_panel,i + (4-order)*10) for i in data)

def caculate_by_mode(mode:str, data:list) -> str:
    result = f"{mode}模式:\n"
    rank_list = MODE_RANK_RANGE[mode]
    for rank in rank_list:
        rank_result = {}
        for order in range(4,0,-1):
            panel = final_panel(data, mode, order)
            evaluation_required = RANK_2_EVALUATION[rank] - int(panel*2.3) - ORDER_2_EVALUATION[order]
            score = evaluation2score(evaluation_required)
            if score < 0:score = 0
            if order != 1 and score in range(CONTEST_RIVALS_SCORE_RANGE[mode][order][0],CONTEST_RIVALS_SCORE_RANGE[mode][order][1]):
                rank_result[order] = score
            elif order == 1 and score in range(CONTEST_RIVALS_SCORE_RANGE[mode][1][0],RANK_MAX_SCORE[rank]):
                rank_result[order] = score
            elif score < CONTEST_RIVALS_SCORE_RANGE[mode][order][0]:
                rank_result[order] = 0
        if rank_result:
            all_order = list(rank_result.keys())
            if len(all_order) > 1:
                for i in range(len(all_order)-1,0,-1):
                    if rank_result[all_order[i]] == 0 and rank_result[all_order[i-1]] == 0:
                        del rank_result[all_order[i]]
            result += f"{rank} → "
            for order in rank_result:
                order_txt = f"({order}位)" if order != 4 else "(不合格)"
                if order == 1 and rank_result[order] > CONTEST_RIVALS_SCORE_RANGE[mode][1][1]:
                    order_txt = ""
                result += f"{rank_result[order]}{order_txt}" if rank_result[order] != 0 else f"{order}位"
                result += "/"
            result = result[:-1] + "\n"
    if result == f"{mode}模式:\n":
        return ""
    return result

def reverse_caculate_by_mode(mode:str, data:list):
    evaluation = data[-1]
    panel = sum(data[:-1])
    diff = evaluation - int(panel*2.3)
    if diff < 0:
        return False,""
    if diff < ORDER_2_EVALUATION[3] + score2evaluation(CONTEST_RIVALS_SCORE_RANGE[mode][3][0]):order = 4
    elif diff < ORDER_2_EVALUATION[2] + score2evaluation(CONTEST_RIVALS_SCORE_RANGE[mode][2][0]):order = 3
    elif diff < ORDER_2_EVALUATION[1] + score2evaluation(CONTEST_RIVALS_SCORE_RANGE[mode][1][0]):order = 2
    else:order = 1
    order_txt = f"({order}位)" if order != 4 else "(不合格)"
    if order == 1 and evaluation2score(diff-ORDER_2_EVALUATION[order]) > CONTEST_RIVALS_SCORE_RANGE[mode][1][1]:
        order_txt = ""
    result = f"{mode}模式:{evaluation2score(diff-ORDER_2_EVALUATION[order])}~{evaluation2score(diff+1-ORDER_2_EVALUATION[order])-1}分{order_txt}\r"
    return True,result

def target_caculate_by_mode(mode:str, data:list) -> str:
    target_evaluation = data[-1]
    panel = sum(data[:-1])
    diff = target_evaluation - int(panel*2.3)
    if diff < 0:
        return f"{mode}模式:0分(不合格)"
    order_result = {}
    for order in range(4,0,-1):
        score = evaluation2score(target_evaluation - ORDER_2_EVALUATION[order]- int(final_panel(data[:-1], mode, order)*2.3))
        if score < 0:score = 0
        if order != 1:
            if score in range(CONTEST_RIVALS_SCORE_RANGE[mode][order][0],CONTEST_RIVALS_SCORE_RANGE[mode][order][1]):
                order_result[order] = score
            elif score < CONTEST_RIVALS_SCORE_RANGE[mode][order][0]:
                order_result[order] = 0
        else:
            if score < CONTEST_RIVALS_SCORE_RANGE[mode][1][0]:
                order_result[order] = 0
            else:
                order_result[order] = score
    result = ""
    if order_result:
        all_order = list(order_result.keys())
        if len(all_order) > 1:
            for i in range(len(all_order)-1,0,-1):
                if order_result[all_order[i]] == 0 and order_result[all_order[i-1]] == 0:
                    del order_result[all_order[i]]
        result = f"{mode}模式:"
        for order in order_result:
            order_txt = f"({order}位)" if order != 4 else "(不合格)"
            if order == 1 and order_result[order] > CONTEST_RIVALS_SCORE_RANGE[mode][1][1]:
                order_txt = ""
            result += f"{order_result[order]}{order_txt}" if order_result[order] != 0 else f"{order}位"
            result += "/"
        result = result[:-1] + "\r"
    return result

def oikomi_caculate_3_by_mode(mode:str, data:list) -> str:
    main_panel,sub_panel = OIKOMI_PANEL[mode]
    max_panel = MAX_PANEL[mode]
    f_main = lambda x,y:min(max_panel,int(x+main_panel*(y/100 + 1))+30)
    f_sub = lambda x,y:min(max_panel,int(x+sub_panel*(y/100 + 1))+30)
    vo_result = f_main(data[0],data[1]) + f_sub(data[2],data[3]) + f_sub(data[4],data[5])
    da_result = f_sub(data[0],data[1]) + f_main(data[2],data[3]) + f_sub(data[4],data[5])
    vi_result = f_sub(data[0],data[1]) + f_sub(data[2],data[3]) + f_main(data[4],data[5])
    max_result = max(vo_result,da_result,vi_result)
    if vo_result == max_result:
        lesson = "vo"
    elif da_result == max_result:
        lesson = "da"
    else:
        lesson = "vi"
    result = f"{mode}模式:建议选择{lesson}加练\r"
    result += f"vo:{vo_result}" + (f"(-{max_result-vo_result})," if vo_result != max_result else ",")
    result += f"da:{da_result}" + (f"(-{max_result-da_result})," if da_result != max_result else ",")
    result += f"vi:{vi_result}" + (f"(-{max_result-vi_result})" if vi_result != max_result else "")
    return result + "\r"

def oikomi_caculate_1_by_mode(mode:str, data:list) -> str:
    main_panel,sub_panel = OIKOMI_PANEL[mode]
    max_panel = MAX_PANEL[mode]
    result = f"{mode}模式:\r主训练:{min(max_panel,int(data[0]+main_panel*(data[1]/100 + 1)))},副训练:{min(max_panel,int(data[0]+sub_panel*(data[1]/100 + 1)))}\r"
    return result
    
if __name__ == '__main__':
    while True:
        type = "5"#input("输入模式(1=算分,2=逆算分,3=算目标分,4=算加练(三属性),5=算加练(单属性))")
        data = input("输入数据(用空格分隔):").split()
        if type == "1":print(caculate_by_mode("master", [int(i) for i in data]))
        elif type == "2":print(reverse_caculate_by_mode("master", [int(i) for i in data]))
        elif type == "3":print(target_caculate_by_mode("master", [int(i) for i in data]))
        elif type == "4":print(oikomi_caculate_3_by_mode("master", [int(i) for i in data]))
        elif type == "5":print(oikomi_caculate_1_by_mode("master", [int(i) for i in data]))
        else:print("输入错误")