import pandas as pd
    
df=pd.read_csv("./Judgement_Feature1.csv")
judge_resultInt=df.loc[:,"judge_resultInt"]

judge_class3=[]
for i in judge_resultInt:
    if i ==0:
        judge_class3.append(0)
    elif 0<i<=60:
        judge_class3.append(1)
    elif 60<i<=180:
        judge_class3.append(2)
    elif 180<i<=730:
        judge_class3.append(3)
    elif 730<i<=1825:
        judge_class3.append(4)
    elif 1825<i:
        judge_class3.append(5)
       
df['judge_class3']=judge_class3
    # print(df)
pd.DataFrame(df).to_csv("./Judgement_Feature1.csv", index=None, encoding="utf-8-sig")