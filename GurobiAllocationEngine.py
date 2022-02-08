from gurobipy import *
from GurobiOutput import *
from HomeDepotData import HomeDepotData

class AllocationModel():

   def __init__(self, data, costOn=False, allocationPen=1, MQCPen=1):

      self.data = data

      self.gurobi = Model("allocation")##Begin model
      
      self.x = {}
      for i in data.I:
         for j in data.R[i]:
            if costOn: self.x[i,j] = self.gurobi.addVar(obj=data.cost[i,j], vtype=GRB.INTEGER, name=('x[%s,%s]'%(i,j)).replace(" ", "_"))
            else: self.x[i,j] = self.gurobi.addVar(obj=0, vtype=GRB.INTEGER, name=('x[%s,%s]'%(i,j)).replace(" ", "_"))

      self.y = {} ##Decision variable for MQC penalties by carrier
      for k in data.K:
         self.y[k] = self.gurobi.addVar(obj=MQCPen, name=('y[%s]'%k).replace(" ", "_"))

      self.z = {} ##Decision variable for target penalties by carrier
      for k in data.K:
         for l in data.L: ##REMEMBER TO FIX L TO NOT INCLUDE EXTRA LANES
            if (k,l) in data.target:
               #self.z[k,l] = self.gurobi.addVar(obj=data.targetpen[k,l], name=('z[%s,%s]'%(k,l)).replace(" ", "_"))
               self.z[k,l] = self.gurobi.addVar(obj=allocationPen, name=('z[%s,%s]'%(k,l)).replace(" ", "_"))

      self.gurobi.update()


      ###MQC constraints
      for k in data.K:
         self.gurobi.addConstr(self.y[k] >= (data.MQC[k] - quicksum(quicksum(self.x[i,j]*i.FEU for i in data.P[j]) for j in data.C[k])), ('y_pen[%s]'%k).replace(" ", "_"))

      ####Target constraints
      for k in data.K:
         for l in data.L: ##REMEMBER TO FIX L TO NOT INCLUDE EXTRA LANES
            if (k,l) in data.target:
               self.gurobi.addConstr(self.z[k,l] >= (data.target[k,l] - quicksum(quicksum(self.x[i,j]*i.FEU for j in data.C[k].intersection(data.R[i])) for i in data.O[l])), ('z_under[%s,%s]'%(k,l)).replace(" ", "_"))
               self.gurobi.addConstr(self.z[k,l] >= (quicksum(quicksum(self.x[i,j]*i.FEU for j in data.C[k].intersection(data.R[i])) for i in data.O[l]) - data.target[k,l]), ('z_over[%s,%s]'%(k,l)).replace(" ", "_"))

      ####Count constraints
      for i in data.I:
         self.gurobi.addConstr(quicksum(self.x[i,j] for j in data.R[i]) == data.count[i], ('count[%s]'%i).replace(" ", "_"))

      ###Capacity constraints (user inputted)
      

      ###Force allocations that were already made
      for i in data.alreadyAllocated:
         for j in data.alreadyAllocated[i]:
            if (i,j) in self.x:
               self.gurobi.addConstr(self.x[i,j] >= data.alreadyAllocated[i][j], ('original_x[%s,%s]'%(i,j)).replace(" ", "_"))

      ###Set capacity constraints
      for (k, l) in data.CarrierCaps:
         self.gurobi.addConstr(data.CarrierCaps[k,l] >= quicksum(quicksum(self.x[i,j]*i.FEU for j in data.C[k].intersection(data.R[i])) for i in data.O[l]), ('cap[%s, %s]'%(k,l)).replace(" ", "_"))
         

      self.gurobi.update()
      self.gurobi.params.MIPGap=0.0025
      self.gurobi.optimize()
      self.gurobi.write("model.lp")

      
