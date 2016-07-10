from setuptools import setup, find_packages

setup(name='overwatch_events',
    version='0.1',
    description="Parsers upcoming Overwatch events",
    url='',
    author='Ewen Chou',
    author_email='ewenchou@gmail.com',
    license='Apache 2.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'lxml',
        'cssselect'
    ],
    zip_safe=False)
