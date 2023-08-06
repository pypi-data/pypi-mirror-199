from setuptools import setup, find_packages

setup(
    name = "shutil_extra",
    version = "0.0.6",
    keywords = ("pip", "shutil extra", "dir tree"),
    description = "A successful sign for python setup",
    long_description_content_type = 'text/markdown',
    long_description = open('README.md', encoding='UTF8').read(),
    license = "MIT Licence",
    url = "https://github.com/novawei/shutil_extra",
    author = "novawei",
    author_email = "913252732@qq.com",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = [],
)