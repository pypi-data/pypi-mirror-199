import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='PyAlchemista',
    version='0.0.6',
    author='Siddhu Pendyala',
    author_email='elcientifico.pendyala@gmail.com',
    description='A Python library that deals with different fields of science.',
    long_description = long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/PyndyalaCoder/PyAlchemista',
    project_urls = {
        "Bug Tracker": "https://github.com/PyndyalaCoder/PyAlchemista/issues"
    },
    license='MIT',
    packages=['PyAlchemista', 'Tempore', 'Lunastra', 'Disciplina', 'Acoustica'],
    install_requires=['requests', 'matplotlib', 'numpy', 'scipy'],
)
