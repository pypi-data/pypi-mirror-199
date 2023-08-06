from setuptools import setup, find_packages

setup(
    name='py_colored_logs',
    version='1.0',
    author='AndrewFox_DEV',
    description='You will be able to color Python logs with this little module. The colorable logs are as follows: success log, warning log, error log, and info log!',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AndrewFox-DEV/Python-colored-logs',
    packages=find_packages(),
    install_requires=[
        'colorama>=0.4.6'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ]
)
