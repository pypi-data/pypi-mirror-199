from setuptools import setup, find_packages

setup(
    name='crypto-sqlite-browser',
    version='1.0.1',
    author='Crypt00o',
    author_email='0xCrypt00o@protonmail.com',
    description='A tool for encrypting and decrypting SQLite databases and browsing it securely',
    packages=find_packages(),
    install_requires=[
        'pycryptodome',
        'litecli'
    ],
    entry_points={
        'console_scripts': [
            'crypto-sqlite-browser=crypto_sqlite_browser.main:main'
        ]
    }
)
