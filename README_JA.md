# Rotate Image Node

日本語 | [English](README.md)

入力画像を回転するための ComfyUI カスタムノードです。回転によって生じる余白の処理方法を選択できます。
ComfyUIの標準ノードでは対応していない中途半端な角度への回転が可能です

<img width="1658" height="1452" alt="image" src="https://github.com/user-attachments/assets/0804d800-b2ae-491e-9868-2ccfc256f1de" />


## インストール

1. このリポジトリを `ComfyUI/custom_nodes` 内にクローンします。

   ```bash
   cd ComfyUI/custom_nodes
   git clone https://github.com/palealloy2999-prog/comfyUI-rotate-image.git
   ```

2. ComfyUI を再起動します。
3. ノード一覧で `Rotate Image` を検索します。

## 入力

- `image`: 入力画像
- `angle`: 回転角度（度）
- `background_mode`: 余白の処理方法
  - `fit`: 回転後の画像が元のキャンバス全体を覆うように拡大し、元のサイズに中央クロップします
  - `white`: 余白を白で塗りつぶします
  - `black`: 余白を黒で塗りつぶします
  - `custom`: 余白を指定色で塗りつぶします
- `custom_color`: `custom` で使用する16進数の色（例: `#FF00AA`）

## 出力

- `image`: 回転後の画像
