Auto Generate Metasploit Resouce Script
=======================================

This Program run an exploit with automate search for open port using
only excellent rank in Metasploit Module. Generate shell / bash scripts
to use in security automate test

Getting Started
---------------

Prerequisites
~~~~~~~~~~~~~

::

   - Python >= 3.10
   - python3-nmap
   - pymetasploit3
   - pyfiglet

Installing
~~~~~~~~~~

::

   pip install augrs 

MSFRPC Installing
^^^^^^^^^^^^^^^^^

This project use MSFRPC API and msfconsole you must install and start
RPC server before running the program In case of you don’t have MSFRPC
or msfconsole instance We provide the docker image that contain both you
may follow the step below 1. Install docker desktop `Get
Docker <https://docs.docker.com/get-docker/>`__ 2. Pull docker image for
running MSFRPC and msfconsole ~~~ docker pull
wisarud2k/ubuntu-metasploit ~~~ 3. Start docker image and mapping port
using port 55553 and 443 ~~~ docker run -it -p 55553:55553 -p 443:443
–name={your own container name} wisarud2k/ubuntu-metasploit:latest ~~~
4. Run program with MSFRPC password “test” ~~~ python3 autogen.py ~~~
After first docker run you can start your own docker container with ~~~
docker start -i {your own container name} ~~~ ## Usage

Run exploit in program:
~~~~~~~~~~~~~~~~~~~~~~~

1. Use Nmap module
2. Go to Exploit module
3. Use Search for exploit
4. Run all exploit and wait for report
5. The report will create in exploit_report folder

create shell or bash script for running exploit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Use Nmap module
2. Go to Exploit module
3. Use Generate resource script
4. select the environment to create script (linux or window)
5. name the script and enter
6. The script will create in rc folder

Options manage
~~~~~~~~~~~~~~

1. Use Options module
2. select options that want to edit
3. edit you options

License
-------

This project is licensed under the MIT License - see the LICENSE.md file
for details.
