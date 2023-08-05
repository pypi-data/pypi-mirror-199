from setuptools import setup, find_packages

VERSION = '0.0.1'

setup(
    name="mkdocs-dsfr",
    version=VERSION,
    url='https://www.systeme-de-design.gouv.fr',
    license='MIT',
    description='DSFR theme for Mkdocs',
    author='Ministère Transition Écologique - DNUM',
    author_email='numerique-ecologie@developpement-durable.gouv.fr',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['mkdocs>=1.4'],
    python_requires='>=3.7',
    entry_points={
        'mkdocs.themes': [
            'themename = mkdocs_dsfr',
        ]
    },
    zip_safe=False
)