from setuptools import setup, find_packages

VERSION = '1.0'
DESCRIPTION = 'A Prank program for confessing love to your crush'

# Setting up
setup(
    name="cybersafeiloveu",
    version=VERSION,
    author="Min Sovan Sokheng(Cody) and CyberSafe Team",
    author_email="hengmin1213@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    keywords=['python', 'Messagebox'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)