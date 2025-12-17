import pyxel
import pytweening as tween

class App:
    def __init__(self):
        pyxel.init(220, 100, title="EaseInQuad Bullet Demo", fps=30)
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):
        startX, startY = 10, 50
        endX, endY = 210, 50
        intervalSize = 1 / 60 # 

        # iterEaseInQuad で座標列を生成
        self.points = list(tween.iterEaseInQuad(startX, startY, endX, endY, intervalSize))
        self.frame = 0

    def update(self):
        # スペースキーでリセット
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.reset()

        # フレーム進行
        if self.frame < len(self.points) - 1:
            self.frame += 1

    def draw(self):
        pyxel.cls(0)
        x, y = self.points[self.frame]
        pyxel.circ(int(x), int(y), 4, 11)

        # UI表示
        pyxel.text(5, 5, "SPACE: Reset", 7)
        pyxel.text(5, 15, f"Frame: {self.frame}", 7)

App()