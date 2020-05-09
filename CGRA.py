from pulp import LpMinimize, LpProblem, LpVariable, lpSum, LpMaximize, LpSolverDefault
import pandas

# 读取数据
df = pandas.read_csv("src/g1.CSV", header=None)
# 获取行数和列数
maxNode = df.shape[0]
maxStep = maxNode
ii = 3

df = df.T
# 构造变量字典
vName = [[i+j*maxStep for i in range(maxStep)] for j in range(maxNode)]

# 创建问题实例
prob = LpProblem("CGRA_Problem", LpMinimize)

# 创建变量字典
vDict = []
for i in range(maxNode):
    vDict.append(LpVariable.dicts('V', vName[i], 0, 1, 'Integer'))

maxPE = LpVariable("max_PE_node", 0, 16, cat='Integer')
# kp = LpVariable('kp', 1, 100, cat='Integer')
# 添加目标方程
prob += maxPE
# prob += lpSum(vDict[:][i])

# 添加约束
# 最大最小约束
for i in range(maxStep):
    prob += lpSum(vDict[:][i]) <= lpSum(maxPE)
# 资源约束
for i in range(maxStep):
    prob += lpSum(vDict[:][i]) <= 16
# 长/依赖约束
for i in range(maxNode):
    for k in range(1, 5):
        if(df[i][k] != 0):
            prob += lpSum(vDict[i][j+maxStep*i] * j for j in range(maxStep)
                          ) <= lpSum(vDict[df[i][k] - 1][m+maxStep*(df[i][k] - 1)] * m for m in range(maxStep))
            # prob += lpSum(vDict[i][j+maxStep*i] * j for j in range(maxStep)
            #               ) == lpSum(vDict[df[i][k] - 1][m+maxStep*(df[i][k] - 1)] * m for m in range(maxStep))

LpSolverDefault.msg = 1
status = prob.solve()
print(status)
