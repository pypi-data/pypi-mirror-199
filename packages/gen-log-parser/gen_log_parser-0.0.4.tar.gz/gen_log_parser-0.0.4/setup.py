from setuptools import setup, find_packages
# import versioneer

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='gen_log_parser',
    version='0.0.2',
    description="A package to parse log files,",
    # long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',  
    author='Sanil Tison',
    author_email='saniltison@gmail.com',
    license='MIT', 
    classifiers=classifiers,
    keywords='log parser', 
    packages=find_packages(),
    install_requires=[''] 
)

# config = {
#     'name': 'ms-mint',
#     'version': versioneer.get_version(),
#     'cmdclass': versioneer.get_cmdclass(),
#     'description': 'Metabolomics Integrator (Mint)',
#     'long_description': setup[4],
#     'long_description_content_type': 'text/markdown',
# #    ...
# }