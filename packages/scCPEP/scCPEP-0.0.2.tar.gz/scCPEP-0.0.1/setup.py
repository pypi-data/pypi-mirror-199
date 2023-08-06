import setuptools

with open("README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'scCPEP',
    version = '0.0.1',
    description = 'scCPEP_pkg',
    author = 'Qi Qi',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    author_email = 'qiqi20@mails.jlu.edu.cn',
    packages = setuptools.find_packages(),
    url = 'https://github.com/IrisQi7/scCPEP',
    license = 'MIT',
    classifiers = ['Operating System :: OS Independent',
                   'Topic :: Scientific/Engineering :: Artificial Intelligence',
                   "Programming Language :: Python :: 3.7",]
)

 