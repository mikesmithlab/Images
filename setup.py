import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='py-images',
    version='1.0.0',
    description='Package for openCV image analysis',
    package_dir={'': 'images'},
    packages=setuptools.find_packages(where='images'),
    python_requires='>3.5',
    install_requires=[
        'opencv-python',
        'numpy',
        'scipy',
        'pillow',
        'matplotlib'
    ],
)
