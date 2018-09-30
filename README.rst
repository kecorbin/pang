====================================
Playbook for Ansible + NSO Generator
====================================


.. image:: https://img.shields.io/pypi/v/pang.svg
        :target: https://pypi.python.org/pypi/pang

.. image:: https://img.shields.io/travis/kecorbin/pang.svg
        :target: https://travis-ci.org/kecorbin/pang

.. image:: https://readthedocs.org/projects/pang/badge/?version=latest
        :target: https://pang.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




A simple utility which will create Ansible playbooks for existing networks using NSO


* Free software: MIT license
* Documentation: https://pang.readthedocs.io.


Installation
-------------------

To install pang from source run the following commands::

  git clone https://github.com/kecorbin/pang
  cd pang
  python setup.py install

Usage
--------

Running::

  Usage: pang [OPTIONS]

    PANG - Playbook for Ansible + NSO Generator

  Options:
    --nso <host_or_ip>     FQDN/IP of NSO Server (default: localhost)
    --username <username>  NSO Username (default: admin)
    --password <password>  NSO Password (default: admin)
    --help                 Show this message and exit.


Sample Output::

  Generating Ansible Playbook...
  Syncing Configuration from Devices
  Generating host_vars for core1
  Generating host_vars for core2
  Generating host_vars for dist1
  Generating host_vars for dist2


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
