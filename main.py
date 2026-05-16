import os
import math
import PIL
from PIL import Image
from PIL import ImageEnhance

import discord
from discord.ext import commands
from discord import app_commands

client = commands.Bot(command_prefix="//", intents = discord.Intents.all())

client.remove_command("help")


blocks = []


def staticReader ():
  blockDirs = os.listdir ('static_values/Properties')

  for i in range (len (blockDirs)):
    f = open ('static_values/Properties/' + blockDirs[i])
    
    blocks.append ([[], [], [], [], [], [], []])
    blocks[i][0] = int (f.readline().rstrip('\n'))
    blocks[i][1] = int (f.readline().rstrip('\n'))
    blocks[i][2] = int (f.readline().rstrip('\n'))
    blocks[i][3] = f.readline().rstrip('\n')
    blocks[i][4] = f.readline().rstrip('\n')
    blocks[i][5] = blockDirs[i]
    blocks[i][6] = 0
    # the last one is block distances

  print ('  --== Block library has been loaded! ==--')



# wszystko co się dzieje na starcie
@client.event
async def on_ready():
    print(
        "\n  --== Bot jest uruchomiony! zamknięcie tego okna zakończy pracę bota ://. Nie rób tego (chyba że kończysz robotę) ==--")
    print('  --== Add bot to server with link: ' + discord.utils.oauth_url(1071785578552643614) + " ==--  ")

    try:
        synced = await client.tree.sync()
        print ('  --== The bot commands are synced! ==--  ')
    except Exception as e:
        print (e)


    staticReader ()






@client.tree.command (name = 'color_mix', description = 'I give you the block pallete')
@app_commands.describe (blocks_amount = '1')
async def colormix(interaction: discord.Interaction, image: discord.Attachment, blocks_amount: str):
  await image.save ('temp.png')

  r = 0
  g = 0
  b = 0

  img = PIL.Image.open('temp.png')
  imgC = PIL.ImageEnhance.Color (img)
  img = imgC.enhance(1.75)
  pix = img.load()

  for y in range (img.height):
      for x in range (img.width):
          rgb = pix[x, y]

          r += rgb[0]
          g += rgb[1]
          b += rgb[2]


  r = int (r / (img.height * img.width))
  g = int (g / (img.height * img.width))
  b = int (b / (img.height * img.width))

  
  # --== porównywarka ==--
  for i in range (len (blocks)):
    rmean = (r + blocks[i][0]) / 2
    red = r - blocks[i][0]
    green = g - blocks[i][1]
    blue = b - blocks[i][2]
    blocks[i][6] = math.sqrt ((((512 + rmean) * red * red) / 256) + 4 * green * green + (((767 - rmean) * b * b) / 256))

  
  color = discord.Color.from_rgb(r, g, b)
  mixture = "Pełna mieszanka:  "

  
  embed = discord.Embed (title = "Oto lista najbliższych " + blocks_amount + " bloków:", color = color)
  embed.set_footer (text = "Stworzone przez: Budown1k, BTE Poland")

  tempBlocks = sorted (blocks, key = lambda block: block[6])
  
  for i in range (int (blocks_amount)):
    embed.add_field(name = tempBlocks[i][4], value="", inline=True)

    if tempBlocks[i][3] != '-1':
      mixture += tempBlocks[i][3] + ','
    else:
      mixture += tempBlocks[i][4] + ','

  mixture = mixture.rstrip (",")
  
  embed.add_field(name = mixture, value="", inline=False)



  # making the image for adding to the embed 
  images = []

  for i in range (int(blocks_amount)):
    tempImage = Image.open ("static_values/Blocks/" + tempBlocks[i][5][:len (tempBlocks[i][5]) - 4] + ".png")
    images.append (tempImage.resize((80,80)))

  totalWidth = int (blocks_amount) * 80
  height = 80

  new_image = Image.new ('RGB', (totalWidth, height)) 

  xOffset = 0
  for i in images:
    new_image.paste (i, (xOffset, 0))
    xOffset += 80

  new_image.save ('tempImage.png')


  
  file = discord.File("tempImage.png", filename="image.png")
  embed.set_image(url="attachment://image.png")
  
  
  
  await interaction.response.send_message(file = file, embed = embed)




  

# --== Wielki start bota ==--
TOKEN = "..."
client.run(TOKEN)