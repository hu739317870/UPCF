# UPCF
称这些文件为一个个的脚本更为合适，每个文件就是处理了 算法 中的一个步骤，所以需按顺序依次执行。论文需进行算法的比较，所以有些地方有多个方法，根据需求自行选择（用的笨方法，需自己手动去改）。
如果看过我的毕业论文（基于用户画像与协同过滤的混合推荐系统研究）会对理解代码有所帮助。是用MovieLens-1m数据集，主要目的是通过MAE、Persicion、Recall看预测评分的准确性。

## 算法概要
基于用户的协同过滤推荐算法中，笔者认为主要过程有三种步：
1. 用户-项目评分矩阵的构建
2. 用户间相似度的计算
3. 位置项目评分预测的计算

使用了皮尔逊相关系数（PCC）、余弦相似度（COS）、改进的余弦相似度（Adjust COS）三种传统的相似度算法，以及一种基于奇异性（SM）的相似度量算法。  
使用了加权聚合（WS）、改进的加权聚合（DFM）两种评分预测算法。  
我论文中提出的方法，是从用户-项目评分矩阵出发，来改进推荐算法预测评分的准确性。思路为将用户统计信息与评分矩阵相结合，构建出满秩、低维、能反映出用户偏好的用户-特征矩阵，来计算用户的相似度。  

## 总体介绍
每一个文件代表一个过程，并且需按顺序，由上到下依次执行。每一过程产生的数据，都用 CSV 输出在本地，供下一过程使用。python 版本为 2.XX。
1. 划分 ratings 数据集，输出 train_set.csv test_set.csv 两个文件（仅需执行一次，若需更换训练集、测试集则需再次执行）：
   - DivideData
2. 用于生成用户画像（传统基于用户的协同过滤不需要这一步），三个文件必须按书写顺序从前往后执行（依赖 users.dat train_set.csv 两个文件）。输出 user_profile.csv 文件。
   - GenerateNewUserInfo
   - MovieLabelIndex
   - UserProfile
3. 计算用户之间相似度（依赖生成的用户画像、训练集两个文件），输出 COS_UPsim.csv 文件:   
   - CosUpSimilarity
   - AdCosUpSimilarity
   - PccUpSimilarity
-----
之后根据自己需求执行不同的文件

4. 对测试集中的项目进行评分预测（依赖 COS_UPsim.csv、train_set.csv 两个文件），输出 prediction_rate_cos_upsim_*.csv 文件：
   - WsPredictionRate
   - DfmPredictionRate
5. 计算 MAE 值，输出 mae_cosup_*.csv 文件：
   - EvaluateMaeInDifferentK_Ws
   - EvaluateMaeInDifferentK_Dfm
6. 计算 P、R 值，输出 pr_cosup_Dfm.csv 文件（WS需要的自己做）：
   - EvaluatePRinDifferentN

old_method 中是对传统基于用户协同过滤推荐算法的实现。

## 718新增
1. 增加对用户冷启动问题的解决（Gold_Start)。试验了 100 位新用户仅使用用户信息进行评分预测后所得到的 MAE、P、R 值。
2. 实验了算法对用户属性的敏感性分析（G_A_O)。用户的 性别、年龄、职业，这种用户属性不同组合对算法的影响。

## 下一步工作
1. 重复代码过多，需进行改良
2. 继续完善其它推荐算法
