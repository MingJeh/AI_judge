import pandas as pd
    
df=pd.read_csv("./Judgement_Feature1.csv")
judge_crimeCategory=df.loc[:,'crimeCategory']
min=[]
max=[]
for i in judge_crimeCategory:
    if i ==1:
        min.append(1)
        max.append(365)
    elif i ==2:
        min.append(1)
        max.append(1095)
    elif i ==3:
        min.append(1)
        max.append(1825)
    elif i ==4:
        min.append(1095)
        max.append(3650)
    elif i ==5:
        min.append(2555)
        max.append(36500)
    elif i ==6:
        min.append(1825)
        max.append(4380)
    elif i ==7:
        min.append(1825)
        max.append(4380)
    elif i ==8:
        min.append(3650)
        max.append(36500)
    elif i ==9:
        min.append(1)
        max.append(2737)
    elif i ==10:
        min.append(3832)
        max.append(36500)
    elif i ==11:
        min.append(180)
        max.append(1825)
    elif i ==0:
        min.append(0)
        max.append(0)   

judge_resultInt=df.loc[:,'judge_resultInt']
light_heavy=[]
for i in range(len(judge_resultInt)):
    if judge_resultInt[i]!=0:
        j=((judge_resultInt[i]-min[i])/(max[i]-min[i]))
        if j<=0.35:
            light_heavy.append("light")
        elif 0.35<j<=0.65:
            light_heavy.append("medium")
        elif j>0.65:
            light_heavy.append("heavy")
    else:
        light_heavy.append("0")
# print(light_heavy)
df['light_heavy']=light_heavy

pd.DataFrame(df).to_csv("./Judgement_Feature2.csv", index=None, encoding="utf-8-sig")