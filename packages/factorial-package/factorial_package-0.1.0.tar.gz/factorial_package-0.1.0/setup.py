from setuptools import setup, find_packages

setup(
    name='factorial_package',
    version='0.1.0',
    author='Mihir Vora',
    author_email='er.voramihir@gmail.com',
    description='A package to calculate the factorial of a number',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mihir-vora/factorial_package',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
