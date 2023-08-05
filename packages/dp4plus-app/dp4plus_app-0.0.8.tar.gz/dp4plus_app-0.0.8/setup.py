# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 13:34:57 2023

@author: Franco, Bruno Agustín 


AGREGAR DOCUMENTACION
AGREGAR DOCUMENTACION
AGREGAR DOCUMENTACION
"""

from setuptools import setup, find_packages
  
with open('README.md') as file:         #sirve para incluir el REEDME
    long_description = file.read()

short_description = 'A tool to simplify your DP4+ calculations'
requirements = ['numpy', 
                'openpyxl', 
                'pandas',
                'pathlib', 
                'scikit-learn', 
                'scipy', 
                'tk']  #etc...

setup(  name ='dp4plus_app',
        version ='0.0.8',
        author='Bruno A. Franco',
        author_email='bruno.agustin.franco@gmail.com',
        url='https://github.com/RosarioCCLab/DP4plus-App',
        description =short_description	,
        long_description = long_description,
        long_description_content_type ="text/markdown",
        license ='MIT',
        
        packages=find_packages(where="dp4plus_app"),
        package_dir={"": "dp4plus_app"},
        include_package_data=True,
        
        
        entry_points = {'gui_scripts': ['dp4plus = dp4plus_app.main_dp4:main'],
                        'console_scripts':['dp4plus-exe = dp4plus_app.main_dp4:create_exe'],
                        },
        
        classifiers = [
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent"],
        keywords = 'NMR structural elucidation', 
        install_requires = requirements
        )  