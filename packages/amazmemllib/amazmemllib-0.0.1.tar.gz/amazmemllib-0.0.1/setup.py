# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['package']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'amazmemllib',
    'version': '0.0.1',
    'description': '',
    'long_description': '# Шаблон проекта pypi\n\n## Как применить шаблон к себе:\n- в pyproject.toml поменяйте данные на свой\n\n```\n[tool.poetry]\nname = "basic_pypi"\nversion = "0.0.2"\ndescription = ""\nauthors = ["Nikolay Baryshnikov <root@k0d.ru>"]\npackages=[\n    { include = "package" },\n]\nlicense="MIT"\nreadme="README.md"\nhomepage="https://github.com/p141592"\nrepository="https://github.com/p141592/basic_pypi"\nkeywords=["poetry", "pypi"]\n```\n\n- Установите классифайды которые подходят для вашего проекта https://pypi.org/classifiers/\n\n- Поменяйте автора лицензии\n\n```\nCopyright (c) 2020 Baryshnikov Nikolay\n```\n\n## Запушить проект в pypi\n\n- Зарегистрируйтесь там https://pypi.org/account/register/\n- Если poetry еще не установлен, установите `pip install poetry`\n- Выполните `make push` в корне проекта. В консоли попросят ввести логин/пароль от учетки в pypi\n- Наслаждайтесь проектом в pypi `pip install <имя проекта, которое [tool.poetry].name>`\n',
    'author': 'Nikolay Baryshnikov',
    'author_email': 'root@k0d.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/p141592',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
