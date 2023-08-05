from setuptools import setup
import pyfiglet 
import sys

from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint 
from pyfiglet import figlet_format
version='0.0.5'


with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='chromedrivermutual-update',
    install_requires=['requests','wget','pyfiglet','termcolor','colorama'],
    version=version,
    license='MIT License',
    author='Thiago Graça',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='thiago448@gmail.com',
    keywords='chromedriver update, selenium, chromedriver',
    description=u'Update automatic for automations python, when your path, takes your chrome version and update ',
    packages=['update_chrome'],

    
    
    ),



    
print("Chrome Driver mutual update - are you ready??")
cprint(figlet_format('V: {}'.format(version), width= 500, font='starwars'),
       'white',  attrs=['bold'])