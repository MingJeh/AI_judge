import pandas as pd
    
df=pd.read_csv("C:/Users/student/Desktop/Judgement_Feature_ver_5.csv")
judge_resultInt=df.loc[:,"judge_resultInt"]

judge_class=[]
for i in judge_resultInt:
    if i ==0:
        judge_class.append(0)
    elif 0<i<=30:
        judge_class.append(1)
    elif 30<i<=60:
        judge_class.append(2)
    elif 60<i<=180:
        judge_class.append(3)
    elif 180<i<=730:
        judge_class.append(4)
    elif 730<i<=1825:
        judge_class.append(5)
    elif 1825<i:
        judge_class.append(6)
    # elif 3651<i:
    #     judge_class.append(7)
df['judge_class']=judge_class
    # print(df)
pd.DataFrame(df).to_csv("./Judgement_Feature1.csv", index=None, encoding="utf-8-sig")
