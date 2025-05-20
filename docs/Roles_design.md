# Roles API設計書

## ✅ 実装項目チェックリスト

- [ ] APIリファレンス作成
- [ ] ツール関数実装
- [ ] Toolクラス実装
- [ ] MCPサーバ(main.py)対応
- [ ] テストコード作成
- [ ] テスト実行・修正

---

## 1. 要件定義

RedmineのRoles（ロール）情報を取得するAPIツールを実装する。  
- ロール一覧取得API
- ロール詳細（権限一覧含む）取得API

### 対象API

- GET /roles.:format  
  ロール一覧を取得する

- GET /roles/[id].:format  
  指定したロールIDの詳細情報（権限含む）を取得する

---

## 2. APIリファレンス

### 2.1 ロール一覧取得

- **エンドポイント**: `/roles.json`
- **メソッド**: GET
- **パラメータ**: なし
- **レスポンス例**:
```json
{
  "roles": [
    {
      "id": 1,
      "name": "Manager"
    },
    {
      "id": 2,
      "name": "Developer"
    }
  ]
}
```

### 2.2 ロール詳細取得

- **エンドポイント**: `/roles/{id}.json`
- **メソッド**: GET
- **パラメータ**:  
  - id: 取得したいロールのID
- **レスポンス例**:
```json
{
  "role": {
    "id": 5,
    "name": "Reporter",
    "assignable": true,
    "issues_visibility": "default",
    "time_entries_visibility": "all",
    "users_visibility": "all",
    "permissions": [
      "view_issues",
      "add_issues",
      "add_issue_notes"
      // ...
    ]
  }
}
```

---

## 3. 概略設計

### 3.1 機能概要

- Redmine REST APIを利用し、ロール一覧・ロール詳細（権限含む）を取得するツールを実装する。
- MCPサーバからToolとして呼び出せるようにする。

### 3.2 クラス構成

- `tools/Roles/get_roles_tool.py`  
  ロール一覧取得ツール

- `tools/Roles/get_role_tool.py`  
  ロール詳細取得ツール

- `tools/redmine_api_client.py`  
  Redmine APIクライアント（既存利用）

- `main.py`  
  MCPサーバエントリポイント

- `tests/Roles/test_get_roles_tool.py`  
  ロール一覧取得テスト

- `tests/Roles/test_get_role_tool.py`  
  ロール詳細取得テスト

---

## 4. 詳細設計

### 4.1 ツール関数

- get_roles():  
  `/roles.json` にGETリクエストし、ロール一覧を返す

- get_role(role_id):  
  `/roles/{id}.json` にGETリクエストし、指定ロールの詳細を返す

### 4.2 Toolクラス

- `GetRolesTool`  
  - 入力: なし
  - 出力: ロール一覧

- `GetRoleTool`  
  - 入力: role_id (int)
  - 出力: ロール詳細

### 4.3 MCPサーバ対応

- main.pyにToolを登録

### 4.4 テスト

- pytestでツール単体・MCPサーバ経由のテストを実施

---

## 5. 備考

- APIレスポンスはjson形式を利用
- 認証情報は .env から取得
- 既存のAPIクライアントを流用

---

以上が設計書案です。内容をご確認ください。
