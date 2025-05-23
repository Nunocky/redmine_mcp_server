# Groupsツール 実装計画書

## 実装API一覧（進捗管理用チェックリスト）

- [x] グループ一覧取得（GET /groups.json）
- [x] グループ作成（POST /groups.json）
- [x] グループ詳細取得（GET /groups/{id}.json）
- [x] グループ更新（PUT /groups/{id}.json）
- [x] グループ削除（DELETE /groups/{id}.json）
- [x] グループにユーザー追加（POST /groups/{id}/users.json）
- [ ] グループからユーザー削除（DELETE /groups/{id}/users/{user_id}.json）

## 目的

RedmineのGroups API（JSON対応）を操作するPythonツール群を、既存の設計・実装方針に従い新規開発する。

---

## スケジュール・工程

1. **ディレクトリ作成**
   - tools/Groups/ ディレクトリを作成

2. **APIクライアント関数の実装**
   - 各APIごとにRedmineAPIClientを利用した関数を作成
   - get_groups.py, create_group.py, get_group.py, update_group.py, delete_group.py, add_user_to_group.py, remove_user_from_group.py

3. **Toolクラスの実装**
   - 各APIクライアント関数に対応するToolクラスを作成
   - GetGroupsTool.py, CreateGroupTool.py, GetGroupTool.py, UpdateGroupTool.py, DeleteGroupTool.py, AddUserToGroupTool.py, RemoveUserFromGroupTool.py

4. **テストコード作成**
   - tests/Groups/ ディレクトリを作成し、各APIごとにpytestベースのテストを実装

5. **ドキュメント整備**
   - 実装後、設計書・仕様書の修正・追記

---

## 実装手順詳細

1. **ディレクトリ構成準備**
   - tools/Groups/ 配下に必要なファイルを新規作成

2. **APIクライアント関数の作成**
   - 既存のtools/redmine_api_client.pyを利用し、各API仕様に従った関数を作成
   - 必要な引数・レスポンス・例外処理をGoogleスタイルDocstringで明記

3. **Toolクラスの作成**
   - fastmcp.tools.tool.Tool.from_functionを用いて各API関数をTool化
   - name, descriptionを明確に記述

4. **テストの実装**
   - pytest形式で正常系・異常系（404, バリデーションエラー等）を網羅
   - テスト用のRedmineサーバ設定・APIキーは環境変数で管理

5. **ドキュメント更新**
   - 実装内容に応じてdocs/Groups_api_spec.md, docs/Groups_implementation_spec.mdを更新

---

## 注意事項

- すべてJSON形式のみ対応
- 認証情報は必須
- 例外処理・Docstring・PEP8・コメント英語
- 既存の他ツールの実装・テストを参考にすること

---

## 完了基準

- すべてのAPIエンドポイントに対し、ツール・テスト・ドキュメントが揃っていること
- テストが全てパスすること
- コードレビュー・PRルール（docs/pull_request.md）を遵守していること
