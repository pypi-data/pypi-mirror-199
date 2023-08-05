from setuptools import setup
import pyfiglet 
import sys




with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='chromedrivermutual-update',
    version='0.0.6',
    license='MIT License',
    author='Thiago Graça',
    long_description=readme,
    post_install_message="Thanks for installing v: 0.0.5 chromedrivermutual-update!",
    long_description_content_type="text/markdown",
    author_email='thiago448@gmail.com',
    keywords='chromedriver update, selenium, chromedriver',
    description=u'Update automatic for automations python, when your path, takes your chrome version and update ',
    packages=['update_chrome'],
    install_requires=['requests','wget'],


    
    
    ),



