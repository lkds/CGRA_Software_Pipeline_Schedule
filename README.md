# CGRA_Software_Pipeline_Schedule
Coarse-Grained Reconfigurable Architecture supported software pipeline loop scheduling project

## 背景描述
### CGFA：粗粒度可重构架构
### 软件流水：最小化循环间隔

## 问题定义
### 目标
对循环体 DFG 进行调度，使调度之后的DFG 满足资源约束和长依赖约束，最小化CGRA计算阵列的处理单元使用量
### 约束
* **依赖约束**
  * $$t_j\$$
* **资源约束**
* **依赖长度约束**