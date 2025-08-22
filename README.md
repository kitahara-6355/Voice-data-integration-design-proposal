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
