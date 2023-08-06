# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot-plugin-resolver']

package_data = \
{'': ['*']}

install_requires = \
['PyExecJS>=1.5.1,<2.0.0',
 'aiohttp>=3.7,<4.0',
 'httpx>=0.23,<0.24',
 'lxml>=4.9,<5.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot2>=2.0.0-beta.5,<3.0.0',
 'tweepy>=4.12,<5.0']

setup_kwargs = {
    'name': 'nonebot-plugin-resolver',
    'version': '1.0.13',
    'description': 'NoneBot2链接分享解析器插件。解析视频、图片链接/小程序插件，tiktok、bilibili、twitter等实时发送！',
    'long_description': '<div align="center">\n  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>\n  <br>\n  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>\n</div>\n\n<div align="center">\n\n# nonebot-plugin-resolver\n\n_✨ NoneBot2 链接分享解析器插件 ✨_\n\n\n<a href="./LICENSE">\n    <img src="https://img.shields.io/github/license/owner/nonebot-plugin-resolver.svg" alt="license">\n</a>\n<a href="https://pypi.org/project/nonebot-plugin-resolver">\n    <img src="https://img.shields.io/pypi/v/nonebot-plugin-resolver.svg" alt="pypi">\n</a>\n<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">\n\n</div>\n\n## 📖 介绍\n\n适用于NoneBot2的解析视频、图片链接/小程序插件，tiktok、bilibili、twitter等实时发送！\n## 💿 安装\n\n1. 使用 nb-cli 安装，不需要手动添加入口，更新使用 pip\n\n```\nnb plugin install nonebot-plugin-resolver\n```\n\n2. 使用 pip 安装和更新，初次安装需要手动添加入口\n\n```\npip install --upgrade nonebot-plugin-resolver\n```\n\n## ⚙️ 配置\n\n在 nonebot2 项目的`.env`文件中添加下表中的可选配置\n\n```\n# twitter的token和本地代理\nbearer_token = ""\nresolver_proxy = "http://127.0.0.1:7890"\n```\n\n## 🎉 使用 & 效果图\n![help](./img/example.png)\n![help](./img/example2.png)\n![help](./img/example3.png)\n![help](./img/example4.png)\n![help](./img/example5.png)\n\n',
    'author': 'zhiyu1998',
    'author_email': 'renzhiyu0416@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/zhiyu1998/nonebot_plugin_resolver',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
