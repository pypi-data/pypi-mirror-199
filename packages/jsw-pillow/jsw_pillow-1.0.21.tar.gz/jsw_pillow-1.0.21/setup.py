# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jsw_pillow', 'jsw_pillow.modules']

package_data = \
{'': ['*'], 'jsw_pillow.modules': ['fonts/*']}

install_requires = \
['pillow>=9.3.0,<10.0.0',
 'python-resize-image>=1.1.20,<2.0.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'jsw-pillow',
    'version': '1.0.21',
    'description': 'Pillow for jsw.',
    'long_description': "# jsw-pillow\n> Pillow for jsw.\n\n## installation\n```shell\npip install jsw-pillow -U\n```\n\n## usage\n- watermark\n\n### Watermark\n> Watermark 水印的基本生成API。\n\n![Alt text](https://tva1.sinaimg.cn/large/008vxvgGgy1h7su9f3j8pj30uh0p6n1z.jpg)\n\n```python\n# watermark\nfrom jsw_pillow import Watermark\n\n# watermark - single\nim1 = Watermark.multiple(\n    source='./__tests__/assets/test.png',\n    mark='js.work',\n    font_size=50,\n    angle=45,\n    position='center',\n    color=(0, 255, 0, int(255 * 0.5)),\n)\n\n# watermark - multiple\nim2 = Watermark.multiple(\n    source='./__tests__/assets/test.png',\n    mark='js.work',\n    font_size=50,\n    angle=45,\n    color=(0, 255, 0, int(255 * 0.5)),\n)\n```\n\n## positions\n> Only for single watermark.\n\n![Alt text](https://tva1.sinaimg.cn/large/008vxvgGgy1h7u1m6nmvkj30gh0evt92.jpg)",
    'author': 'aric',
    'author_email': '1290657123@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://js.work',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
