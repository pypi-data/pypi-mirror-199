from setuptools import setup, find_packages

setup(
    name='patatas',
    version='0.1.1',
    description='A powerful package for K-NN regression, data preprocessing, and analysis for Data Science',
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author='Patata Team',
    author_email='demstalfer@gmail.com',
    url='https://github.com/PatataTeam/patata-poderosa',
    packages=find_packages(),
    install_requires=[
        'scikit-learn',
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='data preprocessing knn regression analysis data science scikit-learn pandas',
)