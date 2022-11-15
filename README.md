# OutOfSwufe

**[OutOfSwufe](https://github.com/JinHanLei/OutOfSwufe)** ——西南财经大学一键报备出校门<br>
懒惰是第一生产力，每次出去吃饭都得点进swufe移动校园，填几乎一样的报备信息，好麻烦(⑉･̆-･̆⑉)，就写了这个程序

- 前提：得有个**服务器**，服务器有**python**环境

- 代码中的username和password替换为这里的帐号密码：[统一身份认证平台](https://authserver.swufe.edu.cn/authserver)

### 部署

```shell
pip install - r requirements.txt
python app.py
```

### 实现方案

手机快捷指令——访问网站（服务器ip:8000）

### 代码解析

#### 方法

1. index()：主方法
2. login()：帐号密码登录统一身份认证平台，获得你的登录信息
3. baobei()：用你的登录信息完成报备

#### 技能

- flask微服务
- 爬虫
- 正则

#### 难点

- 登录密码是动态加密的，这里采用的方案是：get其用于加密的js文件，直接用execjs执行js代码
- 登录时post的数据较多，且有动态的，这里采用的方案是：正则解析网站相关参数，填入dist变量
- 报备时post的数据也较多，同样正则解析

**声明：本程序仅做学习使用，其中内容仅作示例。目的地、出行方式、报备原因等在使用时，应根据实际情况做相应修改。因没有修改信息而造成问题，本程序及程序作者概不负责~**
