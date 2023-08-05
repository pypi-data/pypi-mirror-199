from setuptools import setup, find_packages

setup(
    name='streamlit_tile_grid',
    version='0.3.7',
    author='Ramee Abdallah',
    author_email='ramee.abdallah@hotmail.com',
    description='A custom Streamlit component for rendering tiles',
    packages=find_packages(),
    install_requires=[
        'streamlit>=0.86.0',
        'pandas>=1.3.0',
        'numpy>=1.21.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
