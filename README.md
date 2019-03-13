# UPCF
对传统基于用户的协同过滤（CF）推荐算法的实现。以及对我毕业论文（基于用户画像与协同过滤的混合推荐系统研究）中提出新方法的实现。是用MovieLens-1m数据集，主要目的是通过MAE、Persicion、Recall看预测评分的准确性。

## 算法概要
基于用户的协同过滤推荐算法中，笔者认为主要过程有三种步：
1. 用户-项目评分矩阵的构建
2. 用户间相似度的计算
3. 位置项目评分预测的计算

使用了皮尔逊相关系数（PCC）、余弦相似度（COS）、改进的余弦相似度（Adjust COS）三种传统的相似度算法，以及一种基于奇异性（SM）的相似度量算法。  
使用了加权聚合（WS）、改进的加权聚合（DFM）两种评分预测算法。  
我论文中提出的方法，是从用户-项目评分矩阵出发，来改进推荐算法预测评分的准确性。思路为将用户统计信息与评分矩阵相结合，构建出满秩、低维、能反映出用户偏好的用户-特征矩阵，来计算用户的相似度。  

## 总体介绍
每一个文件代表一个过程，并且需按顺序，由上到下依次执行。每一过程产生的数据，都用 CSV 输出在本地，供下一过程使用。
- 划分 ratings 数据集，输出 train_set.csv test_set.csv 两个文件（仅需执行一次，若需更换训练集、测试集则需再次执行）：
   1. DivideData
- 用于生成用户画像（传统基于用户的协同过滤不需要这一步），三个文件必须按书写顺序从前往后执行（依赖 users.dat train_set.csv 两个文件）。输出 user_profile.csv 文件。
   1. GenerateNewUserInfo
   2. MovieLabelIndex
   3. UserProfile
- 计算用户之间相似度（依赖生成的用户画像、训练集两个文件），输出 COS_UPsim.csv 文件:   
   1. CosUpSimilarity
   2. AdCosUpSimilarity
   3. PccUpSimilarity
- 对测试集中的项目进行评分预测（依赖 COS_UPsim.csv、train_set.csv 两个文件），输出 prediction_rate_cos_upsim_*.csv 文件：
   1. WsPredictionRate
   2. DfmPredictionRate
- 计算 MAE 值，输出 mae_cosup_*.csv 文件：
   1. EvaluateMaeInDifferentK_Ws
   2. EvaluateMaeInDifferentK_Dfm
- 计算 P、R 值，输出 pr_cosup_Dfm.csv 文件（WS需要的自己做）：
   1. EvaluatePRinDifferentN

old_method 中是对传统基于用户协同过滤推荐算法的实现。
