from distutils.core import setup
import setuptools

packages = ['pymongoRawQuery']  # 唯一的包名，自己取名
setup(name='pymongoRawQuery',
      version='1.0',
      author='YiZhang.You',
      packages=packages,
      package_dir={'pymongo': 'pymongo'}, )
