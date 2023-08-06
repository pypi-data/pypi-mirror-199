from setuptools import setup, find_packages

def read_requirements():
   with open('requirements.txt', 'r') as req:
       requirements = req.readlines()
       requirements = [x.strip() for x in requirements]
   return requirements

setup(
   name="codetalk",
   version="0.1.7",
   package_dir={'': 'src'},
   packages=find_packages(where='src'),
   package_data={'codetalk': ['assets/*']},
   install_requires=read_requirements(),
   entry_points={
      'console_scripts': [
         'codetalk=codetalk.main:converse'
      ]
   }
)
