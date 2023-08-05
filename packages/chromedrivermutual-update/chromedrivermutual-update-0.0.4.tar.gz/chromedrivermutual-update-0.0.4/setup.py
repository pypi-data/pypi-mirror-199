from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='chromedrivermutual-update',
    version='0.0.4',
    license='MIT License',
    author='Thiago Graça',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='thiago448@gmail.com',
    keywords='chromedriver update, selenium, chromedriver',
    description=u'Update automatic for automations python, when your path, takes your chrome version and update ',
    packages=['update_chrome'],
    install_requires=['requests','wget'],)

