from suds.client import Client
import pandas as pd
import os
import re
import subprocess 
import time

client = Client('http://retake.tyai.tyc.edu.tw/WcfYIR/SvcYIR.svc?wsdl')
ttObjid = 2
ttWWSelParam = client.factory.create('ns0:WWSelParam')
TempWWParam = client.factory.create('ns0:WWParam')
TempWWParam.CondiOrder = 10
TempWWParam.StartValue = "國語文,數學"
TempWWParam.StopValue = ""
ttWWSelParam.WWParamS.WWParam.append(TempWWParam)
TempWWParam = client.factory.create('ns0:WWParam')
TempWWParam.CondiOrder = 20
TempWWParam.StartValue = "108"
TempWWParam.StopValue = "109"
ttWWSelParam.WWParamS.WWParam.append(TempWWParam)
ttStuOrgIdStr = 'D306108A,D306108B,D306109A,D306109B'
result = client.service.GetWWRowDataS2('NHI',ttObjid,ttStuOrgIdStr,ttWWSelParam)

title = []
data = []
for i in range(len(result.RowS.WWRetRow)-1):
    if i == 0:
        title = result.RowS.WWRetRow[i].ColS[0]
    else:
        data.append(result.RowS.WWRetRow[i].ColS[0])
df = pd.DataFrame(data,columns = title)

df = df.sort_values(by=['學號','學年','學期','課程名稱'],ignore_index=True)
#df.head(20)

gdObj = []
courseName=sorted(df.iloc[:,9].unique())
print(courseName)
gdObj=sorted(list(df.columns[13:]))
gdObj.append(gdObj[0])
gdObj = list(reversed(gdObj))
gdObj.pop()
gdObj = list(reversed(gdObj))
print(gdObj)

year = list(df.iloc[:,6].unique())
sem = list(df.iloc[:,7].unique())

df2=df

for c in range(len(courseName)):
    for i in range(len(year)):
        for j in range(len(sem)):
            df_fresh = df[(df.iloc[:,9]==courseName[c])&(df.iloc[:,6]==year[i])&(df.iloc[:,7]==sem[j])]
            for k in range(len(gdObj)):
                title = str(year[i])+'_'+str(sem[j])+'_'+courseName[c]+'_'+gdObj[k]
                df_fresh[title] = df_fresh.loc[:][gdObj[k]]
            df_fresh.reset_index(inplace=True)
            df_fresh.drop('index',axis=1,inplace=True)
            df_fresh.drop(df_fresh.columns[4:-3],axis=1,inplace=True)
            df2 = df2.merge(df_fresh,on=list(df_fresh.columns)[0:4],how='outer')
df2.drop(list(df2.columns[1:6])+list(df2.columns[6:16]),axis=1,inplace=True)
df2.drop_duplicates(inplace=True,ignore_index=True)


for y in range(len(year)):
    globals()['drop_list'+str(year[y])]=[]
for c in range(len(courseName)):
    p = re.compile(courseName[c])
    drop_col = []
    for col in range(len(list(df2.columns))):
        if col == 0:
            continue
        if p.search(list(df2.columns)[col]) == None:
            drop_col.append(col)
        for y in range(len(year)):
            if int(list(df2.columns)[col][0:3])<int(year[y]):
                if col not in globals()['drop_list'+str(year[y])]:
                    globals()['drop_list'+str(year[y])].append(col)
        #print(list(df2.columns)[col])
    for y in range(len(year)):
        drop_col2 = list(set(globals()['drop_list'+str(year[y])]+drop_col))
        df_y_course = df2[df2['學號'].str.match('^'+year[y]+'.*') == True].drop(df2.columns[drop_col2],axis=1)
        ccol_list = []
        for ccol in range(len(list(df_y_course.columns))-1):
            ccol_list.append("X"+str(ccol+1))
        df_y_course.columns = ['ID']+ccol_list
        df_y_course.fillna(0,inplace=True)
        df_y_course.to_csv("C:/git-repos/mathpix_to_sympy/"+str(year[y])+'_'+courseName[c]+'.csv',encoding = 'utf-8',index=False)
        df_y_stdID = df_y_course['ID'].reset_index().drop('index',axis=1)
        #print(df_y_course.columns)
        #print(list(range(1,len(df_y_course.columns))))
        time_list = []
        for i in range(df_y_course.shape[0]):
            time_list.append(list(range(1,len(df_y_course.columns))))
        tcol_list = []
        for tcol in range(len(list(df_y_course.columns))-1):
            tcol_list.append("time"+str(tcol+1))
        df_time = pd.DataFrame(time_list,columns=tcol_list)
        df_time = pd.concat([df_y_stdID,df_time],axis=1)
        df_time.to_csv("C:/git-repos/mathpix_to_sympy/"+str(year[y])+'_'+courseName[c]+'_time.csv',encoding = 'utf-8',index=False)

path = os.getcwd()
for i in range(len(year)):
    for j in range(len(courseName)):
        cmd = "C:\\Program Files\\R\\R-4.1.2\\bin\\Rscript.exe --vanilla C:\\git-repos\\mathpix_to_sympy\\test.R "+str(year[i])+" "+str(courseName[j])
        #print(cmd)
        subprocess.call(cmd)
        time.sleep(7)
        try:
            globals()['df_R_Result_'+str(year[i])+"_"+str(courseName[j])]=pd.read_csv("C:/git-repos/mathpix_to_sympy/"+str(year[i])+"_"+str(courseName[j])+".csv",encoding='utf-8')
        except:
            pass