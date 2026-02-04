import argparse
from environment import SnakeEnv
from agent import QLearningAgent
from gui import SnakeGUI

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=int, default=1000, help="学習回数")
    parser.add_argument("--load", type=str, help="モデルの読み込みパス")
    parser.add_argument("--save", type=str, default="models/snake_model.json", help="モデルの保存パス")
    parser.add_argument("--visual", action="store_true", help="可視化の有効化")
    parser.add_argument("--no-train", action="store_false", dest="train", help="テストモード")
    args = parser.parse_args()

    env = SnakeEnv()
    agent = QLearningAgent()
    gui = SnakeGUI() if (not args.train and args.visual) else None

    if args.load:
        agent.load(args.load)

    max_steps = 500

    for episode in range(args.episodes):
        state = env.reset()
        total_reward = 0
        steps = 0

        while not env.done and steps < max_steps:
            action = agent.get_action(state, train=args.train, episode=episode)
            next_state, reward, done = env.step(action)

            if args.train:
                agent.learn(state, action, reward, next_state)

            state = next_state
            total_reward += reward
            steps += 1

            if gui:
                gui.render(env)
        if (episode + 1) % 100 == 0:
            if steps >= max_steps:
                print(f"Episode: {episode + 1}: Time out (reached {max_steps} steps)")
            else:
                print(f"Episode: {episode + 1}, Score: {env.score}, Total Reward: {total_reward}")

    if args.train:
        agent.save(args.save)
        print(f"Model saved to {args.save}")

if __name__ == "__main__":
    main()