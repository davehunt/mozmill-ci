#!/usr/bin/env python

import os
from subprocess import call
import urllib2

JENKINS_VERSION = '1.509.4'
JENKINS_URL = 'http://mirrors.jenkins-ci.org/war-stable/%s/jenkins.war' % JENKINS_VERSION
JENKINS_WAR = 'jenkins-%s.war' % JENKINS_VERSION

def download_jenkins(url, war_file):
    """Downloads Jenkins.war file"""

    tmp_file = JENKINS_WAR + ".part"
    
    while True:
        try:
            r = urllib2.urlopen(url)
            CHUNK = 16 * 1024
            with open(tmp_file, 'wb') as f:
                for chunk in iter(lambda: r.read(CHUNK), ''):
                    f.write(chunk)
            break
        except (urllib2.HTTPError, urllib2.URLError):
            print "Download failed."
    os.rename(tmp_file, JENKINS_WAR)

if __name__ == "__main__":
    print "Downloading Jenkins %s from %s" % (JENKINS_VERSION, JENKINS_URL)
    download_jenkins(JENKINS_URL, JENKINS_VERSION)
    
    # for more info see:
    # http://stackoverflow.com/questions/6943208/activate-a-virtualenv-with-a-python-script/14792407#14792407
    try:    
        activate_this_file = 'jenkins-env/bin/activate_this.py'
        execfile(activate_this_file, dict(__file__=activate_this_file))
        print "Virtual environment activated successfully."
        
        # TODO: Start Jenkins as daemon
        print "Starting Jenkins"
        args = ['java', '-jar', '-Xms2g', '-Xmx2g', '-XX:MaxPermSize=512M',
                '-Xincgc', JENKINS_WAR]
        p = call(args)
    except IOError:
        print "Could not activate virtual environment."
        print "Exiting."
