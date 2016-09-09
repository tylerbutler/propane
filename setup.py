# coding=utf-8
from __future__ import absolute_import, print_function

from setuptools import Command, find_packages, setup


# noinspection PyShadowingBuiltins
def get_install_requirements(requirements_file='requirements.txt'):
    requirements = []
    with open(requirements_file) as file:
        temp = file.readlines()
        temp = [i[:-1] for i in temp]

        for line in temp:
            if line is None or line == '' or line.startswith(('#', '-e', '-r')):
                continue
            else:
                requirements.append(line)
        return requirements


# noinspection PyShadowingBuiltins
def get_readme():
    with open('README.md') as file:
        return file.read()


# noinspection PyMethodMayBeStatic
class Version(Command):
    description = 'Outputs the current version of the package'
    user_options = []
    boolean_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from setuptools_scm import get_version

        print('Current version is: ' + get_version(root='.', relative_to=__file__))


setup(
    name='propane',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    author='Tyler Butler',
    author_email='tyler@tylerbutler.com',
    platforms='any',
    packages=find_packages(),
    url='http://github.com/tylerbutler/propane',
    license='MIT',
    description='A collection of somewhat random, helpful utility functions, data structures, '
                'Django fields, and other miscellany.',
    long_description=get_readme(),
    install_requires=get_install_requirements(),
    tests_require=(['nose']),
    cmdclass={
        'version': Version
    },
    include_package_data=True,
    # package_data=find_package_data(PROJECT,
    #                                package=PROJECT,
    #                                only_in_packages=False),
    zip_safe=True,  # Setting to False doesn't create an egg - easier to debug and hack on
)
