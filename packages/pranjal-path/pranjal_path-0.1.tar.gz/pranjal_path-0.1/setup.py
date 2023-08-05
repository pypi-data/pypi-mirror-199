from setuptools import setup
import sys

setup_args=dict(
    name="pranjal_path",
    packages=['pranjal_path'],
    version='0.1',
    description="",
    long_description="",
    author="pranjal",
    author_email="pranjalt7869@gmail.com", 
)

def main():
    setup(**setup_args)

if __name__ == '__main__':
    main()