from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

    with open('changelog.md') as history_file:
        HISTORY = history_file.read()

setup_args = dict(
    name='PythonCoordinates',
    version='0.5.3a0',
    packages=['PythonCoordinates', 'PythonCoordinates/conversions', 'PythonCoordinates/coordinates',
              'PythonCoordinates/linear_algebra', 'PythonCoordinates/measurables'],
    url='https://gitlab.com/frankmobley/physical_quantities_coordinates',
    license='',
    author='Dr. Frank Mobley',
    author_email='frank.mobley.1@afrl.af.mil',
    description='A collection of classes for representing the physical '
                'measurable quantities and the methods to '
                'locate them',
    package_dir={'': 'src'},
    long_description=README+'\n\n' + HISTORY,
    long_description_content_type="text/markdown"
)

install_requires = [
    'numpy',
    'scipy',
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
