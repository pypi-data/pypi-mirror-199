from setuptools import setup
from setuptools import find_namespace_packages,find_packages

readme = open("./README.md", "r")


setup(
    # Define the library name, this is what is used along with `pip install`.
    name='logyca',

    # here are the packages I want "build."
    # packages=find_namespace_packages(
    #     where=['data', 'data.*']
    # ),
    packages = find_packages(),

    # I also have some package data, like photos and JSON files, so
    # I want to include those as well.
    include_package_data=True,

    # Define the version of this library.
    # Read this as
    #   - MAJOR VERSION 0
    #   - MINOR VERSION 1
    #   - MAINTENANCE VERSION 0
    version='0.0.1a7',
    
     # Here is a small description of the library. This appears
    # when someone searches for the library on https://pypi.org/search.
    description='Logyca libraries, apiresult, health check dto',

    # I have a long description but that will just be my README
    # file, note the variable up above where I read the file.
    long_description=readme.read(),
    
    # This will specify that the long description is MARKDOWN.
    long_description_content_type='text/markdown',

     # Define the author of the repository.
    author='Logyca',

    # Define the Author's email, so people know who to reach out to.
    author_email='',

    # These are the dependencies the library needs in order to run.
    # install_requires=[
    #         "matplotlib >= 2.0.0",
    #         "numpy >= 1.11.3",
    #         "openpyxl >= 2.4.1",
    #         "openturns >= 1.9",
    #         "pandas >= 0.19.2",
    #         "pip >= 9.0.1",
    #         "pyodbc >= 4.0.17",
    #         "pyqt >= 5.6.0",
    #         "pywin32 >= 220.0.0",
    #         "pywinauto >= 0.6.3",
    #         "qt >= 5.6.2",
    #         "scipy >= 0.18.1",
    #         "statistics >= 1.0.3.5",
    #         "tqdm >= 4.15.0",
    #         "xlwings >= 0.10.2",
    #     ],  

    # use the URL to the github repo
    url='https://github.com/xxx/xxx',    
    download_url='https://github.com/xxx/xxx/tarball/0.1',
    
    # Here are the keywords of my library.
    keywords=['logyca','apiresult'],

    # Additional classifiers that give some characteristics about the package.
    # For a complete list go to https://pypi.org/classifiers/.
    classifiers=[

        # I can say what phase of development my library is in.
        'Development Status :: 3 - Alpha',

        # Here I'll add the audience this library is intended for.
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Financial and Insurance Industry',

        # Here I'll define the license that guides my library.
        'License :: OSI Approved :: MIT License',

        # Here I'll note that package was written in English.
        'Natural Language :: English',

        # Here I'll note that any operating system can use it.
        'Operating System :: OS Independent',

        # Here I'll specify the version of Python it uses.
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.11',

        # Here are the topics that my library covers.
        'Topic :: Database',
        'Topic :: Education',
        'Topic :: Office/Business'

    ],
    
    # Here I'll define the license that guides my library.
    license='MIT',

    # Here I can specify the python version necessary to run this library.
    python_requires='>=3.11'
)