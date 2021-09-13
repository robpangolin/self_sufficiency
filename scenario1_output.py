import pandas as pd, platypus, csv, numpy, matplotlib, pulp, itertools as it
from pulp import *
data = pd.read_csv(file)

land_uses = list(data['Land.use'])
carbo = dict(zip(land_uses, data['Carbohydrate']))
VitA = dict(zip(land_uses, data['Vitamin.A..g.']))
VitD = dict(zip(land_uses, data['Vitamin.D..g.']))
Calcium = dict(zip(land_uses, data['Calcium']))
VitK = dict(zip(land_uses, data['Vitamin.K..g.']))
VitC = dict(zip(land_uses, data['Vitamin.C..g.g.']))
Thiam = dict(zip(land_uses, data['Thiamine']))
Ribo = dict(zip(land_uses, data['Niacin']))
Niac = dict(zip(land_uses, data['Thiamine']))
VitB6 = dict(zip(land_uses, data['Vitamin.B6']))
Panto = dict(zip(land_uses, data['Pantothenate']))
Biotin = dict(zip(land_uses, data['Biotin']))
Selen = dict(zip(land_uses, data['Selenium']))
Magnes = dict(zip(land_uses, data['Magnesium']))
Zinc = dict(zip(land_uses, data['Zinc']))
Iron = dict(zip(land_uses, data['Iron']))
VitB12 = dict(zip(land_uses, data['Vitamin.B12']))
Folate = dict(zip(land_uses, data['Folic.acid']))
Iodine = dict(zip(land_uses, data['Iodine']))
Prot = dict(zip(land_uses, data['Protein']))
Fat = dict(zip(land_uses, data['Fat']))
#following structure is adapted in part from answer to question: https://stackoverflow.com/questions/68805085/land-use-optimisation-where-options-can-use-one-or-other-land-type-to-satisfy-th
reqts = ['vpoor','poor','medium','good','vgood']
reqt_use = { ('Wheat (flour)', 'vpoor'):0, 
             ('Wheat (flour)', 'poor'): 0,
             ('Wheat (flour)', 'medium'): 0.56338,
             ('Wheat (flour)', 'good'): 0,
             ('Wheat (flour)', 'vgood'): 0,
             ('Rye (grain)', 'vpoor'): 0, 
             ('Rye (grain)', 'poor'): 0,
             ('Rye (grain)', 'medium'): 3.311258,
             ('Rye (grain)', 'good'): 0,
             ('Rye (grain)', 'vgood'): 0,
             ('Barley (hulled)', 'vpoor'): 0,
             ('Barley (hulled)', 'poor'): 0,
             ('Barley (hulled)', 'medium'): 1.748251748,
             ('Barley (hulled)', 'good'): 0,
             ('Barley (hulled)', 'vgood'): 0,
             ('Oats', 'vpoor'): 0, 
             ('Oats', 'poor'): 0,
             ('Oats', 'medium'): 1.666667,
             ('Oats', 'good'): 0,
             ('Oats', 'vgood'): 0,
             ('Maize (edible, raw)', 'vpoor'): 0, 
             ('Maize (edible, raw)', 'poor'): 0,
             ('Maize (edible, raw)', 'medium'): 1.109878,
             ('Maize (edible, raw)', 'good'): 0,
             ('Maize (edible, raw)', 'vgood'): 0,
             ('Potatoes', 'vpoor'):0, 
             ('Potatoes', 'poor'): 0,
             ('Potatoes', 'medium'): 2.531646,
             ('Potatoes', 'good'): 0,
             ('Potatoes', 'vgood'): 0,
             ('Rapeseed oil', 'vpoor'): 0 ,
             ('Rapeseed oil', 'poor'): 0,
             ('Rapeseed oil', 'medium'): 0.289855,
             ('Rapeseed oil', 'good'): 0,
             ('Rapeseed oil', 'vgood'): 0,
             ('Lettuce', 'vpoor'): 0, 
             ('Lettuce', 'poor'): 0,
             ('Lettuce', 'medium'): 0,
             ('Lettuce', 'good'): 0,
             ('Lettuce', 'vgood'): 0.449236,
             ('Rocket', 'vpoor'): 0, 
             ('Rocket', 'poor'): 0,
             ('Rocket', 'medium'): 0,
             ('Rocket', 'good'): 0,
             ('Rocket', 'vgood'): 0.045693397,
             ('Spinnach', 'vpoor'): 0, 
             ('Spinnach', 'poor'): 0,
             ('Spinnach', 'medium'): 0,
             ('Spinnach', 'good'): 0,
             ('Spinnach', 'vgood'): 0.045693397,
             ('Watercress', 'vpoor'): 0, 
             ('Watercress', 'poor'): 0,
             ('Watercress', 'medium'): 0,
             ('Watercress', 'good'): 0,
             ('Watercress', 'vgood'): 1290.322581,
             ('Celery', 'vpoor'): 0, 
             ('Celery', 'poor'): 0,
             ('Celery', 'medium'): 0,
             ('Celery', 'good'): 0,
             ('Celery', 'vgood'): 0.148898154,
             ('Tomato (plum)(glasshouse)', 'vpoor'): 0, 
             ('Tomato (plum)(glasshouse)', 'poor'): 0,
             ('Tomato (plum)(glasshouse)', 'medium'): 0,
             ('Tomato (plum)(glasshouse)', 'good'): 0,
             ('Tomato (plum)(glasshouse)', 'vgood'): 0.027548209,
             ('Cucumber', 'vpoor'): 0, 
             ('Cucumber', 'poor'): 0,
             ('Cucumber', 'medium'): 0,
             ('Cucumber', 'good'): 0,
             ('Cucumber', 'vgood'): 0.203500204,
             ('Peppers (bell/sweet)', 'vpoor'): 0, 
             ('Peppers (bell/sweet)', 'poor'): 0,
             ('Peppers (bell/sweet)', 'medium'): 0,
             ('Peppers (bell/sweet)', 'good'): 0,
             ('Peppers (bell/sweet)', 'vgood'): 0.333333333,
             ('Asparagus', 'vpoor'): 0, 
             ('Asparagus', 'poor'): 0,
             ('Asparagus', 'medium'): 0,
             ('Asparagus', 'good'): 0,
             ('Asparagus', 'vgood'): 2.666666667,
             ('Peas', 'vpoor'): 0, 
             ('Peas', 'poor'): 0,
             ('Peas', 'medium'): 0,
             ('Peas', 'good'): 0,
             ('Peas', 'vgood'): 7.462686567,
             ('Broccoli', 'vpoor'): 0, 
             ('Broccoli', 'poor'): 0,
             ('Broccoli', 'medium'): 0,
             ('Broccoli', 'good'): 0.4,
             ('Broccoli', 'vgood'): 0,
             ('Cauliflower', 'vpoor'): 0, 
             ('Cauliflower', 'poor'): 0,
             ('Cauliflower', 'medium'): 0,
             ('Cauliflower', 'good'): 0.454545455,
             ('Cauliflower', 'vgood'): 0,
             ('Red Cabbage', 'vpoor'): 0, 
             ('Red Cabbage', 'poor'): 0,
             ('Red Cabbage', 'medium'): 0,
             ('Red Cabbage', 'good'): 0.12195122,
             ('Red Cabbage', 'vgood'): 0,
             ('Green Cabbage', 'vpoor'): 0, 
             ('Green Cabbage', 'poor'): 0,
             ('Green Cabbage', 'medium'): 0,
             ('Green Cabbage', 'good'): 0.12195122,
             ('Green Cabbage', 'vgood'): 0,
             ('Brussels sprouts', 'vpoor'): 0,
             ('Brussels sprouts', 'poor'): 0,
             ('Brussels sprouts', 'medium'): 0,
             ('Brussels sprouts', 'good'): 0.204081633,
             ('Brussels sprouts', 'vgood'): 0,
             ('Kale', 'vpoor'): 0, 
             ('Kale', 'poor'): 0,
             ('Kale', 'medium'): 0,
             ('Kale', 'good'): 0,
             ('Kale', 'vgood'): 0.333333333,
             ('Carrots', 'vpoor'): 0, 
             ('Carrots', 'poor'): 0,
             ('Carrots', 'medium'): 0,
             ('Carrots', 'good'): 0.066666667,
             ('Carrots', 'vgood'): 0,
             ('Parsnips', 'vpoor'): 0, 
             ('Parsnips', 'poor'): 0,
             ('Parsnips', 'medium'): 0,
             ('Parsnips', 'good'): 0.2,
             ('Parsnips', 'vgood'): 0,
             ('Beetroot', 'vpoor'): 0,
             ('Beetroot', 'poor'): 0,
             ('Beetroot', 'medium'): 0,
             ('Beetroot', 'good'): 0,
             ('Beetroot', 'vgood'): 0.120481928,
             ('Sweet potato', 'vpoor'): 0, 
             ('Sweet potato', 'poor'): 0,
             ('Sweet potato', 'medium'): 0,
             ('Sweet potato', 'good'): 0,
             ('Sweet potato', 'vgood'): 0.564971751,
             ('Spring onions', 'vpoor'): 0, 
             ('Spring onions', 'poor'): 0,
             ('Spring onions', 'medium'): 0,
             ('Spring onions', 'good'): 0,
             ('Spring onions', 'vgood'): 10,
             ('Leeks', 'vpoor'): 0, 
             ('Leeks', 'poor'): 0,
             ('Leeks', 'medium'): 0,
             ('Leeks', 'good'): 0,
             ('Leeks', 'vgood'): 0.319488818,
             ('Onions', 'vpoor'): 0, 
             ('Onions', 'poor'): 0,
             ('Onions', 'medium'): 0,
             ('Onions', 'good'): 0.476190476,
             ('Onions', 'vgood'): 0,
             ('Garlic', 'vpoor'): 0, 
             ('Garlic', 'poor'): 0,
             ('Garlic', 'medium'): 0,
             ('Garlic', 'good'): 0.544959128,
             ('Garlic', 'vgood'): 0,
             ('Apples', 'vpoor'): 0, 
             ('Apples', 'poor'): 0,
             ('Apples', 'medium'): 0,
             ('Apples', 'good'): 0,
             ('Apples', 'vgood'): 0.83,
             ('Grapes', 'vpoor'): 0, 
             ('Grapes', 'poor'): 0,
             ('Grapes', 'medium'): 0,
             ('Grapes', 'good'): 0,
             ('Grapes', 'vgood'): 0.5,
             ('Strawberries', 'vpoor'): 0, 
             ('Strawberries', 'poor'): 0,
             ('Strawberries', 'medium'): 0,
             ('Strawberries', 'good'): 0,
             ('Strawberries', 'vgood'): 1.428571429,
             ('Raspberries', 'vpoor'): 0, 
             ('Raspberries', 'poor'): 0,
             ('Raspberries', 'medium'): 0,
             ('Raspberries', 'good'): 0,
             ('Raspberries', 'vgood'): 0.333333333,
             ('Blueberries', 'vpoor'): 0, 
             ('Blueberries', 'poor'): 0,
             ('Blueberries', 'medium'): 0,
             ('Blueberries', 'good'): 0,
             ('Blueberries', 'vgood'): 2.702702703,
             ('Blackberries', 'vpoor'): 0, 
             ('Blackberries', 'poor'): 0,
             ('Blackberries', 'medium'): 0,
             ('Blackberries', 'good'): 0,
             ('Blackberries', 'vgood'): 0.909090909,
             ('Pear', 'vpoor'): 0, 
             ('Pear', 'poor'): 0,
             ('Pear', 'medium'): 0,
             ('Pear', 'good'): 0,
             ('Pear', 'vgood'): 0.357142857,
             ('Plums', 'vpoor'): 0, 
             ('Plums', 'poor'): 0,
             ('Plums', 'medium'): 0,
             ('Plums', 'good'): 0,
             ('Plums', 'vgood'): 0.8,
             ('Cheries', 'vpoor'): 0, 
             ('Cheries', 'poor'): 0,
             ('Cheries', 'medium'): 0,
             ('Cheries', 'good'): 0,
             ('Cheries', 'vgood'): 5.714285714,
             ('Rhubarb', 'vpoor'): 0, 
             ('Rhubarb', 'poor'): 0,
             ('Rhubarb', 'medium'): 0,
             ('Rhubarb', 'good'): 0,
             ('Rhubarb', 'vgood'): 0.357142857,
             ('Lamb', 'vpoor'): 4.8, 
             ('Lamb', 'poor'): 1.7,
             ('Lamb', 'medium'): 2,
             ('Lamb', 'good'): 0,
             ('Lamb', 'vgood'): 0,
             ('Beef', 'vpoor'): 6, 
             ('Beef', 'poor'): 9,
             ('Beef', 'medium'): 15,
             ('Beef', 'good'): 0,
             ('Beef', 'vgood'): 0,
             ('Pork', 'vpoor'): 2,
             ('Pork', 'poor'): 0,
             ('Pork', 'medium'): 10,
             ('Pork', 'good'): 0,
             ('Pork', 'vgood'): 0,
             ('Chicken', 'vpoor'): 0.05, 
             ('Chicken', 'poor'): 0,
             ('Chicken', 'medium'): 9.8,
             ('Chicken', 'good'): 0,
             ('Chicken', 'vgood'): 0,
             ('Turkey', 'vpoor'): 0.26,
             ('Turkey', 'poor'): 0,
             ('Turkey', 'medium'): 11.96,
             ('Turkey', 'good'): 0,
             ('Turkey', 'vgood'): 0,
             ('Cow milk', 'vpoor'): 0.1,
             ('Cow milk', 'poor'): 0.9,
             ('Cow milk', 'medium'): 1,
             ('Cow milk', 'good'): 0,
             ('Cow milk', 'vgood'): 0,
             ('Chicken egg', 'vpoor'): 0.02, 
             ('Chicken egg', 'poor'): 0,
             ('Chicken egg', 'medium'): 6.0,
             ('Chicken egg', 'good'): 0,
             ('Chicken egg', 'vgood'): 0}
cats = [1,2,3,4,5]
cat_pool = { 'vpoor': [1,2,3,4,5],
             'poor': [1,2,3,4],
             'medium':[1,2,3],
             'good':[1,2],
             'vgood':[1]}
avail = {1:3666128624,
         2:23667167062,
         3:83480211508,
         4:72209472283,
         5:26802708091}

x = LpVariable.dicts("commit", [(cat, use, reqt)
    for cat in cats
    for use in land_uses
    for reqt in reqts],
    lowBound=0, cat='Continuous')

build = LpVariable.dicts("build", land_uses, lowBound = 0, cat = 'Continuous')
simple = LpProblem("land_optimisation", LpMaximize)
simple += lpSum([carbo[i] * build[i] for i in build])
for cat in cats:
    simple += lpSum(x[cat,use,reqt] for use in land_uses for reqt in reqts) <= avail[cat]

for use in land_uses:
    for reqt in reqts:
        simple += build[use]*reqt_use[use, reqt] <= lpSum(x[cat,use,reqt] for cat in cat_pool[reqt])
#end of adapted code        
simple += lpSum([carbo[i] * build[i] for i in build]) >= 5.44e+12
simple += lpSum([VitA[i]*build[i]for i in build]) >= 1.455084e+07
simple += lpSum([VitD[i]*build[i]for i in build]) >= 2.139060e+05
simple += lpSum([Calcium[i]*build[i]for i in build]) >= 2.812795e+10 
simple += lpSum([VitK[i]*build[i]for i in build]) >= 1.400092e+06
simple += lpSum([VitC[i]*build[i]for i in build]) >= 1.128753e+09
simple += lpSum([Thiam[i]*build[i]for i in build]) >= 2.867559e+07
simple += lpSum([Ribo[i]*build[i]for i in build]) >= 2.973938e+07
#simple += lpSum([Niac[i]*build[i]for i in build]) >= 3.762555e+08
simple += lpSum([VitB6[i]*build[i]for i in build]) >= 3.527821e+07
simple += lpSum([Panto[i]*build[i]for i in build]) >= 1.251690e+08
#simple += lpSum([Biotin[i]*build[i]for i in build]) >= 7.253949e+05
simple += lpSum([Selen[i]*build[i]for i in build]) >= 7.496641e+05
simple += lpSum([Magnes[i]*build[i]for i in build]) >= 5.594158e+09
simple += lpSum([Zinc[i]*build[i]for i in build]) >= 2.204601e+08
simple += lpSum([Iron[i]*build[i]for i in build]) >= 8.465457e+08
simple += lpSum([VitB12[i]*build[i]for i in build]) >= 5.965377e+04
simple += lpSum([Folate[i]*build[i]for i in build]) >= 9.939047e+06
#simple += lpSum([Iodine[i]*build[i]for i in build]) >= 3.717961e+06
simple += lpSum([Prot[i]*build[i]for i in build]) >= 8.260738e+11
simple += lpSum([Fat[i]*build[i]for i in build]) >=  3.857829e+11

solver = getSolver('GLPK_CMD')
simple.solve(solver)
for v in simple.variables():
    print(v.name, "=", v.varValue)
