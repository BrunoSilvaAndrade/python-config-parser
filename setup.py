import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='python-config-parser',
    version='2.0.3',
    author='Bruno Silva de Andrade',
    author_email='brunojf.andrade@gmail.com',
    description='Project created to given the possibility of create dynamics config files',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/BrunoSilvaAndrade/python-config-parser',
    py_modules=['pyconfigparser'],
    install_requires=open('requirements.txt', 'r').read().split('\n'),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)