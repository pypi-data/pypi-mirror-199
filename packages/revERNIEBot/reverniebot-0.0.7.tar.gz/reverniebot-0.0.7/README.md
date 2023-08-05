# revERNIEBot

文心一言 API

- [x] Selenium方法
- [ ] requests调用协议方法

目前仅支持使用Selenium的方案

## 安装

### 安装Chrome

<details>
<summary>Windows系统</summary>

自行前往 https://www.google.cn/chrome/index.html 下载安装

</details>
<details>
<summary>Ubuntu/Debian系统</summary>

安装依赖软件
```bash
sudo apt install udev fonts-liberation libu2f-udev libvulkan1 xdg-utils -y
```

下载Chrome安装包
```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
```

安装Chrome
```bash
sudo dpkg -i google-chrome-stable_current_amd64.deb
```

检查Chrome版本
```bash
google-chrome -version
```

记住此版本号

</details>

<details>
<summary>CentOS/Rocky Linux系统</summary>

安装Chrome

```bash
yum install https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
```

</details>
<!-- 
### 下载ChromeDriver

<details>
<summary>点击此处展开</summary>

前往 https://registry.npmmirror.com/binary.html?path=chromedriver/

找到对应你Chrome版本号的目录，根据系统下载其中的文件，解压到任意目录

</details> -->

### 下载browsermob-proxy

<details>
<summary>点击此处展开</summary>

前往 https://github.com/lightbody/browsermob-proxy/releases/tag/browsermob-proxy-2.1.4 

下载 `browsermob-proxy-2.1.4-bin.zip`，解压

</details>

## 使用

1. 安装本依赖库

```bash
pip3 install --upgrade revERNIEBot
```

2. 安装 [Chrome/Edge](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) 或 [Firefox](https://addons.mozilla.org/en-US/firefox/addon/cookie-editor/) 上的Cookies Editor插件
3. 前往yiyan.baidu.com

4. 打开此插件，点击`Export`->`Export as JSON`，将复制的Cookies内容保存到文件`cookies.json`

5. 代码调用

```python
from revERNIEBot.selenium import ChatBot  # 目前仅支持Selenium的方案

chatbot = ChatBot(
    cookieFile="cookies.json"
    browsermobProxyPath="pathToBrowserMobProxyExecFile",  # browsermob-proxy的可执行文件路径，详见下方说明
)

print(chatbot.ask("你好"))  # 获取回复
print(chatbot.ask("你是谁？"))

chatbot.reset_session()  # 开启新对话

chatbot.quit()
```

- `browsermobProxyPath`：填写刚刚下载的browsermobproxy的压缩包解压出来的`bin/`中的可执行文件路径，例如Linux系统下填写`bin`中的`browsermob-proxy`的路径，Windows填写`browsermob-proxy.bat`路径（Windows系统下需要将路径使用\\分隔）
- 系统上的java版本不能高于java8

## 注意

- 有问题请在issue中发起讨论
- 此仓库仅供学习
