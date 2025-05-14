# Projects API設計書

## 1. 要件定義書

### 概要
RedmineのProjects（プロジェクト）情報を取得・作成・更新・削除するAPIクライアント機能をPythonで実装する。

### 対象APIエンドポイント
- プロジェクト一覧取得: `GET /projects.xml`
- プロジェクト詳細取得: `GET /projects/[id].xml`
- プロジェクト作成: `POST /projects.xml`
- プロジェクト更新: `PUT /projects/[id].xml`
- プロジェクトアーカイブ: `PUT /projects/[id]/archive.xml`
- プロジェクトアーカイブ解除: `PUT /projects/[id]/unarchive.xml`
- プロジェクト削除: `DELETE /projects/[id].xml`

### 機能一覧
- プロジェクト一覧取得（パラメータ: include, レスポンス: プロジェクト配列）
- プロジェクト詳細取得（パラメータ: id/identifier, include, レスポンス: プロジェクト詳細）
- プロジェクト作成（パラメータ: name, identifier, description, ...）
- プロジェクト更新
- プロジェクトアーカイブ/アーカイブ解除
- プロジェクト削除

### パラメータ例
- include: trackers, issue_categories, enabled_modules, time_entry_activities, issue_custom_fields
- project: name, identifier, description, homepage, is_public, parent_id, inherit_members, default_assigned_to_id, default_version_id, tracker_ids, enabled_module_names, issue_custom_field_ids, custom_field_values

### レスポンス例
- プロジェクト一覧（XML/JSON）
- プロジェクト詳細（XML/JSON）
- 作成/更新/削除時のHTTPステータス

---

## 2. 設計書

### 概略
RedmineのProjects APIに対応したPythonクライアントツールをtools/配下に実装する。  
各機能ごとにツールを分割し、テストはtests/配下に同名ファイルで作成する。

### 機能設計
- get_projects_tool.py: プロジェクト一覧取得
- get_project_tool.py: プロジェクト詳細取得
- create_project_tool.py: プロジェクト作成
- update_project_tool.py: プロジェクト更新
- archive_project_tool.py: プロジェクトアーカイブ
- unarchive_project_tool.py: プロジェクトアーカイブ解除
- delete_project_tool.py: プロジェクト削除

### クラス構成
- RedmineAPIClient
  - APIリクエスト共通処理（認証、リクエスト送信、エラーハンドリング）
- 各ツール（例: GetProjectsTool）
  - RedmineAPIClientを利用し、各APIエンドポイントに対応

### ディレクトリ構成（予定）
```
tools/
  get_projects_tool.py
  get_project_tool.py
  create_project_tool.py
  update_project_tool.py
  archive_project_tool.py
  unarchive_project_tool.py
  delete_project_tool.py
tests/
  test_get_projects_tool.py
  test_get_project_tool.py
  test_create_project_tool.py
  test_update_project_tool.py
  test_archive_project_tool.py
  test_unarchive_project_tool.py
  test_delete_project_tool.py
```

### テスト
- pytestを用い、正常系・異常系のテストを実装
- モックを活用し、Redmineサーバーがなくてもテスト可能とする

---

以上がProjects APIの要件定義・設計書案です。  
ご確認のうえ、修正点や追加要望があればご指摘ください。
