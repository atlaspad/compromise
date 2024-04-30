# $figlet compromise
Setup:
generate ABIs by any means (solc, remix, etc...)
put ABIs of pool manager and the pool contract to their respective files. The ones I provided are old (probably)
Create a python venv `pip venv venv`
Activate python venv `source venv/bin/activate`
Install requirements `pip install -r requirements.txt`
Run the project `python compromise.py`

Usage:
Set up the network you want to interact with contracts
Set up the private account key (Make sure you don't have anything suspicious on your computer. Your private key will be stored unencrypted)
Set up the contract addresses and update the ABIs of contracts if you see fit
Enter the functions you want to interact with
Interact with the contracts. You'll need to enter each argument by hand in an unintuitive way.
(Hint: You can set up the project to interact with local network if you choose "Custom" entry)