from gurobipy import*
import os
import xlrd
import xlsxwriter
import numpy as np
from random import randint
import random

n=50
digit=[]
chromosome=[]

chrom=["chromosome"]
for i in range(1,51):
    digit.append(i)
    
for j in range(50):
    chromosome.append(chrom[0]+str(digit[j]))



  
Facility=[]

Demand={} 
distance = {}
fixed_cost = {}


chromosome_genes={}
book = xlrd.open_workbook(os.path.join("Fixed_charge_1.xlsx"))

sh = book.sheet_by_name("cost")

i = 1
while True:
    try:
        sp = sh.cell_value(i,0)
        Facility.append(sp)
        fixed_cost[sp] = sh.cell_value(i,1)
        Demand[sp]=sh.cell_value(i,2)
        i = i + 1   
    except IndexError:
        break
sh = book.sheet_by_name("distance")

i = 1
for P in Facility:
    j = 1
    for Q in Facility:
        distance[P,Q] = sh.cell_value(i,j)
        j += 1
    i += 1

m = Model("GA_FC")


m.modelSense=GRB.MINIMIZE

X_j = m.addVars(Facility,vtype=GRB.BINARY,name='X_j')
Y_ij = m.addVars(Facility,Facility,vtype=GRB.CONTINUOUS,name='Y_ij')

m.setObjective(sum(fixed_cost[j]*X_j[j] for j in Facility) + sum((Demand[i]*distance[i,j]*Y_ij[i,j]) for i in Facility for j in Facility))
    
for i in Facility:
    m.addConstr(sum(Y_ij[i,j] for j in Facility) == 1)

for i in Facility:
    for j in Facility:
        m.addConstr(Y_ij[i,j] <= X_j[j])

m.optimize()

for v in m.getVars():
    if v.x > 0.01:
        print(v.varName, v.x)
print('Objective:',m.objVal)

#GA ALGO START


#chromosome_genes={}
#for i in chromosome:
#    for j in Facility:
#        a = np.random.random(1)[0]
#        if a >= 0.5:
#            b = 1
#        else:
#            b = 0
#        chromosome_genes[i,j]=b


# TO CREATE 50 EMPTY LIST        
chrom_some=[[] for i in range(50)]

#TO STORE 50 RANDOM VALUES IN EACH EMPTY LIST
for i in chrom_some:
   for j in range(50):
     a = np.random.random(1)[0]
     if a >= 0.5:
         b = 1
     else:
         b = 0
     i.append(b)        

#TO ASSIGN 50 RANDOM VALUES GENERATED IN PREVIOUS STEP INTO CHROMOSOME1,CHROMOSOME2....
chrom_dict={}
x=0
for i in chromosome:
    
    chrom_dict[i]=chrom_some[x]
    x+=1        

#TO CHECK FITNESS OF EACH CHROMOSOME
Con1 = {}        
def Fitness_Value_of_chromosome(a):     ##a=chromosome1,2.....
    k = 0
    for j in Facility:
        Con1[j] = m.addConstr(X_j[j] == chrom_dict[a][k])
        k = k + 1 
    m.update()    
    m.optimize()
#    m.write('abc.lp')
    fit_crom_1 = m.objVal   
    for j in Facility:
        m.remove(Con1[j])  
#    print("value of fitness ",fit_crom_1)
    return(fit_crom_1)

#TO CREATE A NEW DICTIONARY TO STORE FITNESS VALUES OF VARIOUS CHROMOSOMES ALONG WITH CHROMOSOMES NAME
def dict_chromo_fitness(chromosome):    
    Chromo_Fitness={}
    for i in chromosome:
        Chromo_Fitness[i]=Fitness_Value_of_chromosome(i)
    return(Chromo_Fitness)    

#TO FIND MID VALUE OF FITNESS VALUES SO THAT WE CAN KEEP SOLUTION GIVVING BETTER RESULTS THAN MID VALUE AND REJECT OTHERS 
def mid_value(a):       #a=Chromo_Fitness
    z=[]
    for i in chromosome:
        z.append(a[i])
    maximum=max(z)
    minimum=min(z)
    mid=(maximum+minimum)/2
    return mid

#TO STORE ONLY THOSE CHROMOSOMES WHICH GIVES BETTER RESULTS THAN THE MID VALUE
def dict_First_gen(chromosome):
    First_gen={}
    for i in chromosome:
        if Chromo_Fitness[i]<=mid_value(Chromo_Fitness):
            First_gen[i]=Chromo_Fitness[i]
    return First_gen
#new_chromosome=[]
#for i in chromosome:
#    for j in First_gen.keys():
#        if i==j:
#            new_chromosome.append(i)
#for i in range(len(new_chromosome)):
#    chromosome.remove(new_chromosome[i])


#TO CROSS AMONG THE SELECTED BETTER CHROMOSOMES AND STORE THEM.
#IT ALSO STORES THE BETTER CHROMOSOMES OF PREVIOUS STEP AND APPENDS THEM INTO A DICTIONARY ALONG WITH NEW CROSSED CHROMOSOMES    
new_generation={}        
def cross_gen(f,g):        #a=First_gen
    array1=[]
    num=50
    new_chromosome=[]
    for i in chromosome:
        for j in First_gen.keys():
            if i==j:
                new_chromosome.append(i)
    for i in range(len(new_chromosome)):
        chromosome.remove(new_chromosome[i])

    for j in f.keys():
        array1.append(j)
    for i in range(num-len(First_gen)):
        a=random.choice(array1)
        b=random.choice(array1)
        cross_point=random.randrange(2,50,1)
        list_1=[]
        list_2=[]
        c=g[a]
        d=g[b]
        
        for v in range(50):
            if v<=cross_point:
                list_1.append(c[v])
            else:
                list_1.append(d[v])
        
#        for b in range(50):
#            if b<=cross_point:
#                list_2.append(d[b])
#            else:
#                list_2.append(c[b])
                
#        print(list_1)
#        for j in range(num):
#            if chromosome[j]!=First_gen[j]
#                new_generation[chromosome[j]]=list_1
#                break
        new_generation[chromosome[i]]=list_1
    
    for i in new_generation.keys():
        chrom_dict[i]=new_generation[i]
        
    for i in range(len(new_chromosome)):
        chromosome.append(new_chromosome[i])
        
#cross_gen(First_gen,chrom_dict)        

#TERMINATION CONDITION BY FIXING NO OF GENERATION    
num_gen=1
Chromo_Fitness=dict_chromo_fitness(chromosome)
for i in range(num_gen):
#    Fitness_Value_of_chromosome(a)
    Chromo_Fitness=dict_chromo_fitness(chromosome)
    First_gen=dict_First_gen(chromosome)
    cross_gen(First_gen,chrom_dict)       #gives new chrom_dict and chromosome
    Chromo_Fitness=dict_chromo_fitness(chromosome)
    