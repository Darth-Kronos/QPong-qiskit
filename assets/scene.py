import pygame

from assets.circuit_grid import CircuitGrid, CircuitGridModel
from assets import globals, ui, paddle, ball, computer, resources

class Scene:
    def __init__(self) -> None:
        pass
    def update(self, sm):
        pass
    def draw(self, sm, screen):
        pass

class SceneManager:
    def __init__(self) -> None:
        self.scenes = []
        self.exit = False
    def update(self):
        if len(self.scenes) > 0:
            self.scenes[-1].update(self)
    def draw(self, screen):
        screen.fill(globals.BLACK)
        if len(self.scenes) > 0:
            self.scenes[-1].draw(self, screen)
        pygame.display.flip()
    def push(self, scene):
        self.scenes.append(scene)

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 750
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)
WIDTH_UNIT = round(WINDOW_WIDTH / 100)

CIRCUIT_DEPTH = 18

class GameScene(Scene):
    def __init__(self) -> None:
        super().__init__()
        self._circuit_depth = (
            CIRCUIT_DEPTH // 2
        )
        
        
        self._circuit_grid_model_1 = CircuitGridModel(3, self._circuit_depth)
        self._circuit_grid_model_2 = CircuitGridModel(3, self._circuit_depth)
        self.circuit_grid_1 = CircuitGrid(
                1.45 * WIDTH_UNIT,
                round(WINDOW_HEIGHT * 0.7),
                self._circuit_grid_model_1,
                2,
            )
        self.circuit_grid_2 = CircuitGrid(
                WINDOW_WIDTH // 2 ,
                round(WINDOW_HEIGHT * 0.7),
                self._circuit_grid_model_2,
                2,
            )
        
        # self.classical_paddle = paddle.Paddle(9*globals.WIDTH_UNIT)
        # self.classical_computer = computer.ClassicalComputer(self.classical_paddle)
        self.quantum_paddles_1 = paddle.QuantumPaddles(11*globals.WIDTH_UNIT)
        self.quantum_computer_1 = computer.QuantumComputer(self.quantum_paddles_1, self.circuit_grid_1)

        self.quantum_paddles_2 = paddle.QuantumPaddles(globals.WINDOW_WIDTH - 9*globals.WIDTH_UNIT)
        self.quantum_computer_2 = computer.QuantumComputer(self.quantum_paddles_2, self.circuit_grid_2)

        self.pong_ball = ball.Ball()
        self.moving_sprites = pygame.sprite.Group()
        self.moving_sprites.add(self.quantum_paddles_1.paddles)
        self.moving_sprites.add(self.quantum_paddles_2.paddles)
        self.moving_sprites.add(self.pong_ball)
    
    def update(self, sm):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sm.exit = True
            elif event.type == pygame.KEYDOWN:
                if event.type == pygame.K_h:
                    self.circuit_grid_1.handle_input_h(event.key)

        self.pong_ball.update(self.quantum_computer_1, self.quantum_computer_2)
        # self.classical_computer.update(self.pong_ball)

        self.quantum_computer_1.update(self.pong_ball)
        self.quantum_computer_2.update(self.pong_ball)

        if self.quantum_computer_1.score >= globals.WIN_SCORE:
            sm.push(WinScene(player=1))
        elif self.quantum_computer_1.score >= globals.WIN_SCORE:
            sm.push(WinScene(player=2))

    def draw(self, sm, screen):
        self.circuit_grid_1.draw(screen)
        self.circuit_grid_2.draw(screen)
        ui.draw_statevector_grid(screen)
        ui.draw_score(screen, self.quantum_computer_1.score, self.quantum_computer_2.score)
        ui.draw_dashed_line(screen)
        self.moving_sprites.draw(screen)

class LoseScene(Scene):
    def __init__(self) -> None:
        super().__init__()

    def update(self, sm):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sm.exit = True
            elif event.type == pygame.KEYDOWN:
                # press SPACE to reply
                if event.key == pygame.K_SPACE:
                    sm.push(GameScene())

    def draw(self, sm, screen):
        font = resources.Font()

        gameover_text = "Game Over"
        text = font.gameover_font.render(gameover_text, 1, globals.WHITE)
        text_pos = text.get_rect(center=(globals.WINDOW_WIDTH/2, globals.WIDTH_UNIT*10))
        screen.blit(text, text_pos)

        gameover_text = "Classical computer"
        text = font.replay_font.render(gameover_text, 5, globals.WHITE)
        text_pos = text.get_rect(center=(globals.WINDOW_WIDTH/2, globals.WIDTH_UNIT*22))
        screen.blit(text, text_pos)

        gameover_text = "still rules the world"
        text = font.replay_font.render(gameover_text, 5, globals.WHITE)
        text_pos = text.get_rect(center=(globals.WINDOW_WIDTH/2, globals.WIDTH_UNIT*27))
        screen.blit(text, text_pos)

class WinScene(Scene):
    def __init__(self, player) -> None:
        super().__init__()
        self.player = player

    def update(self, sm):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sm.exit = True
            elif event.type == pygame.KEYDOWN:
                # press SPACE to reply
                if event.key == pygame.K_SPACE:
                    sm.push(GameScene())

    def draw(self, sm, screen):
        font = resources.Font()
        if self.player == 1:
            gameover_text = "Congratulations Player 1!"
            text = font.gameover_font.render(gameover_text, 5, globals.WHITE)
            text_pos = text.get_rect(center=(globals.WINDOW_WIDTH/2, globals.WIDTH_UNIT*10))
            screen.blit(text, text_pos)

            gameover_text = "You demonstrated quantum advantage"
            text = font.replay_font.render(gameover_text, 5, globals.WHITE)
            text_pos = text.get_rect(center=(globals.WINDOW_WIDTH/2, globals.WIDTH_UNIT*22))
            screen.blit(text, text_pos)

            gameover_text = "for the first time in human history!"
            text = font.replay_font.render(gameover_text, 5, globals.WHITE)
            text_pos = text.get_rect(center=(globals.WINDOW_WIDTH/2, globals.WIDTH_UNIT*27))
            screen.blit(text, text_pos)
        else:
            gameover_text = "Congratulations Player 2!"
            text = font.gameover_font.render(gameover_text, 5, globals.WHITE)
            text_pos = text.get_rect(center=(globals.WINDOW_WIDTH/2, globals.WIDTH_UNIT*10))
            screen.blit(text, text_pos)

            gameover_text = "You demonstrated quantum advantage"
            text = font.replay_font.render(gameover_text, 5, globals.WHITE)
            text_pos = text.get_rect(center=(globals.WINDOW_WIDTH/2, globals.WIDTH_UNIT*22))
            screen.blit(text, text_pos)

            gameover_text = "for the first time in human history!"
            text = font.replay_font.render(gameover_text, 5, globals.WHITE)
            text_pos = text.get_rect(center=(globals.WINDOW_WIDTH/2, globals.WIDTH_UNIT*27))
            screen.blit(text, text_pos)