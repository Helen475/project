import random
import pygame
import sys
from time import sleep


class ShipFlight:
    def __init__(self):
        self.bg_speed = None
        self.bg_y2 = None
        self.bg_y1 = None
        self.bg_x2 = None
        self.bg_x1 = None
        self.bg_img = None

        self.meteorite_start_x = None
        self.meteorite_start_y = None
        self.meteorite_width = None
        self.meteorite_height = None
        self.meteorite_speed = None
        self.meteorite_rect = None
        self.meteorite_img = None
        self.meteorite_images = None
        self.meteorite_sprite_mask = None
        self.meteorite_sprite = None

        self.ship_rect = None
        self.ship_img = None
        self.ship_images = None
        self.ship_width = None
        self.ship_y_coordinate = None
        self.ship_x_coordinate = None
        self.ship_m_right = False
        self.ship_m_left = False
        self.ship_sprite_mask = None
        self.ship_sprite = None

        self.oil_start_y = None
        self.oil_rect = None
        self.oil_img = None
        self.oil_height = None
        self.oil_width = None
        self.oil_speed = None
        self.oil_start_x = None
        self.oil_sprite_mask = None
        self.oil_sprite = None

        self.stone_sprite_mask = None
        self.stone_speed = None
        self.stone_start_x = None
        self.stone_sprite = None
        self.stone_height = None
        self.stone_start_y = None

        self.food_sprite_mask = None
        self.food_height = None
        self.food_speed = None
        self.food_start_y = None
        self.food_start_x = None
        self.food_sprite = None

        self.display_width = 800
        self.display_height = 600

        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

        self.clock = pygame.time.Clock()

        self.index = 0
        self.final = False
        self.final_score = 500  # значение установлено для проверки финального экрана
        self.crash_img = None
        self.crashed = None
        self.game_display = None
        self.increase_speed = None
        self.count = None
        self.time_count = None

        pygame.init()
        pygame.mixer.music.load("./sounds/ballad.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

        with open('high_score.txt', 'r') as f:
            self.high_score = int(f.readline())
        self.initialize()

    def initialize(self):

        self.crashed = False

        # космический корабль

        self.ship_images = []
        self.ship_images.append(pygame.image.load('./img/ship1.png'))
        self.ship_images.append(pygame.image.load('./img/ship2.png'))
        self.ship_images.append(pygame.image.load('./img/ship3.png'))
        self.ship_images.append(pygame.image.load('./img/ship4.png'))
        self.ship_images.append(pygame.image.load('./img/ship5.png'))
        self.ship_images.append(pygame.image.load('./img/ship6.png'))
        self.ship_x_coordinate = (self.display_width * 0.45)
        self.ship_y_coordinate = (self.display_height * 0.6)
        self.ship_width = 70

        # метеорит

        self.meteorite_sprite = pygame.sprite.Sprite()
        self.meteorite_sprite.image = pygame.image.load('./img/meteorite1.png')
        self.meteorite_start_x = random.randint(0, 31) * 10 + 220
        self.meteorite_start_y = -600
        self.meteorite_speed = 5
        self.meteorite_height = 45

        # капля масла

        self.oil_sprite = pygame.sprite.Sprite()
        self.oil_sprite.image = pygame.image.load('./img/oil.png')
        self.oil_start_x = random.randint(0, 31) * 10 + 220
        self.oil_start_y = random.randrange(-800, -200, 10)
        self.oil_speed = 3
        self.oil_height = 40

        # банка тушёнки

        self.food_sprite = pygame.sprite.Sprite()
        self.food_sprite.image = pygame.image.load('./img/food.png')
        self.food_start_x = random.randint(0, 31) * 10 + 220
        self.food_start_y = random.randrange(-800, -200, 10)
        self.food_speed = 3
        self.food_height = 40

        # драгоценный метеорит

        self.stone_sprite = pygame.sprite.Sprite()
        self.stone_sprite.image = pygame.image.load('./img/stone.png')
        self.stone_start_x = random.randint(0, 31) * 10 + 220
        self.stone_start_y = random.randrange(-800, -200, 10)
        self.stone_speed = 3
        self.stone_height = 40

        # фон

        self.bg_img = pygame.image.load("./img/background.jpg")
        self.bg_x1 = (self.display_width / 2) - (360 / 2)
        self.bg_x2 = (self.display_width / 2) - (360 / 2)
        self.bg_y1 = 0
        self.bg_y2 = -600
        self.bg_speed = 3

        # статистика

        self.count = 0
        self.time_count = 0

    def flight_window(self):
        """основное окно игры"""
        self.game_display = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Звёздный Ворс - полёт "Скарабея"')
        self.start_screen()

    def start_screen(self):
        """стартовый экран игры"""
        intro_text = ["F1 - посмотреть правила игры", "ENTER - выбор уровня и начало игры"]

        fon = pygame.image.load('./img/fon.jpg')
        self.game_display.blit(fon, (0, 0))
        font = pygame.font.SysFont("courier new", 15, True)
        text_coord = 5

        for line in intro_text:
            string_rendered = font.render(line, True, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 8
            intro_rect.top = text_coord
            intro_rect.x = 8
            text_coord += intro_rect.height
            self.game_display.blit(string_rendered, intro_rect)

        while True and not self.final:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return self.display_level_menu()
                    if event.key == pygame.K_F1:
                        return self.display_about_menu()
            pygame.display.flip()

    def display_level_menu(self):
        """экран с выбором уровня сложности игры"""
        self.increase_speed = 0
        fon_level = pygame.image.load('./img/fon_level.jpg')
        self.game_display.blit(fon_level, (0, 0))
        level_title = ['Выберите уровень игры:',
                       '1 - лёгкий',
                       '2 - средний',
                       '3 - сложный']
        font = pygame.font.SysFont("courier new", 25, True)
        text_coord = 230
        for line in level_title:
            string_rendered = font.render(line, True, pygame.Color('black'))
            level_rect = string_rendered.get_rect()
            text_coord += 8
            level_rect.top = text_coord
            level_rect.x = 240
            text_coord += level_rect.height
            self.game_display.blit(string_rendered, level_rect)
        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        return self.start_screen()

                    if event.key == pygame.K_1:
                        self.increase_speed = 0.2

                    elif event.key == pygame.K_2:
                        self.increase_speed = 0.4

                    elif event.key == pygame.K_3:
                        self.increase_speed = 0.6

                if self.increase_speed:
                    return self.run_ship()  # начинаем игру

            pygame.display.flip()

    def display_about_menu(self):
        """окно с правилами игры"""
        about_text = ["Правила игры:",
                      "1. Корабль управляется стрелками влево-вправо.",
                      "2. Не врезайтесь в стены!",
                      "3. Избегайте столкновений с движущимися метеоритами.",
                      "4. Очки начисляются при движении корабля по туннелю.",
                      "5. Собирайте полезные предметы, они добавляют очки:",
                      "   - капля масла добавляет 20 очков;",
                      "   - банка консервов добавляет 30 очков;",
                      "   - ценный метеорит для НИИ 'Парсек' - 50 очков;",
                      f"6. Цель - набрать {self.final_score} очков.",
                      f"7. Рекорд - {self.high_score} очков.",
                      "Нажмите ESC для возврата на стартовый экран."]

        fon = pygame.image.load('./img/about_fon.jpg')
        self.game_display.blit(fon, (0, 0))
        font = pygame.font.SysFont("courier new", 22, True)
        text_coord = 100

        for line in about_text:
            string_rendered = font.render(line, True, pygame.Color('white'))
            about_rect = string_rendered.get_rect()
            text_coord += 8
            about_rect.top = text_coord
            about_rect.x = 60
            text_coord += about_rect.height
            self.game_display.blit(string_rendered, about_rect)

        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_ESCAPE:
                        return self.start_screen()

            pygame.display.flip()

    def run_ship(self):
        """движение корабля, основное окно игры"""
        while not self.crashed or not self.final:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    sys.exit()

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_LEFT:
                        self.ship_m_left = True

                    if event.key == pygame.K_RIGHT:
                        self.ship_m_right = True

                elif event.type == pygame.KEYUP:

                    if event.key == pygame.K_LEFT:
                        self.ship_m_left = False

                    if event.key == pygame.K_RIGHT:
                        self.ship_m_right = False

            self.update_ship()
            self.game_display.fill(self.black)
            self.background_tunnel()

            self.run_oil()
            self.run_food()
            self.run_stone()
            self.run_meteorite()

            self.meteorite_start_y += self.meteorite_speed
            self.oil_start_y += self.oil_speed
            self.food_start_y += self.food_speed
            self.stone_start_y += self.stone_speed

            if self.meteorite_start_y > self.display_height:
                self.meteorite_start_y = 0 - self.meteorite_height
                self.meteorite_start_x = random.randint(0, 31) * 10 + 220

            if self.oil_start_y > self.display_height:
                self.oil_start_y = 0 - self.oil_height
                self.oil_start_x = random.randint(0, 31) * 10 + 220

            if self.food_start_y > self.display_height:
                self.food_start_y = 0 - self.food_height
                self.food_start_x = random.randint(0, 31) * 10 + 220

            if self.stone_start_y > self.display_height:
                self.stone_start_y = 0 - self.stone_height
                self.stone_start_x = random.randint(0, 31) * 10 + 220

            self.ship()
            self.count += 0.05
            self.time_count += 1

            if self.time_count % 100 == 0:
                self.meteorite_speed += self.increase_speed

            self.check_collisions()

            self.set_score()

            if self.count >= self.final_score:
                self.final = True
                self.final_screen()

            pygame.display.update()
            self.clock.tick(60)

    def background_tunnel(self):
        """движение и отрисовка туннеля"""
        self.game_display.blit(self.bg_img, (self.bg_x1, self.bg_y1))
        self.game_display.blit(self.bg_img, (self.bg_x2, self.bg_y2))

        self.bg_y1 += self.bg_speed
        self.bg_y2 += self.bg_speed

        if self.bg_y1 >= self.display_height:
            self.bg_y1 = -600

        if self.bg_y2 >= self.display_height:
            self.bg_y2 = -600

    def run_meteorite(self):
        """отрисовка метеорита"""
        self.game_display.blit(self.meteorite_sprite.image, (self.meteorite_start_x, self.meteorite_start_y))

    def run_oil(self):
        """отрисовка капли масла"""
        self.game_display.blit(self.oil_sprite.image, (self.oil_start_x, self.oil_start_y))

    def run_food(self):
        """отрисовка банки тушёнки"""
        self.game_display.blit(self.food_sprite.image, (self.food_start_x, self.food_start_y))

    def run_stone(self):
        """отрисовка ценного камня"""
        self.game_display.blit(self.stone_sprite.image, (self.stone_start_x, self.stone_start_y))

    def set_score(self):
        """установка счёта игры, установка рекорда, запись в файл, отрисовка на экране"""
        if self.count > self.high_score:
            self.high_score = int(self.count)
            with open('high_score.txt', 'w') as f:
                if self.high_score > self.final_score:
                    f.write(str(self.final_score))
                else:
                    f.write(str(self.high_score))

        font = pygame.font.SysFont("courier new", 20)
        text = font.render("Счёт: " + str(int(self.count)), True, self.white)
        self.game_display.blit(text, (10, 10))
        text = font.render("Рекорд: " + str(self.high_score), True, self.white)
        self.game_display.blit(text, (10, 40))

    def ship(self):
        """движение и отрисовка корабля"""
        self.index += 1

        if self.index >= len(self.ship_images):
            self.index = 0

        self.ship_sprite = pygame.sprite.Sprite()
        self.ship_sprite.image = self.ship_images[self.index]

        self.game_display.blit(self.ship_sprite.image, (self.ship_x_coordinate, self.ship_y_coordinate))

    def update_ship(self):
        """обновление корабля"""
        if self.ship_m_right:
            self.ship_x_coordinate += 5

        if self.ship_m_left:
            self.ship_x_coordinate -= 5

    def check_collisions(self):
        """проверка взаимодействий с другими объектами (коллизий)"""
        self.ship_sprite.rect = self.ship_sprite.image.get_rect(topleft=(self.ship_x_coordinate,
                                                                         self.ship_y_coordinate))
        self.ship_sprite_mask = pygame.mask.from_surface(self.ship_sprite.image)
        self.meteorite_sprite.rect = self.meteorite_sprite.image.get_rect(topleft=(self.meteorite_start_x,
                                                                                   self.meteorite_start_y))
        self.meteorite_sprite_mask = pygame.mask.from_surface(self.meteorite_sprite.image)

        self.oil_sprite.rect = self.oil_sprite.image.get_rect(topleft=(self.oil_start_x, self.oil_start_y))
        self.oil_sprite_mask = pygame.mask.from_surface(self.oil_sprite.image)

        self.food_sprite_mask = pygame.mask.from_surface(self.food_sprite.image)
        self.food_sprite.rect = self.food_sprite.image.get_rect(topleft=(self.food_start_x, self.food_start_y))

        self.food_sprite_mask = pygame.mask.from_surface(self.food_sprite.image)
        self.food_sprite.rect = self.food_sprite.image.get_rect(topleft=(self.food_start_x, self.food_start_y))

        self.stone_sprite_mask = pygame.mask.from_surface(self.stone_sprite.image)
        self.stone_sprite.rect = self.stone_sprite.image.get_rect(topleft=(self.stone_start_x, self.stone_start_y))

        ship_collide = pygame.sprite.collide_mask(self.meteorite_sprite, self.ship_sprite)
        oil_collide = pygame.sprite.collide_mask(self.ship_sprite, self.oil_sprite)
        food_collide = pygame.sprite.collide_mask(self.ship_sprite, self.food_sprite)
        stone_collide = pygame.sprite.collide_mask(self.ship_sprite, self.stone_sprite)

        if ship_collide or self.ship_x_coordinate < 210 or self.ship_x_coordinate > 500:
            self.crashed = True
            self.display_crash()
            self.display_message()
            self.restart_game()

        if oil_collide:
            self.get_oil()

        if food_collide:
            self.get_food()

        if stone_collide:
            self.get_stone()

    def get_oil(self):
        """взятие капли масла"""
        self.count += 20
        self.oil_start_y = random.randrange(-800, -200, 10)
        s = pygame.mixer.Sound("sounds/get_oil.mp3")
        s.play()

    def get_food(self):
        """взятие банки консервов"""
        self.count += 30
        self.food_start_y = random.randrange(-800, -200, 10)
        s = pygame.mixer.Sound("sounds/food.mp3")
        s.play()

    def get_stone(self):
        """взятие ценного камня"""
        self.count += 50
        self.stone_start_y = random.randrange(-1200, -800, 10)
        s = pygame.mixer.Sound("sounds/stone.mp3")
        s.play()

    def display_message(self):
        """показ сообщения при столкновении с метеоритом или со стеной туннеля"""
        phrases = [
            'Игра окончена, профессор Чащарский!',
            'Герман Борисович, мы врезались!',
            'Куда рулишь, Жишинников?',
            'Шерстюк, спасай шотландки!',
            'Ядвига, на борту раненые!',
            'Цирк закрылся, Хаврон!',
            'Допрыгались, золотоискатели!',
            'Жупов, нам нужна помощь!',
            'Куда ты нас завёл, Мозг?',
            'Юлий, поиски Бога придётся отложить!',
            'Нюхолай, спасайся!',
            'Эх, не долетели до Леонида!',
            'Где же ты, планета Колобок?',
            'Скарабей, приключения закончились...'
        ]

        msg = random.choice(phrases)
        font = pygame.font.SysFont("courier new", 30, True)
        text = font.render(msg, True, (255, 255, 255))
        self.game_display.blit(text, (400 - text.get_width() // 2, 240 - text.get_height() // 2))

    def display_crash(self):
        """отрисовка столкновения"""
        self.crash_img = pygame.image.load('./img/smoke.png')
        self.game_display.blit(self.crash_img, (self.ship_x_coordinate - 70, self.ship_y_coordinate - 150))
        self.ship_m_right = False
        self.ship_m_left = False
        s = pygame.mixer.Sound("sounds/crash.mp3")
        s.play()

    def restart_game(self):
        """перезагрузка после столкновения"""
        pygame.display.update()
        self.clock.tick(60)
        sleep(3)
        ship_flight.initialize()
        ship_flight.flight_window()

    def final_screen(self):
        """финальный экран игры"""
        fon = pygame.image.load('./img/final_fon.jpg')
        final_title = ['Вот и закончились',
                       'приключения «Скарабея»!',
                       'Хаврон остался на Пятачке,',
                       'Ядвига и Ряп - на Атите.',
                       'Остальная команда благополучно',
                       'вернулась в Иштым,а Юлий',
                       'завершил поиски Бога',
                       'и написал книгу!',
                       'Нажмите ESC для выхода']
        self.game_display.blit(fon, (0, 0))
        font = pygame.font.SysFont("courier new", 25, True)
        text_coord = 120
        for line in final_title:
            string_rendered = font.render(line, True, pygame.Color('white'))
            final_rect = string_rendered.get_rect()
            text_coord += 8
            final_rect.top = text_coord
            final_rect.x = 50
            text_coord += final_rect.height
            self.game_display.blit(string_rendered, final_rect)
        pygame.mixer.music.load("./sounds/symphony.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()


if __name__ == '__main__':
    ship_flight = ShipFlight()
    ship_flight.flight_window()
