import setuptools

import jtr


with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
    name='jtr',
    version=jtr.__version__,
    description=jtr.__doc__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    keywords='jinja render cli',
    url=jtr.__website__,
    author='Michael Samoglyadov',
    author_email='mixas.sr@gmail.com',
    license=jtr.__license__,
    packages=['jtr'],
    entry_points={
        'console_scripts': [
            'jtr=jtr:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
