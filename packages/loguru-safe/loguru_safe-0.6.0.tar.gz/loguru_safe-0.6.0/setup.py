import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("loguru_safe/__init__.py", "r") as file:
    regex_version = r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]'
    version = re.search(regex_version, file.read(), re.MULTILINE).group(1)

with open("README.rst", "rb") as file:
    readme = file.read().decode("utf-8")

setup(
    name="loguru_safe",
    version=version,
    packages=["loguru_safe"],
    package_data={"loguru_safe": ["__init__.pyi", "py.typed"]},
    description="Python logging made (stupidly) simple",
    author="Delgan",
    author_email="delgan.py@gmail.com",
    url="https://github.com/Delgan/loguru_safe",
    download_url="https://github.com/Delgan/loguru_safe/archive/{}.tar.gz".format(version),
    project_urls={
        "Changelog": "https://github.com/Delgan/loguru_safe/blob/master/CHANGELOG.rst",
        "Documentation": "https://loguru_safe.readthedocs.io/en/stable/index.html",
    },
    keywords=["loguru_safe", "logging", "logger", "log"],
    license="MIT license",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: System :: Logging",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    install_requires=[
        "colorama>=0.3.4 ; sys_platform=='win32'",
        "aiocontextvars>=0.2.0 ; python_version<'3.7'",
        "win32-setctime>=1.0.0 ; sys_platform=='win32'",
    ],
    python_requires=">=3.5",
)
