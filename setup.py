import setuptools

requirements = [
    'certifi==2020.6.20'
    'chardet==3.0.4'
    'database-sanitizer==1.1.0'
    'django==2.2.15'
    'django-cors-headers==3.5.0'
    'django-environ==0.4.5'
    'django-filter==2.3.0'
    'django-sanitized-dump==1.2.1'
    'djangorestframework==3.11.1'
    'djangorestframework-gis==0.15'
    'djangorestframework-jwt==1.11.0'
    'drf-jwt-2fa==0.3.0'
    'idna==2.10'
    'lxml==4.5.2'
    'owslib==0.19.1'
    'psycopg2==2.8.4'
    'pyjwt==1.7.1'
    'pyproj==2.6.0'
    'python-dateutil==2.8.1'
    'python-memcached==1.59'
    'pytz==2020.1'
    'pyyaml==5.3.1'
    'raven==6.10.0'
    'requests==2.24.0'
    'six==1.15.0'
    'sqlparse==0.3.1'
    'urllib3==1.25.10'
]

setuptools.setup(
    name="parkkihubi",
    version="0.0.1",
    author="dac",
    packages=setuptools.find_packages(exclude=['tests']),
    test_suite="tests",
    tests_require=[],
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.7.6',
)
