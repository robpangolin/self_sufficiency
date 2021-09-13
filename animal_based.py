import pandas as pd, platypus, csv, numpy, matplotlib, pulp, itertools as it
from pulp import *
file = "animal_uses.csv"
data = pd.read_csv(file)
land_uses = list(data['Unnamed: 0'])
carbo = dict(zip(land_uses, data['Carbohydrate ']))
cost = dict(zip(land_uses, data['Total']))
VitA = dict(zip(land_uses, data['Vitamin A (g)']))
VitD = dict(zip(land_uses, data['Vitamin D (g)']))
Calcium = dict(zip(land_uses, data['Calcium']))
VitK = dict(zip(land_uses, data['Vitamin K (g)']))
VitC = dict(zip(land_uses, data['Vitamin C (g/g)']))
Thiam = dict(zip(land_uses, data['Thiamine ']))
Ribo = dict(zip(land_uses, data['Riboflavin ']))
Niac = dict(zip(land_uses, data['Niacin ']))
VitB6 = dict(zip(land_uses, data['Vitamin B6 ']))
Panto = dict(zip(land_uses, data['Pantothenate ']))
Biotin = dict(zip(land_uses, data['Biotin ']))
Selen = dict(zip(land_uses, data['Selenium ']))
Magnes = dict(zip(land_uses, data['Magnesium']))
Zinc = dict(zip(land_uses, data['Zinc ']))
Iron = dict(zip(land_uses, data['Iron ']))
VitB12 = dict(zip(land_uses, data['Vitamin B12 ']))
Folate = dict(zip(land_uses, data['Folic acid ']))
Iodine = dict(zip(land_uses, data['Iodine ']))
Prot = dict(zip(land_uses, data['Protein']))
Fat = dict(zip(land_uses, data['Fat ']))

land_vars = LpVariable.dicts("Land_use", land_uses, lowBound = 0, cat = 'Continuous')
total_carb = LpProblem("land_optimisation", LpMaximize)
total_carb += lpSum([carbo[i] * land_vars[i] for i in land_vars])

total_carb += lpSum([carbo[i] * land_vars[i] for i in land_vars])<= 5.0097e+12
total_carb += lpSum([cost[i]*land_vars[i] for i in land_vars]) <= 218721510067
#total_carb += lpSum([VitA[i]*land_vars[i]for i in land_vars]) >= 1.343837e+07
#total_carb += lpSum([VitD[i]*land_vars[i]for i in land_vars]) >= 1.875182e+05
#total_carb += lpSum([Calcium[i]*land_vars[i]for i in land_vars]) >= 2.570267e+10 
#total_carb += lpSum([VitK[i]*land_vars[i]for i in land_vars]) >= 1.284501e+06
#total_carb += lpSum([VitC[i]*land_vars[i]for i in land_vars]) >= 1.044726e+09
total_carb += lpSum([Thiam[i]*land_vars[i]for i in land_vars]) >= 2.650924e+07
total_carb += lpSum([Ribo[i]*land_vars[i]for i in land_vars]) >= 2.746771e+07
total_carb += lpSum([Niac[i]*land_vars[i]for i in land_vars]) >= 3.479568e+08
total_carb += lpSum([VitB6[i]*land_vars[i]for i in land_vars]) >= 3.231519e+07
total_carb += lpSum([Panto[i]*land_vars[i]for i in land_vars]) >= 1.157954e+08
#total_carb += lpSum([Biotin[i]*land_vars[i]for i in land_vars]) >= 6.681567e+05
total_carb += lpSum([Selen[i]*land_vars[i]for i in land_vars]) >= 6.950612e+05
total_carb += lpSum([Magnes[i]*land_vars[i]for i in land_vars]) >= 5.185360e+09
total_carb += lpSum([Zinc[i]*land_vars[i]for i in land_vars]) >= 2.062908e+08
#total_carb += lpSum([Iron[i]*land_vars[i]for i in land_vars]) >= 7.963802e+08
total_carb += lpSum([VitB12[i]*land_vars[i]for i in land_vars]) >= 5.513048e+04
#total_carb += lpSum([Folate[i]*land_vars[i]for i in land_vars]) >= 9.185334e+06
#total_carb += lpSum([Iodine[i]*land_vars[i]for i in land_vars]) >= 3.464959e+06
total_carb += lpSum([Prot[i]*land_vars[i]for i in land_vars]) >= 7.633401e+11
total_carb += lpSum([Fat[i]*land_vars[i]for i in land_vars]) >=  3.551532e+11

total_carb.solve()

for v in total_carb.variables():
    print(v.name, "=", v.varValue)
