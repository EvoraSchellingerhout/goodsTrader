# goodsTrader
Idle Programming game based around transport logistics built on a REST API

#What is this?
This is an open source REST API built around python and flask with the intent to allow anyone to run their own instance of the API for personal programming practice or to host a server for them and their friends to compete on

#Why was this project started?
This project was originally started as a way to get back into programming and provide a new openSource game to the public. I was inspired by other programming games such as screeps and spaceTraderAPI. However, none of these projects where open source and I belived that focusing more on the logistics chain rather than control of territory or vertical integration.

#So What is currently working?
Currently you can create accounts, purchase transports, move them around, buy and sell generic goods, and fully automate this process using your own programming skills!

#What is planned for the future?
Currently we plan on implementing a travel time for transports, dynamic pricing for goods based on the inventory avalible (goods sell for less when inventories are fuller, and goods buy for more when inventories are low), and refining goods to sell for more.

The eventual plan is to create a true "living economy" possibly even having nodes grow and shrink when better supported by the logistics setup by players.

#Alright I'm sold how do I make my own server?
You can check out our wiki page here on github to learn about getting started setting up your own server

#Alright my friend setup a server and sent me here, what should I do
This is a REST API that runs off http requests to the server where a JSON output is returned, make or use a program that can send http requests (ex. httpie) to send the server http requests at certain urls. You can see the full functionality in the wiki.

#Happy Trading!
