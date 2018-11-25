# PUBG: Did everyone suck, or was it just me?

**Author**: [Adrienne Karnoski](https://github.com/adriennekarnoski)

**Version**: 1.0.0

## Overview

Using the PUBG [API](https://documentation.playbattlegrounds.com/en/introduction.html), 
the program takes a user's XBOX gamertag and returns a (roughly estimated, purely for entertainment)
answer to the question I often ask myself after a round of PUBG:

*Did everyone suck, or was it just me?*

###### Included in the response 

The program also returns data on the player's personal stats, averages of all players,
and averages of the top ten players in the match. Stats include:

**Kills:** Enemy players killed

**Headshot Kills:** Enemy players killed with headshots

**Assists:** Enemy players the user damaged that were killed by teammates

**DBNOs:** Enemy players knocked

**Longest Kill:** Distance of longest kill (meters)

**Kill Points:** Points based on number of kills

**Damage Dealt:** Total damage dealt

**Walk Distance:** Distance traveled on foot (meters)

**Ride Distance:** Distance traveled in vehicles (meters)

**Swim Distance:** Distance traveled while swimming (meters)

**Time Survived:** Amount of time survived (min:sec)

**Win Points:** Points based on user's placement in the match

**Boosts:** Boost items used

**Heals:** Healing items used

**Revives:** Times this player revived teammates

**Weapons Acquired:** Weapons picked up


## Getting Started

Clone down the repository to your local machine:
```
$ git clone https://github.com/adriennekarnoski/PUBG
```
Once your download is complete, cd into the ```PUBG``` repository:
```
$ cd PUBG
```
Create a new virtual environment with Python 3 and activate it:
```
PUBG $ python3 -m venv ENV
PUBG $ . ENV/bin/activate
```
Install the program along with it's requirements, via pip:
```
(ENV) PUBG $ pip install .
```
### Configuration
The program requires a development API key, which you can get [here](https://developer.pubg.com/?locale=en#).

After receiving your API key, save it as an environmental variable:
```
export API_KEY='<your-api-key>'
``` 

**The program can run using mock data without the need for an API key by entering 'example' when prompted for gamertag**

