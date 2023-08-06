from setuptools import setup, find_packages

def readme():
  with open('README.md', 'r') as f:
    return f.read()

setup(
  name='baddrop',
  version='1.0.0',
  author='Dvurechensky',
  author_email='dvurechensky_pro@mail.com',
  description='Rebuild Airdrop',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='http://89.207.90.60:3000/dvurechensky/STM.git',
  packages=find_packages(),
  install_requires=['setuptools~=57.5.0',
  'bs4', 'lxml', 'fleep'
  , 'Pillow', 'pybluez', 'requests', 'pycrypto', 
  'netifaces', 'prettytable', 'libarchive-c', 'ctypescrypto'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='airdrop smk',
  project_urls={
    'Documentation': 'http://89.207.90.60:3000/dvurechensky/STM/src/branch/master/README.md'
  },
  python_requires='>=2.7'
)