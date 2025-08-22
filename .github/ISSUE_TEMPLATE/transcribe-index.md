---
name: 文字起こし & 埋め込み登録 (Phase2-3)
about: Whisper で文字起こしし、sentence-transformers→Chroma に登録するタスク
labels: backend, phase2, phase3
assignees: ''
---

## 概要
アップロード済み音声ファイルを transcribe し、セグメント化 → 埋め込み生成 → Chroma に登録するワークフローを実装する。

## 要求仕様
- transcribe: `backend/app/services/transcribe.py` に実装（Whisper の利用）
- embed & index: `backend/app/services/embed_index.py` に実装（sentence-transformers + chromadb）
- メタデータ: 各セグメントに `source`, `start`, `end`, `file_name` を含める
- Chroma は `./chroma_db` に persist する

## チェックリスト
- [ ] `POST /api/ingest/audio` で音声を POST すると transcription と segments が作られる
- [ ] segments が Chroma に登録され、`./chroma_db` が作成される
- [ ] `POST /api/search` を使って検索結果が返る（少なくとも1ヒット）

## テスト手順（受け入れ）
1. サンプル音声を `POST /api/ingest/audio` で送付
2. レスポンスで `segments` 数が 1 以上であること
3. `POST /api/search` でキーワード検索を行い、ヒットが返ること
