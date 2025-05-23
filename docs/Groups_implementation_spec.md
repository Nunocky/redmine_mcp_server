# Groups一覧取得ツール 実装手順書

## 1. ディレクトリ構成準備

- `tools/Groups/` ディレクトリを作成（未作成の場合）

## 2. APIクライアント関数の作成

- ファイル: `tools/Groups/get_groups.py`
- 内容:
    - RedmineAPIClientを利用し、GET /groups.json を叩く関数 `get_groups` を実装
    - 必須引数: redmine_url, api_key
    - 任意引数: limit, offset, name
    - 404時は空リストを返す
    - GoogleスタイルDocstring、PEP8、英語コメント

## 3. Toolクラスの作成

- ファイル: `tools/Groups/GetGroupsTool.py`
- 内容:
    - `get_groups` 関数をTool化
    - name, descriptionを明記

## 4. テストコード作成

- ディレクトリ: `tests/Groups/`
- ファイル: `test_get_groups_tool.py`
- 内容:
    - pytest形式で正常系・異常系（404, バリデーションエラー等）を網羅
    - テスト用Redmineサーバ設定・APIキーは環境変数で管理

## 5. ドキュメント更新

- 実装内容に応じて設計書・仕様書を修正

---
