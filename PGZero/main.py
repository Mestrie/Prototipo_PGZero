import random
from pygame import Rect

WIDTH = 800
HEIGHT = 450

GROUND_Y = 320

game_state = "menu"
music_on = True
ground_tiles = []

# --------------------------------------------------
# Botões
# --------------------------------------------------
class Button:
    def __init__(self, text, rect, action):
        self.text = text
        self.rect = rect
        self.action = action

    def draw(self):
        screen.draw.filled_rect(self.rect, (40, 40, 40))
        screen.draw.rect(self.rect, "white")
        screen.draw.text(
            self.text,
            center=self.rect.center,
            fontsize=30,
            color="white"
        )

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.action()


# --------------------------------------------------
# Sprite Animados
# --------------------------------------------------
class AnimatedSprite:
    def __init__(self, frames, pos):
        self.frames = frames
        self.frame_index = 0
        self.actor = Actor(frames[0], pos)

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.actor.image = self.frames[int(self.frame_index)]

    def draw(self):
        self.actor.draw()


# --------------------------------------------------
# Heroi
# --------------------------------------------------
class Hero(AnimatedSprite):
    def __init__(self):
        super().__init__(
            frames=["hero/idle_0", "hero/idle_1"],
            pos=(120, GROUND_Y)
        )
        self.idle_frames = ["hero/idle_0", "hero/idle_1"]
        self.walk_frames = ["hero/walk_0", "hero/walk_1"]

        self.velocity_y = 0
        self.on_ground = False
        self.speed = 3

    def update(self):
        moving = False
        self.on_ground = False

        # Movimento horizontal
        if keyboard.left:
            self.actor.x -= self.speed
            moving = True

        if keyboard.right:
            self.actor.x += self.speed
            moving = True

        # Gravidade
        self.velocity_y += 0.5
        self.actor.y += self.velocity_y

        # --- COLISÃO COM O CHÃO ---
        for tile in ground_tiles:
            if self.actor.colliderect(tile):
                if self.velocity_y >= 0:
                    self.actor.bottom = tile.top
                    self.velocity_y = 0
                    self.on_ground = True

        # Pulo
        if keyboard.space and self.on_ground:
            self.velocity_y = -10
            self.on_ground = False
            sounds.jump.play()

        # --- ANIMAÇÃO ---
        if moving:
            self.frames = self.walk_frames
            self.frame_index += 0.2
        else:
            self.frames = self.idle_frames
            self.frame_index += 0.06

        if self.frame_index >= len(self.frames):
            self.frame_index = 0

        self.actor.image = self.frames[int(self.frame_index)]





# --------------------------------------------------
# Inimigos
# --------------------------------------------------
class Enemy(AnimatedSprite):
    def __init__(self, x, left_limit, right_limit):
        super().__init__(
            frames=["enemy/walk_0", "enemy/walk_1"],
            pos=(x, GROUND_Y)
        )
        self.left_limit = left_limit
        self.right_limit = right_limit
        self.direction = random.choice([-1, 1])
        self.speed = 2

        self.velocity_y = 0
        self.on_ground = False

    def update(self):
        # Movimento horizontal
        self.actor.x += self.speed * self.direction

        if self.actor.x <= self.left_limit or self.actor.x >= self.right_limit:
            self.direction *= -1

        # Gravidade
        self.velocity_y += 0.5
        self.actor.y += self.velocity_y
        self.on_ground = False

        # Colisão com o chão
        for tile in ground_tiles:
            if self.actor.colliderect(tile):
                if self.velocity_y >= 0:
                    self.actor.bottom = tile.top
                    self.velocity_y = 0
                    self.on_ground = True

        self.animate()



# --------------------------------------------------
# Controle do Jogo
# --------------------------------------------------
def start_game():
    global game_state
    game_state = "playing"
    reset_game()


def toggle_music():
    global music_on
    music_on = not music_on
    if music_on:
        music.unpause()
    else:
        music.pause()


def exit_game():
    quit()


# --------------------------------------------------
# Menu botões
# --------------------------------------------------
buttons = [
    Button("Start Game", Rect(300, 160, 200, 50), start_game),
    Button("Music ON / OFF", Rect(300, 230, 200, 50), toggle_music),
    Button("Exit", Rect(300, 300, 200, 50), exit_game),
]


# --------------------------------------------------
# Musica
# --------------------------------------------------
music.play("walen_gameboy")
music.set_volume(0.4)


# --------------------------------------------------
# Loop
# --------------------------------------------------
def update():
    if game_state == "playing":
        hero.update()
        for enemy in enemies:
            enemy.update()
            if hero.actor.colliderect(enemy.actor):
                sounds.hit.play()
                reset_game()


def draw():
    screen.clear()
    screen.fill((120, 180, 240))

    if game_state == "menu":
        screen.draw.text(
            "Platformer Test",
            center=(WIDTH // 2, 90),
            fontsize=48,
            color="white"
        )
        for button in buttons:
            button.draw()
    else:
        for tile in ground_tiles:
            tile.draw()
        hero.draw()
        for enemy in enemies:
            enemy.draw()


def on_mouse_down(pos):
    if game_state == "menu":
        for button in buttons:
            button.check_click(pos)


def reset_game():
    global hero, enemies, ground_tiles

    hero = Hero()
    enemies = [
        Enemy(420, 380, 520),
        Enemy(650, 600, 750)
    ]

    ground_tiles = []

    base_tile = Actor("platform/ground")
    tile_width = base_tile.width
    tile_height = base_tile.height

    y = GROUND_Y + tile_height // 2

    x = 0
    while x < WIDTH:
        tile = Actor("platform/ground")
        tile.left = x
        tile.centery = y
        ground_tiles.append(tile)
        x += tile_width


