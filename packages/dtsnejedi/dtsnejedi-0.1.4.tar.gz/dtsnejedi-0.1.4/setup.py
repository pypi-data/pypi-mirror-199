
from setuptools import setup, find_packages
#python setup.py sdist bdist_wheel
#twine upload dist/*
setup(name = "dtsnejedi",
      author="Aleksandr Odnakov",
      author_email="me@dnakov.ooo",
      packages = find_packages(),
      install_requires = ['matplotlib','numpy','scipy','tqdm'],
      version='0.1.4')