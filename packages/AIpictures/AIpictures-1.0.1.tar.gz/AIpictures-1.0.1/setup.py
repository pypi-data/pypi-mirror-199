from setuptools import setup, find_packages

setup(
    name='AIpictures',
    version='1.0.1',
    description='My awesome package',
    author='Justin Alter',
    author_email='jane@example.com',
    install_requires=[
        'openai',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'AIpictures=pictures:get_response',
        ],
    },
)