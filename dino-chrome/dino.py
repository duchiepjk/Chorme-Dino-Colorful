import pygame, sys, random
from pygame.locals import *

WINDOWWIDTH = 600
WINDOWHEIGHT = 150
FPS = 60
GRAVITY = 0.75

SPEED_GROUND = 6
IMG_GROUND = pygame.image.load('./img/ground.png')

SPEED_SKY = 1
IMG_SKY = pygame.image.load('./img/sky.png')

IMG_TREX = pygame.image.load('./img/tRex.png')
TIME_CHANGE_TREX = 6
Y_TREX = 105
X_TREX = 50
HIGH_MIN = 90
SPEED_TREX = -12.5

IMG_CATUS = pygame.image.load('./img/cactus.png')
Y_CATUS = 100

BIRD_IMG = pygame.image.load('./img/bird.png')
TIME_CHANGE_BIRD = 10
Y_BIRD_1 = 110
Y_BIRD_2 = 80
Y_BIRD_3 = 50

IMG_HEART = pygame.image.load('./img/heart.png')
MIN_Y_HEART = 10  # Giá trị Y tối thiểu
MAX_Y_HEART = 100  # Giá trị Y tối đa


DISTANCE_MIN = 400
DISTANCE_MAX = 600

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(16) 
pygame.display.set_caption('T-REX')
FPSCLOCK = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

# Thêm các constant cho âm thanh
SOUND_JUMP = pygame.mixer.Sound('./sound/jump.wav')
SOUND_DIE = pygame.mixer.Sound('./sound/die.wav')
SOUND_HEART = pygame.mixer.Sound('./sound/heart.wav')
SOUND_SCORE = pygame.mixer.Sound('./sound/score.wav')
SOUND_HIGHSCORE = pygame.mixer.Sound('./sound/highscore.wav')

SOUND_JUMP.set_volume(0.5)
SOUND_DIE.set_volume(2)  
SOUND_HEART.set_volume(0.6) 
SOUND_HIGHSCORE.set_volume(0.3) 
SOUND_SCORE.set_volume(0.1) 
class T_Rex():
    def __init__(self, option=3):
        self.x = X_TREX
        self.y = Y_TREX
        self.speed = 0
        self.img = IMG_TREX
        self.option = option
        self.surface = pygame.Surface((55, 43), pygame.SRCALPHA)
        self.surface.blit(self.img, (0, 0), (80, 0, 40, 43))
        self.timeChange = 0
        self.jumping = False
        self.lowering = False
        self.invincible_time = 0 
        self.blinking = False
        self.blink_count = 0
        self.blink_duration = 10  # Thời gian mỗi lần nháy (in frames)
        self.total_blinks = 3  # Tổng số lần nháy (2 lần on, 2 lần off)
        
        # New attributes to capture state
        self.captured_image = None
        self.captured_position = (self.x, self.y)

    def capture_state(self):
        """Capture the current image and position of the T-Rex."""
        self.captured_image = self.surface.copy()
        self.captured_position = (self.x, self.y)

    def update(self, up, down):
        self.surface.fill((0, 0, 0, 0))
        # Remove the frozen logic
        if not self.jumping:
            if up:
                self.jumping = True
                self.speed = SPEED_TREX
                SOUND_JUMP.play()
            elif down:
                self.lowering = True
                if self.timeChange <= TIME_CHANGE_TREX:
                    self.option = 4
                else:
                    self.option = 5
                self.timeChange += 1
                if self.timeChange > TIME_CHANGE_TREX * 2:
                    self.timeChange = 0
            else:
                if self.timeChange <= TIME_CHANGE_TREX:
                    self.option = 0
                else:
                    self.option = 1
                self.timeChange += 1
                if self.timeChange > TIME_CHANGE_TREX * 2:
                    self.timeChange = 0
        elif self.jumping:
            self.option = 2

            if self.y <= Y_TREX - HIGH_MIN and self.speed < 0 and (not up):
                self.speed = 0
            self.y += int(self.speed + GRAVITY / 2)
            self.speed += GRAVITY

            if self.y >= Y_TREX:
                self.jumping = False
                self.y = Y_TREX

        # Blitting based on the option
        if self.option == 0:
            self.surface.blit(self.img, (0, 0), (0, 0, 40, 43))
        elif self.option == 1:
            self.surface.blit(self.img, (0, 0), (40, 0, 40, 43))
        elif self.option == 2:
            self.surface.blit(self.img, (0, 0), (80, 0, 40, 43))
        elif self.option == 3:
            self.surface.blit(self.img, (0, 0), (120, 0, 40, 43))
        elif self.option == 4:
            self.surface.blit(self.img, (0, 0), (160, 0, 55, 43))
        elif self.option == 5:
            self.surface.blit(self.img, (0, 0), (215, 0, 55, 43))

        if self.invincible_time > 0:
            self.invincible_time -= 1

        if self.blinking:
            self.blink_count += 1
            if self.blink_count >= self.total_blinks * self.blink_duration:
                self.blinking = False
                self.blink_count = 0

    def draw(self, captured=False):
        if captured and self.captured_image:
            DISPLAYSURF.blit(self.captured_image, self.captured_position)
        else:
            if self.blinking and (self.blink_count // self.blink_duration) % 2 == 0:
                # Không vẽ T-Rex trong nửa thời gian nháy
                return
            DISPLAYSURF.blit(self.surface, (self.x, self.y))

    def start_blinking(self):
        self.blinking = True
        self.blink_count = 0


class Life():
    def __init__(self, lives=3):
        self.lives = lives
        self.img = IMG_HEART
        self.size = 20
        self.surface = pygame.transform.scale(self.img, (self.size, self.size))

    def lose_life(self):
        if self.lives > 0:
            self.lives -= 1
        if self.lives == 0:
            SOUND_DIE.play()

    def add_life(self):
        if self.lives < 3:
            self.lives += 1
            return True
        return False

    def play_heart_sound(self):
        SOUND_HEART.play()

    def reset_lives(self, new_lives=3):
        self.lives = new_lives

    def draw(self):
        for i in range(self.lives):
            DISPLAYSURF.blit(self.surface, (10 + i * (self.size + 5), 10))
class Heart():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = IMG_HEART  # Tải hình ảnh trái tim

        # Giả sử kích thước trái tim là 20x20, có thể điều chỉnh theo kích thước thực tế
        self.width = 20  # Chiều rộng của trái tim
        self.height = 20  # Chiều cao của trái tim
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)  # Tạo hình chữ nhật cho trái tim

        # Nếu cần thiết, có thể thu nhỏ kích thước
        self.img = pygame.transform.scale(self.img, (self.width, self.height))  # Đặt kích thước trái tim

    def update(self, speed):
        self.x -= int(speed)
        self.rect.x = self.x  # Cập nhật vị trí của rect

    def draw(self):
        DISPLAYSURF.blit(self.img, (self.x, self.y))  # Vẽ hình ảnh trái tim lên màn hình


class Catus():
    def __init__(self, x, y, option):
        self.x = x
        self.y = y
        self.option = option
        self.img = IMG_CATUS
        self.rect = [0, 0, 0, 0]
        if option == 0:
            self.rect = [0, 0, 23, 46]
        elif option == 1:
            self.rect = [0, 0, 47, 46]
        elif option == 2:
            self.rect = [100, 0, 49, 46]
        elif option == 3:
            self.rect = [100, 0, 49, 46]
        elif option == 4:
            self.rect = [25, 0, 73, 46]
        self.surface = pygame.Surface((self.rect[2], self.rect[3]), pygame.SRCALPHA)
        self.surface.blit(self.img, (0, 0), self.rect)

    
    def update(self, speed):
        self.x -= int(speed)
    
    def draw(self):
        DISPLAYSURF.blit(self.surface, (self.x, self.y))

class Bird():
    def __init__(self, x, y, option = 0):
        self.x = x
        self.y = y
        self.option = option
        self.surface = pygame.Surface((42, 36), pygame.SRCALPHA)
        self.timeChange = 0
        self.img = pygame.image.load('./img/bird.png')
    
    def update(self, speed):
        self.surface.fill((0, 0, 0, 0))

        self.x -= int(speed)

        if self.timeChange <= TIME_CHANGE_BIRD:
            self.option = 0
        else:
            self.option = 1
        self.timeChange += 1
        if self.timeChange > TIME_CHANGE_BIRD * 2:
            self.timeChange = 0
        
        if self.option == 0:
            self.surface.blit(self.img, (0, 0), (0, 0, 42, 36))
        elif self.option == 1:
            self.surface.blit(self.img, (0, 0), (42, 0, 42, 36))
    
    def draw(self):
        DISPLAYSURF.blit(self.surface, (self.x, self.y))

class ListCatusAndBirds():
    def __init__(self):
        self.list = [] 
        self.hearts = []  # Danh sách trái tim
        for i in range(0, 3):
            self.list.append(Catus(500 + WINDOWWIDTH + random.randint(DISTANCE_MIN, DISTANCE_MAX)*i, Y_CATUS, random.randint(0, 3)))
        self.speed = SPEED_GROUND

    def update(self, score):
        self.speed = SPEED_GROUND * (1 + score/500)
        if self.speed > SPEED_GROUND * 2:
            self.speed = SPEED_GROUND * 2
        
        # Cập nhật vị trí của các vật cản
        for i in range(len(self.list)):
            self.list[i].update(self.speed)

        # Cập nhật vị trí của các trái tim
        for heart in self.hearts:
            heart.update(self.speed)  # Cập nhật vị trí trái tim

        # Tạo trái tim với xác suất ngẫu nhiên
        if random.randint(0, 1000) < 5:  # Xác suất ngẫu nhiên xuất hiện trái tim
            random_y = random.randint(MIN_Y_HEART, MAX_Y_HEART)  # Chọn ngẫu nhiên vị trí Y trong khoảng
            self.hearts.append(Heart(WINDOWWIDTH + random.randint(50, 200), random_y))
        
        # Loại bỏ trái tim đã đi qua khỏi màn hình
        self.hearts = [heart for heart in self.hearts if heart.x > -50]
        
        # Xóa và thêm vật cản mới nếu vật cản cũ đã ra khỏi màn hình
        if self.list[0].x < -132:
            self.list.pop(0)
            if self.speed > SPEED_GROUND * 1.5:
                rand = random.randint(0, 5)
                if rand == 5:
                    self.list.append(Bird(self.list[1].x + random.randint(DISTANCE_MIN + 200, DISTANCE_MAX + 100), random.choice((Y_BIRD_1, Y_BIRD_2, Y_BIRD_3))))
                else:
                    self.list.append(Catus(self.list[1].x + random.randint(DISTANCE_MIN + 100, DISTANCE_MAX + 100), Y_CATUS, random.randint(0, 4)))
            else:
                self.list.append(Catus(self.list[1].x + random.randint(DISTANCE_MIN, DISTANCE_MAX), Y_CATUS, random.randint(0, 3)))


                
    def draw(self):
        for i in range(len(self.list)):
            self.list[i].draw()
        for heart in self.hearts:  # Vẽ trái tim
            heart.draw()
    


class Ground():
    def __init__(self):
        self.x = 0
        self.y = 138
        self.img = IMG_GROUND
        self.speed = SPEED_GROUND
    
    def update(self, score):
        self.speed = SPEED_GROUND * (1 + score/500)
        if self.speed > SPEED_GROUND * 2:
            self.speed = SPEED_GROUND * 2
        self.x -= int(self.speed)
        if self.x <= -600:
            self.x += 600
    
    def draw(self):
        DISPLAYSURF.blit(self.img, (self.x, self.y))


class Sky():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = SPEED_SKY
        self.img = IMG_SKY
    
    def update(self, score):
        self.speed = SPEED_SKY * (1 + score/500)
        if self.speed > SPEED_SKY * 2:
            self.speed = SPEED_SKY * 2
        self.x -= int(self.speed)
        if self.x <= -600:
            self.x += 600
    
    def draw(self):
        DISPLAYSURF.blit(self.img, (self.x, self.y))


class Score():
    def __init__(self):
        self.score = 0
        self.highScore = 0
        self.textScore = ""
        self.textHighScore = ""
        self.size = 15
        self.last_milestone = 0
        self.new_high_score_reached = False
        self.first_game = True

    def update(self):
        current_score = int(self.score)
        
        # Kiểm tra cột mốc điểm
        if current_score % 100 == 0 and current_score != self.last_milestone:
            SOUND_SCORE.play()
            self.last_milestone = current_score
        
        # Kiểm tra điểm cao mới
        if current_score > self.highScore:
            if not self.new_high_score_reached and not self.first_game:
                SOUND_HIGHSCORE.play()
                self.new_high_score_reached = True
            self.highScore = current_score
        
        self.score += 0.15

        self.textScore = str(current_score).zfill(5)
        self.textHighScore = "HI: " + str(self.highScore).zfill(5)

    def reset(self):
        self.score = 0
        self.new_high_score_reached = False
        self.last_milestone = 0
        if self.first_game:
            self.first_game = False

    def draw(self):
        fontObj = pygame.font.SysFont('consolas', self.size)

        textSurfaceScore = fontObj.render(self.textScore, True, (0, 0, 0))
        DISPLAYSURF.blit(textSurfaceScore, (550, 10))

        textSurfaceHighScore = fontObj.render(self.textHighScore, True, (60, 60, 60))
        DISPLAYSURF.blit(textSurfaceHighScore, (450, 10))

class BlinkText():
    def __init__(self, text):
        self.text = text
        self.timeChange = 0
        self.size = 14
        fontObj = pygame.font.SysFont('consolas', self.size)
        textSurface = fontObj.render(self.text, False, (0, 0, 0))
        self.surface = pygame.Surface(textSurface.get_size()) 
        self.surface.fill((255, 255, 255))
        self.surface.blit(textSurface, (0, 0))
        self.surface.set_colorkey((255, 255, 255))
        self.alpha = 255
    def update(self):
        self.alpha = abs(int(255 - self.timeChange))
        if self.timeChange > 255*2:
            self.timeChange = 0
        self.timeChange += 5

    def draw(self): 
        self.surface.set_alpha(self.alpha)
        DISPLAYSURF.blit(self.surface, (int(WINDOWWIDTH/2 - self.surface.get_width()/2), 100))

def isCollisionWithHeart(tRex, heart):
    tRex_rect = pygame.Rect(tRex.x, tRex.y, tRex.surface.get_width(), tRex.surface.get_height())
    heart_rect = pygame.Rect(heart.x, heart.y, heart.rect[2], heart.rect[3])
    return tRex_rect.colliderect(heart_rect)



def isCollisionWithObstacle(tRex, obstacle):
    """Check if T-Rex collides with a Cactus or Bird."""
    tRexMask = pygame.mask.from_surface(tRex.surface)
    obstacleMask = pygame.mask.from_surface(obstacle.surface)
    result = tRexMask.overlap(obstacleMask, (obstacle.x - tRex.x, obstacle.y - tRex.y))
    if result:
        return True
    return False



def main():
    pygame.mixer.init()
    sky = Sky()
    ground = Ground()
    tRex = T_Rex(0)
    up = False
    down = False
    ls = ListCatusAndBirds()
    score = Score()
    blinkText = BlinkText("Space or Up Arrow to Play, Esc to Exit")
    life = Life(3)
    game_state = "START"

    # Variables to store captured T-Rex state
    captured_trex_image = None
    captured_trex_position = (X_TREX, Y_TREX)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    if game_state == "START":
                        game_state = "PLAYING"
                    elif game_state == "GAME_OVER":
                        # Reset the game
                        game_state = "START"
                        score.reset()
                        life.reset_lives()
                        ls = ListCatusAndBirds()
                        tRex = T_Rex(0)
                        sky = Sky()
                        ground = Ground()
                        # Reset captured state
                        captured_trex_image = None
                        captured_trex_position = (X_TREX, Y_TREX)
                    up = True
                elif event.key == pygame.K_DOWN:
                    down = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    up = False
                elif event.key == pygame.K_DOWN:
                    down = False

        # Cập nhật và vẽ nền chỉ khi đang chơi
        if game_state == "PLAYING":
            sky.update(score.score)
            ground.update(score.score)

        # Vẽ nền cho tất cả các trạng thái
        sky.draw()
        ground.draw()

        if game_state == "START":
            # Hiển thị màn hình bắt đầu tĩnh
            tRex.draw()
            life.draw()
            blinkText.update()
            blinkText.draw()
        elif game_state == "PLAYING":
            # Cập nhật và vẽ các đối tượng trò chơi
            tRex.update(up, down)
            ls.update(score.score)
            score.update()

            # Kiểm tra va chạm với trái tim
            for heart in ls.hearts[:]:
                if isCollisionWithHeart(tRex, heart):
                    life.play_heart_sound()
                    life.add_life()
                    ls.hearts.remove(heart)

            # Kiểm tra va chạm với chướng ngại vật
            for obstacle in ls.list:
                if tRex.invincible_time == 0 and isCollisionWithObstacle(tRex, obstacle):
                    life.lose_life()
                    tRex.invincible_time = 60
                    tRex.start_blinking()
                    if life.lives == 0:
                        game_state = "GAME_OVER"
                        # Capture T-Rex's current state
                        tRex.capture_state()
                        captured_trex_image = tRex.captured_image
                        captured_trex_position = tRex.captured_position

            # Vẽ các đối tượng trò chơi
            ls.draw()
            tRex.draw()
            score.draw()
            life.draw()
        elif game_state == "GAME_OVER":
            # Vẽ các đối tượng trò chơi nhưng sử dụng captured T-Rex
            ls.draw()
            if captured_trex_image:
                DISPLAYSURF.blit(captured_trex_image, captured_trex_position)
            else:
                tRex.draw()
            score.draw()
            blinkText.update()
            blinkText.draw()

            gameOverFontObj = pygame.font.SysFont('consolas', 30, bold=1)
            gameOverTextSurface = gameOverFontObj.render("GAME OVER", True, (0, 0, 0))
            DISPLAYSURF.blit(
                gameOverTextSurface,
                (
                    int(WINDOWWIDTH / 2 - gameOverTextSurface.get_width() / 2),
                    50
                )
            )

        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()