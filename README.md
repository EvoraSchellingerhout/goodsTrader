# goodsTrader
Idle Programming game based around transport logistics built on a REST API

# What is this?
This is an open source REST API built around python and flask with the intent 
of allowing anyone to run their own instance of the API for personal 
programming practice or to host a server to use with friends.

# Why was this project started?
This project was originally started as a way to get back into programming and 
provide a new openSource game to the public. We were inspired by other 
programming games such as screeps and spaceTraderAPI. However, none of these 
projects were open source, and we believed that focusing more on the logistics 
chain rather than control of territory or vertical integration would provide 
a more interesting user experience.

# So What is currently working?
Currently, you can create accounts, purchase transports, move them around, 
buy and sell generic goods, and fully automate this process using your own 
programming skills!

# What is planned for the future?
Currently, we plan on implementing a travel time for transports, dynamic 
pricing for goods based on the inventory available (goods sell for less when 
inventories are more full, and goods sell for more when inventories are low), 
and refining goods to sell at a higher value.

The eventual plan is to create a true "living economy", possibly even having 
nodes grow and shrink when better supported by the logistics set up by players.

# Alright, I'm sold. How do I make my own server?
You can check out our wiki page here on github to learn about getting started 
with setting up your own server.

# Alright, my friend set up a server and sent me here. What should I do?
This is a REST API that runs off http requests to the server where a JSON 
output is returned. Make or use a program that can send http requests 
(ex. httpie) to send the server http requests at certain URLs. You can see 
the full functionality in the wiki.

# Happy Trading!
