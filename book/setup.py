from setuptools import find_packages, setup

setup(
    name='TurboGears2Docs',
    version='2.1.4',
    author='TurboGears Community',
    url='http://www.turbogears.org/',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'sphinx>=1.0.7',
        'pyvcs',
        'dulwich',
    ],
    dependency_links=[
        "http://www.turbogears.org/2.1/downloads/current/"
        ]
)
