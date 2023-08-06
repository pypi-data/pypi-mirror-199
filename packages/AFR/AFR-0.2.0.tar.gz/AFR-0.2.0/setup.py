from setuptools import setup

with open('AFR manual.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='AFR',
    version='0.2.0',
    description='Statistical toolkit aimed to help statisticians, data analysts, data scientists, bankers and other professionals to analyze financial data',
    author='Timur Abilkassymov, Alua Makhmetova',
    author_email='alua.makhmetova@gmail.com',
    url='https://github.com/AFRKZ/AFR',
    license="3-clause BSD",
    packages=['AFR'],
    package_dir={'': '.'},
    install_requires=[
        'setuptools', 'pandas', 'sklearn',
        'scikit-learn', 'numpy', 'statsmodels', 'matplotlib',
        'matplotlib', 'mlxtend'
    ],
    package_data={'AFR': ['load/macroKZ.csv', 'load/finratKZ.csv']},
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown',
    options={
        'bdist_wheel': {
            'universal': True,
        }
    }
)
