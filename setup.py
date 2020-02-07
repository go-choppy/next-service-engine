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
        'plotly>=3.6.1',
        'bokeh>=1.0.4',
        'Jinja2>=2.10',
        'Markdown>=3.0.1',
        'pyparsing>=2.3.1',
        'requests>=2.21.0',
        'multiqc>=1.7',
        'sqlalchemy>=1.2.18',
        'psutil>=5.5.1'
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
