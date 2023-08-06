from setuptools import setup, find_packages

setup(
    name='dangqu-sdk',
    version='0.2',
    description='dangqu sdk',
    author='ZhaoHui',
    author_email='myemail@example.com',
    packages=find_packages(exclude=('venv',), include=('__init__.py', 'client.py',)),
    install_requires=[
        'requests',
        'oauthlib',
        'requests-oauthlib',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
