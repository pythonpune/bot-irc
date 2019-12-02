import socket
from time import sleep


irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect_to(server,port):
    irc.connect((server, port))
    print(f"Connected to server {server}")

def join_channel(channel, bot_nick):
    irc.send(bytes('USER ' + bot_nick + " " + bot_nick + " " + bot_nick + " " + bot_nick + ' \n', 'utf-8'))
    irc.send(bytes('NICK ' + bot_nick + ' \n', 'utf-8'))
    irc.send(bytes('JOIN ' + channel + ' \n', 'utf-8'))
    print(f"Joined channel {channel}")

def karmas(name, point):
    if name not in karma.keys():
        karma[name] = 1
    elif point == "+":
        karma[name] += 1
    elif point == "-":
        karma[name] -= 1
    irc.send(bytes("PRIVMSG " + channel + " :" + name + " Has " + str(karma[name]) + " Points. \n", 'utf-8'))
    
server = 'chat.freenode.net'
port = 6667
channel = '#pythonpune'
bot_nick = 'gitircbot_test'

connect_to(server, port)
join_channel(channel, bot_nick)
karma = {}

while True:
    sleep(3)
    complete_str = irc.recv(2024).decode('utf-8')
    msg = complete_str.split(channel)[-1][2:-2]
    sender = complete_str.split('!')[0][1:]

    if f"{bot_nick} @ {channel}" in complete_str:
        karma = { y : 0 for x,y in enumerate(complete_str.split(':')[-3].split())}

    if 'ping' in complete_str.lower() and 'freenode.net' in complete_str.lower():
        irc.send(bytes("PONG \r\n", 'utf-8'))

    if 'ping' in msg and bot_nick in msg:
        irc.send(bytes("PRIVMSG " + channel + " :" + sender + ", pong \n", 'utf-8'))

    if msg.startswith(':info'):
        if msg.split()[-1] in karma.keys():
            irc.send(bytes("PRIVMSG " + channel + " :" + msg.split()[-1] + ", has " + str(karma[msg.split()[-1]]) + " points. \n", 'utf-8'))
        else:
            irc.send(bytes("PRIVMSG " + channel + " :No such nick \n", 'utf-8'))

    if msg.endswith('++') and msg.startswith(':'):
        karmas(msg[1:-2], '+')
    
    if msg.endswith('--') and msg.startswith(':'):
        karmas(msg[1:-2], '-')