#!/usr/bin/env python

import os
import re
from subprocess import call
import urllib2

from mozdownload import DirectScraper

JENKINS_VERSION = '1.509.4'
JENKINS_URL = 'http://mirrors.jenkins-ci.org/war-stable/%s/jenkins.war' % JENKINS_VERSION
JENKINS_ROOT = os.path.dirname(JENKINS_URL)
JENKINS_WAR = 'jenkins-%s.war' % JENKINS_VERSION
JENKINS_ENV = 'jenkins-env/bin/activate_this.py'


def jenkins_is_up_to_date():
    """Checks if Jenkins was updated"""
    req = urllib2.urlopen(JENKINS_ROOT)
    page = req.read()

    months_regex = '(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
    regex = r'\d\d-%(MONTH)s-\d\d\d\d \d\d:\d\d' % {'MONTH': months_regex}

    pattern = re.compile(regex)
    match = re.search(pattern, page).group()

    if os.path.isfile('last_update.txt'):
        with open('last_update.txt', 'r') as txt:
            check = txt.read()
            if match == check:
                return True

    with open('last_update.txt', 'w') as txt:
        txt.write(match)
    return False


def download_jenkins():
    """Downloads Jenkins.war file"""

    if jenkins_is_up_to_date():
        pass
    else:
        print "Downloading Jenkins %s from %s" % (JENKINS_VERSION, JENKINS_URL)
        if os.path.isfile('jenkins.war'):
            os.remove('jenkins.war')
        scraper = DirectScraper(url=JENKINS_URL,
                                directory=os.getcwd(),
                                version=None)
        scraper.download()

if __name__ == "__main__":
    download_jenkins()

    try:
        # for more info see:
        # http://www.virtualenv.org/en/latest/#using-virtualenv-without-bin-python
        activate_this_file = 'jenkins-env/bin/activate_this.py'
        execfile(JENKINS_ENV, dict(__file__=JENKINS_ENV))
        print "Virtual environment activated successfully."

        # TODO: Start Jenkins as daemon
        print "Starting Jenkins"
        args = ['java', '-jar', '-Xms2g', '-Xmx2g', '-XX:MaxPermSize=512M',
                '-Xincgc', JENKINS_WAR]
        p = call(args)
    except IOError:
        print "Could not activate virtual environment."
        print "Exiting."
