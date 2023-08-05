# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zetops',
 'zetops.zetmiko',
 'zetops.zetmiko.fiberhome',
 'zetops.zetmiko.hillstone',
 'zetops.zetmiko.huawei',
 'zetops.zetmiko.mypower']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'zetops',
    'version': '0.1.8',
    'description': 'A NetDevOps package aiming to improve NetDevOps(network automation) development efficiency for network development engineer!',
    'long_description': '\n# ZetOps\nZetOps是旨在提高网络运维自动化开发效率的一款工具包。\n\n名字的来源主要是之前做过的一个项目，叫做“织网”，\n\n你可以把z看做是“自”，它旨在解决网络自动化开发效率问题，垂直于网络自动化开发领域。\n\n你可以把Z看做是"织"，代表的是网络自动化人一针一线缝缝补补编织梦想的精神。\n\n你可以把Z看做是“中”,它的一大特色是应对国产化趋势之下国内网络设备适配的不足。\n\n你可以把Z看做是“N”的转置，代表的是网络人锐意创新的决心。\n\n然而，目前它还刚刚起步。\n\n# RoadMap\n\n1. 在这个最初的版本，我会聚焦在netmiko对国产化设备适配的不足，写一些国产化设备的驱动。\n\n对华为、山石、烽火进行了适配。\n\n2. 后续将会分享一些自己写的国产化textfsm的模板，也会试图寻求网友的帮助。\n\n3. 我会根据自己的理解，创建一个基于CLI的类似napalm的网络抽象层，不过这块可大可小，可能还需要我再思考一下。\n\n4. 同时也会针对NetDevOps场景中的数据提取和配置备份做一些nornir的task模块\n',
    'author': 'feifeiflight',
    'author_email': 'feifeiflight@126.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jiujing/zetops',
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
