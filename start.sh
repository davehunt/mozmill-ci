#!/usr/bin/env bash

JENKINS_VERSION=1.509.4
JENKINS_URL="http://mirrors.jenkins-ci.org/war-stable/$JENKINS_VERSION/jenkins.war"
JENKINS_WAR=jenkins-$JENKINS_VERSION.war

export JENKINS_HOME=$(dirname $BASH_SOURCE)/jenkins-master


echo "Downloading Jenkins $JENKINS_VERSION from $JENKINS_URL"
curl --location $JENKINS_URL -z $JENKINS_WAR -o $JENKINS_WAR.part
if [ -f $JENKINS_WAR.part ]; then
  mv $JENKINS_WAR.part $JENKINS_WAR
fi

source jenkins-env/bin/activate
if [ $? -eq 0 ]; then
    echo "Virtual environment activated successfully."
    # TODO: Start Jenkins as daemon
    echo "Starting Jenkins"
    java -server -jar -Xms2g -Xmx2g -XX:MaxPermSize=512M -XX:+HeapDumpOnOutOfMemoryError -Xincgc $JENKINS_WAR
else
    echo "Could not activate virtual environment."
    echo "Exiting."
fi


