#!/usr/bin/env python

from distutils.core import setup

setup(name='dataeng',
      version='1.1',
      description='Python code for the Data Engineering Course Example',
      author='Dr Owain Kenway',
      author_email='o.kenway@ucl.ac.uk',
      url='TBC',
      packages=['dataeng'],
      install_requires=['bs4','requests', 'mr4mp', 'lxml'],
      entry_points={'console_scripts': ['build-index = dataeng.gather:parse_index_entry',
                                        'analyse = dataeng.analysis:analysis_entry',
                                        'combine = dataeng.combine:combine_entry'
                                        ]}
     )
