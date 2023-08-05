from setuptools import setup, find_packages

setup(
    name='patatas',
    version='0.1.0',
    description='A package for K-NN regression and data preprocessing',
    author='Patata Team',
    author_email='demstalfer@gmail.com',
    packages=find_packages(),
    install_requires=[
        'scikit-learn',
        'pandas',
        'numpy',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)