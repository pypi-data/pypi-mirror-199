<p align="center">
   <a href="https://github.com/RiZoeLX">
      <img src="RiZoeLX/data/RiZoeLX.png" alt="RiZoeLX" width="300" aligne='centre'>
   </a>
</p>
<h1 align="center">
   <b> pyRiZoeLX </b> <br>  

</h1>

 * [![PyPI - Version](https://img.shields.io/pypi/v/pyRiZoeLX?style=round)](https://pypi.org/project/pyRiZoeLX) 
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pyRiZoeLX?label=DOWNLOADS&style=round)](https://pypi.org/project/pyRiZoeLX) 

----

<b>About:</b> pyRiZoeLX have many useful functions, that you can use in your repos/repostory. It'll make you code/bot smooth and fast!

<h4> Installation </h4>

```python 
pip3 install pyRiZoeLX
```

<h4> Import functions </h4>

``` python
from RiZoeLX.functions import <functions name>
```

<h4> Functions available: </h4>

 > [Click Here](https://github.com/RiZoeLX/pyRiZoeLX/tree/main/RiZoeLX/functions#-functions-available-) </b> 

<h3> Example. </h3>

``` python
from RiZoeLX.functions import ban_user
from pyrogram import Client, filters 
from pyrogram.types import Message


@Client.on_message(filters.command("ban"))
async def ban_(client, message):
   await ban_user(client, message)
```
