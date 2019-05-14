import pygame as pg
import random


pg.init()
pg.mixer.pre_init(44100, -16, 1, 512)
pg.mixer.init()

class Hero:
    def __init__(self):
        self.x = 270
        self.y = 640
        self._width = 60
        self._height = 60
        self.move_s_x = 0
        self.move_s_y = 0
        self.max_s_x = 6
        self.max_s_y = 15
        self.boost = 3
        self.jumping_s = 15
        self.jump_right_image = []
        self.jump_left_image = []
        self.run_right_image = []
        self.run_left_image = []
        self.jumping_right = pg.image.load('img/ninja8.png')
        self.jumping_left = pg.transform.flip(self.jumping_right, True, False)
        self.stand = pg.image.load('img/ninja8.png')
        self.falling = pg.image.load('img/ninja7.png')
        self.animation_count = 0
        self.sound_step = pg.mixer.Sound('sounds/step.ogg')
        self.sound_jump = pg.mixer.Sound('sounds/jump.wav')
        self.sound_jump.set_volume(0.5)
        #self.sound_step.set_volume()

        for index in range(1, 8):
            self.jump_right_image.append(pg.image.load('img/ninja' + str(index) + '.png'))
            self.jump_left_image.append(pg.transform.flip(self.jump_right_image[index - 1], True, False))
        for index in range(1, 7):
            self.run_right_image.append(pg.image.load('img/ninja_' + str(index) + '.png'))
            self.run_left_image.append(pg.transform.flip(self.run_right_image[index - 1], True, False))
        self.image = self.stand


    def running(self, list_of_steps):
        press_events = pg.key.get_pressed()
        if record > 300:
            self.max_s_x = 7

        if record > 600:
            self.max_s_x = 6

        if self.animation_count + 1 >= 60:
            self.animation_count = 0

        # Сквозные границы.
        if self.x > WIDTH:
            self.x = -self._width
        elif self.x + self._width < 0:
            self.x = WIDTH

        # Физика отскока от платформы + анимация.
        self.jump_step(list_of_steps)

        # Движения играка по Х, при условии, что он выше стартовой плоскости (выше себя).
        if self.y < HEIGHT - self._height:
            if press_events[pg.K_LEFT]:
                self.move_s_x -= self.boost
            elif press_events[pg.K_RIGHT]:
                self.move_s_x += self.boost
            else:
                # Падение с замедлением после прохождения высоты прыжка.
                if self.move_s_x < 0:
                    self.move_s_x = self.move_s_x + self.boost / 8
                if self.move_s_x > 0:
                    self.move_s_x = self.move_s_x - self.boost / 8

        # Ограничение скорости при движении по осям (в невесомости).
        if self.move_s_y > self.max_s_y:
            self.move_s_y = self.max_s_y
            self.move_s_x = self.max_s_x

        elif self.move_s_x < -self.max_s_x:
            self.move_s_x = -self.max_s_x

        elif self.move_s_x > self.max_s_x:
            self.move_s_x = self.max_s_x

        # Аниамция сальто.
        if self.move_s_y > 0:
            if self.move_s_x > 0:
                self.image = self.jump_right_image[self.animation_count // 9]
                self.animation_count += 1
            elif self.move_s_x < 0:
                self.image = self.jump_left_image[self.animation_count // 9]
                self.animation_count += 1
        elif self.move_s_x == 0 and self.move_s_y != 0:
            self.image = self.falling

        # Анимация бега (по стартовой плоскости).
        elif self.move_s_x == 0 and self.move_s_y == 0:
            if press_events[pg.K_LEFT]:
                self.sound_step.play()
                self.image = self.run_left_image[self.animation_count // 10]
                self.animation_count += 1
            elif press_events[pg.K_RIGHT]:
                self.sound_step.play()
                self.image = self.run_right_image[self.animation_count // 10]
                self.animation_count += 1
            else:
                self.image = self.stand

        # Анимация паления по Y, относительно сдвига по Х.
        else:
            if self.move_s_x > 0:
                self.image = self.jump_right_image[self.animation_count // 9]
                self.animation_count += 1
            elif self.move_s_x < 0:
                self.image = self.jump_left_image[self.animation_count // 9]
                self.animation_count += 1

        # Изменение координаты персонажа после расчёта скорости выше.
        self.x += self.move_s_x
        self.y -= self.move_s_y

        return [self.image, [self.x, self.y, self._width, self._height]]

    def jump_step(self, list_of_steps):
        press_events = pg.key.get_pressed()
        jump = False

        # Контакт с платформой
        for img, step in list_of_steps:
            x_step, y_step, width_step, height_step = step[0], step[1], step [2], step[3]
            if x_step < self.x + self._width / 2 < x_step + width_step:
                if y_step <= self.y + self._height <= y_step + height_step:
                    if self.move_s_y < 0:
                        jump = True

                        self.sound_jump.play()


        # Скорость прыжка.
        if not jump and not self.y >= HEIGHT - self._height:
            self.move_s_y -= 0.5
        elif jump:
            self.move_s_y = self.jumping_s
        else:
            self.y = HEIGHT - self._height
            self.move_s_x = 0
            self.move_s_y = 0
            if press_events[pg.K_LEFT]:
                self.x -= 4
            elif press_events[pg.K_RIGHT]:
                self.x += 4
            if press_events[pg.K_SPACE]:
                self.move_s_y = self.jumping_s


class Step:
    def __init__(self, x, y, run):
        self.x = x
        self.y = y
        self.run = run
        self.pl_2 = pg.image.load('img/platform1.png')
        self.pl_3 = pg.image.load('img/platform4.png')

        self.move_speed_step = random.choice([1, 2, 3])
        self._height = 30
        self._width = 130

    def moving(self):
        if self.run == 0:
            self._width = 90
        self.x += self.move_speed_step * self.run

        # "Отскоки" от границ.
        if self.x <= 0:
            self.run = 1
        if self.x + self._width >= WIDTH:
            self.run = -1

        if self.run != 0:
            self.image = self.pl_2
        else:
            self.image = self.pl_3

    def screen_control(self):
        if self.y <= height_y + HEIGHT:
            return True
        return False

    def save(self):
        if self.run != 0:
            self.image = self. pl_2
        else:
            self.image = self.pl_3
        return [self.image, [self.x, self.y, self._width, self._height]]


class Step_creator:
    def __init__(self, distance):
        self.distance = distance
        self.step_count = 0
        self.start_spawn = HEIGHT - 100
        self.steps = []
        self._width = 130
        self._height = 30

    def running(self):
        new_steps = []
        draw_steps = []

        if HEIGHT - height_y > self.step_count * self.distance:
            y_spawn = self.start_spawn - self.step_count * self.distance
            x_spawn = random.randint(-self._width, WIDTH)
            r_spawn = random.choice([1, 0, 0, 0, 0, 0, -1])
            self.steps.append(Step(x_spawn, y_spawn, r_spawn))
            self.step_count += 1

        for step in self.steps:
            step.moving()
            draw_steps.append(step.save())
            if step.screen_control():
                new_steps.append(step)
        self.steps = new_steps
        return draw_steps

    def first_step(self):
        return [pg.image.load('img/platform6.png'), [175, 630, 250, 40]]


class Suriken():
    def __init__(self, pos, dis, w, h):
        self.dis = dis
        self.surikens = []
        self.image = pg.image.load('img/suricen.png')
        self.x = pos[0]
        self.y = pos[1]
        self.w = w
        self.h = h
        self.speed_x = random.randint(4, 6)
        self.jump = 10
        self.g = True

    def moving(self):
        if self.jump >= -10:
            if self.jump < 0:
                self.y += (self.jump ** 2) / 2
                self.x += self.speed_x * self.dis
            else:
                self.y -= (self.jump ** 2) / 2
                self.x += self.speed_x * self.dis
            self.jump -= 1
        else:
            self.jump = 10
        screen.blit(pg.transform.scale(self.image, (self.w, self.h)), (self.x, self.y))


class Button:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.color_on = (51, 66, 60)
        self.color_off = (16, 20, 13)
        self.sound_click = pg.mixer.Sound('sounds/button.ogg')

    def draw_button(self, x, y, msg='START', act=None, size_text=25):
        motion = pg.mouse.get_pos()
        mouse_down = pg.mouse.get_pressed()

        if x < motion[0] < x + self.w and y < motion[1] < y + self.h:

            pg.draw.rect(screen, self.color_on, (x, y, self.w, self.h))

            if mouse_down[0] == 1:
                self.sound_click.play()
                #pg.time.delay(300)
                if act is not None:
                    act()

        else:
            pg.draw.rect(screen, self.color_off, (x, y, self.w, self.h))
        self.draw_msg(msg, x + 35, y + 5, size_text=size_text)

    @staticmethod
    def draw_msg(msg, x, y, color_text=(100, 100, 100), type_text='arial', size_text=25):
        type_text = pg.font.SysFont(type_text, size_text)
        txt = type_text.render(msg, True, color_text)
        screen.blit(txt, (x, y))


def update_record(record, position):
    msg = font.render(str(round(record)), True, (136, 255, 125))
    table = msg.get_rect()
    y_table = table.height + 15

    if position == 0:
        x_table = WIDTH - table.width - 15
    else:
        x_table = 15

    screen.blit(msg, (x_table, y_table))


def lose_suriken(pos):
    lst = []
    for _ in range(10):
        lst.append(Suriken(pos, random.choice([-1, 1]), random.randint(20, 50), random.randint(20, 50)))
    return lst


def menu():
    background = pg.image.load('img/start_menu.png')
    logo = pg.image.load('img/logo.png')
    start_button = Button(250, 60)

    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        screen.blit(background, (0, 0))
        screen.blit(pg.transform.scale(logo, (600, 250)), (20, 50))
        start_button.draw_button(175, 350, act=start_game, size_text=80)
        pg.display.update()
        clock.tick(60)


def start_game():
    global height_y, hero, a, record
    game = True
    bg = pg.image.load('img/bg.png')
    sound_drop = pg.mixer.Sound('sounds/drop_suriken.wav')
    fon = pg.mixer.Sound('sounds/background.ogg')
    fon.play(-1)
    fon.set_volume(0.5)

    height_y = 0
    record = 0
    new_record = 0

    count_suriken = 0
    a = lose_suriken((WIDTH / 2, HEIGHT))
    hero = Hero()
    step_creator = Step_creator(70)
    while game:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game = False
                fon.stop()

        steps = step_creator.running()
        ninja = hero.running(steps)

        # Скроллинг экрана.
        height_y = min(min(0, ninja[1][1] - HEIGHT * 0.45), height_y)
        record = (-ninja[1][1] + 670) / 10

        # Конец игры.
        if ninja[1][1] - 670 > height_y:
            record = 0
            height_y = 0
            hero = Hero()
            step_creator = Step_creator(70)
            count_suriken += 1
            a = lose_suriken((WIDTH / 2, HEIGHT))
            sound_drop.play()

        screen.blit(bg, (0, 0))
        if count_suriken != 0:
            for i in a:
                i.moving()

        for step in steps:
            step[1][1] -= height_y
            screen.blit(pg.transform.scale(step[0], (step[1][2], step[1][3])), (step[1][0], step[1][1]))
        screen.blit(pg.transform.scale(ninja[0], (ninja[1][2], ninja[1][3])), (ninja[1][0], ninja[1][1] - height_y))
        new_record = max(new_record, record)
        update_record(record, 1)
        update_record(new_record, 0)
        pg.display.flip()
        clock.tick(fps)


WIDTH = 600
HEIGHT = 700
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Ninja jump!')
clock = pg.time.Clock()
font = pg.font.SysFont('', 45)
fps = 60

menu()
pg.quit()
