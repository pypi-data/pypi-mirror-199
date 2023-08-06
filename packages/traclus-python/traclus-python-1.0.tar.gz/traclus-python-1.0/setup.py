from setuptools import setup, find_packages


setup(
    name='traclus-python',
    version='1.0',
    license='apache-2.0',
    author="Adriel Isaiah Amoguis",
    author_email='adriel.isaiah.amoguis@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/AdrielAmoguis/TRACLUS',
    keywords='Trajectory Clustering',
    install_requires=[
          'scikit-learn',
          'numpy',
      ],

)