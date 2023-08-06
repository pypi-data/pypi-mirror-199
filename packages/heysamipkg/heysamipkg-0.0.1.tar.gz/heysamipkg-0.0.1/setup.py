from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Say hello for samiforgit package.'
LONG_DESCRIPTION = 'Say hello for samiforgit package long description.'

setup(
    name='heysamipkg',
    version=VERSION,
    author="Md Samiul Alim",
    author_email="<mdsamiul05@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'print'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ])
