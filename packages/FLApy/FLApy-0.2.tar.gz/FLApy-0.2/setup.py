from setuptools import setup, find_packages


with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='FLApy',
    version='0.02',
    description='Forest Light availability heterogeneity Analysis in Python',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    author='Bin Wang',
    author_email='wb931022@hotmail.com',
    url='https://github.com/niB-gnaW/FLApy',
    packages=find_packages(),
    py_modules=['FLApy.__init__', 'FLApy.DataManagement', 'FLApy.LAcalculator', 'FLApy.LAHanalysis', 'FLApy.Visualization'],
    classifiers=['Programming Language :: Python :: 3.7', 'License :: OSI Approved :: MIT License', 'Operating System :: OS Independent',],
    python_requires='>=3.7',
    install_requires=['numpy', 'scipy', 'matplotlib', 'open3d', 'pyvista', 'pygeos', 'laspy', 'pandas', 'tqdm', 'p_tqdm', 'miniball'],)

