from setuptools import setup, find_packages

setup(
    name='abdlmutii',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'click',
        'pyfiglet'
    ],
    entry_points={
        'console_scripts': [
            'abdlmutii = abdlmutii:abdlmutii'
        ]
    },
    author='Abdlmu\'tii',
    author_email='abdlmutii@outlook.com',
    description='A mini-portfolio for me via ✨ terminal ✨.',
    url='https://github.com/abdlmutii',
    python_requires='>=3.6',
)
