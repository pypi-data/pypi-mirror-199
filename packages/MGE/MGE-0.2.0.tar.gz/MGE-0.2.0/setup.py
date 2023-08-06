from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='MGE',
    version='0.2.0',
    license='MIT License',
    author='Lucas Guimarães',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='lucasguimaraes.commercial@gmail.com',
    keywords='MGE pygame',
    description=u'A library for creating games and interfaces graphics',
    packages=['MGE'],
    install_requires=['pygame', 'numpy', 'pillow', 'opencv-python', 'screeninfo', 'pyperclip'],)
