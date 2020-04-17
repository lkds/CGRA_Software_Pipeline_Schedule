from pulp import LpVariable

x = LpVariable("x", lowBound=None, upBound=None, cat='Integer')
y = LpVariable("y", lowBound=None, upBound=None, cat='Integer')
prob = LpProblem("myProblem", LpMinimize)
prob += x + y <= 2
prob += -4*x + y
status = prob.solve()
