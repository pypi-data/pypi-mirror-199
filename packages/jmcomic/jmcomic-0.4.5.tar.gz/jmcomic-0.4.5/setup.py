import os
import codecs

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = "\n" + f.read()

version = '0.4.5'

setup(
    name='jmcomic',
    version=version,

    description='Python API For JMComic (禁漫天堂)',
    long_description_content_type="text/markdown",
    long_description=long_description,

    author='hect0x7',
    author_email='93357912+hect0x7@users.noreply.github.com',

    packages=find_packages(),
    install_requires=[
        'commonX',
        'curl_cffi',
        'PyYAML',
        'Pillow',
        'setuptools',
    ],

    keywords=['python', 'jmcomic', '18comic', '禁漫天堂', 'NSFW'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
