import pygame, random, time


#ancho y alto de la ventana
WIDTH = 800
HEIGHT = 600
#colores basados en R-G-B
BLACK = (0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
pygame.init() #inicia la libreria pygame
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Trabajo Integrador Pygame") #le ponemos nombre a la ventana
clock = pygame.time.Clock() 

def draw_text(surface, text, size, x, y):
	font = pygame.font.SysFont("serif", size)
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surface.blit(text_surface, text_rect)

def draw_shield_bar(surface, x, y, percentage, lenght, color):
	BAR_COLOR = color
	BAR_LENGHT = lenght
	BAR_HEIGHT = 10
	# Calcular el ancho de la barra de vida
	fill = (percentage / 100) * BAR_LENGHT
	border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
	# Definir el rectángulo para la barra de vida
	fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
	# Dibujar la barra de vida dependiendo de si 1:player o 2:enemigo
	if BAR_COLOR == 1:
		pygame.draw.rect(surface, GREEN, fill)
	if BAR_COLOR == 2:
		pygame.draw.rect(surface, RED, fill)
	# Dibujar el borde de la barra de vida
	pygame.draw.rect(surface, WHITE, border, 2)


class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("assets/player.png").convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH // 2
		self.rect.centery = HEIGHT // 2
		self.rect.bottom = HEIGHT - 10
		self.speed_x = 0
		self.speed_y = 0
		self.shield = 100

	def update(self):
		self.speed_x = 0
		self.speed_y = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speed_x = -5
		if keystate[pygame.K_RIGHT]:
			self.speed_x = 5
		if keystate[pygame.K_UP]:
			self.speed_y = -5
		if keystate[pygame.K_DOWN]:
			self.speed_y = 5
		self.rect.x += self.speed_x
		self.rect.y += self.speed_y
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.bottom > HEIGHT:
			self.rect.bottom = HEIGHT
		if self.rect.top < 0:
			self.rect.top = 0

	def shoot(self):
		bullet = Bullet(self.rect.centerx, self.rect.top)
		all_sprites.add(bullet)
		bullets.add(bullet)
		laser_sound.play()

class Meteor(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.direction = random.choice([-1, 1])
		if self.direction == 1:
			self.image = random.choice(meteor_images[0:10])
		else:
			self.image = random.choice(meteor_images[10:19])
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-140, -100)
		self.speedy = random.randrange(1, 10)
		self.speedx = random.randrange(1, 5) * self.direction
		
	def update(self):
		self.rect.y += self.speedy
		self.rect.x += self.speedx
		if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 40:
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-140, - 100)
			self.speedy = random.randrange(1, 10)

class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/Enemigo.png ").convert()
        self.image.set_colorkey(BLACK) 
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.centery = 0  # Ajusta la posición inicial del enemigo
        self.speed_Y = 0  # Ajusta la velocidad de movimiento del enemigo
        self.speed_X = 4
        self.vida = 100 # Agregamos la vida inicial del enemigo
        
	
    def update(self):
        self.speed_Y = 0
        if (self.rect.centery != 100):
            self.speed_Y = 1
            self.rect.y += self.speed_Y
        else:
            self.rect.x += self.speed_X
            if self.rect.right > WIDTH or self.rect.left < 0:
                self.speed_X = -self.speed_X  # Invierte la dirección

        		
class Misil(pygame.sprite.Sprite):
	def __init__(self,x,y):
		super().__init__()
		if x == 0:
			self.direction = 1
		else:
			self.direction = -1
		if self.direction == 1:
			self.image = misiles_images[1]
		else:
			self.image = misiles_images[0]

		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.x = x
		self.speedx = 3 * self.direction

	def update(self):
		self.rect.x += self.speedx
		if self.rect.left < -40 or self.rect.right > WIDTH + 40:
			self.kill()

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load("assets/laser2.png")
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.centerx = x
		self.rect.centery = y
		self.speedy = -10

	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0:
			self.kill()

class Explosion(pygame.sprite.Sprite):
	def __init__(self, center):
		super().__init__()
		self.image = explosion_anim[0]
		self.rect = self.image.get_rect()
		self.rect.center = center 
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 50 # VELOCIDAD DE LA EXPLOSION

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.frame += 1
			if self.frame == len(explosion_anim):
				self.kill()
			else:
				center = self.rect.center
				self.image = explosion_anim[self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center

def show_intro_screen():


    pygame.display.flip()
    screen.blit(background, [0,0])
    draw_text(screen,"TRABAJO PRACTICO PYTHON", 40, WIDTH // 2, HEIGHT // 7)
    draw_text(screen,"integrantes:",30, WIDTH // 2, HEIGHT // 4)
    draw_text(screen," Franco Macri , Johnny Rafael Arvelo Cabrera , Agustin Bardelli   ",20, WIDTH // 2, HEIGHT // 3)
    draw_text(screen,"Ramos Florecia Ayelen , Elias Serantes , Leon Caceres Christian", 20, WIDTH // 2, HEIGHT // 2)
    draw_text(screen,"Presione enter para continuar...", 22, WIDTH // 2, HEIGHT // 1.5)
   
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                waiting = False

def show_go_screen():

	screen.blit(background, [0,0])
	draw_text(screen, "VIAJE AL ESPACIO", 75, WIDTH // 2, HEIGHT // 4)
	draw_text(screen, "Usar flechas direccionales para moverte en la pantalla y espacio para disparar", 22, WIDTH // 2, HEIGHT // 2)
	draw_text(screen, "Presione una tecla para iniciar y Buena suerte :D", 20, WIDTH // 2, HEIGHT * 3/4)
	pygame.display.flip()
	waiting = True

	while waiting:
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYUP:
				waiting = False

meteor_images = []
meteor_list = ["assets/meteorGrey_big1.png", "assets/meteorGrey_big2.png", "assets/meteorGrey_big3.png", 
			   "assets/meteorGrey_big4.png", "assets/meteorGrey_med1.png", "assets/meteorGrey_med2.png", 
			   "assets/meteorGrey_small1.png", "assets/meteorGrey_small2.png", "assets/meteorGrey_tiny1.png", 
			   "assets/meteorGrey_tiny2.png", "assets/Meteorito_G_2.png", "assets/Meteorito_G_3.png",
			   "assets/Meteorito_G_4.png", "assets/Meteorito_M_1.png", "assets/Meteorito_M_2.png",
			   "assets/Meteorito_mP_1.png", "assets/Meteorito_mP_2.png", "assets/Meteorito_P_1.png",
			   "assets/Meteorito_P_2.png"
				]
for img in meteor_list:
	meteor_images.append(pygame.image.load(img).convert())

misiles_images = []
misiles_list = ["assets/Misil_1.png", "assets/Misil_2.png"]
for img in misiles_list:
	misiles_images.append(pygame.image.load(img).convert())

####----------------EXPLOSTION IMAGENES --------------
explosion_anim = []
for i in range(9):
	file = "assets/regularExplosion0{}.png".format(i)
	img = pygame.image.load(file).convert()
	img.set_colorkey(BLACK)
	img_scale = pygame.transform.scale(img, (70,70))
	explosion_anim.append(img_scale)

# Cargar imagen de fondo
background = pygame.image.load("assets/background.png").convert()

# Cargar sonidos
laser_sound = pygame.mixer.Sound("assets/laser5.ogg")
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")
pygame.mixer.music.load("assets/Modelo de musica Prueba.mp3")
pygame.mixer.music.set_volume(0.2)

#### ----------GAME OVER
show_intro_screen()
game_over = True
running = True
pygame.mixer.music.play(loops=-1)
enemigo_aparecido = False
enemigo = Enemigo()
puntos = 100 #Cantidad de puntos para que aparezca el jefe
last_misil_time = pygame.time.get_ticks()
while running:
	if game_over:
		show_go_screen()
		game_over = False
		all_sprites = pygame.sprite.Group()
		meteor_list = pygame.sprite.Group()
		misiles_list = pygame.sprite.Group()
		bullets = pygame.sprite.Group()
		enemigo_aparecido = False
		player = Player()
		all_sprites.add(player)
		score = 0
		puntos = 100
		for i in range(15):
		  	meteor = Meteor()
		  	all_sprites.add(meteor)
		  	meteor_list.add(meteor)

	current_time = pygame.time.get_ticks()
	clock.tick(60)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player.shoot()
		
	all_sprites.update()

	#colisiones - meteoro - laser
	hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)
	for hit in hits:
		score += 10
		explosion_sound.play()
		explosion = Explosion(hit.rect.center)
		all_sprites.add(explosion)
		if score < puntos:
			meteor = Meteor()
			all_sprites.add(meteor)
			meteor_list.add(meteor)
	# Checar colisiones - jugador - meteoro
	hits = pygame.sprite.spritecollide(player, meteor_list, True)
	for hit in hits:
		player.shield -= 25
		if score < puntos:
			meteor = Meteor()
			all_sprites.add(meteor)
			meteor_list.add(meteor)
		if player.shield <= 0:
			game_over = True
	# Checamos colisiones jugador - misiles
	hits = pygame.sprite.spritecollide(player, misiles_list, True)
	for hit in hits:
		player.shield -= 25
		explosion = Explosion(hit.rect.center)
		all_sprites.add(explosion)
		if player.shield <= 0:
			game_over = True
	# Dentro del bucle principal, después de la línea que maneja las colisiones meteor-bala
	if score >= puntos:
		hits = pygame.sprite.spritecollide(enemigo, bullets, True)
		for hit in hits:
			enemigo.vida -= 10  # Resta vida al enemigo cuando es alcanzado por una bala
			if enemigo.vida <= 0:
				enemigo.kill()  # Elimina al enemigo si su vida llega a cero o menos
				enemigo_aparecido = False  # Restablece el indicador para que pueda aparecer de nuevo
				game_over = False
				puntos = score+200
				pygame.time.delay(1000)
				if enemigo.vida == 0 :
					if player.shield <=50:
						player.shield += 50
					else:
						if player.shield != 100:
							player.shield += 25
					for i in range(7):
			  			meteor = Meteor()
		  				all_sprites.add(meteor)
		  				meteor_list.add(meteor)

	screen.blit(background, [0, 0])
	all_sprites.draw(screen)
       
	#hacer aparecer el enemigo
	if score >= puntos and not enemigo_aparecido:
		enemigo = Enemigo()
		all_sprites.add(enemigo)
		enemigo_aparecido = True
	if enemigo_aparecido:
		enemigo.update()
		
	if score >= puntos:
		if current_time - last_misil_time >= 300:
			cuadrantemisil = [70,100,150,200,250,300,350,400,450,500,550,600,650,700]
			ladomisil = [0,770]
			cuadranteelegido = random.choice(cuadrantemisil)
			ladoelegido = random.choice(ladomisil)
			misil = Misil(ladoelegido,cuadranteelegido)
			all_sprites.add(misil)
			misiles_list.add(misil)
			last_misil_time = current_time
			
	# Marcador
	draw_text(screen, str(score), 25, WIDTH // 2, 10)
	# Escudo.
	draw_shield_bar(screen, 5, 590, player.shield, 100,1)
	#vida enemigo
	if score >= puntos:
		draw_shield_bar(screen,140,5, enemigo.vida, 500,2)

	pygame.display.flip()
	
pygame.quit()