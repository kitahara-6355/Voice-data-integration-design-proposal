# SpeechHub Local

Windows PCでローカル処理（Whisper等OSS）を使い、音声 → 文字起こし → 埋め込み → 検索（スマホブラウザで確認）まで動く最小実装（PoC）です。

## 必須要件

-   [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)

## セットアップと実行手順

### 1. Dockerのインストール
上記リンクからDocker Desktopをダウンロードし、お使いのWindows PCにインストールしてください。インストール後、Docker Desktopが起動していることを確認してください。

### 2. モデルのダウンロード
このアプリケーションは、機械学習モデルを事前にダウンロードする必要があります。プロジェクトのルートディレクトリで、以下のコマンドを実行してください。

```bash
python scripts/download_models.py
```
これにより、`hf_cache`ディレクトリにモデルがダウンロードされます。初回のみ時間がかかります。

### 3. アプリケーションの起動
すべての準備が整ったら、以下のコマンド一つでアプリケーションを起動できます。

```bash
docker-compose up --build
```
このコマンドは、`backend/Dockerfile`を元にコンテナイメージをビルドし、`docker-compose.yml`の定義に従ってサービスを起動します。初回ビルドは時間がかかりますが、2回目以降はキャッシュが利用され高速になります。

### 4. 動作確認
サーバーが起動したら、Webブラウザで以下のURLにアクセスしてください。

-   **フロントエンドUI:** `http://localhost:8000`
-   **APIヘルスチェック:** `http://localhost:8000/api/health`

フロントエンドの画面が表示され、検索機能が利用できれば成功です。

### 5. アプリケーションの停止
アプリケーションを停止するには、`docker-compose`を実行したターミナルで `Ctrl + C` を押してください。あるいは、別のターミナルから以下のコマンドを実行します。

```bash
docker-compose down
```

---

## ローカルでの直接実行（非推奨・開発者向け）

Dockerを使わずに、お使いのPCに直接Python環境を構築して実行することも可能です。依存関係の競合などが発生する可能性があるため、開発に慣れている方向けの手順です。

### 1. 前提ツールのインストール
- **Python 3.11:** [公式サイト](https://www.python.org/downloads/)からインストールします。インストール時に「Add Python to PATH」にチェックを入れてください。
- **ffmpeg:** `faster-whisper`が音声ファイルを処理するために必要です。
    - [公式サイト](https://ffmpeg.org/download.html)からダウンロードし、解凍します。
    - 解凍したフォルダの中の `bin` フォルダのパスを、システムの環境変数 `PATH` に追加します。

### 2. プロジェクトのセットアップ
PowerShellまたはコマンドプロンプトで以下のコマンドを実行します。

```powershell
# 仮想環境の作成
python -m venv .venv

# 仮想環境のアクティベート
.\.venv\Scripts\Activate.ps1

# 依存ライブラリのインストール
pip install -r backend/requirements.txt
```

### 3. モデルのダウンロード
Dockerでの実行と同様に、モデルをダウンロードします。

```powershell
python scripts/download_models.py
```

### 4. サーバーの起動
以下のコマンドでバックエンドサーバーを起動します。

```powershell
# uvicornを直接実行
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --loop asyncio
```

### 5. 動作確認
ブラウザで `http://localhost:8000` にアクセスします。

---

## トラブルシューティング

### Dockerの起動に失敗する場合

`docker-compose up` が失敗する場合、以下のコマンドで詳細なログを確認・保存できます。

**1. ビルドのログを確認する**

イメージのビルド中にエラーが発生している場合、以下のコマンドでビルドプロセスのみを実行し、ログをファイルに保存します。

```bash
docker-compose build --no-cache > build.log 2>&1
```
`build.log` ファイルに詳細なエラーが出力されます。

**2. コンテナの実行ログを確認する**

ビルドは成功するが、コンテナの起動後に問題が発生する場合、以下のコマンドでコンテナのログを確認できます。

```bash
# 起動中のコンテナのログをリアルタイムで表示
docker-compose logs -f backend

# すべてのログをファイルに保存
docker-compose logs backend > backend.log 2>&1
```
`backend.log` ファイルで、アプリケーションの起動エラーなどを確認できます。
