from pulp import LpMinimize, LpProblem, LpVariable, lpSum, LpMaximize, LpSolverDefault
import pandas

# 读取数据
fileName = "g2"
df = pandas.read_csv("src/"+fileName+".CSV", header=None)
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
# 求最小的最大值
for i in range(maxStep):
    prob += lpSum(vDict[j][i+maxStep*j]
                  for j in range(maxNode)) <= lpSum(maxPE)

# 资源约束
for i in range(maxStep):
    # 每一个时间步的资源总数不得超过16
    prob += lpSum(vDict[j][i + maxStep * j] for j in range(maxNode)) <= 16

# 节点单步约束
# 每个节点的实践步只有一个
for i in range(maxNode):
    prob += lpSum(vDict[i]) == 1

# 完成约束
# 所有调度时间步必须和节点数目相同
prob += lpSum(lpSum(vDict[i]) for i in range(maxStep)) == maxNode

# 长/依赖约束
for i in range(maxNode):
    for k in range(1, 5):
        # 如果有子节点
        if (df[i][k] != 0):
            # 子节点调度步数在父节点之后
            prob += lpSum(vDict[i][j+maxStep*i] * j for j in range(maxStep)
                          ) <= lpSum(vDict[df[i][k] - 1][m + maxStep * (df[i][k] - 1)] * m for m in range(maxStep))
            for kp in range(1, maxStep):
                # 长依赖约束，不能是倍数
                prob += lpSum(vDict[i][j+maxStep*i] * j for j in range(maxStep)
                              ) != lpSum(vDict[df[i][k] - 1][m+maxStep*(df[i][k] - 1)] * m for m in range(maxStep)) * kp * ii

# 时间步约束
# 节点的时间步必须在规定时间内
for i in range(maxNode):
    prob += lpSum(vDict[i][j+maxStep*i] for j in range(maxStep)) == lpSum(vDict[i][j+maxStep*i]
                                                                          for j in range(df[i][5], df[i][6]+1))

# LpSolverDefault.msg = 1
status = prob.solve()
print("求解完成")
print("最小资源使用为：")
print(maxPE.varValue)

# 输出结果
res = []
for i in range(maxNode):
    res.append(sum(vDict[i][j + maxStep * i].varValue *
                   j for j in range(maxStep)))

result = pandas.DataFrame()
result['No'] = df.T[0]
result['TimeStep'] = res
result['Sub1'] = df.T[1]
result['Sub2'] = df.T[2]
result['Sub3'] = df.T[3]
result['Sub4'] = df.T[4]
result['Type'] = 0
result['SrcNo'] = result['No']

result.to_csv('Result-'+fileName+'.csv', index=None)
print("求解结果保存到 Result-"+fileName+".csv")
