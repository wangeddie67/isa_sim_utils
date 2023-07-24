# Welcome to Utilization for ISA Simulator

This project aims to provide useful codes to build up an ISA simulator as quickly as possible. This
project can be used to simulate the behavior of ISA in both execution-driven simulators and
interactive execution simulators.

## Installation

The whole project is developed based on Python3. The required environment can be easily set up.

The project repository is stored at https://github.com/wangeddie67/isa_sim_utils. Fellow commands 
clone the project to local.

```bash
# git clone repository
git clone git@github.com:wangeddie67/isa_sim_utils.git
```

## Import

## Submodules

This project contains several submodules:

- Data type:
  - Data type with limited bit width for computer ISA.
- Register file:
  - The data structure of registers for specified ISA.
  - Imaging interface of register files.
- Memory imaging:
  - The data structure of memory.
  - Imaging interface of memory imaging.

## Generate Documents

The document for this project is generated by Sphinx. The environment of Sphinx can be set up by 
following commands:

``` bash
cd /root/to/isa_sim_utils/docs

# Install Sphinx
sudo apt-get install python3-sphinx

# Install plugin for Sphinx
sudo pip3 install sphinxext sphinx-autopackagesummary sphinx-mdinclude sphinx_rtd_theme

# Install Markdown parser
sudo pip3 install myst-parser
```

The document can be generated through Makefile.

```bash
make doc
```

The generated documents are located in `docs/build`. The index page of generated documents is 
`docs/build/index.html`.

## TO DO

The project is under development. the following features will come soon:

* Test of data type.
* Dump interface for Register file.
* Memory file.
