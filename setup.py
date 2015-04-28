from setuptools import setup, find_packages

setup(
    name='atviriduomenys-lt',
    version='0.1',
    license='AGPLv3+',
    packages=find_packages(),
    install_requires=[
        'django',
        'django-nose',
        'django-compressor',
        'django-libsass',
        'django-crispy-forms',
        'django-floppyforms',
        'django-debug-toolbar',
        'django-extensions',
        'wtforms',
        'wtforms-django',
        'markdown',
        'xmltodict',
        'yattag',
        'psycopg2',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
    ]
)
