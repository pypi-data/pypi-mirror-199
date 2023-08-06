from setuptools import setup 
from setuptools import find_namespace_packages

setup(
    
    name = "hmxlabs.sysinfo",
    version = "1.0.6",
    py_modules= ['hmxlabs.sysinfo.sysinfo'],
    packages = find_namespace_packages('src')
)