##
# contains the Tile Class for every tile on the board
# tile.py
# 

class Tile():
	def __init__(self, tile_type):
		'''Takes one variable called tile_type 
		this can be either "Switch" or "Block"'''

		tile_type = tile_type.title()
		if tile_type == 'Switch':
			self.off = True
			self.on = False
			self.switch = True
			self.block = False
		elif tile_type == 'Block':
			self.block = True
			self.switch = False
		else:
			raise 'Tile type not Valid'

	def change_type(self):
		if self.switch:
			self.switch = False
			self.block = True
		else:
			self.block = False
			self.switch = True
			self.on = False
			self.off = True

	def is_open(self):
		''' Returns if the player can move to this position'''
		return self.switch

	def touched(self):
		''' Turns the switch on '''
		if self.off:
			self.on = True
			self.off = False

	def is_on(self):
		return self.on

	def is_off(self):
		return self.off

	def is_block(self):
		return self.block

	def is_switch(self):
		return self.switch

