# GoldStar


# API DOCS
Link to api docs: [API DOCS](https://docs.goldstar.cf)

## Installation
```
pip install goldstar
```
## example 
Server Count Post :
```python
from goldstar import goldstar
from discord.ext import commands

client = commands.Bot(command_prefix="!") 
dbl = goldstar(client,"token of goldstar")

@client.event
async def on_ready():
  x = await dbl.serverCountPost()
  print(x)

client.run("token")
```

Search bot: 
```python
from goldstar import goldstar

client = commands.Bot(command_prefix="!") 
dbl = goldstar(client,"token of goldstar")
id=botid

a = dbl.search(id)
print(a)

```
All functions in api:
```angular2html
1: serverCountPost()
2: search()
3: hasVoted()
```




