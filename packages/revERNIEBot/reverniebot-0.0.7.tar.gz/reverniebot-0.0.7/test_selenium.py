from revERNIEBot import selenium

import colorlog

import logging


sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
sh.setFormatter(colorlog.ColoredFormatter(
    fmt="%(log_color)s[%(asctime)s.%(msecs)03d] %(filename)s (%(lineno)d) - [%(levelname)s] : "
        "%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    log_colors={
        'DEBUG': 'green',  # cyan white
        'INFO': 'white',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'cyan',
    }
))
logging.basicConfig(level=logging.DEBUG,  # 设置日志输出格式
                    format="[%(asctime)s.%(msecs)03d] %(filename)s (%(lineno)d) - [%(levelname)s] : %(message)s",
                    handlers=[sh],
                    # 日志输出的格式
                    # -8表示占位符，让输出左对齐，输出长度都为8位
                    datefmt="%Y-%m-%d %H:%M:%S"  # 时间输出的格式
                    )


bot = selenium.ChatBot(
    cookieFile="cookies.json",
    browsermobProxyPath="res/browsermob-proxy-2.1.4/bin/browsermob-proxy",
)

print(bot.ask("你叫什么"))

bot.quit()

