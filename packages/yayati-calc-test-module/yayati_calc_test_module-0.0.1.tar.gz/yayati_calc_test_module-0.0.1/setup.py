from setuptools import setup, find_packages

classifiers = [
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
]

setup(
    name='yayati_calc_test_module',
    version='0.0.1',
    description='A basic calculator for testing pypy.',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Yayati Naresh Palai',
    author_email='yayati@cat.hokudai.ac.jp',
    license='MIT',
    classifiers=classifiers,
    keywords='calculator',
    packages=find_packages(),
    install_requires=['']
)