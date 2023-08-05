from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

reqs = [
    'textx',    
    'numpyro',
    'funsor',
]

long_description = "BayesLDM: A Domain-specific Modeling Language for Probabilistic Modeling of Longitudinal Data"

if __name__ == '__main__':
    setup(
        name="BayesLDM",

        version='1.0.9',

        package_data={'': ['default.yml']},

        description="BayesLDM",
        long_description_content_type='text/markdown',
        long_description=long_description,

        author='BayesLDM developer',
        author_email='bayesldm@gmail.com',

        license='MIT',
        url = 'https://github.com/reml-lab/BayesLDM/',

        classifiers=[

            'Development Status :: 5 - Production/Stable',

            'Intended Audience :: Healthcare Industry',
            'Intended Audience :: Science/Research',

            'License :: OSI Approved :: MIT License',

            'Natural Language :: English',

            'Programming Language :: Python :: 3',

            'Topic :: Scientific/Engineering :: Information Analysis',
            'Topic :: System :: Distributed Computing'
        ],

        keywords='mHealth machine-learning data-analysis',

        # You can just specify the packages manually here if your project is simple.
        # Or you can use find_packages().
        packages=find_packages(exclude=['Examples']),

        # List run-time dependencies here.  These will be installed by pip when
        # your project is installed. For an analysis of "install_requires" vs pip's
        # requirements files see:
        # https://packaging.python.org/en/latest/requirements.html
        install_requires=reqs,


        entry_points={
            'console_scripts': [
                'main=main:main'
            ]
        },

    )
