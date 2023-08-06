from setuptools import setup

setup(
    name='abdlmutii',
    version='0.1.0',
    description='A mini-portfolio for me via ✨ terminal ✨.',
    py_modules=['abdlmutii'],
    install_requires=[
        'argparse',
        'textwrap',
        'webbrowser',
        'termcolor',
        'pyfiglet',
        'gradient',
        'prompt_toolkit',
    ],
    entry_points={
        'console_scripts': [
            'abdlmutii=abdlmutii:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
