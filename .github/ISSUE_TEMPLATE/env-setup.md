---
name: 環境構築 (Phase0)
about: Windows 開発環境を整えて PoC を動かせる状態にするタスク
labels: setup, phase0
assignees: ''
---

## 概要
Windows PC に必要なソフトをインストールし、README の「セットアップ手順」に従って実行できることを確認する。

## 目的
- Python 3.10+、ffmpeg、adb をインストールする
- 仮想環境で `backend` を起動できること
- `scripts/pull_recordings.ps1` が実行できること（adb 接続確認含む）

## チェックリスト
- [ ] Python 3.10+ をインストール済み
- [ ] ffmpeg が PATH に追加されている
- [ ] adb (Android Platform Tools) が動作する（`adb devices` が表示される）
- [ ] Git が使える
- [ ] `python -m venv .venv` → `.\\.venv\\Scripts\\activate` → `pip install -r backend/requirements.txt` が完了する
- [ ] `uvicorn backend.app.main:app --host 0.0.0.0 --port 8000` で API が立ち上がる
- [ ] README に Windows 向け手順が記載されている

## テスト手順（受け入れ）
1. `uvicorn` を起動し、`http://<PC_IP>:8000/api/health` にアクセスして `{"status":"ok"}` が返ること
2. 実行ログのスクリーンショットを添付すること
