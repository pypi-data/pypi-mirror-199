from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='beggs-and-brill',
    version='0.0.1',
    license='MIT License',
    author='Matheus Delduque',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='matheusdelduque1@gmail.com',
    keywords='begss and brill',
    description=u'Funções para beggs and brill',
    packages=['beggs_and_brill_MatheusDelduque'],
    install_requires=['math'],)