# 整理 json 使用的工具
import csv
import json
# 執行 command 的時候用的
import os
# 匯入 正規表達式
import re
# 子處理程序，用來取代 os.system 的功能
import subprocess
import time
from pathlib import Path
# 強制等待 (執行期間休息一下)
from time import sleep

import numpy as np
import pandas as pd

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 普通傷害罪
T_277 = [
    '出於傷害', '傷害之犯意', '傷害之不確定故意', '具有主觀上傷害之犯意', '基於傷害', '傷害他人身體之犯意', '傷害人身體之犯意',
    '傷害人之身體之犯意', '之傷害', '等傷害', '受有起訴書所載之傷勢', '受有起訴書之所載傷勢'
]

# 傷害致重傷害
T_277_serious = [
    '客觀上可得預見', '客觀上雖可預見', '客觀上能預見', '承前傷害之犯意', '出於傷害', '傷害之犯意', '傷害之不確定故意',
    '具有主觀上傷害之犯意', '基於傷害', '傷害他人身體之犯意', '傷害人身體之犯意', '傷害人之身體之犯意', '在客觀情形下',
    '傷害之接續犯意', '能預見', '客觀上並可預見', '客觀上可以預見', '客觀上得預見', '應可預見', '客觀上應知悉', '而能預見',
    '智識能力正常之成年人', '智慮正常之成年人', '客觀上應可預見', '客觀上均應可預見', '客觀上可預見', '思慮成熟之成年人',
    '一般正常人之生活經驗', '客觀上知悉', '能預見', '客觀上應得預見', '客觀上應能預見', '之重傷害', '具相當智識程度之人',
    '有重大不治或難治之傷害', '重大不治之傷害', '重大難治之傷害', '之重大傷害', '等重傷害', '等重大傷害', '之重大傷害',
    '重大不治之重傷害', '重大難治之重傷害', '如犯罪事實所載之重傷害', '如犯罪事實所載重傷害', '已達重傷害之程度', '已達重傷害程度',
    '屬重大不治', '屬重大難治', '之重傷程度', '無法完全回復正常功能之可能', '受有重傷害', '受有重大傷害', '受有重大之傷害',
    '之重傷害程度', '之重傷程度', '之重傷害結果', '重傷害之結果', '重傷之結果'
    '之重傷結果'
]

# 傷害致死
T_277_death = [
    '客觀上可得預見', '客觀上雖可預見', '客觀上能預見', '出於傷害', '承前傷害之犯意', '傷害之犯意', '傷害之不確定故意',
    '具有主觀上傷害之犯意', '基於傷害', '傷害他人身體之犯意', '傷害人身體之犯意', '傷害人之身體之犯意', '在客觀情形下',
    '傷害之接續犯意', '能預見', '客觀上並可預見', '客觀上可以預見', '客觀上得預見', '應可預見', '客觀上應知悉', '而能預見',
    '具相當智識程度之人', '智識能力正常之成年人', '智慮正常之成年人', '客觀上應可預見', '客觀上均應可預見', '客觀上可預見',
    '思慮成熟之成年人', '一般正常人之生活經驗', '客觀上知悉', '能預見', '客觀上應得預見', '客觀上應能預見', '不治死亡',
    '傷重致死之結果', '宣告死亡', '窒息死亡', '呼吸衰竭死亡', '死亡結果', '死亡之結果', '而死亡', '休克死亡',
    '當場死亡', '倒地死亡', '死亡之嚴重結果'
]

# 傷直血
T_280 = [
    '家庭成員關係', '所定之家庭成員', '所定家庭成員', '出於傷害', '傷害之犯意', '傷害之不確定故意', '具有主觀上傷害之犯意',
    '基於傷害', '傷害他人身體之犯意', '傷害人身體之犯意', '傷害人之身體之犯意', '傷害直系血親尊親屬之接續犯意',
    '傷害直系血親尊親屬之犯意', '傷害直系血親尊親屬犯意', '之傷害', '等傷害', '受有起訴書所載之傷勢', '受有起訴書之所載傷勢'
]

# 傷直血致死
T_280_death = [
    '家庭成員關係', '所定之家庭成員', '所定家庭成員', '出於傷害', '傷害之犯意', '傷害之不確定故意', '具有主觀上傷害之犯意',
    '基於傷害', '傷害他人身體之犯意', '傷害人身體之犯意', '傷害人之身體之犯意', '傷害直系血親尊親屬之接續犯意',
    '傷害直系血親尊親屬之犯意', '傷害直系血親尊親屬犯意', '客觀上可得預見', '客觀上雖可預見', '客觀上能預見', '承前傷害之犯意',
    '傷害之犯意', '傷害之不確定故意', '具有主觀上傷害之犯意', '基於傷害', '傷害他人身體之犯意', '傷害人身體之犯意',
    '傷害人之身體之犯意', '在客觀情形下', '傷害之接續犯意', '能預見', '客觀上並可預見', '客觀上可以預見', '客觀上得預見',
    '應可預見', '客觀上應知悉', '而能預見', '具相當智識程度之人', '智識能力正常之成年人', '智慮正常之成年人', '客觀上應可預見',
    '客觀上均應可預見', '客觀上可預見', '思慮成熟之成年人', '一般正常人之生活經驗', '客觀上知悉', '能預見', '客觀上應得預見',
    '客觀上應能預見', '不治死亡', '傷重致死之結果', '宣告死亡', '窒息死亡', '呼吸衰竭死亡', '死亡結果', '死亡之結果',
    '而死亡', '休克死亡', '當場死亡', '倒地死亡', '死亡之嚴重結果'
]

# 重傷害罪
T_278 = [
    '重傷害之不確定故意', '重傷害之故意', '基於使人受重傷害之犯意', '重傷害之犯意', '重傷害不確定故意',
    '重傷害亦不違背其本意之不確定犯意', '之重傷害', '有重大不治或難治之傷害', '重大不治之傷害', '重大難治之傷害', '之重大傷害',
    '等重傷害', '等重大傷害', '之重大傷害', '重大不治之重傷害', '重大難治之重傷害', '如犯罪事實所載之重傷害',
    '如犯罪事實所載重傷害', '已達重傷害之程度', '已達重傷害程度', '屬重大不治', '屬重大難治', '之重傷程度',
    '無法完全回復正常功能之可能', '受有重傷害', '受有重大傷害', '受有重大之傷害', '之重傷害程度', '之重傷程度', '之重傷害結果',
    '重傷害之結果', '重傷之結果'
    '之重傷結果'
]

# 重傷害未遂
T_278_att = [
    '重傷害之不確定故意', '重傷害之故意', '基於使人受重傷害之犯意', '重傷害之犯意', '重傷害不確定故意',
    '重傷害亦不違背其本意之不確定犯意', '之重傷害結果而未遂', '未達毀敗或減損', '未達毀敗或嚴重減損', '如經過相當之診治而能回復原狀',
    '或雖不能回復原狀而僅減衰其效用者', '仍不得謂為該款之重傷', '未有重傷害結果', '應以未遂論', '重傷害程度而未遂'
]

# 重傷害致死
T_278_death = [
    '重傷害之不確定故意', '重傷害之故意', '基於使人受重傷害之犯意', '重傷害之犯意', '重傷害不確定故意',
    '重傷害亦不違背其本意之不確定犯意', '能預見', '客觀上並可預見', '客觀上可以預見', '客觀上得預見', '應可預見',
    '客觀上應知悉', '而能預見', '具相當智識程度之人', '智識能力正常之成年人', '智慮正常之成年人', '客觀上應可預見',
    '客觀上均應可預見', '客觀上可預見', '思慮成熟之成年人', '一般正常人之生活經驗', '客觀上知悉', '能預見', '客觀上應得預見',
    '客觀上應能預見', '不治死亡', '傷重致死之結果', '宣告死亡', '窒息死亡', '呼吸衰竭死亡', '死亡結果', '死亡之結果',
    '而死亡', '休克死亡', '當場死亡', '倒地死亡', '死亡之嚴重結果'
]

# 過失傷害
T_284 = [
    '無不能注意之情事', '無不能注意之情形', '竟疏未注意', '疏未注意上開注意義務', '違反上開注意義務', '違反前揭注意義務',
    '違反前開注意義務', '本應具有前揭注意義務', '本應具有前開注意義務', '本應具有上開注意義務', '本應審慎注意', '本應注意',
    '無不能注意之特別情事', '疏未注意', '疏未意及', '無不能注意之情狀', '非不能注意', '竟疏未'
]

# 過失傷害致重傷
T_284_serious = [
    '無不能注意之情事', '無不能注意之情形', '竟疏未注意', '疏未注意上開注意義務', '違反上開注意義務', '違反前揭注意義務',
    '違反前開注意義務', '本應具有前揭注意義務', '本應具有前開注意義務', '本應具有上開注意義務', '本應審慎注意', '本應注意',
    '無不能注意之特別情事', '疏未注意', '疏未意及', '無不能注意之情狀', '非不能注意', '竟疏未', '之重傷害',
    '有重大不治或難治之傷害', '重大不治之傷害', '重大難治之傷害', '之重大傷害', '等重傷害', '等重大傷害', '之重大傷害',
    '過失重傷害', '重大不治之重傷害', '重大難治之重傷害', '如犯罪事實所載之重傷害', '如犯罪事實所載重傷害', '已達重傷害之程度',
    '已達重傷害程度', '屬重大不治', '屬重大難治', '之重傷程度', '無法完全回復正常功能之可能', '受有重傷害', '受有重大傷害',
    '受有重大之傷害', '之重傷害程度', '之重傷程度', '之重傷害結果', '重傷害之結果', '重傷之結果'
    '之重傷結果'
]

# 無罪
Recht = [
    '尚符合正當防衛', '尚符合緊急避難', '尚符合父母懲戒權', '尚符合教師懲戒權', '符合正當防衛而阻卻違法', '符合緊急避難而阻卻違法',
    '無證據不得認定犯罪事實', '須經合法之調查程序', '屬有效必要之防衛行為', '不足為不利於被告之犯罪事實之認定',
    '不足為不利於被告事實之認定', '不足為不利於被告之事實認定'
]

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 加重減輕罪刑Feature
教育程度_list = ["國小畢業", "國小肄業", "初中畢業", "初中肄業", "國中畢業", "國中肄業"]

罪責1_list = ["為累犯", "行經行人穿越道不依規定", "道路交通管理處罰條例第86條"]
罪責2_list = [
    "爰依刑法第62條前段之規定", "符合自首要件", "瘖啞人士", "爰依刑法第20條規定減輕其刑", "爰依刑法第20條之規定減輕其刑",
    "刑法第59條規定之酌量減輕其刑", "自承其為肇事者", "與自首要件相符", "並願接受裁判", "發覺之前即自首", "嗣並接受裁判",
    "承認為肇事人而接受裁判", "客觀上足以引起一般同情"
]

傷害方式_list = [
    "以頭撞擊", "持筆刺", "劃向", "揮砍", "分持安全帽、木棍", "持安全帽", "持木棍", "持球棒攻擊", "以安全帽攻擊",
    "持甩棍毆打", "持水煙管毆打", "持竹棍毆打", "持剪刀", "刺擊", "刺中"
]

下手力道_list = ["力道非輕", "下手力道甚猛", "左手用力揮擊", "右手用力揮擊", "手段暴戾", "犯罪情節非輕"]

攻擊部位_list = ["朝人體要害攻擊", "朝人體要害之告訴人頭部攻擊"]

傷害結果1_list = [
    "閉鎖性骨折", "牙齒斷裂", "所受傷勢尚非甚鉅", "腓骨遠端骨折", "腓骨非移位線性骨折", "腓骨外踝非移位閉鎖性骨折", "傷勢非輕",
    "受傷非輕", "下顎骨骨折", "齒裂", "橈神經裂傷", "肌腱斷裂", "深度撕裂傷", "近端骨折", "橈神經撕裂傷",
    "所受傷害及遭強制程度非鉅", "掌骨骨折", "所受傷害非重", "所受傷害非鉅", "傷勢非重", "傷勢非鉅", "腸繫膜血腫", "穿刺傷",
    "刺傷", "肋骨骨折", "閉鎖性骨折合併韌帶撕裂"
]
傷害結果2_list = [
    "癲癇症", "顱骨穹窿開放性骨折併氣顱症", "小腸穿孔併血腹", "腹壁穿刺傷", "穿刺傷合併氣血胸", "小腸穿孔", "交通性水腦症",
    "十二指腸撕裂傷併後腹腔出血", "失語症", "頭部外傷併顱骨骨折", "顱內出血", "脛腓骨骨幹骨折"
]

犯後態度1_list = [
    "素行尚佳", "態度良好", "已見悔意", "向告訴人道歉", "尚能正視所為之不法", "深感後悔", "感到抱歉", "犯後態度尚佳",
    "素行良好", "主動傳訊息向告訴人道歉", "素行尚稱良好", "主動與告訴人聯絡並道歉"
]
犯後態度2_list = [
    "犯後態度不佳", "未見悔意", "態度不佳", "未能正視所為之不法", "矢口否認有何傷害犯行", "空言否認犯行", "顯屬推託卸責之詞",
    "絲毫未見悔意", "犯後態度明顯不佳", "卸責之詞", "飾詞卸責", "難認其有何悔意", "難認其有何悔意", "矢口否認有何過失"
]

坦承情況1_list = [
    "自始未坦承犯罪", "未坦承犯罪", "矢口否認", "矢口否認犯行", "始終否認犯行", "否認犯罪", "顯屬卸責之詞", "被告否認犯罪",
    "矢口卸責", "否認其犯行"
]
坦承情況2_list = ["先否認犯行", "才坦承犯行"]

賠償狀況1_list = ["賠償完畢"]
賠償狀況2_list = ["依約賠償中"]

經濟狀況_list = ["經濟貧寒", "家境困難"]

被告身心狀況_list = [
    "癲癇症", "良性陣發性眩暈", "頸椎退化性脊椎炎", "高血壓", "雙相情緒障礙症", "重度身心障礙", "輕度身心障礙",
    "中度身心障礙", "欠缺自我情緒管理能力", "瘖啞人士", "精神障礙", "心智缺陷", "領有身心障礙證明"
]

被害身心狀況_list = [
    "癲癇症", "頸椎退化性脊椎炎", "高血壓", "雙相情緒障礙症", "重度身心障礙", "輕度身心障礙", "中度身心障礙"
]

和解狀況1_list = [
    "無法達成和、調解", "無法達成和解", "無法達成調解", "告訴人無和解意願", "有與告訴人和解之意願", "沒有要跟被告和解",
    "未與告訴人達成和解", "未與告訴人達成調解", "未與告訴人達成調、和解", "未與告訴人達成和、調解", "未與告訴人和解",
    "願與告訴人和解", "未取得告訴人之原諒", "未取得告知人原諒", "未能獲告訴人原諒", "未能達成民事和解", "未達成和解",
    "告訴人並無調解意願", "無法與告訴人達成賠償金額合意", "告訴人嗣後表明無調解意願", "告訴人表明無調解意願", "尚未與告訴人達成民事賠償"
]
和解狀況2_list = ["已與告訴人和解", "表示願原諒被告", "達成和解"]

告訴人和被告人之關係_list = [
    "家庭成員關係", "有家庭暴力防治法第3條第4款規定之家庭成員關係", "有家庭暴力防治法第3條第1款規定之家庭成員關係",
    "有家庭暴力防治法第3條第2款規定之家庭成員關係", "有家庭暴力防治法第3條第3款規定之家庭成員關係",
    "有家庭暴力防治法第3條第1款所定之家庭成員關係", "有家庭暴力防治法第3條第2款所定之家庭成員關係",
    "有家庭暴力防治法第3條第3款所定之家庭成員關係"
]

法官心證_list = ["未達於通常一般人不致有所懷疑", "未達於一般人不致有所懷疑", "無足採酌", "犯後態度方面難以對被告為有利之考量"]

feature_elememtsAndCrime = []

# 建立儲存文件的資料夾
# folderPath = '/Users/allentsai/python_web_scraping-master/judgement_file'
folderPath = Path(__file__).resolve().parent/'judgement_file'
if not os.path.exists(folderPath):
    os.makedirs(folderPath)
folderList = os.listdir(folderPath)
pIndex = 0
for p in folderList:
    print(p, ':', pIndex)
    pIndex += 1
fp = int(input("\nChoose work folder : "))
folder = folderList[fp]  # 檔案名：judge案由分類
print(f'你選擇的是：{folder}\n')
folderName = 'Judgement_Feature'
version = '_ver_5'


# 針對構成要件的組合判斷出罪刑
def rawdata_to_featureForm():
    efolderList = os.listdir(f'{folderPath}/{folder}')
    epIndex = 0
    for ep in efolderList:
        print(ep, ':', epIndex)
        epIndex += 1
    efp = int(input("\n選擇要分出罪刑的rawdata.json : "))
    efolder = efolderList[efp]
    print(f'你選擇的是：{efolder}\n')

    with open(f'{folderPath}/{folder}/{efolder}', 'r',
              encoding='utf-8') as jsr:
        strJs = jsr.read()
    listJudge = json.loads(strJs)

    for i in range(len(listJudge)):
        strJudgeCont = listJudge[i]['judge_content']
        T_278_score, T_278_att_score, T_278_death_score, T_284_score, T_284_serious_score, T_277_score, T_277_serious_score, T_277_death_score, T_280_score, T_280_death_score, Recht_score, Crime_pred = elements_to_judgecrime_2(
            strJudgeCont)
        教育程度, 罪責, 傷害方式, 下手力道, 攻擊部位, 傷害結果, 犯後態度, 坦承情況, 賠償狀況, 經濟狀況, 被告身心狀況, 被害身心狀況, 和解狀況, 告訴人和被告人之關係, 法官心證 = aggravatedAndReduced_feature(
            strJudgeCont)
        crimeCategory = crimeToCategory(listJudge[i]['judge_crime'])
        match = 0
        if str(Crime_pred[1]) == str(crimeCategory[1]):
            match = 1
        feature_elememtsAndCrime.append({
            'judge_court': listJudge[i]['judge_court'],  # 判決法院
            'judge_year': listJudge[i]['judge_year'],  # 裁判年度
            'judge_month': listJudge[i]['judge_month'],  # 裁判月份
            'judge_index': listJudge[i]['judge_index'],  # 地院年度月份的第幾筆
            'judge_title': listJudge[i]['judge_title'],  # 裁判案由
            'F_01': str(教育程度),                      # 教育程度
            'F_02': str(罪責),                             # 罪責
            'F_03': str(傷害方式),                      # 傷害方式
            'F_04': str(下手力道),                      # 下手力道
            'F_05': str(攻擊部位),                      # 攻擊部位 x
            'F_06': str(傷害結果),                      # 傷害結果
            'F_07': str(犯後態度),                      # 犯後態度
            'F_08': str(坦承情況),                      # 坦承情況
            'F_09': str(賠償狀況),                      # 賠償狀況 x
            'F_10': str(經濟狀況),                      # 經濟狀況 x
            'F_11': str(被告身心狀況),               # 被告身心狀況
            'F_12': str(被害身心狀況),               # 被害身心狀況 x
            'F_13': str(和解狀況),                      # 和解狀況
            'F_14': str(告訴人和被告人之關係),    # 告訴人和被告人之關係
            'F_15': str(法官心證),                      # 法官心證 x
            'T_278_score': str(T_278_score[0]),  # 重傷害罪_分數
            'T_278_att_score': str(T_278_att_score[0]),  # 重傷害未遂_分數
            'T_278_death_score': str(T_278_death_score[0]),  # 重傷害致死_分數
            'T_284_score': str(T_284_score[0]),  # 過失傷害_分數
            'T_284_serious_score': str(T_284_serious_score[0]),  # 過失傷害致重傷_分數
            'T_277_score': str(T_277_score[0]),  # 普通傷害_分數
            'T_277_serious_score': str(T_277_serious_score[0]),  # 傷害致重傷害_分數
            'T_277_death_score': str(T_277_death_score[0]),  # 傷害致死_分數
            'T_280_score': str(T_280_score[0]),  # 傷直血_分數
            'T_280_death_score': str(T_280_death_score[0]),  # 傷直血致死_分數
            'Recht_score': str(Recht_score[0]),  # 無罪_分數
            'judge_crimePred': str(Crime_pred[1]),  # 罪刑預測
            'crimePredCategory': str(Crime_pred[2]),  # 罪刑預測分類別
            'judge_crime': str(listJudge[i]['judge_crime']),  # 罪名
            'judge_crimeClassify': str(crimeCategory[1]),  # 罪名類別
            'crimeCategory': str(crimeCategory[2]),  # 罪名分類別
            'Match': match,                                      # 罪刑預測與實際罪名是否相符
            'judge_result': listJudge[i]['judge_result'],  # 刑責
            'judge_resultInt': listJudge[i]['judge_resultInt']  # 刑責int
        })
    with open(f'{folderPath}/{folder}/{folderName}{version}.json',
              'w',
              encoding='utf-8') as jsw:
        jsw.write(json.dumps(feature_elememtsAndCrime, ensure_ascii=False))
    pd.DataFrame(feature_elememtsAndCrime).to_csv(
        f'{folderPath}/{folder}/{folderName}{version}.csv',
        index=None,
        encoding='utf-8-sig')


# 針對構成要件的組合判斷出罪刑
def elements_to_judgecrime_2(strJudgeCont):
    T_278_score = [0, '重傷害', '6']            # 重傷害 6
    T_278_att_score = [0, '重傷害未遂', '7']      # 重傷害未遂 7
    T_278_death_score = [0, '重傷致死', '8']     # 重傷致死 8
    T_284_score = [0, '過失傷害', '1']             # 過失傷害 1
    T_284_serious_score = [0, '過失傷害致重傷', '2']  # 過失傷害致重傷 2
    T_277_score = [0, '傷害', '3']            # 傷害 3
    T_277_serious_score = [0, '傷害致重傷', '4']  # 傷害致重傷 4
    T_277_death_score = [0, '傷害致死', '5']      # 傷害致死 5
    T_280_score = [0, '傷害直系血親尊親屬', '9']              # 傷害直系血親尊親屬 9
    T_280_death_score = [0, '傷害直系血親尊親屬致死', '10']    # 傷害直系血親尊親屬致死 10
    Recht_score = [0, '無罪', '0']              # 無罪 0

    Crime_pred = []  # 罪刑預測

    for t in T_278:
        if t in strJudgeCont:
            T_278_score[0] += 1
    for t in T_278_att:
        if t in strJudgeCont:
            T_278_att_score[0] += 1
    for t in T_278_death:
        if t in strJudgeCont:
            T_278_death_score[0] += 1
    for t in T_284:
        if t in strJudgeCont:
            T_284_score[0] += 1
    for t in T_284_serious:
        if t in strJudgeCont:
            T_284_serious_score[0] += 1
    for t in T_277:
        if t in strJudgeCont:
            T_277_score[0] += 1
    for t in T_277_serious:
        if t in strJudgeCont:
            T_277_serious_score[0] += 1
    for t in T_277_death:
        if t in strJudgeCont:
            T_277_death_score[0] += 1
    for t in T_280:
        if t in strJudgeCont:
            T_280_score[0] += 1
    for t in T_280_death:
        if t in strJudgeCont:
            T_280_death_score[0] += 1
    for r in Recht:
        if r in strJudgeCont:
            Recht_score[0] += 1

    if Recht_score[0] > 0:
        Crime_pred = Recht_score
    elif max(T_278_score, T_278_att_score, T_278_death_score, T_284_score,
             T_284_serious_score, T_277_score, T_277_serious_score,
             T_277_death_score, T_280_score, T_280_death_score)[0] == 0:
        Crime_pred = Recht_score
    else:
        Crime_pred = max(T_278_score, T_278_att_score, T_278_death_score,
                         T_284_score, T_284_serious_score, T_277_score,
                         T_277_serious_score, T_277_death_score, T_280_score,
                         T_280_death_score)

    return T_278_score, T_278_att_score, T_278_death_score, T_284_score, T_284_serious_score, T_277_score, T_277_serious_score, T_277_death_score, T_280_score, T_280_death_score, Recht_score, Crime_pred


# 實際罪責的分類
def crimeToCategory(judge_crime):
    classPath = '/Users/allentsai/python_web_scraping-master/judgement_file/judge案由分類/Crime_classify/Crime_總表.csv'
    crimeClassifyDocs = pd.read_csv(classPath)
    crimeCategory = pd.Series(['其它', '其它', 11])  # 分類：其他 = 11
    crimeForm = list(crimeClassifyDocs.loc[:, '罪名總表'])
    # for i in range(len(crimeForm)):
    #     if crimeForm[i] == judge_crime:
    #         crimeCategory = str(crimeClassifyDocs.loc[i, '罪刑classify'])

    if judge_crime in crimeForm:
        for i in range(len(crimeForm)):
            if crimeForm[i] == judge_crime:
                print(crimeForm[i])
                crimeCategory = crimeClassifyDocs.loc[i, :]
    # else:
    #     crimeCategory = '11'
    return crimeCategory


# 加重減輕罪刑Feature
def aggravatedAndReduced_feature(strJudgeCont):
    教育程度 = 0
    罪責 = 0
    傷害方式 = 0
    下手力道 = 0
    攻擊部位 = 0
    傷害結果 = 0
    犯後態度 = 0
    坦承情況 = 0
    賠償狀況 = 0
    經濟狀況 = 0
    被告身心狀況 = 0
    被害身心狀況 = 0
    和解狀況 = 0
    告訴人和被告人之關係 = 0
    法官心證 = 0
    # 教育程度
    for a in 教育程度_list:
        if a in strJudgeCont:
            教育程度 = 1
            break
    # 罪責
    for b1 in 罪責1_list:
        if b1 in strJudgeCont:
            罪責 = 1
            break
    if 罪責 != 1:
        for b2 in 罪責2_list:
            if b2 in strJudgeCont:
                罪責 = 2
                break
    # 傷害方式
    for c in 傷害方式_list:
        if c in strJudgeCont:
            傷害方式 = 1
            break
    # 下手力道
    for d in 下手力道_list:
        if d in strJudgeCont:
            下手力道 = 1
            break
    # 攻擊部位
    for e in 攻擊部位_list:
        if e in strJudgeCont:
            攻擊部位 = 1
            break
    # 傷害結果
    for f in 傷害結果2_list:
        if f in strJudgeCont:
            傷害結果 = 2
            break
    if 傷害結果 != 2:
        for f in 傷害結果1_list:
            if f in strJudgeCont:
                傷害結果 = 1
                break
    # 犯後態度
    for g2 in 犯後態度2_list:
        if g2 in strJudgeCont:
            犯後態度 = 2
            break
    if 犯後態度 != 2:
        for g1 in 犯後態度1_list:
            if g1 in strJudgeCont:
                犯後態度 = 1
                break
    # 坦承情況
    for h2 in 坦承情況2_list:
        if h2 in strJudgeCont:
            坦承情況 = 2
            break
    if 坦承情況 != 2:
        for h1 in 坦承情況1_list:
            if h1 in strJudgeCont:
                坦承情況 = 1
                break
    # 賠償狀況
    for i2 in 賠償狀況2_list:
        if i2 in strJudgeCont:
            賠償狀況 = 2
            break
    if 賠償狀況 != 2:
        for i1 in 賠償狀況1_list:
            if i1 in strJudgeCont:
                賠償狀況 = 1
                break
    # 經濟狀況
    for j in 經濟狀況_list:
        if j in strJudgeCont:
            經濟狀況 = 1
            break
    # 被告身心狀況
    for k in 被告身心狀況_list:
        if k in strJudgeCont:
            被告身心狀況 = 1
            break
    # 被害身心狀況
    for l in 被害身心狀況_list:
        if l in strJudgeCont:
            被害身心狀況 = 1
            break
    # 和解狀況
    for m2 in 和解狀況2_list:
        if m2 in strJudgeCont:
            和解狀況 = 2
            break
    if 和解狀況 != 2:
        for m1 in 和解狀況1_list:
            if m1 in strJudgeCont:
                和解狀況 = 1
                break
    # 告訴人和被告人之關係
    for n in 告訴人和被告人之關係_list:
        if n in strJudgeCont:
            告訴人和被告人之關係 = 1
            break
    # 法官心證
    for o in 法官心證_list:
        if o in strJudgeCont:
            法官心證 = 1
            break
    # print(教育程度, 罪責, 傷害方式, 下手力道, 攻擊部位, 傷害結果, 犯後態度, 坦承情況, 賠償狀況, 經濟狀況, 被告身心狀況, 被害身心狀況, 和解狀況, 告訴人和被告人之關係, 法官心證)
    return 教育程度, 罪責, 傷害方式, 下手力道, 攻擊部位, 傷害結果, 犯後態度, 坦承情況, 賠償狀況, 經濟狀況, 被告身心狀況, 被害身心狀況, 和解狀況, 告訴人和被告人之關係, 法官心證


if __name__ == "__main__":
    startTime = time.time()
    rawdata_to_featureForm()
    print(f"總花費時間 : {((time.time() - startTime)/60):.2f} 分鐘")
