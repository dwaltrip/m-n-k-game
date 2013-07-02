import pygame
Rect, Color = pygame.Rect, pygame.Color
import sys
import math

CIRCLE_CURSOR = (
		"                        ",
		"                        ",
		"         XXXXXX         ",
		"       XX......XX       ",
		"      X..........X      ",
		"     X....XXXX....X     ",
		"    X...XX    XX...X    ",
		"   X...X        X...X   ",
		"   X..X          X..X   ",
		"  X...X          X...X  ",
		"  X..X            X..X  ",
		"  X..X            X..X  ",
		"  X..X            X..X  ",
		"  X..X            X..X  ",
		"  X...X          X...X  ",
		"   X..X          X..X   ",
		"   X...X        X...X   ",
		"    X...XX    XX...X    ",
		"     X....XXXX....X     ",
		"      X..........X      ",
		"       XX......XX       ",
		"         XXXXXX         ",
		"                        ",
		"                        ")

X_CURSOR = (
		"                        ",
		"                        ",
		" XXX               XXX  ",
		" X..X             X..X  ",
		"  X..X           X..X   ",
		"   X..X         X..X    ",
		"    X..X       X..X     ",
		"     X..X     X..X      ",
		"      X..X   X..X       ",
		"       X..X X..X        ",
		"        X..X..X         ",
		"         X.,.X          ",
		"         X...X          ",
		"        X..X..X         ",
		"       X..X X..X        ",
		"      X..X   X..X       ",
		"     X..X     X..X      ",
		"    X..X       X..X     ",
		"   X..X         X..X    ",
		"  X..X           X..X   ",
		" X..X             X..X  ",
		" XXX               XXX  ",
		"                        ",
		"                        ")

def draw_text(screen, text, font_name, size, color, pos, centered=False):
	font = pygame.font.SysFont(font_name, size)
	textSurface = font.render(text, True, color)
	width, height = textSurface.get_size()
	topleft = left, top =  (pos[0] - width/2, pos[1] - height/2) if centered else pos
	screen.blit(textSurface, topleft)
	return Rect(left, top, width, height)

class Box(object):
	def __init__(self, surface, inner_rect, bg_color, thickness, border_color):
		self.surface = surface
		self.inner_rect = inner_rect
		self.border_thickness = thickness
		self.border_color = border_color
		self.bg_color = bg_color
		self.outer_rect = pygame.Rect(self.inner_rect.left - thickness, self.inner_rect.top - thickness,
			self.inner_rect.width + thickness*2, self.inner_rect.height + thickness*2)
		self.has_text = False
		self.textImg = None
		self.action = None

	def add_text(self, text, font_name, color):
		font_size = height = self.inner_rect.height
		width = self.inner_rect.width
		ds = int(font_size)/10
		font_size += ds
		while height > self.inner_rect.height*.7 or width > self.inner_rect.width*.7:
			font_size -= ds
			font = pygame.font.SysFont(font_name, font_size)
			self.text_img = font.render(text, True, color)
			width, height = self.text_img.get_size()
		self.text_pos = (self.inner_rect.left + (self.inner_rect.width - width)/2,
						self.inner_rect.top + (self.inner_rect.height - height)/2)
		self.has_text = True

	def contains(self, pos):
		return self.outer_rect.collidepoint(pos)

	def draw(self):
		self.surface.fill(self.border_color, self.outer_rect)
		self.surface.fill(self.bg_color, self.inner_rect)
		if self.has_text:
			self.surface.blit(self.text_img, self.text_pos)

class BasePlayer(object):
	# N = size of board, K = number in-a-row needed for victory
	def __init__(self, number, N, K, shape, color, cursor):
		self.number = number
		self.shape = shape
		self.color = color
		self.N, self.K = N, K
		self.squares = []
		self.opponent_squares = []
		self.cursor = cursor

	def add_square(self, coord, opponent_move=False):
		if not opponent_move:
			self.squares.append(coord)
		else:
			self.opponent_squares.append(coord)

	def victory_check(self):
		for j in xrange(1, self.N + 1):
			x_count = 0
			y_count = 0
			for i in xrange(1, self.N + 1):
				x_count += 1 if (i, j) in self.squares else -x_count
				y_count += 1 if (j, i) in self.squares else -y_count
				if x_count == self.K:
					return [(k, j) for k in xrange(i + 1 -self.K, i + 1)]
				elif y_count == self.K:
					return [(j, k) for k in xrange(i + 1 - self.K, i + 1)]
		for x in xrange(1, self.N + 1):
			for y in xrange(1, self.N + 1):
				dl_count = dr_count = 1
				if (x, y) in self.squares:
					for d in xrange(1, self.K):
						dr_count += 1 if (x + d, y + d) in self.squares else -dr_count
						dl_count += 1 if (x - d, y + d) in self.squares else -dl_count
						if dr_count == self.K:
							return [(x + k, y + k) for k in xrange(self.K)]
						if dl_count == self.K:
							return [(x - k, y + k) for k in xrange(self.K)]
		return []

	def move(self):
		pass

class HumanPlayer(BasePlayer):
	def __init__(self, number, N, K, shape, color, cursor):
		super(HumanPlayer, self).__init__(number, N, K, shape, color, cursor)

class ComputerPlayer(BasePlayer):
	def __init__(self, number, N, K, shape, color, cursor):
		super(ComputerPlayer, self).__init__(number, N, K, shape, color, cursor)

	def move(self):
		pass

class TicTacToe(object):
	# N = size of board, K = number in-a-row needed for victory
	def __init__(self):
		pygame.init()
		self.title = 'Tic-Tac-Toe'
		self.N_min, self.K_min = 3, 3
		self.N_max, self.K_max = 20, 10
		self.N, self.K = self.N_min, self.K_min
		self.text_font = "Times New Roman"

		vid_info = pygame.display.Info()
		self.size = self.width, self.height = vid_info.current_w, vid_info.current_h
		self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
		pygame.display.set_caption(self.title)
		self.tile_img = pygame.image.load("data/tile.png").convert_alpha()
		self.colors = {'grid_bg': Color(0,0,0), #Color(26,82,166),
					'grid_border': Color(139,69,19),
					'grid_line': Color(150,150,150),
					'options_bg_invalid': Color(65,65,65),
					'options_bg_unselected': Color(26,82,166),
					'options_bg_hover': Color(26,72,136),
					'options_bg_selected': Color(26,62,106),
					'options_border': Color(139,69,19),
					'options_text': Color(205,205,205),
					'victory_highlight': Color(255,255,0),
					'text': Color(255,255,255),
					'p1': Color(0,255,0),
					'p2': Color(0,0,255)
					}
		self.border_thickness = 3
		self.button_spacing = 20
		self.buttons = []

		self.clock = pygame.time.Clock()
		self.pregame_screen()

	def pregame_screen(self):
		self.game_started = False
		self.game_over = False

		rows = 2
		cols = (self.N_max + 1 - self.N_min)/rows
		size = int(self.width*.5)/cols
		outer_size = size + self.border_thickness*2
		w = cols*outer_size + (cols - 1)*self.button_spacing
		h = rows*outer_size + (rows - 1)*self.button_spacing
		top, left = int(self.height*.3), self.width/2 - w/2
		self.N_options = []
		for i in xrange(self.N_max + 1 - self.N_min):
			dx, dy = i%cols, i/cols
			rect = Rect(left + dx*(outer_size + self.button_spacing) + self.border_thickness,
						top + dy*(outer_size + self.button_spacing) + self.border_thickness,
						size, size)
			color = self.colors['options_bg_selected'] if self.N_min + i == self.N else self.colors['options_bg_unselected']
			box = Box(self.screen, rect, color, self.border_thickness, self.colors['options_border'])
			box.N = self.N_min + i
			#box.add_text(str(box.N)+'x'+str(box.N), self.text_font, self.colors['text'])
			box.add_text(str(box.N), self.text_font, self.colors['text'])
			self.N_options.append(box)

		cols = self.K_max + 1 - self.K_min
		w = cols*outer_size + (cols - 1)*self.button_spacing
		left = self.width/2 - w/2
		top = top + rows*outer_size + (rows - 1)*self.button_spacing + 6*self.button_spacing
		self.K_options = []
		for i in xrange(self.K_max + 1 - self.K_min):
			dx = i%cols
			rect = Rect(left + dx*(outer_size + self.button_spacing) + self.border_thickness,
						top + self.border_thickness, size, size)
			color = self.colors['options_bg_selected'] if self.K_min + i == self.K else self.colors['options_bg_unselected']
			box = Box(self.screen, rect, color, self.border_thickness, self.colors['options_border'])
			box.K, box.valid = self.K_min + i, True
			if box.K > self.N:
				box.bg_color = self.colors['options_bg_invalid']
				box.valid = False
			box.add_text(str(box.K), self.text_font, self.colors['text'])
			self.K_options.append(box)

		self.buttons = []
		buttons_mid = (self.K_options[0].outer_rect.bottom + self.height)/2
		w, h = self.width/7, (self.height - self.K_options[0].outer_rect.bottom)/4
		total_w = 2*w + self.button_spacing
		left = self.width/2 - total_w/2
		dx = w + self.button_spacing

		start_button = Box(self.screen, Rect(left, buttons_mid - h/2, w, h), self.colors['options_bg_unselected'],
								self.border_thickness, self.colors['options_border'])
		start_button.add_text('Start', self.text_font, self.colors['text'])
		start_button.action = self.new_game
		self.buttons.append(start_button)

		quit_button = Box(self.screen, Rect(left + dx, buttons_mid - h/2, w, h), self.colors['options_bg_unselected'],
								self.border_thickness, self.colors['options_border'])
		quit_button.add_text('Quit', self.text_font, self.colors['text'])
		quit_button.action = self.quit
		self.buttons.append(quit_button)

	def new_game(self):
		self.game_started = True
		self.game_over = False
		self.players = [HumanPlayer(1, self.N, self.K, "x", self.colors['p1'], X_CURSOR),
						HumanPlayer(2, self.N, self.K, "circle", self.colors['p2'], CIRCLE_CURSOR)]
		self.cp_index = 0
		self.player_cursor = self.players[self.cp_index].cursor
		self.filled_squares = set()
		self.game_info_msg = 'Player %d, it is your turn to move!' % (self.current_player().number)
		self.victory_path = []

		self.grid_size = int(math.ceil(self.height*.006))*100
		self.square_size = self.grid_size/self.N
		self.grid_size -= (self.grid_size % self.square_size)
		self.grid_rect = Rect((self.width - self.grid_size)/2, (self.height - self.grid_size)/2, self.grid_size, self.grid_size)
		self.grid_box = Box(self.screen, self.grid_rect, self.colors['grid_bg'], self.border_thickness, self.colors['grid_border'])

		self.buttons = []
		buttons_mid = (self.grid_rect.bottom + self.height)/2
		w, h = self.width/7, (self.height - self.grid_rect.bottom)/3
		total_w = 3*w + 2*self.button_spacing
		left = self.width/2 - total_w/2
		dx = w + self.button_spacing

		restart_button = Box(self.screen, Rect(left, buttons_mid - h/2, w, h), self.colors['options_bg_unselected'],
								self.border_thickness, self.colors['options_border'])
		restart_button.add_text('Restart', self.text_font, self.colors['text'])
		restart_button.action = self.new_game
		self.buttons.append(restart_button)
		new_game_button = Box(self.screen, Rect(left +
												dx, buttons_mid - h/2, w, h), self.colors['options_bg_unselected'],
								self.border_thickness, self.colors['options_border'])
		new_game_button.add_text('New Game', self.text_font, self.colors['text'])
		new_game_button.action = self.pregame_screen
		self.buttons.append(new_game_button)

		quit_button = Box(self.screen, Rect(left + 2*dx, buttons_mid - h/2, w, h), self.colors['options_bg_unselected'],
								self.border_thickness, self.colors['options_border'])
		quit_button.add_text('Quit', self.text_font, self.colors['text'])
		quit_button.action = self.quit
		self.buttons.append(quit_button)

	def current_player(self):
		return self.players[self.cp_index]

	def switch_players(self):
		self.cp_index = ~self.cp_index
		self.game_info_msg = 'Player %d, it is your turn to move!' % (self.current_player().number)
		self.player_cursor = self.current_player().cursor
		self.current_player().move()

	def update_cursor(self, pos):
		if self.grid_rect.collidepoint(pos):
			self.set_cursor(self.current_player().cursor)
		else:
			self.set_cursor()

	def set_cursor(self, cursor=None):
		if cursor:
			size = w,h = len(cursor[0]), len(cursor)
			curs, mask = pygame.cursors.compile(cursor, 'X', '.')
			pygame.mouse.set_cursor(size, (w/2,h/2), curs, mask)
		else:
			pygame.mouse.set_cursor(*pygame.cursors.arrow)

	def process_move(self, coord):
		if coord not in self.filled_squares and coord not in self.current_player().squares:
			# process move
			self.filled_squares.add(coord)
			self.current_player().add_square(coord)
			self.victory_path = self.current_player().victory_check()
			if self.victory_path:
				self.game_info_msg = "Congratulations Player %d! You win!" % (self.current_player().number)
				self.game_over = True
			else:
				self.switch_players()

	def mouse_click(self, pos):
		for b in self.buttons:
			if b.contains(pos):
				b.action()

		if self.game_started and not self.game_over and self.grid_rect.collidepoint(pos):
			x, y = pos
			grid_pos = (x - self.grid_rect.left)/self.square_size + 1, (y - self.grid_rect.top)/self.square_size + 1
			self.process_move(grid_pos)

		elif not self.game_started and not self.game_over:
			for n_box in self.N_options:
				if n_box.contains(pos):
					self.N = n_box.N
					n_box.bg_color = self.colors['options_bg_selected']
					if self.K > self.N:
						self.K = self.N
					for k_box in self.K_options:
						k_box.valid = True
						if k_box.K == self.K:
							k_box.bg_color = self.colors['options_bg_selected']
						elif k_box.K <= self.N:
							k_box.bg_color = self.colors['options_bg_unselected']
						else:
							k_box.bg_color = self.colors['options_bg_invalid']
							k_box.valid = False
					return
			for k_box in self.K_options:
				if k_box.contains(pos) and k_box.valid:
					self.K = k_box.K
					k_box.bg_color = self.colors['options_bg_selected']
					return

		elif self.game_started and self.game_over:
			pass

	def highlight_winner(self):
		d = self.square_size
		for x,y in self.victory_path:
			tl_x = self.grid_rect.left + d*(x-1)
			tl_y = self.grid_rect.top + d*(y-1)
			pygame.draw.polygon(self.screen, self.colors['victory_highlight'], [(tl_x,tl_y),(tl_x+d,tl_y),(tl_x+d,tl_y+d),(tl_x,tl_y+d)], 2)

	def draw_shape(self, pos, shape, color):
		x,y = pos
		r = self.square_size/3
		cx, cy = (int(self.grid_rect.left + self.square_size*(x - 0.5)), int(self.grid_rect.top + self.square_size*(y - 0.5)))
		if shape == 'x':
			pygame.draw.line(self.screen, color, (cx - r, cy - r), (cx + r, cy + r), 1)
			pygame.draw.line(self.screen, color, (cx - r, cy + r), (cx + r, cy - r), 1)
		else:
			pygame.draw.circle(self.screen, color, (cx, cy), r, 1)

	def draw_background(self):
		img_rect = self.tile_img.get_rect()
		nrows = int(self.screen.get_height() / img_rect.height) + 1
		ncols = int(self.screen.get_width() / img_rect.width) + 1
		for y in xrange(nrows):
			for x in xrange(ncols):
				img_rect.topleft = (x * img_rect.width, y * img_rect.height)
				self.screen.blit(self.tile_img, img_rect)

	def draw_grid_lines(self):
		tl_x, tl_y = self.grid_rect.topleft
		br_x, br_y = self.grid_rect.bottomright
		for i in xrange(1,self.N):
			pygame.draw.line(self.screen, self.colors['grid_line'], (tl_x + self.square_size*i, tl_y), (tl_x + self.square_size*i, br_y))
			pygame.draw.line(self.screen, self.colors['grid_line'], (tl_x, tl_y + self.square_size*i), (br_x, tl_y + self.square_size*i))

	def draw_shapes(self):
		for p in self.players:
			for pos in p.squares:
				self.draw_shape(pos, p.shape, p.color)

	def update_buttons(self, mouse_pos):
		for b in self.buttons:
			if b.contains(mouse_pos):
				b.bg_color = self.colors['options_bg_hover']
			else:
				b.bg_color = self.colors['options_bg_unselected']
			b.draw()

	def update_pre_game(self, mouse_pos):
		msg_height = self.N_options[0].outer_rect.top/3
		draw_text(self.screen, self.title, self.text_font, 50, self.colors['text'], (self.width/2, msg_height), True)
		draw_text(self.screen, 'Choose the size of the game grid:', self.text_font, 36,
				self.colors['text'], (self.width/2, msg_height*2.5), True)
		d = self.K_options[0].outer_rect.top - self.N_options[-1].outer_rect.bottom
		msg_height = self.N_options[-1].outer_rect.bottom + 2*d/3
		draw_text(self.screen, 'Choose how many squares in-a-row you need to win:', self.text_font, 36,
				self.colors['text'], (self.width/2, msg_height), True)

		for n_box in self.N_options:
			if n_box.contains(mouse_pos) and n_box.N != self.N:
				n_box.bg_color = self.colors['options_bg_hover']
			elif n_box.N != self.N:
				n_box.bg_color = self.colors['options_bg_unselected']
			n_box.draw()
		for k_box in self.K_options:
			if k_box.contains(mouse_pos) and k_box.valid and k_box.K != self.K:
				k_box.bg_color = self.colors['options_bg_hover']
			elif k_box.K <= self.N and k_box.K != self.K:
				k_box.bg_color = self.colors['options_bg_unselected']
			k_box.draw()

	def update(self, mouse_pos):
		self.grid_box.draw()
		self.draw_grid_lines()
		self.draw_shapes()

		msg_height = self.grid_rect.top/3
		title_rect = draw_text(self.screen, self.title, self.text_font, 50, self.colors['text'], (self.width/2, msg_height), True)
		msg_height = (self.grid_rect.top + title_rect.bottom)/2
		draw_text(self.screen, self.game_info_msg, self.text_font, 36, self.colors['text'], (self.width/2, msg_height), True)

		if self.game_over:
			self.highlight_winner()
			self.set_cursor()
		else:
			self.update_cursor(mouse_pos)

	def run(self):
		while True:
			time_passed = self.clock.tick(20)
			if time_passed > 100:
				continue
			for event in pygame.event.get():
				if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					self.quit()
				elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					self.mouse_click(event.pos)
			mouse_pos = pygame.mouse.get_pos()
			self.draw_background()
			self.update_buttons(mouse_pos)
			if self.game_started:
				self.update(mouse_pos)
			elif not self.game_started and not self.game_over:
				self.update_pre_game(mouse_pos)
			pygame.display.flip()

	def quit(self):
		sys.exit()

if __name__ == '__main__':
	#import pdb
	#pdb.set_trace()
	game = TicTacToe()
	game.run()