try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='PyNWN',
    version='0.1dev',
    packages = ['pynwn',
                'pynwn.nwn',
                'pynwn.file',
                'pynwn.util',],
    license='GPL v2 and 2-Clause BSD License',
    install_requires=[
        'prettytable',
    ],
    zip_safe=False
)
