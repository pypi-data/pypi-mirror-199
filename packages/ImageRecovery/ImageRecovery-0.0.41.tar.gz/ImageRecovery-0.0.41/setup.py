from setuptools import setup, find_packages

VERSION = '0.0.41'
DESCRIPTION = 'Recover images from proximity information.'
LONG_DESCRIPTION = 'Staged Image Recovery uses a combination of structural embedding and manifold learning to ' \
                   'recover images from proximity information. Such information is encoded in a graph, '\
                   'where edges denote proximity. Although the problem ' \
                   'to be solved is quite general, it has special relevance' \
                   'in the context of DNA sequencing-based microscopy.' \
                   'For more information, please read our paper:' \
                   'https://www.biorxiv.org/content/10.1101/2022.09.29.510142v1'


# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="ImageRecovery",
    version=VERSION,
    author="David Fernandez Bonet",
    author_email="<dfb@kth.se>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['setuptools~=60.2.0', 'pandas~=1.4.3','matplotlib~=3.5.3','pycpd~=2.0.0','scikit-learn~=1.1.2','scipy~=1.9.0','numpy~=1.22.4','csrgraph~=0.1.28','nodevectors~=0.1.23','networkx~=2.8.6','seaborn~=0.11.2','umap-learn~=0.5.3','gensim==3.7.1'],  # add any additional packages that
    # needs to be installed along with your package. 

    keywords=['python', 'node embedding', 'structural embedding', 'graph representation learning',
              'manifold learning', 'DNA sequencing-based microscopy', 'image reconstruction', 'image recovery'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux"
    ]
)
