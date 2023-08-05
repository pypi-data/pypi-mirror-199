from setuptools import setup
import os

def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        return file.read()
    
setup(
    name='kube_app',
    version='0.12',
    packages=['kube_app'],
    license='MIT',
    author='lalit',
    author_email='lalit.krishna@kockpit.in',
    url='https://pypi.org/project/kube-app/',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
)
