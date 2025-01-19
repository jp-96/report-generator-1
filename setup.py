from setuptools import setup, find_packages

setup(
    name='rptgen1',     # The name of your package
    version='0.1.0',    # The initial release version
    author='jp-96',     # Your name or organization
    author_email='jp-96@example.com',  # Your email
    description='report generator 1',  # A short description
    long_description=open('README.md').read(),          # Long description read from README.md
    long_description_content_type='text/markdown',      # Description content type (e.g., text/markdown)
    url='https://github.com/jp-96/report-generator-1',  # URL to your package repository
    package_dir={'': 'src'},                # Specify the source directory
    packages=find_packages(where='src'),    # Automatically find packages under 'src'
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Python version requirement
    install_requires=[        # External packages as dependencies
        'unoserver',
        'jinja2',
        'markdown2',
        'python_odt_template',
    ],
)
