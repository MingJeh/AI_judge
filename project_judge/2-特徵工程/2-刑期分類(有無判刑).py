import pandas as pd
    
df=pd.read_csv("./Judgement_Feature1.csv")
judge_resultInt=df.loc[:,"judge_resultInt"]

judge_class2=[]
for i in judge_resultInt:
    if i ==0:
        judge_class2.append(0)
    else:
        judge_class2.append(1)
df['judge_class2']=judge_class2
    # print(df)
pd.DataFrame(df).to_csv("./Judgement_Feature1.csv", index=None, encoding="utf-8-sig")