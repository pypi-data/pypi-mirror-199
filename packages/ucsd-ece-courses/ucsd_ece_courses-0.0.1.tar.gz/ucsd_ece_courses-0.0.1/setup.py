from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

VERSION = '0.0.1'
DESCRIPTION = "UCSD ECE Department's course catalog"
LONG_DESCRIPTION = "A neat package to scrape, organize, and filter for UCSD ECE Department's course catalog."

# Setting up
setup(
    name='ucsd_ece_courses',
    version=VERSION,
    author='kendrick010',
    author_email='ken010@ucsd.edu',
    description=DESCRIPTION,
    long_description_content_type='text/markdown',
    long_description=long_description,
    packages=find_packages(),
    install_requires=['requests', 'beautifulsoup4'],
    extras_require={'dev': ['wheel', 'twine']},
    python_requires='>=3.10',
    keywords=['python', 'ucsd', 'web-scraping'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ]
)