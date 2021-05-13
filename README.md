MIT License

Copyright (c) 2021 Cade Tipton, Gatlin Cruz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
# MiniGNC:  
**G**raphical **N**etwork **C**ustomizer for Visualizing and Storing Mininet Networks  
Made by Gatlin Cruz and Cade Tipton  

---

**Ways to Install This Project:**
**[Latest Release](https://github.com/GatlinCruz/Capstone/releases "MiniGNC Releases")**
- Click the Latest Release link above and follow the instructions there **(preferred)**.  
  If that does not work for you for whatever reason, the options below are available.  
  
- Manually install the dependencies by entering the commands in `install/install_reqs.txt`
- Install with Bash script (Should work on at least Ubuntu 18.04 & Ubuntu 20.04)
  1. Clone the github repository with `git clone https://github.com/GatlinCruz/Capstone.git`
  2. Navigate to the root of the Capstone directory
  3. Run the bash script to install dependencies `sudo install/install.sh`  
  **Note:** sudo is used to execute Mininet commands. Unless your password is 'Mininet'
  you must change `mysite/gui/templates/gui/buttons.py line 231` to your sudo password.  
  Yes, this is insecure for native installs and should be handled differently in the future.

**To Run The Project:**
From the root of the Capstone directory...  
1. Enter `python3 mysite/manage.py runserver`
2. Click on "http://127.0.0.1:8000/" or navigate there from your preferred browser.  
**Note:** Saving networks to the database requires starting Neo4j with `sudo neo4j start`  
(Make sure to wait a couple seconds for the database to start)
