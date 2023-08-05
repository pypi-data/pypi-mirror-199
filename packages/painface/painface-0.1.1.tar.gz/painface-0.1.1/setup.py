import setuptools

with open("README.md", 'r') as f:
    long_description = f.read()

setuptools.setup(name='painface',
                 version='0.1.1',
                 author='Rohan Ray, Rahul Patel',
                 author_email='painfaceanalysis@gmail.com',
                 description='CSV parsing and analysis for PainFace generated CSVs',
                 long_description=long_description,
                 long_description_content_type='text/markdown',
                 include_package_data=True,
                 packages=setuptools.find_packages(),
                 classifiers=['Programming Language :: Python :: 3', 'Operating System :: OS Independent'],
                 python_requires='>=3.6',
                 license="MIT",
                 install_requires=[
                     'numpy', 'pandas', 'scipy', 'matplotlib'
                 ])