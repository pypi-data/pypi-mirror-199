from setuptools import setup
# read the contents of your README file

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(name='turbie_bruno',
version='1.0',
description='necessary functions to run the DTU turbie model', 
long_description = long_description,
long_description_content_type='text/markdown',
author='bruno',
packages=['turbie_bruno'],
packages_data={'turbie_bruno':['Data_model/*.txt', 'Data_TI_0.1/wind_4_ms_TI_0.1.txt']}
)