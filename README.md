# Learn2Slither - Snake AI with Q-Learning

強化学習（Q-Learning）を用いて、ヘビが自動でリンゴを食べるAIを実装したプロジェクトです。

## 概要

このプロジェクトは、シンプルなスネークゲームの環境をPythonで構築し、Q-Learningエージェントが「視界（Vision）」のみを頼りにリンゴを追いかけ、壁や自分自身を避けるように学習します。

### ステート（状態）表現

ルールに基づき、エージェントは以下の情報のみを取得して判断を下します：

- 4方向（前、右、後、左）の直線視界情報
- 各方向で見えるオブジェクト（壁、緑リンゴ、赤リンゴ、自分自身の体）
- 各オブジェクトまでの距離

## インストール

Python 3.x がインストールされていることを確認してください。

```bash
pip install pygame
```

## 実行方法

### 1. 学習（トレーニング）

指定した回数（エピソード数）だけ学習を行い、モデルを保存します。

```bash
# 50,000回学習させる例
python main.py --episodes 50000 --save models/snake_model.json
```

### 2. テスト（可視化）

学習済みモデルを読み込み、GUIでヘビの動きを確認します。

```bash
python main.py --no-train --load models/snake_model.json --visual --episodes 5
```

## GUI 操作方法

テスト実行中（`--visual` 有効時）、以下のキー操作が可能です：

| キー | 操作内容 |
| :--- | :--- |
| **SPACE** | ゲームの一時停止 / 再開 |
| **S** | 1ステップ進む（一時停止中のみ） |
| **UP / DOWN** | 実行スピード（FPS）の調整 |

## デモ

学習済みAIの動作の様子です：

<video src="docs/demo.mov" controls title="Snake AI Demo" style="max-width: 100%"></video>

## プロジェクト構成

- `main.py`: エントリポイント（学習・実行の制御）
- `environment.py`: スネークゲームの環境ロジック
- `agent.py`: Q-Learningアルゴリズムの実装
- `gui.py`: Pygameによる描画処理
- `models/`: 学習済みモデルの保存先
