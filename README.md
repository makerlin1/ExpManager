Experiment Manager
===
## Intro
实验管理工具，支持以下功能：
- [x] 接受输入配置(包括各种超参数)，生成实验id并记录到leaderboard.csv文件
- [x] 记录实验结果，添加进leaderboard.csv
- [x] 实验结束后发送邮件通知（需要自行准备163邮箱账户与秘钥）
- [ ] 预构建一些基本Metric
## Quickly Start
```python
from ExpM import Trial
params = dict()
trial = Trial.record(record_path = "leaderboard.csv", **params) 
output_path = trial.output_path  # output path
# 训练结束，记录结果
result = dict()
trial.report_final_result(**result, profile=None)  # profile若为None则不发邮件
```