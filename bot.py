import discord
from discord.ext import commands
import logging
from pieces import getBoard, utils
from dotenv import load_dotenv
import os
import asyncio
import random

load_dotenv()
BOT_KEY = os.getenv("BOT_KEY")
logging.basicConfig()
logger = logging.getLogger('discord')
logger.setLevel(logging.WARNING)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
client = commands.Bot(command_prefix = '-')
players = []
match_id = 0

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await client.process_commands(message)

@client.command()
async def ping(ctx):
    print(discord.__version__)
    await ctx.channel.send('pong')

@client.command()
async def xadrez(ctx, member: discord.Member = None):
    await ctx.send(f'{member.mention} quer jogar xadrez? (sim/não)')
    def check(m):
        return ((m.content == 'sim') or (m.content == 'não')) and m.author == member
    msg = await client.wait_for('message', check = check)
    if msg.content == 'sim':
        await ctx.send('joga ai então')
    else:
        await ctx.send('vacilão')

@client.command()
async def now_playing(ctx):
    if players:
        resp = ''
        for player in players:
            resp += player.name + ' ' 
        resp += 'are playing right now'
    else:
        resp = 'No one is playing right now 😔'
    await ctx.send(resp)


@client.command()
async def chess(ctx, member: discord.Member = None):
    if member is None: #or member == ctx.author:
        await ctx.send('You need someone to play with')
    else:
        global players
        if member in players or ctx.author in players: # only one game at a time
            await ctx.send('Player already in game')
            return
        await ctx.send(f'{member.mention}, do you want to play Chess? (yes/no)')
        
        def check1(m):
            return ((m.content == 'yes') or (m.content == 'no')) and m.author == member
        
        try:
            msg = await client.wait_for('message', check=check1, timeout=60.0)
        except asyncio.TimeoutError:
            await ctx.message.add_reaction(client.get_emoji(814139927519559731)) # donowall
            await ctx.send(f'{member.mention} took too long to respond.')
            return

        if msg.content == 'yes': # match will start
            global match_id
            current_match_id = str(match_id)
            match_id += 1
            jogadores = [member, ctx.author]
            random.shuffle(jogadores)
            players.extend(jogadores)
            turn = jogadores[0]
            turn_white = True
            in_game = True
            red_square = False
            board = utils.initialize_board()
            def check2(m):
                return ((m.author.id == turn.id) and m.channel == ctx.channel and (utils.parseCommand(m.content) is not False))
            await ctx.send("""**How to play:**\n\n- Send a message here with the position of the piece you want to move and where you want it to move, for moving the pawn from d2 to d4 you type `d2d4`\n\n- For castling send either `0-0` or `0-0-0`, for castling short or long, respectively\n\n- For forfeiting send `-forfeit` and for proposing a draw `-draw`
            """)

            # game loop            
            while in_game:
                utils.getBoard(board, turn_white, current_match_id, red_square)
                #utils.print_board(board)
                if utils.check_stalemate(board, turn_white):
                    await ctx.send(f'**Stalemate!** Nobody wins 🤷‍♂️', file=discord.File(current_match_id + '.png'))
                    players.remove(jogadores[0])
                    players.remove(jogadores[1])
                    break
                #utils.print_board(board)
                turn_color = 'White' if turn_white else 'Black'
                await ctx.send(f"{turn.mention}'s turn - {turn_color} moves!", file=discord.File(current_match_id + '.png'))
                msg = await client.wait_for('message', check=check2)
                command = utils.parseCommand(msg.content)
                if command:
                    [x0, y0, x1, y1] = command
                    if [x0, y0, x1, y1] == [0, 0, 1, 1]: # propose draw
                        other_player = jogadores[0] if turn == jogadores[1] else jogadores[1]
                        await ctx.send(f'**{turn.name}** proposes a draw, {other_player.mention} do you accept? (yes/no)')
                        try:
                            msg2 = await client.wait_for('message', check=check1, timeout=60.0)
                        except asyncio.TimeoutError:
                            await msg.add_reaction(client.get_emoji(814139927519559731)) # donowall
                            continue
                        if msg2.content == 'yes':
                            await ctx.send('Match ends in a draw! 🙊')
                            players.remove(jogadores[0])
                            players.remove(jogadores[1])
                            break
                        elif msg2.content == 'no':
                            await ctx.send('The match will procede')
                    elif [x0, y0, x1, y1] == [1, 1, 0, 0]: # forfeit
                        winner = 'White' if turn_color == 'Black' else 'Black'
                        await ctx.send(f'{turn_color} forfeits, **{winner}** wins! 🎉')
                        players.remove(jogadores[0])
                        players.remove(jogadores[1])
                        break
                    
                    # actual movement
                    movimento = utils.movePiece(x0, y0, x1, y1, board, turn_white)
                    if movimento == 'moveu':
                        [position_white, position_black, check] = utils.check_check(board)
                        red_square = position_white if check == 'white_check' else position_black #paint the square red
                        if check == 'white_check' or check == 'black_check':  # if king is under attack
                            if utils.check_stalemate(board, not turn_white):
                                utils.getBoard(board, turn_white, current_match_id, red_square)
                                await ctx.send(f'Checkmate! {turn_color} wins! 🎉', file=discord.File(current_match_id + '.png'))
                                players.remove(jogadores[0])
                                players.remove(jogadores[1])
                                break
                            await ctx.send('**CHECK!**')
                        turn = jogadores[0] if turn == jogadores[1] else jogadores[1]
                        turn_white = False if turn_white else True
                    elif movimento == 'wrong color':
                        await ctx.send('this piece is not yours')
                    elif movimento == 'invalido':
                        await ctx.send('invalid move')
                    elif movimento == 'not found':
                        await ctx.send('piece not found')
        
        elif msg.content == 'no':
            await ctx.send('ok bro')

client.run(BOT_KEY)