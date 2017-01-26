# LastbChecker
基于Python的Linux-sshd登录失败检测以及ip拉黑
## 使用场景
开放远程ssh密码登陆的Linux服务器。定期（默认30s）检查尝试爆破登陆的ip，并拉黑登录失败的ip。
## 使用
```
cd path_to_the_project
sudo pip install -r requirements.txt
python check_lastb.py
```
## 检查&拉黑策略  
do_easy_check（目前默认）：定时检查lastb命令，并逐条虑重+拉黑
## 注意
目前仅可使用 ```do_easy_check``` 作为检查策略。其他高级策略目前开发中
## 开发计划
1. 【p0】本地进程重启后，读取之前已拉黑的ip，在之前的基础上继续检查
2. 【p1】启用云备份、云设置。黑名单可以自动备份、手动解除
3. 【p2】高级check：时效性、准确性增强