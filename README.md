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
メールアドレスを登録します。
これでサーバーのURL発行ができるようになります。

独自度メインの登録を紹介されますが、
固定URLを活用する場合は登録が必要ですが、ランダムURLを活用する場合は不要です。

本記事ではランダムURLで無料で活用しURLが発行される度にGmailでお知らせする内容にしています。
テスト中に何度も試すとシステム側からブロックされることがあります長くても1時間程度で解除されるみたいですが、
早いペースで何度もURL発行をする場合は注意が必要です。


ターミナルを起動し以下を入力
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64.deb

sudo dpkg -i cloudflared-linux-arm64.deb


cloudflared --version



## サーバーが立ち上がるとメールでURLをお知らせ
サーバーは



