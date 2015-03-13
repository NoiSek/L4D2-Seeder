#! /usr/bin/env python3
from valve.source import a2s as volvo
import subprocess
import random
import time
import os

def get_servers():
  """ Grabs a list of servers from servers.lst to query, does not update in realtime. """
  servers = []

  with open('servers.lst') as servers_list:
    for server in servers_list:
      
      # Was a port specified?
      if ":" in server:
        address, port = server.split(":")

        # Is it a port range?
        if "-" in server:
          start, end = port.split("-")

          for sub_port in range(int(start), int(end) + 1):
            server_info = (address, sub_port)
            servers.append(server_info)

          continue

        # If not, grab whatever port it has specified.
        else:
          server_info = (address, int(port))

      # Default to 27015
      else:
        server_info = (address, 27015)

      servers.append(server_info)

  return servers

def launch_game(server, path_to_steam):
  """ Launches L4D2 in textmode, and returns the process """
  launch_options = "-applaunch 550 -silent -textmode -nosound -noipx -novid -nopreload -nojoy -sw -noshader -nosound -low -replay_enable 0 -nohltv -width 640 -height 480 +connect %s:%d" % server
  args = [path_to_steam]

  args.extend(launch_options.split(" "))
  return subprocess.Popen(args, shell=False)

def destroy_instances():
  """ Destroys all running instances of L4D2 very roughly, only works on Windows. """
  devnull = open(os.devnull, 'w')
  subprocess.call("TASKKILL /F /IM left4dead2.exe", stdout=devnull, stderr=subprocess.STDOUT)

def loop(servers, path_to_steam):
  """ Runs through the server list, seeds servers as necessary. """
  current_server = servers[0]
  current_thread = None

  while True:
    try:
      # Grab the server object from Valve's master query server, or timeout
      server = volvo.ServerQuerier(current_server, timeout=5.0)
      player_count = server.get_info()["player_count"]
      
      # Do we need to seed this server?
      if player_count < 2:
        print("Joining %s:%d" % current_server)
        current_thread = launch_game(current_server, path_to_steam)
        
        # Start a timer
        timer_start = time.clock()

        # Check every 30 seconds to see if at least one human has joined
        while player_count < 2:
          try:
            server = volvo.ServerQuerier(current_server, timeout=5.0)
            new_player_count = server.get_info()["player_count"]
            
            # Check if the new_player_count is actually a number due to Volvo shenanigans.
            if isinstance(new_player_count, int):
              player_count = new_player_count

            # After 5 minutes, just disconnect and move on to prevent the server becoming 'stale'
            if time.clock() - timer_start > 300:
              print("5 minutes elapsed, cycling to next server.")
              break

          except volvo.NoResponseError:
            print("Master server request timed out! Volvo pls.")

          time.sleep(30)

        print("Server seeded: %s:%d (%d players)" % (current_server[0], current_server[1], player_count))
        destroy_instances()

      # This server is already seeded.
      else:
        print("Server %s:%d was already seeded. (%d players)" % (current_server[0], current_server[1], player_count))

      # Cycle to the next server in the list
      servers.append(servers.pop(0))
      current_server = servers[0]

    except volvo.NoResponseError:
      print("Master server request timed out! Volvo pls.")

    # Make sure that when the script is canceled it closes running instances of L4D2
    except (KeyboardInterrupt, SystemExit):
      print("Exit: Closing all instances of L4D2.")
      destroy_instances()
      
      raise

    time.sleep(5)

# Change this only if the path to your Steam executable is different.
path_to_steam = "C:\Program Files (x86)\Steam\Steam.exe"

# Parse servers.lst and shuffle it in order to facilitate multiple running instances of the seeder.
servers = get_servers()
random.shuffle(servers)

# Start cycling through the list.
loop(servers, path_to_steam)
