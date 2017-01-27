# Tournament-Results

**Tournament-Results** is a program to maintain tournament pairings and results using postgresql

Submitted by: **Peter Le**

## Functionality

The following **required** functionality is complete:
* [x] Uses Postgresql
* [x] Can clear tables
* [x] Register players
* [x] See players' standings
* [x] Report result of matches
* [x] Create match pairings using Swiss pairing style

## Pictures of Application

<img src='http://i.imgur.com/kbQcvOI.png' title='Logout' width='' alt='Logout' />

## How to run (On Local):
1. Make sure Python is downloaded. If not downloaded, go to https://www.python.org/downloads/ to download
2. Install Vagrant (http://vagrantup.com/) and VirtualBox ()
3. Download tournament repository to computer 
4. Using terminal/powershell navigate to the vagrant folder in FSND-Virtual-MAchine
5. Launch the Vagrant VM using command ("vagarant up")
6. Login to the Vagrant VM using ("vagrant ssh")
7. Change into the shared folder by using ("cd /vagrant")
8. Then navigate to the tournament folder using ("cd /tournament")
9. Run the test file using the command ("python tournament_test.py")

## Notes

This project uses postregsql, vagrant, and virtualbox. More documentation is online
