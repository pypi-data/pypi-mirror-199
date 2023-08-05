from setuptools import setup, find_packages

VERSION = '1.7'
DESCRIPTION = 'bangla-python'
LONG_DESCRIPTION = 'A comprehensive package for bangla language processing in python.<br> Find full documentation here: http://www.nahid.org/bangla-python '

# Setting up
setup(
    name="bangla-python",
    version=VERSION,
    author="Nahid Hossain (nahid@cse.uiu.ac.bd)",
    author_email="mailbox.nahid@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['bangla-python', 'bangla language processing', 'bangla tokenizer', 'remove bangla punctuation','remove foreign words from bangla text', 'remove bangla stop words', 'bangla number to word from text','find bangla numbers from text', 'bangla to english number conversion','english to bangla number conversion','bangla number to word conversion'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)