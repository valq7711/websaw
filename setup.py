from setuptools import setup

__author__ = "Kucherov Valery <valq7711@gmail.com>"
__license__ = "MIT"
__version__ = "0.0.1"

setup(
    name="websaw",
    version=__version__,
    url="https://github.com/valq7711/websaw",
    license=__license__,
    author=__author__,
    author_email="valq7711@gmail.com",
    maintainer=__author__,
    maintainer_email="valq7711@gmail.com",
    description="websaw - a web framework for rapid development with pleasure",
    platforms="any",
    keywords='python webapplication',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        "ombott",
        "click",
        "gunicorn",
        "gevent",
        "threadsafevariable",
        "pydal",
        "pyjwt",
        "yatl",
        "tornado",
        "requests",
        "watchgod",
        "renoir",
    ],
    python_requires='>=3.7',
    python_modules = ['websaw']
)
