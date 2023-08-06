from distutils.core import setup

setup(name='extensible-keys',
      version='v0.2.1',
      description='Reference implementation for the Extensible Key Format file format',
      author='FortunateSon1337',
      author_email='ForunateSon1337@protonmail.com',
      url = 'https://github.com/FortunateSon1337/extensible-keys',
      install_requires = ['pycryptodome'],
      py_modules=['extensiblekeys'],
      license='GPLv3')
      