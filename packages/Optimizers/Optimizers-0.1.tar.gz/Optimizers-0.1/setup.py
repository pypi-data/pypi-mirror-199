from distutils.core import setup
setup(
    name='Optimizers',
    packages=['Optimizers'],
    version='v0.1',
    license='GNU General Public License v3.0',
    description='A collection of examples for learning mathematical modelling',
    author='David S.W. Lai',
    author_email='david.lai@soton.ac.uk',
    url='https://github.com/davidswlai/',
    download_url='https://github.com/davidswlai/Optimizers/releases/latest',
    keywords=['Optimizers', 'Mathematical Optimization', 'Operations Research', 'Logistics', 'Routing', 'Scheduling'],
    install_requires=[
        'requests>=2.24.0'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
)
