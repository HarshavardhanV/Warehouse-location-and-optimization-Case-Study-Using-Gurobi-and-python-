# -*- coding: utf-8 -*-
"""
Created on Wed Nov 01 11:55:53 2017

@author: Vempati's
"""

from gurobipy import *


def kmedian(m, n, c, s):
    model = Model("k-median")
    y,x,k, demand= {}, {}, {}, {}
    p = model.addVar( vtype="C", name="p")
    for j in range(m):
        y[j] = model.addVar(obj=0, vtype="B", name="y[%s]"%j)
        demand[j]=model.addVar(obj=0, vtype="C",name="Demand[%s]"%j)
        for i in range(n):
            x[i,j] = model.addVar(obj=0, vtype="B", name="x[%s,%s]"%(i,j))
            k[i,j]= model.addVar(obj=0,vtype="B",name="k[%s,%s]"%(i,j))
            model.update()
    
    model.ModelSense = GRB.MINIMIZE
    model.setParam("OptimalityTol", 1.00e-07)
    
    
    model.setObjective(p+0.00007*(quicksum(quicksum(x[i,j]*c[i+1,j+1] for j in range(m))for i in range(n))))
    #model.setObjectiveN(quicksum(quicksum(x[i,j]*c[i+1,j+1]*(1-k[i,j]) for i in range(n))for j in range(m)), 1, 1)
    
    #constraint 1       
    for i in range(n):
        coef = [1 for j in range(m)]
        var = [x[i,j] for j in range(m)]
        model.addConstr(LinExpr(coef,var), "=", 1, name="Assign[%s]"%i)
    #constraint 2
    for j in range(m):
        for i in range(n):
            model.addConstr(x[i,j], "<", y[j], name="Strong[%s,%s]"%(i,j))
    #constraint 3
    coef = [1 for j in range(m)]
    var = [y[j] for j in range(m)]
    model.addConstr(LinExpr(coef,var), "=", p, name="to solve p")
    #constraint 4
    for j in range(m):
        for i in range(n):
            model.addConstr(x[i,j]*c[i+1,j+1]*k[i,j] <= 500, name="to solve distance constraint with distance [%s,%s]"%(i,j))
    #constraint 5
    for j in range(m):
        var = [x[i,j] for i in range(n)]
        var2= [s[i] for i in range(n)]
        model.addConstr(LinExpr(var2,var), "=", demand[j], name="cons 5 [%s,%s]"%(i,j))
    #constraint 6
    for j in range(m):
        model.addConstr(quicksum(x[i,j]*k[i,j]*s[i] for i in range(n))>= 0.8*demand[j],name="Cons 6 [%s,%s]"%(i,j))
    model.update()
    model.__data = x,y
    return model

#lOOKING AT THE DATA
import pandas as pd
import os

os.chdir("E:/Opex")

excel_file=pd.ExcelFile("case_study.xlsx")
#print df.sheet_names
df=excel_file.parse('Annual Demand')
df.loc[:,'Demand (in tonnes)']=0.25*df['Demand (in tonnes)']

df = df.groupby(['Customer ID', 'Time Period'], as_index=False)['Demand (in tonnes)'].sum()

df=df.loc[df['Time Period'] == 2012]

#print df.as_matrix(columns=df.columns[2:])
#print df
new_values=df.iloc[:,2:].values
demand = [item for sublist in new_values for item in sublist]
#print demand

df1=excel_file.parse('Distances')
df1 = df1[['Customer ID.1','Customer ID.2','Distance.1']]

#Program for solving the case1
n = 50
c= dict([((a,b),c) for a,b,c in zip(df1['Customer ID.1'],df1['Customer ID.2'],df1['Distance.1'])])

m = n
k = [6042.5271999999986, 16444.179700000001, 8416.7945999999993, 2498.3595000000005, 9345.2453999999998, 9534.3752000000004, 2712.6731, 10407.645699999997, 15402.340799999998, 7085.9366000000018, 7829.9027999999989, 10547.641600000001, 7152.5064000000002, 4587.5931999999993, 13088.341, 14045.3235, 12588.066000000001, 6950.3900999999996, 3682.0886000000005, 3042.2647000000002, 4142.0969999999998, 5095.2232000000004, 8087.8289999999997, 17587.712, 6021.7904999999992, 15646.919599999999, 8064.3598000000002, 1451.8811000000001, 9635.1695000000018, 7540.1687000000002, 14381.6829, 10924.4943, 7439.9005000000006, 7978.8697999999995, 15030.440000000002, 1871.6690999999998, 11875.261399999999, 4761.0706, 9476.0564000000013, 14478.3469, 1099.4215000000002, 10144.592500000001, 4822.6557999999995, 4862.3964000000005, 11519.657400000002, 2342.7222000000002, 1809.1865000000005, 1659.1764000000001, 14555.2425, 10018.495599999998]

model= kmedian(m, n, c, k)
model.optimize()
x,y = model.__data
edges = [(i+1,j+1) for (i,j) in x if x[i,j].X == 1]

nodes = [j+1 for j in y if y[j].X == 1]
print "Optimal value=", model.ObjVal
print "Selected nodes:", nodes
print "Edges:", edges

#for i in range(n):
#    print model.getVarByName("y[%s]"%i)
#k=model.getVarByName("y[0]")
#type(k)    

#After Analysis

warehouse_frames= df1.loc[df1['Customer ID.1'].isin(nodes)]
#print warehouse_frames['Customer ID.1'].uniqu

for i in nodes:
    globals()['warehouse%s' % i]=df1.loc[df1['Customer ID.1']==i]

node_from_to=[]
node_to={}
for i in nodes:
    node_to[i]=[]
for i in nodes:
    for k in edges:
        if k[1]==i:
            node_to[i].append(k[0])

warehouse8=warehouse8.loc[warehouse8['Customer ID.2'].isin(node_to[8])]
warehouse17=warehouse17.loc[warehouse17['Customer ID.2'].isin(node_to[17])]
warehouse13=warehouse13.loc[warehouse13['Customer ID.2'].isin(node_to[13])]
warehouse25=warehouse25.loc[warehouse25['Customer ID.2'].isin(node_to[25])]

print warehouse8
print warehouse13
print warehouse17
print warehouse25

#for warehouse 8
an_demand=excel_file.parse('Annual Demand')
an_demand=an_demand.loc[an_demand['Time Period']==2012]

an_demand.loc[:,'Demand (in tonnes)']=an_demand['Demand (in tonnes)']*0.25
an_demand = an_demand[an_demand['Customer ID'].isin(warehouse8['Customer ID.2'])]

wd_product=an_demand
wd_product=wd_product.groupby(['Product ID'], as_index=False)['Demand (in tonnes)'].sum()

#for warehouse 13
an_demand=excel_file.parse('Annual Demand')
an_demand=an_demand.loc[an_demand['Time Period']==2012]

an_demand.loc[:,'Demand (in tonnes)']=an_demand['Demand (in tonnes)']*0.25
an_demand = an_demand[an_demand['Customer ID'].isin(warehouse13['Customer ID.2'])]

wd_product=an_demand
wd_product=wd_product.groupby(['Product ID'], as_index=False)['Demand (in tonnes)'].sum()
print wd_product
            
#for warehouse 17
an_demand=excel_file.parse('Annual Demand')
an_demand=an_demand.loc[an_demand['Time Period']==2012]

an_demand.loc[:,'Demand (in tonnes)']=an_demand['Demand (in tonnes)']*0.25
an_demand = an_demand[an_demand['Customer ID'].isin(warehouse17['Customer ID.2'])]

wd_product=an_demand
wd_product=wd_product.groupby(['Product ID'], as_index=False)['Demand (in tonnes)'].sum()
print wd_product

#for warehouse 25
an_demand=excel_file.parse('Annual Demand')
an_demand=an_demand.loc[an_demand['Time Period']==2012]

an_demand.loc[:,'Demand (in tonnes)']=an_demand['Demand (in tonnes)']*0.25
an_demand = an_demand[an_demand['Customer ID'].isin(warehouse25['Customer ID.2'])]

wd_product=an_demand
wd_product=wd_product.groupby(['Product ID'], as_index=False)['Demand (in tonnes)'].sum()
print wd_product

