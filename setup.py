from setuptools import setup


setup(
    name='hmbtg-utils',
    version='0.1.6',
    description='A collection of tools and reoccuring functions.',
    url='https://gitlab.sarchiv-0007.vcac/InforegGroup/hmbtg_utils',
    author='Melvyn Linke',
    author_email='linke@hitec-hamburg.de',
    license='BSD 3-clause',
    packages=[
        'hmbtg_utils',
        'hmbtg_utils.net',
        'hmbtg_utils.daos',
        'hmbtg_utils.logging',
        'hmbtg_utils.testing',
        'hmbtg_utils.templates'],
    install_requires=[],
    classifier=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
    ],
)
