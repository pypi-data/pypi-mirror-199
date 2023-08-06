from distutils.core import  setup
import setuptools
packages = ['sprec']# 唯一的包名，自己取名
setup(name='sprec',
	version='1.0',
	author='hhh',
    packages=packages,
    package_dir={'requests': 'requests'},)
