from setuptools import setup

setup(
    name = "SQL-Jobs-Util",
    version = "0.0.1",
    author = "Andrey Khobnya",
    author_email = "andrey@khobnya.me",
    description = "Simple tool to execute SQL jobs for data migration and/or data transfer between multiple database servers",
    license = "MIT",
    keywords = "data, database, jobs, data migration, data transformation",
    install_requires=[
        'validictory',
        'simplejson',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities']
)
