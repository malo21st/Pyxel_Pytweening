import pyxel
import pytweening as tween

WIDTH, HEIGHT = 160, 120 
FPS = 60 # frame / sec
DURATION = 1 # sec
FRAMES = FPS * DURATION # frame: 弾丸のフレーム数
# 弾丸のイージング
EASE_FUNC_L = tween.iterLinear # 等速
EASE_FUNC_R = tween.iterEaseOutQuad # 減速系
# 飛行体の1フレームあたりの移動量
SPEED = 2

class Bullet:
    def __init__(self, ease_func, start_pos, end_pos, frames=FRAMES):
        self.start_x, self.start_y = start_pos
        self.end_x, self.end_y = end_pos
        self.frames = frames
        interval_size = 1.0 / max(1, frames)
        self.iterator = ease_func(self.start_x, self.start_y, self.end_x, self.end_y, interval_size)
        self.current = next(self.iterator, None)

    def update(self):
        self.current = next(self.iterator, None)

    def draw(self):
        if self.current is None:
            return
        pyxel.pset(self.current[0], self.current[1], 10)

    def is_finished(self):
        return self.current[1] < 0 # Y座標マイナスならTrue（表示終了）


class App:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, title="easeing bullets demo", fps=FPS)
        self.x = WIDTH // 2 
        self.y = HEIGHT - 20
        self.size = 20
        self.half_size = self.size // 2
        self.objects = []
        pyxel.run(self.update, self.draw)

    def update(self):
        # 弾丸
        if pyxel.btnp(pyxel.KEY_SPACE, 30, 2): # 30フレーム押し続けたら連射モード
            start_pos_L = (self.x - 7, self.y)
            end_pos_L = (self.x - 7, -1)
            self.objects.append(
                Bullet(EASE_FUNC_L, start_pos_L, end_pos_L)
            )
            start_pos_R = (self.x + 7, self.y)
            end_pos_R = (self.x + 7, -1)
            self.objects.append(
                Bullet(EASE_FUNC_R, start_pos_R, end_pos_R)
            )
        ## 弾丸オブジェクトのアップデートと枠外弾丸は削除（メモリ開放）
        for obj in self.objects[:]:
            obj.update()
            if obj.is_finished():
                self.objects.remove(obj)

        # 飛行体
        left  = pyxel.btn(pyxel.KEY_LEFT)
        right = pyxel.btn(pyxel.KEY_RIGHT)
        if left and not right:
            self.x -= SPEED
        elif right and not left:
            self.x += SPEED
        self.x = max(self.half_size, min(WIDTH - self.half_size, self.x))

    def draw(self):
        pyxel.cls(0)
        # 弾丸
        for obj in self.objects:
            obj.draw()
        # 飛行体
        pyxel.rect(self.x - self.half_size, self.y, self.size, 5, 11)
        # UI表示
        pyxel.text(4, HEIGHT - 10, f"Left/Right: Move | Shot: Space   {len(self.objects):02d}", 7)

App()