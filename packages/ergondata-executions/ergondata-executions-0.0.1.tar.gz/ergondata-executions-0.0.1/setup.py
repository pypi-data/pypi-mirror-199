from setuptools import setup

setup(
    name='ergondata-executions',
    version='0.0.1',
    description="Collection of methods to connect and interact with Ergondata's Execution API",
    author_email="daniel.vossos@ergondata.com.br",
    author='Daniel Anzanello Vossos',
    long_description=open("ergondata_executions/README.md").read() + '\n\n' + open(
        'ergondata_executions/changelog.txt').read(),
    url='',
    packages=['ergondata_executions'],
    license="MIT",
    keywords="executions"
)
