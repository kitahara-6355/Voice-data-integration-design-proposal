# Local Run (Windows) — Docker が使えない場合の代替手順

## 前提
- Windows 10/11, Python 3.10+ がインストール済み
- ffmpeg が PATH に設定されている（必須ではないが音声処理で推奨）
- Project をクローン済み

## セットアップ（1回だけ）
1. PowerShell でプロジェクトルートへ移動
2. `.\scripts\setup_windows_env.ps1` を実行（依存がインストールされます）

## 起動（通常）
- PowerShell で: `.\run_local.ps1`
  - Backend (uvicorn) が :8000 に
  - Frontend static server が :3000 に起動します

## ヘルスチェック
- バックエンド: `http://localhost:8000/api/health` → `{"status":"ok"}`
- フロント: `http://<PC_IP>:3000/index.html` をスマホからアクセスして確認

## 音声取り込みテスト（簡易）
1. 任意の短い音声ファイルを `storage/processed/audio/` に置く（例: sample_short.m4a）
2. cURL で ingest:
```bash
curl -X POST "http://localhost:8000/api/ingest/audio" -F "file=@storage/processed/audio/sample_short.m4a"
```

検索:
```bash
curl -X POST "http://localhost:8000/api/search" -H "Content-Type: application/json" -d '{"q":"キーワード","top":5}'
```

## トラブルシュート
- uvicorn が起動しない場合は uvicorn_stderr.log を確認
- ポート競合がある場合は別ポートを指定して run_local.ps1 の引数で変更
