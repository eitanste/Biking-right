import pygame
import random
import serial
from objects import Road, Player, Tree, Button, \
    Obstacle, Coins, Fuel
import time

ser = serial.Serial("COM10", 9600)
pygame.init()
SCREEN = WIDTH, HEIGHT = 432, 768
win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
info = pygame.display.Info()
width = info.current_w
height = info.current_h

clock = pygame.time.Clock()
FPS = 60

lane_pos = [75, 142, 220, 300]

# COLORS **********************************************************************

WHITE = (255, 255, 255)
BLUE = (30, 144, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 20)

# FONTS ***********************************************************************

font = pygame.font.SysFont('cursive', 40)

select_car = font.render('Select Car', True, WHITE)

# IMAGES **********************************************************************

bg = pygame.image.load('Assets/bg.png')

home_img = pygame.image.load('Assets/home.png')
play_img = pygame.image.load('Assets/buttons/play.png')
tour_de_france_img = pygame.image.load('Assets/tour de france.jpg')
tour_de_france_img = pygame.transform.scale(tour_de_france_img,
                                            (WIDTH, HEIGHT))
end_img = pygame.image.load('Assets/end.jpg')
end_img = pygame.transform.scale(end_img, (WIDTH, HEIGHT))
game_over_img = pygame.image.load('Assets/game_over.png')
game_over_img = pygame.transform.scale(game_over_img, (220, 220))
coin_img = pygame.image.load('Assets/coins/1.png')
dodge_img = pygame.image.load('Assets/car_dodge.png')
loading = pygame.image.load('Assets/loading-bar.png')
loading = pygame.transform.scale(loading, (180, 66))

left_arrow = pygame.image.load('Assets/buttons/arrow.png')
right_arrow = pygame.transform.flip(left_arrow, True, False)

home_btn_img = pygame.image.load('Assets/buttons/home.png')
replay_img = pygame.image.load('Assets/buttons/replay.png')
sound_off_img = pygame.image.load("Assets/buttons/soundOff.png")
sound_on_img = pygame.image.load("Assets/buttons/soundOn.png")
bicycle1 = pygame.image.load('Assets/bicycle1.jpg')
bicycle1 = pygame.transform.scale(bicycle1, (WIDTH, HEIGHT))
bicycle2 = pygame.image.load('Assets/bicycle2.jpg')
bicycle2 = pygame.transform.scale(bicycle2, (WIDTH, HEIGHT))
bicycle3 = pygame.image.load('Assets/bicycle3.jpg')
bicycle3 = pygame.transform.scale(bicycle3, (WIDTH, HEIGHT))

cars = []
car_type = 0
for i in range(1, 9):
    img = pygame.image.load(f'Assets/cars/{i}.png')
    img = pygame.transform.scale(img, (59, 101))
    cars.append(img)
img = pygame.image.load('Assets/cars/Picture_bike.png')
cars.append(img)



# FUNCTIONS *******************************************************************
def center(image):
    return (WIDTH // 2) - image.get_width() // 2


# BUTTONS *********************************************************************
play_btn = Button(play_img, (100, 34), center(play_img) + 10, HEIGHT - 80)
la_btn = Button(left_arrow, (32, 42), 40, 180+200)
ra_btn = Button(right_arrow, (32, 42), WIDTH - 60, 180+200)

home_btn = Button(home_btn_img, (24, 24), WIDTH // 4 - 18, HEIGHT - 80)
replay_btn = Button(replay_img, (36, 36), WIDTH // 2 - 18, HEIGHT - 86)
sound_btn = Button(sound_on_img, (24, 24), WIDTH - WIDTH // 4 - 18,
                   HEIGHT - 80)

# SOUNDS **********************************************************************

click_fx = pygame.mixer.Sound('Sounds/click.mp3')
fuel_fx = pygame.mixer.Sound('Sounds/fuel.wav')
start_fx = pygame.mixer.Sound('Sounds/start.mp3')
restart_fx = pygame.mixer.Sound('Sounds/restart.mp3')
coin_fx = pygame.mixer.Sound('Sounds/coin.mp3')

pygame.mixer.music.load('Sounds/mixkit-tech-house-vibes-130.mp3')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0)  ##sound here

# OBJECTS *********************************************************************
road = Road()
p = Player(100, HEIGHT - 120, car_type)

tree_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
fuel_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()

# VARIABLES *******************************************************************
home_page = True
car_page = False
game_page = False
over_page = False
game_over_counter = 0

move_left = False
move_right = False
sound_on = True

counter = 0
counter_inc = 1
speed = 10
dodged = 0
coins = 0
cfuel = 100
fule_rate = .5

endx, enddx = 0, 0.5
gameovery = -50

running = True
left_foot = 0
right_foot = 0
counter2 = 3
pedal_counter = 0
counter_checker = 0
color_average = 0


def car_selection_page(left_foot, right_foot):
    global car_type, car_page, game_page, p, counter, counter_checker
    if car_page:
        win.blit(select_car, (center(select_car), 80+150))
        win.blit(cars[car_type], (WIDTH // 2 - 30, 150+200))
        la_btn.draw(win)
        ra_btn.draw(win)
        # win.blit(select_car, (center(select_car), 80))
        # win.blit(cars[car_type], (WIDTH // 2 - 30, 150))
        play_btn.draw(win)

        if right_foot > 50 and left_foot > 50:
            car_page = False
            game_page = True
            start_fx.play()
            p = Player(100, HEIGHT - 120, car_type)
            counter = 0

        elif left_foot > 30 and counter_checker % 2 == 0:
            car_type -= 1
            click_fx.play()
            if car_type < 0:
                car_type = len(cars) - 1

        elif right_foot > 30 and counter_checker % 2 == 0:
            car_type += 1
            click_fx.play()
            if car_type >= len(cars):
                car_type = 0


def game_over_page():
    global over_page, home_page, coins, dodged, counter, cfuel, endx, enddx, gameovery, game_page, sound_on, car_page, game_over_counter
    if over_page:

        win.blit(end_img, (endx, 0))
        endx += enddx
        if endx >= 10 or endx <= -10:
            enddx *= -1

        win.blit(game_over_img, (center(game_over_img), gameovery))
        if gameovery < 16:
            gameovery += 1

        num_coin_img = font.render(f'{coins}', True, WHITE)
        num_dodge_img = font.render(f'{dodged}', True, WHITE)
        distance_img = font.render(f'Distance : {counter :.2f} Meters', True,
                                   WHITE)

        win.blit(coin_img, (250, 240))
        win.blit(dodge_img, (180, 280))
        win.blit(num_coin_img, (300, 250))
        win.blit(num_dodge_img, (300, 300))
        win.blit(distance_img, (center(distance_img), (500)))

        home_btn.draw(win)
        replay_btn.draw(win)

        if game_over_counter < 20:
            game_over_counter += 1
            return

        # restart the game
        if right_foot > 50 and left_foot > 50:
            over_page = False
            game_page = True

            coins = 0
            dodged = 0
            counter = 0
            cfuel = 100

            endx, enddx = 0, 0.5
            gameovery = -50

            restart_fx.play()

        # select car again
        elif left_foot > 30 and counter_checker % 2 == 0:
            over_page = False
            car_page = True

            coins = 0
            dodged = 0
            counter = 0
            cfuel = 100

            endx, enddx = 0, 0.5
            gameovery = -50

        elif sound_btn.draw(win):
            sound_on = not sound_on

            if sound_on:
                sound_btn.update_image(sound_on_img)
                pygame.mixer.music.play(loops=-1)
            else:
                sound_btn.update_image(sound_off_img)
                pygame.mixer.music.stop()





def update_game_page():
    global counter, i, counter_inc, cfuel, dodged, speed, game_page, over_page, coins, fule_rate
    if game_page:
        win.blit(bg, (0, 0))
        road.update(speed)
        road.draw(win)
        if speed > 1:
            counter += counter_inc
        if counter % 20 == 0:
            tree = Tree(random.choice([-5, WIDTH - 35]), -20)
            tree_group.add(tree)

        manage_obsticles(speed)

        obstacle_group.update(speed)
        obstacle_group.draw(win)
        tree_group.update(speed)
        tree_group.draw(win)
        coin_group.update(speed)
        coin_group.draw(win)
        fuel_group.update(speed, color_average)
        fuel_group.draw(win)
        p.draw(win)

        if cfuel > 0:
            pygame.draw.rect(win, GREEN, (20, 20, cfuel, 15), border_radius=5)
        else:
            pygame.draw.rect(win, RED, p.rect, 1)
            speed = 1

            game_page = False
            over_page = True

            tree_group.empty()
            coin_group.empty()
            fuel_group.empty()
            obstacle_group.empty()

        pygame.draw.rect(win, WHITE, (20, 20, 100, 15), 2, border_radius=5)
        if speed > 1:
            cfuel -= fule_rate

        # COLLISION DETECTION & KILLS
        collision_detection_and_kills()


def manage_obsticles(speed):
    global counter, i
    if counter % 30 == 0:
        type = random.choices([1, 2], weights=[2, 6], k=1)[0]
        x = random.choice(lane_pos) + 10
        if type == 1:
            counter += 1
            count = random.randint(1, 3)
            for i in range(count):
                coin = Coins(x, -100 - (25 * i))
                coin_group.add(coin)
        elif type == 2:
            counter += 1
            fuel = Fuel(x, -100)
            fuel_group.add(fuel)
    elif counter % 20 == 0 and speed != 1:
        obs = random.choices([1, 2, 3], weights=[6, 3, 3], k=1)[0]
        obstacle = Obstacle(obs)
        obstacle_group.add(obstacle)


def collision_detection_and_kills():
    global dodged, speed, game_page, over_page, coins, cfuel
    for obstacle in obstacle_group:
        if obstacle.rect.y >= HEIGHT:
            if obstacle.type == 1:
                dodged += 1
            obstacle.kill()

        if pygame.sprite.collide_mask(p, obstacle):
            pygame.draw.rect(win, RED, p.rect, 1)
            speed = 1

            game_page = False
            over_page = True

            tree_group.empty()
            coin_group.empty()
            fuel_group.empty()
            obstacle_group.empty()
    if pygame.sprite.spritecollide(p, coin_group, True):
        coins += 1
        coin_fx.play()
    if pygame.sprite.spritecollide(p, fuel_group, True):
        cfuel += Fuel.getVal(fuel_group)
        fuel_fx.play()
        if cfuel >= 100:
            cfuel = 100


def game_home_page():
    global counter, home_page, car_page

    if home_page:
        win.blit(bicycle2, (0, 0))
        win.blit(loading, (220, 20))
        counter += 1
        if counter % 200 == 0:
            home_page = False
            car_page = True


def speed_calculator():
    global move_left, move_right, speed
    if right_foot + left_foot < 30 or pedal_counter == 0:
        speed = 1
        road.update(speed)
        p.update(False, False, left_foot, right_foot)

    elif left_foot > right_foot and left_foot > 100:
        move_left = True
        move_right = False
        p.update(move_left, move_right, left_foot, right_foot)
    elif left_foot <= right_foot and right_foot > 100:

        move_right = True
        move_left = False
        p.update(move_left, move_right, left_foot, right_foot)
        speed = 10
        road.update(speed)

        ## TODO: is it needed?
    else:
        move_right = False
        move_left = False
        p.update(move_left, move_right, left_foot, right_foot)
        speed = 10
        road.update(speed)


while running:

    counter_checker += 1
    if ser.in_waiting > 0:
        if counter2 < 0:
            line = ser.readline().decode('utf-8').rstrip()  # decode the bytes from the serial connection and remove any trailing whitespace
            line2 = line.split(',')
            left_foot = int(line2[12].split(' ')[-1])
            right_foot = int(line2[13].split(' ')[-1])
            pedal_counter = int(line2[14].split(' ')[-1])
            color_average = int(line2[11].split(' ')[-1])
        else:
            counter2 -= 1

    win.fill(BLACK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                running = False

    speed_calculator()
    game_home_page()
    car_selection_page(left_foot, right_foot)
    game_over_page()
    update_game_page()
    pygame.draw.rect(win, BLUE, (0, 0, WIDTH, HEIGHT), 3)
    clock.tick(FPS)
    pygame.display.update()

pygame.quit()
