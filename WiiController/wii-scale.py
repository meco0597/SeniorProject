#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Author: Andreas Älveborn
# URL: https://github.com/aelveborn/Wii-Scale
# 
# This file is part of Wii-Scale
# Copyright (C) 2015 Andreas Älveborn
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import wiiboard
import time
import sys
import getopt

from bluetooth import *


# Global

sleep = True

# Accepts True or False as argument
def receive_connect(self):
	global sleep
	sleep = False

def receive_disconnect(self):
	global sleep
	sleep = True

class WiiController(object):

	def __init__(self):
		self.board1_addr = None
		self.board2_addr = None
		self.board3_addr = None
		self.board4_addr = None

		self.board1 = None
		self.board2 = None
		self.board3 = None
		self.board4 = None


	def start(self, address):
		print "Wii-Controller started"

		global sleep

		board = None

		ready = False
		sleep = True
		connected = False
		
		if self.board1_addr is None:
			self.board1_addr = address
		elif self.board2_addr is None:
			self.board2_addr = address
		elif self.board3_addr is None:
			self.board3_addr = address
		elif self.board4_addr is None:
			self.board4_addr = None
		else:
			print "Serious Error"

		board = wiiboard.Wiiboard()


		while True:
			if connected is not board.isConnected():
				connected = board.isConnected()
				
			if not connected:
					#Turn off lights
				time.sleep(0.1) # This is needed for wiiboard.py
				board.setLight(False)

			if not board.isConnected():
				# Re initialize each run due to bug in wiiboard
				# Note: Seems to be working though :/
				board = wiiboard.Wiiboard()
				
				board.connect(address)
				print "Connecting to ", address
			if board.isConnected():
				connected = True

				if self.board4_addr is not None:
					self.board4 = board
				elif self.board3_addr is not None:
					self.board3 = board
				elif self.board2_addr is not None:
					self.board2 = board
				elif self.board1_addr is not None:
					self.board1 = board
				else:
					print "Error all boards connected"
				break

	def get_data(self, address):
		if address is self.board1_addr:
			if self.board1.isConnected():
				a = [self.board1.mass.topLeft, self.board1.mass.topRight, self.board1.mass.bottomLeft, self.board1.mass.bottomRight]
				return a 
		elif address is self.board2_addr:
			if self.board2.isConnected():
				a = [self.board2.mass.topLeft, self.board2.mass.topRight, self.board2.mass.bottomLeft, self.board2.mass.bottomRight]
				return a
		elif address is board3_addr:
			if self.board3.isConnected():
				a =  [self.board3.mass.topLeft, self.board3.mass.topRight, self.board3.mass.bottomLeft, self.board3.mass.bottomRight]
				return a
		elif address is self.board4_addr:
			if self.board4.isConnected():
				a = [self.board4.mass.topLeft, self.board4.mass.topRight, self.board4.mass.bottomLeft, self.board4.mass.bottomRight]
				return a
		else:
			print "Something messed up, no address exists"
			print address
			return 0
