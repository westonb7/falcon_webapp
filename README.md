## falcon_webapp
## This repository is for testing out the Falcon framework to test a simple web app.

## This was built and tested on Mac OS X version 10.9.5.
## As a result, running this app on newer versions of OS X or on different 
##  operating systems may not work properly

## This readme will document how I built the app, as well as how to install 
##  and run on another computer. Again, this has only been tested on OS X 10.9.5, 
##  and running on other platforms will require a different setup process.

## Anything on a line without "#" at the start indicates a command that can be run
##  on the command line with bash.

## Initial setup:
## Install Homebrew using this command in the terminal:
##  (taken from Homebrew's webpage) (https://brew.sh)

/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

## Verify installation was successful:

brew doctor

## If there were issues with Homebrew's installation, this command should show the warnings.
## Set usr/local/bin to occur before usr/bin

echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bash_profile

## Install python3 with Homebrew

brew install python3

## Create a directory, and set up falcon
## At this point I mostly followed the tutorial on 
##  https://falcon.readthedocs.io/en/stable/user/tutorial.html
##  to set up the app, and for setting up virtualenv for testing.

# cd path/to/dir/

mkdir myFalconApp
cd myFalconApp
pip3 install falcon
mkdir myFalconApp
touch myFalconApp/__init__.py
touch myFalconApp/app.py
touch myFalconApp/weights.py
pip3 install ipython 

## From here I followed the Falcon tutorial to write up the code found 
##  in myFalconApp/app.py and in myFalconApp/weights.py, and deviated
##  from the tutorial to have the app perform the functions I wanted.
##  Note that weights.py is where most of the relevant code is.

## For testing the app, I used virtualenv (suggested by Falcon's tutorial page)

## Install virtualenv if it isn't installed already
## Install gunicorn, and HTTPie

pip3 install virtualenv
pip3 install gunicorn
pip3 install httpie

## With virtualenv and gunicorn, we can set up a testing environment
##  to make sure the app is working.

# (in a new terminal)
virtualenv .venv
source .venv/bin/activate
gunicorn --reload myFalconApp.app

## This will run a local version of the app that can be used for testing purposes.
## It would probably be best to write unit tests to make sure the app works as 
##  intended, but for the purposes of a small app like this, this should work fine.
## To test the app, commands similar to the ones below can be run on the 
##  command line:

http --json POST localhost:8000/weights test:='{"reputer":"name", "reputee":"foo", "repute":{"rid":"xyz12345", "feature":"Clarity", "value":"5"}}'

http GET localhost:8000/weights?name=foo

## Where "foo" (reputee) can be replaced by the reputee name of choice, 
##  "xyz12345" (rid) can be replaced by rid of choice, "Clarity" (feature) 
##  can be either "Clarity" or "Reach", and "5" (value) can be replaced 
##  by value of choice (which should only be between 0-10)
