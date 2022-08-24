# sort_by_zero_shot
这是利用rpc写的一个后端程序，输入标签和topk，然后利用zero_shot_classification得到排序top_k的句子
# json文件即为我们的数据集
# 使用说明
输入：
用户输入标签和想要看到句子个数
输出：
句子和它对应的置信度
我将其保存为json文件
#
首先启动rpc_server.py程序，这个程序可以提取加载模型
然后利用rpc_client.py输入两个变量，最后将结果保存为json文件
此外zero_shot.json为我们的数据集，在zero_shot.py脚本中需要改一下加载它的路径
