from setuptools import setup, find_packages


setup(
    name="mangust228",
    version="0.3",
    description="My custom library",
    author="mangust228",
    author_email="bacek.mangust@gmail.com",
    packages=find_packages(),
    install_requires=[
        'requests',
        'pandas',
        'pydantic',
        'loguru'
    ],
    classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
    ],
    python_requires = '>=3.8'
)