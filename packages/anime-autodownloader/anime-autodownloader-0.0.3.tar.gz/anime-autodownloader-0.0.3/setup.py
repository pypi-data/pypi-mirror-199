# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['anime_autodownloader']

package_data = \
{'': ['*']}

install_requires = \
['filelock>=3.10.4,<4.0.0',
 'requests>=2.28.2,<3.0.0',
 'selenium>=4.8.2,<5.0.0',
 'uuid-by-string>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'anime-autodownloader',
    'version': '0.0.3',
    'description': 'A package for downloading animes automatically from a given streaming website',
    'long_description': '# anime-autodownloader\nA package for automatically download animes. For now supported websites are\n- AnimeUnity: https://animeunity.tv\n\n## Installation\nTo install from PyPI simple type\n```\npip install anime-autodownloader\n```\n\n### From source code\n- You need first to install poetry https://python-poetry.org/docs/#installation\n- Then clone this repository, go inside it and type the command \n```\npoetry install\n```\n\n\n## Usage\n\n```python\nimport logging\nfrom pathlib import Path\nfrom anime_autodownloader import configure_logger, getNavigator, getSupportedSites, Downloader\n\nloglevel = logging.INFO\nlogger = logging.getLogger()\nconfigure_logger(logger, loglevel, logfile="anime_download.log")\n\nnav = getNavigator("AnimeUnity", "https://www.animeunity.tv/anime/2791-jujutsu-kaisen")\n\nlogger.info("start")\noutput_dir = Path.home() / "Downloads"\n\nnav.visitBaseUrl()\nurls = nav.collectAllDownloadUrls()\n\ndw = Downloader(num_workers=5, output_dir=output_dir)\ndw.download_files(urls, timeout=5400, blocking=True)\n```',
    'author': 'Luca Paganin',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/LucaPaganin/animedownloader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
