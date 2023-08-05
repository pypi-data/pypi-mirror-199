from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name='vpitools',
    version='1.0.1',
    
    description='VPI Tools',
    url='https://vpi.pvn.vn/',
    
    author='DnA Teams',
    author_email='dna.teams@vpi.pvn.vn',
    license='MIT',
    
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(), include_package_data=True,
    zip_safe=False,
    
    install_requires=['seaborn', 
                    'plotly', 
                    'altair', 
                    'numpy==1.21.6',
                    'matplotlib==3.4.3',
                    'pandas >=1.4.3',
                    'scikit-learn >=1.1.1',
                    'xgboost >= 1.5.1',
                    'lightgbm >= 3.3.2',
                    'matplotlib >= 3.4.3',
                    'shap >= 0.41.0',
                    'fasttreeshap >= 0.1.2',
                    'scipy >= 1.9.0',
                    'mlens >= 0.2.3',
                    'scikit-optimize',
                    'imblearn',
                    'optuna',
                    'catboost',
                    ]
)
