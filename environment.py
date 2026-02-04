import random

class SnakeEnv:
    def __init__(self, size=10):
        self.size = size
        self.reset()

    def reset(self):
        """
        ボードの初期化
        ヘビの初期位置(長さ3、ランダム配置)
        りんごの配置(緑2,赤1)
        """
        self.done = False
        self.score = 0

        self.snake = self._generate_random_snake(length=3)

        self.red_apple = None
        self.green_apples = []
        self._place_apple('G')
        self._place_apple('G')
        self._place_apple('R')

        return self.get_state()
    
    def _generate_random_snake(self, length):
        while True:
            head = (random.randint(0, self.size-1), random.randint(0, self.size-1))
            snake = [head]

            directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
            dir_y, dir_x = random.choice(directions)

            valid = True
            for i in range(1, length):
                next_port = (head[0] + dir_y * i, head[1] + dir_x * i)
                if 0 <= next_port[0] < self.size and 0 <= next_port[1] < self.size:
                    snake.append(next_port)
                else:
                    valid = False
                    break
            
            if valid:
                return snake

    def _place_apple(self, type):
        while True:
            pos = (random.randint(0, self.size-1), random.randint(0, self.size-1))
            if pos not in self.snake and pos not in self.green_apples and pos != self.red_apple:
                if type == 'G':
                    self.green_apples.append(pos)
                else:
                    self.red_apple = pos
                break

    def step(self, action):
        """
        action: 0:UP, 1:RIGHT, 2:DOWN, 3:LEFT
        1. ヘビの移動
        2. 衝突判定
        3. 報酬計算
        4. 状態の更新
        """
        head_y, head_x = self.snake[0]

        def get_min_dist(y, x):
            if not self.green_apples:
                return 0
            return min(abs(y - ay) + abs(x - ax) for ay, ax in self.green_apples)
        
        dist_before = get_min_dist(head_y, head_x)

        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        dy, dx = directions[action]
        new_head = (head_y + dy, head_x + dx)

        if (not (0 <= new_head[0] < self.size and 0 <= new_head[1] < self.size) or new_head in self.snake):
            self.done = True
            reward = -100
            return self.get_state(), reward, self.done

        self.snake.insert(0, new_head)

        if new_head in self.green_apples:
            reward = 50
            self.score += 1
            self.green_apples.remove(new_head)
            self._place_apple('G')
        elif new_head == self.red_apple:
            reward = -50
            self.snake.pop()
            if len(self.snake) > 0: self.snake.pop()
            if len(self.snake) == 0:
                self.done = True
                return self.get_state(), reward, self.done
            self._place_apple('R')
        else:
            self.snake.pop()

            dist_after = get_min_dist(new_head[0], new_head[1])
            if dist_after < dist_before:
                reward = 1
            else:
                reward = -1.5

        return self.get_state(), reward, self.done

    def get_state(self):
        """
        頭から4方向の全ての視界情報を取得
        各方向について、壁にあたるまでのマスの情報と距離をタプルで返す
        """
        if not self.snake:
            return ('W', 0, 'W', 0, 'W', 0, 'W', 0)

        head_y, head_x = self.snake[0]
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        vision = []
        for dy, dx in directions:
            item = '0'
            dist = 0
            curr_y, curr_x = head_y + dy, head_x + dx
            while 0 <= curr_y < self.size and 0 <= curr_x < self.size:
                dist += 1
                cell = self.get_cell_type(curr_y, curr_x)
                if cell != '0':
                    item = cell
                    break
                curr_y += dy
                curr_x += dx
            else:
                item = 'W'
                dist += 1

            vision.append(item)
            vision.append(dist)

        return tuple(vision)

    def get_cell_type(self, y, x):
        """指定された座標のせるの種類を返すメソッド"""
        if (y, x) in self.snake[1:]:
            return "S"

        if (y, x) in self.green_apples:
            return "G"

        if (y, x) == self.red_apple:
            return "R"

        return "0" 