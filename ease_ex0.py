import pyxel
import pytweening as tween

# Y軸イージングの順序リスト（クリックのたびに順番に適用）
EASINGS = [
    tween.easeInQuad, tween.easeOutQuad, tween.easeInOutQuad,
    tween.easeInCubic, tween.easeOutCubic, tween.easeInOutCubic,
    tween.easeInQuart, tween.easeOutQuart, tween.easeInOutQuart,
    tween.easeInQuint, tween.easeOutQuint, tween.easeInOutQuint,
    tween.easeInSine, tween.easeOutSine, tween.easeInOutSine,
    tween.easeInExpo, tween.easeOutExpo, tween.easeInOutExpo,
    tween.easeInCirc, tween.easeOutCirc, tween.easeInOutCirc,
    tween.easeInElastic, tween.easeOutElastic, tween.easeInOutElastic,
    tween.easeInBack, tween.easeOutBack, tween.easeInOutBack,
    tween.easeInBounce, tween.easeOutBounce, tween.easeInOutBounce,
    tween.easeInPoly, tween.easeOutPoly, tween.easeInOutPoly,
]

OFF_SET = 30

class MovingObject:
    def __init__(self, start_pos, end_pos, duration, easing_y):
        self.start_x, self.start_y = start_pos
        self.end_x, self.end_y = end_pos
        self.duration = duration
        self.frame_count = 0
        self.easing_y = easing_y

    def update(self):
        self.frame_count += 1

    def draw(self):
        progress = self.frame_count / self.duration
        # Xはリニア
        eased_x = progress
        # Yは指定イージング
        eased_y = self.easing_y(progress)

        x = int(self.start_x + (self.end_x - self.start_x) * eased_x)
        y = int(self.start_y + (self.end_y - self.start_y) * eased_y)
        pyxel.circ(x, y, 5, 8)

    def is_finished(self):
        return self.frame_count >= self.duration


class App:
    def __init__(self):
        pyxel.init(160, 120, title="Y easing (list order) & X linear, BL->TR", fps=60)
        self.objects = []
        self.next_ease_idx = 0       # 次に使うイージングのインデックス
        self.current_ease_idx = None # 現在実行中のイージング番号
        self.clicked_once = False    # クリック済みかどうか
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            # 左下→右上
            start_pos = (OFF_SET, pyxel.height - OFF_SET)
            end_pos = (pyxel.width - OFF_SET, OFF_SET)

            easing_y = EASINGS[self.next_ease_idx]
            self.current_ease_idx = self.next_ease_idx  # 実行中の番号を記録
            self.next_ease_idx = (self.next_ease_idx + 1) % len(EASINGS)

            self.objects.append(
                MovingObject(
                    start_pos=start_pos,
                    end_pos=end_pos,
                    duration=120,
                    easing_y=easing_y,
                )
            )
            self.clicked_once = True

        for obj in self.objects[:]:
            obj.update()
            if obj.is_finished():
                self.objects.remove(obj)

    def draw(self):
        pyxel.cls(0)  # 最初は真っ黒
        # クリック後のみ現在のイージング名を表示
        if self.clicked_once and self.current_ease_idx is not None:
            pyxel.text(
                5, 5,
                f"{self.current_ease_idx + 1:02d}: {EASINGS[self.current_ease_idx].__name__}",
                7
            )
        pyxel.rectb(OFF_SET, OFF_SET, pyxel.width - OFF_SET * 2, pyxel.height - OFF_SET * 2, 7)
        for obj in self.objects:
            obj.draw()

App()