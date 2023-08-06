#!/usr/env python
from setuptools import find_packages, setup

version = "0.1.3"

requirements = [
    'appdirs',
    ]

with open('README.md', encoding='utf-8') as readme_file:
    readme = readme_file.read()


setup(
    name="pycronscript",
    version=version,
    author="José Antonio Díaz Miralles",
    author_email='joseantoniodiazmiralles@gmail.com',
    url='https://github.com/tiyujopite/pycronscript',
    description='Schedule your Python scripts',
    long_description=readme,
    long_description_content_type='text/markdown',
    download_url='https://github.com/tiyujopite/pycronscript',
    keywords=[
        "schedule",
        "cron",
        "python",
        "scripts",
        "tasks",
        ],
    packages=find_packages(where='src'),
    package_dir={
        '': 'src/',
        'pycronscript': 'src/pycronscript'
        },
    entry_points={
        'console_scripts': ['pycronscript=pycronscript.main:run']
        },
    python_requires='>=3.7',
    install_requires=requirements,
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        "Topic :: Software Development",
        ],
    )
