---
name: 録音取り込み (Phase1)
about: Pixel から音声を取り込み、加工用フォルダに整理するタスク
labels: data, phase1
assignees: ''
---

## 概要
`scripts/pull_recordings.ps1` を使い、端末から `storage/raw/` に音声・テキスト・PDF を取り出す。取り出したデータを `scripts/normalize_and_metadata.py` で正規化する。

## チェックリスト
- [ ] USBデバッグが ON の Pixel に接続できること（adb devices）
- [ ] `.\scripts\pull_recordings.ps1` を実行して `storage/raw/` にファイルが保存される
- [ ] `python scripts/normalize_and_metadata.py` を実行して `storage/processed/` にファイルが整理され、`metadata.csv` が出力される
- [ ] 取り込んだサンプル音声ファイル（例: sample_short.m4a）を `storage/processed/audio/` に置いて動作確認できる

## テスト手順（受け入れ）
1. `storage/processed/metadata.csv` を確認し、最低1レコード存在すること
2. 取得した音声ファイルの再生確認ができるスクリーンショット or 簡単なログを添付
