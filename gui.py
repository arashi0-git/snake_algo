import pygame
import sys

class SnakeGUI:
    def __init__(self, size=10, cell_size=40):
        pygame.init()
        self.size = size
        self.cell_size = cell_size
        self.screen_size = size * cell_size
        self.screen = pygame.display.set_mode((self.screen_size, self.screen_size))
        pygame.display.set_caption("Learn2Slither")
        self.clock = pygame.time.Clock()
        self.fps = 10
        self.paused = False
        self.step_mode = False

    def render(self, env):
        self._handle_events()

        while self.paused and not self.step_mode:
            self._handle_events()
            self._draw_all(env)
            pygame.display.flip()
            self.clock.tick(60)

        self.step_mode = False

        self._draw_all(env)
        pygame.display.flip()
        self.clock.tick(self.fps)

    def _draw_all(self, env):
        self.screen.fill((0, 0, 0))
        for apple in env.green_apples:
            self._draw_cell(apple, (0, 255, 0))
        self._draw_cell(env.red_apple, (255, 0, 0))
        for i, pos in enumerate(env.snake):
            color = (0, 0, 255)
            self._draw_cell(pos, color)

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.fps = min(100, self.fps + 5)
                    print(f"Speed: {self.fps} FPS")
                if event.key == pygame.K_DOWN:
                    self.fps = max(1, self.fps - 5)
                    print(f"Speed: {self.fps} FPS")
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                    print("Paused" if self.paused else "Resumed")
                if event.key == pygame.K_s and self.paused:
                    self.step_mode = True
                    print("Step forward")

    def _draw_cell(self, pos, color):
        if pos is None: return
        y, x = pos
        rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
        pygame.draw.rect(self.screen, color, rect)