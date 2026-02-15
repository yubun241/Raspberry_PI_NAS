## Raspberry_PI_NAS
RaspBerryPiをNasとして活用する手順をまとめます。
USBメモリや外付けHD,SSDをインターネットサーバーとして活用できるにします。

## 環境
Raspberry Pi 4

Raspberry Pi OS

Python 3.x

FastAPI

Uvicorn

Cloudflared

Gmail (SMTP)

外付けのSSD 1TB

## プログラムの内容
main.py FatAPIのwebAppのプログラム

send_url.py gmail送付のプログラム

start.sh サーバーを自動で起動させるプログラム


## python仮想環境を用意
今回はHomeディレクトリにvenv env1を設置

※仮想環境を設置しないと動作しませんでした。

仮想環境の立ち上げの詳細は以下に記載しています。

https://github.com/yubun241/python_venv

## ライブラリの導入

pip install fastapi uvicorn python-multipart



## Cloudflare Tunnelの設定
こちらを設定することで同じネット環境下でなくともサーバーに接続できるようになります。

https://developers.cloudflare.com/

メールアドレスを登録します。これでサーバーのURL発行ができるようになります。

独自度メインの登録を紹介されますが、固定URLを活用する場合は登録が必要ですが、ランダムURLを活用する場合は不要です。

本記事ではランダムURLで無料で活用しURLが発行される度にGmailでお知らせする内容にしています。

テスト中に何度も試すとシステム側からブロックされることがあります長くても1時間程度で解除されるみたいですが、
早いペースで何度もURL発行をする場合は注意が必要です。


ターミナルを起動し以下を入力

wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64.deb

sudo dpkg -i cloudflared-linux-arm64.deb

確認

cloudflared --version



## サーバーが立ち上がるとメールでURLをお知らせ
本記事ではGmailでの連携をご紹介します。
パスワード発行のページにアクセス

https://myaccount.google.com/apppasswords

今回のサーバー向けに新規でパスコードを起こす必要があります。

※２段階認証が既に有効化されている必要がありますのであらかじめアカウントの状態を確認して下さい。

パスワードを発行できれば後はpythonのプログラムに組み入れます。


## 立ち上げ手順
start.shを起動すれば基本何も操作する必要はないですが
仮に手動で行った場合も記載しておきます。


※プログラムを起動する前は一度ご自身の環境でコードを配置するpathやUSBもしくはSSD,HD,ローカルのpath設定はお願いします。

### start.shで起動する場合
ターミナルを起動して権限付与を行う

chmod +x start_server.sh

サーバー起動
./start_server.sh

設定したアドレスにメールが届くのでそこにアクセス。


### 手動手順
ターミナルを起動する

python環境に入る

main.pyが配置されているpathにカレンとディレクトを設定する

source ~/env1/bin/activate

cd ~/Desktop

以下をでサーバーを起動する

uvicorn main:app --host 0.0.0.0 --port 8000

別のターミナルを開いてTunnelを起動

cloudflared tunnel --url http://localhost:8000
こちらにURLが発行される
























