import os
from setuptools import setup
from next_service_engine.version import get_version


def get_packages(package):
    """Return root package and all sub-packages."""
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


setup(
    name='next-service-engine',
    version=get_version(),
    description='Next Service Engine for Interactive Plot, Web Component, Microservice etc.',
    long_description=open('README.md').read(),
    author='Jingcheng Yang',
    author_email='yjcyxky@163.com',
    url='http://choppy.3steps.cn/go-choppy/next-service-engine',
    zip_safe=False,
    platforms='any',
    include_package_data=True,
    packages=get_packages("next_service_engine"),
    keywords='Service Engine, Interactive Plot, Multimedia, Web Component',
    install_requires=[
        'Alembic==0.8.10',
        'apispec>=0.20.0,<0.39',
        'bokeh>=1.0.4',
        'flask-caching>=1.7.1',
        'flask-cors==3.0.8',
        'flask-marshmallow==0.7.0',
        'flask-migrate==2.5.2',
        'flask-restplus>=0.13.0',
        'flask-script>=2.0.6',
        'Flask-SQLAlchemy>=2.4.0',
        'flask>=1.0.2',
        'gevent>=1.4.0',
        'Jinja2>=2.10',
        'Markdown>=3.0.1',
        'marshmallow-sqlalchemy==0.12.0',
        'marshmallow==2.20.5',
        'multiqc>=1.7',
        'plotly>=3.6.1',
        'psutil>=5.5.1',
        'pyparsing>=2.3.1',
        'requests>=2.21.0',
        'sqlalchemy-utils==0.36.1',
        'SQLAlchemy>=1.3.1',
        'verboselogs>=1.7',
        'webargs==5.5.0',
        'Werkzeug==0.16.1'
    ],
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: AGPL 3.0 License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        "console_scripts": [
            "next-service-engine = api_server.server:run_server"
        ],
    }
)
