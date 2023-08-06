# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_chatgpt_turbo']

package_data = \
{'': ['*'],
 'nonebot_plugin_chatgpt_turbo': ['.idea/*', '.idea/inspectionProfiles/*']}

install_requires = \
['aiohttp>=3.8.4,<4.0.0',
 'nonebot-adapter-onebot>=2.2.1,<3.0.0',
 'nonebot2>=2.0.0rc3,<3.0.0',
 'openai>=0.27.0,<0.28.0']

setup_kwargs = {
    'name': 'nonebot-plugin-chatgpt-turbo',
    'version': '0.3.0',
    'description': 'A nonebot plugin for openai gpt3.5-turbo',
    'long_description': '<div align="center">\n  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>\n  <br>\n  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>\n</div>\n\n<div align="center">\n\n# nonebot-plugin-chatgpt-turbo\n</div>\n\n# 介绍\n- 本插件适配OpenAI在2023年3月1日发布的最新版API，可以在nonebot中调用OpenAI的ChatGPT生产环境下的模型（GPT3.5-turbo）进行回复。\n- 接口调用速度与网络环境有关，经过测试，大陆外的服务器的OpenAI API响应时间能在十秒之内。\n- 免费版OpenAI的调用速度限制为20次/min\n- 本插件具有上下文回复功能(可选)，根据每个成员与机器人最近30条（可修改）的聊天记录进行响应回复,该功能消耗服务器资源较大\n# 安装\n\n* 手动安装\n  ```\n  git clone https://github.com/Alpaca4610/nonebot_plugin_chatgpt_turbo.git\n  ```\n\n  下载完成后在bot项目的pyproject.toml文件手动添加插件：\n\n  ```\n  plugin_dirs = ["xxxxxx","xxxxxx",......,"下载完成的插件路径/nonebot-plugin-gpt3.5-turbo"]\n  ```\n* 使用 pip\n  ```\n  pip install nonebot-plugin-chatgpt-turbo\n  ```\n\n# 配置文件\n\n在Bot根目录下的.env文件中追加如下内容：\n\n```\nOPENAI_API_KEY = key\nOPENAI_MODEL_NAME = "gpt-3.5-turbo"\nOPENAI_HTTP_PROXY = "http://127.0.0.1:8001"    # 请使用代理访问api，中国大陆/香港IP调用API有几率会被封禁\n```\n\n可选内容：\n```\nOPENAI_MAX_HISTORY_LIMIT = 30   # 保留与每个用户的聊天记录条数\nENABLE_PRIVATE_CHAT = True   # 私聊开关，默认开启，改为False关闭\n```\n\n\n# 使用方法\n\n- @机器人发送问题时机器人不具有上下文回复的能力\n- chat 使用该命令进行问答时，机器人具有上下文回复的能力\n- clear 清除当前用户的聊天记录\n',
    'author': 'Alpaca',
    'author_email': 'alpaca@bupt.edu.cn',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
