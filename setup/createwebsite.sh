#!/bin/bash
#
# shell script to init site - run as root
#

# enshure server environment

sudo apt install libapache2-mod-wsgi-py3

sudo ln -s /var/www/compute/apache/danbots-compute.conf /etc/apache2/sites-available/danbots-compute.conf
sudo a2ensite danbots-compute.conf

#sudo mkdir /var/log/apache2/
sudo mkdir /var/www/compute/data /var/www/compute/site

sudo chown www-data /var/www/compute/data
sudo chgrp -R www-data /var/www/compute
