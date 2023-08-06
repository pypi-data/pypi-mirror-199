from setuptools import setup, find_packages

setup(
    name='dangqu_sdk',
    version='0.4',
    description='dangqu sdk',
    author='ZhaoHui',
    author_email='myemail@example.com',
    packages=find_packages(exclude=('venv',)),
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
