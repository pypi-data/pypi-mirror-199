# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['onestep', 'onestep.broker', 'onestep.broker.store', 'onestep.middleware']

package_data = \
{'': ['*']}

install_requires = \
['asgiref>=3.6.0,<4.0.0']

extras_require = \
{'rabbitmq': ['amqpstorm>=2.10.6,<3.0.0']}

setup_kwargs = {
    'name': 'onestep',
    'version': '0.0.2',
    'description': '',
    'long_description': '# OneStep\n\n内部测试阶段，请勿用于生产\n\n## example\n\n```python\nfrom onestep import step\nfrom onestep.broker import WebHookBroker\n\nstep.set_debugging()\n\nwebhook_broker = WebHookBroker(path="/push")\n\n\n@step(from_broker=webhook_broker)\ndef build_todo_list(message):\n    return 1\n\n\nif __name__ == \'__main__\':\n    step.start(block=True)\n```',
    'author': 'miclon',
    'author_email': 'jcnd@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
