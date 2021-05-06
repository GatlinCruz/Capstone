## MiniGNC (Capstone)
# Visualizing and Storing Software Defined Networks
# Made by Gatlin Cruz and Cade Tipton

# Ways to Install This Project (Choose One)
- Download the virtual machine image [here](www.example.com "Need to find a suitable host...")
- Bash script installation (Should work on at least Ubuntu 18.04 & Ubuntu 20.04)
    1. Clone the github repository with `git clone https://github.com/GatlinCruz/Capstone.git`
    2. Navigate to the root of the Capstone directory
    3. Run the bash script to install dependencies `sudo install/install.sh`
    **Note:** sudo is used to execute Mininet commands. Unless your password is 'Mininet'  
    you must change `mysite/gui/templates/gui/buttons.py line 231` to your sudo password.
    Yes, this is insecure for native installs and should be handled differently in the future.
- Manually install the dependencies by entering the commands in `install/install_reqs.txt`

# To Run The Project
From the root of the Capstone directory...  
1. Enter `python3 mysite/manage.py runserver`
2. Click on the "http://127.0.0.1:8000/" or navigate there from your preferred browser.
3. Saving networks to the database requires starting Neo4j with `sudo neo4j start`  
    (Make sure to wait a couple seconds for the database to start)
