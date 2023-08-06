import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

REQUIREMENTS = [
]

setuptools.setup(
    name='gica',
    version='0.0.0',
    description='Your project description here',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='USERNAME',
    license='MIT',
    packages=setuptools.find_packages(),
    python_requires='>=3.7, <4',
)
