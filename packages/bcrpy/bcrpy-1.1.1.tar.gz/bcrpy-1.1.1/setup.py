# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bcrpy']

package_data = \
{'': ['*']}

install_requires = \
['iteration-utilities>=0.11.0,<0.12.0',
 'matplotlib>=3.7.1,<4.0.0',
 'numpy>=1.24.2,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'requests>=2.28.2,<3.0.0',
 'sphinx>=6.1.3,<7.0.0',
 'tqdm>=4.65.0,<5.0.0']

setup_kwargs = {
    'name': 'bcrpy',
    'version': '1.1.1',
    'description': 'Un cliente API para la extraccion, consulta y analisis de la base de datos BCRPData del Banco Central de Reserva del Peru (BCRP)',
    'long_description': '# bcrpy\n\n[![](docs/img/bcrpy.png)](https://bcrpy.readthedocs.io/en/latest/)\n\n\nUn cliente API para la extraccion, consulta y analisis de la base de datos [BCRPData](https://estadisticas.bcrp.gob.pe/estadisticas/series/) del [Banco Central de Reserva del Peru (BCRP)](https://www.bcrp.gob.pe/) escrito para Python. Este cliente es un _wrapper_ de la [API para Desarrolladores](https://estadisticas.bcrp.gob.pe/estadisticas/series/ayuda/api) del BCRP.\n\n![](docs/img/bcrp.png)\n\n## Vinculos \n\n[Documentación en linea (readthedocs)](https://bcrpy.readthedocs.io/en/latest/) \n\n[Manual bcrpy (pdf)](https://raw.githubusercontent.com/andrewrgarcia/bcrpy/main/bcrpy.pdf)\n\n[pip package index](https://pypi.org/project/bcrpy/) \n\n# Instalacion\n\nEn su sistema local (laptop o computadora) bcrpy puede ser instalada con el comando pip install bcrpy. Aun asi, se\nrecomienda instalar bcrpy dentro de un ambiente virtual virtualenv. El protocolo para aquel seria el siguiente:\n\n\n```ruby\nvirtualenv venv\nsource venv/bin/activate\npip install bcrpy\n```\n\nbcrpy ha sido desarrollado con un protocolo de programación orientada a objetos (tambien conocido como *Object\nOriented Programming (OOP)*) lo cual se reduce a que objetos pueden ser usados a almacenar metodos (funciones),\ndatos, y su manejo de aquellos.\n\n\n[![](docs/img/colaboratory.svg)](https://colab.research.google.com/drive/1YdyCYeU0S98428WgBg4n9Ad9auKrurQZ?usp=sharing)\n',
    'author': 'andrewrgarcia',
    'author_email': 'garcia.gtr@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
