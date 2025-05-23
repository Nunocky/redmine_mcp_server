# Groups一覧取得・作成・詳細取得ツール 実装手順書

## 1. ディレクトリ構成準備

- `tools/Groups/` ディレクトリを作成済みであること

## 2. グループ詳細取得APIクライアント関数の作成

- ファイル: `tools/Groups/get_group.py`
- 内容:
    - RedmineAPIClientを利用し、GET /groups/{id}.json を叩く関数 `get_group` を実装
    - 必須引数: redmine_url, api_key, group_id
    - 404時は {"group": None} を返す
    - GoogleスタイルDocstring、PEP8、英語コメント

## 3. Toolクラスの作成

- ファイル: `tools/Groups/GetGroupTool.py`
- 内容:
    - `get_group` 関数をTool化
    - name, descriptionを明記

## 4. テストコード作成

- ディレクトリ: `tests/Groups/`
- ファイル: `test_get_group_tool.py`
- 内容:
    - pytest形式で正常系・異常系（404, バリデーションエラー等）を網羅
    - テスト用Redmineサーバ設定・APIキーは環境変数で管理

## 5. ドキュメント更新

- 実装内容に応じて設計書・仕様書を修正

---
