# Groups一覧取得・作成・詳細取得・更新ツール 実装手順書

## 1. ディレクトリ構成準備

- `tools/Groups/` ディレクトリを作成済みであること

## 2. グループ更新APIクライアント関数の作成

- ファイル: `tools/Groups/update_group.py`
- 内容:
    - RedmineAPIClientを利用し、PUT /groups/{id}.json を叩く関数 `update_group` を実装
    - 必須引数: redmine_url, api_key, group_id
    - 任意引数: name, users, custom_fields
    - 404時は {"group": None} を返す
    - GoogleスタイルDocstring、PEP8、英語コメント

## 3. Toolクラスの作成

- ファイル: `tools/Groups/UpdateGroupTool.py`
- 内容:
    - `update_group` 関数をTool化
    - name, descriptionを明記

## 4. テストコード作成

- ディレクトリ: `tests/Groups/`
- ファイル: `test_update_group_tool.py`
- 内容:
    - pytest形式で正常系・異常系（404, バリデーションエラー等）を網羅
    - テスト用Redmineサーバ設定・APIキーは環境変数で管理

## 5. ドキュメント更新

- 実装内容に応じて設計書・仕様書を修正

---
