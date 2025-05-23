# Groupsツール 実装仕様書

## 前提

- Redmine REST APIのGroupsエンドポイント（JSONのみ対応）を操作するPythonツール群を実装する。
- すべてのAPI呼び出しはJSON形式のみをサポートする。
- 認証にはredmine_url, api_keyが必須。
- 実装は tools/Groups/ ディレクトリ配下に配置する。
- 各APIごとに「APIクライアント関数」と「Toolクラス」をペアで作成する。

---

## ディレクトリ構成

```
tools/Groups/
    get_groups.py
    GetGroupsTool.py
    create_group.py
    CreateGroupTool.py
    get_group.py
    GetGroupTool.py
    update_group.py
    UpdateGroupTool.py
    delete_group.py
    DeleteGroupTool.py
    add_user_to_group.py
    AddUserToGroupTool.py
    remove_user_from_group.py
    RemoveUserFromGroupTool.py
```

---

## 各APIの実装仕様

### 1. グループ一覧取得

- ファイル: get_groups.py, GetGroupsTool.py
- 関数: get_groups(redmine_url: str, api_key: str) -> dict
- メソッド: GET /groups.json
- レスポンス: グループ一覧（dict）

---

### 2. グループ作成

- ファイル: create_group.py, CreateGroupTool.py
- 関数: create_group(redmine_url: str, api_key: str, name: str, user_ids: Optional[List[int]] = None) -> dict
- メソッド: POST /groups.json
- ボディ: 
  ```json
  {
    "group": {
      "name": "グループ名",
      "user_ids": [1, 2]
    }
  }
  ```
- レスポンス: 作成したグループ情報（dict）

---

### 3. グループ詳細取得

- ファイル: get_group.py, GetGroupTool.py
- 関数: get_group(redmine_url: str, api_key: str, group_id: int, include: Optional[str] = None) -> dict
- メソッド: GET /groups/{id}.json?include=users,memberships
- レスポンス: グループ詳細（dict）

---

### 4. グループ更新

- ファイル: update_group.py, UpdateGroupTool.py
- 関数: update_group(redmine_url: str, api_key: str, group_id: int, name: Optional[str] = None, user_ids: Optional[List[int]] = None) -> dict
- メソッド: PUT /groups/{id}.json
- ボディ: 
  ```json
  {
    "group": {
      "name": "新しいグループ名",
      "user_ids": [1, 2]
    }
  }
  ```
- レスポンス: 更新後のグループ情報（dict）

---

### 5. グループ削除

- ファイル: delete_group.py, DeleteGroupTool.py
- 関数: delete_group(redmine_url: str, api_key: str, group_id: int) -> dict
- メソッド: DELETE /groups/{id}.json
- レスポンス: 削除結果（dict, 204の場合は {"success": True}）

---

### 6. グループにユーザー追加

- ファイル: add_user_to_group.py, AddUserToGroupTool.py
- 関数: add_user_to_group(redmine_url: str, api_key: str, group_id: int, user_id: int) -> dict
- メソッド: POST /groups/{id}/users.json
- ボディ: 
  ```json
  {
    "user_id": 5
  }
  ```
- レスポンス: 204の場合は {"success": True}

---

### 7. グループからユーザー削除

- ファイル: remove_user_from_group.py, RemoveUserFromGroupTool.py
- 関数: remove_user_from_group(redmine_url: str, api_key: str, group_id: int, user_id: int) -> dict
- メソッド: DELETE /groups/{id}/users/{user_id}.json
- レスポンス: 204の場合は {"success": True}

---

## 実装上の注意

- すべてのAPI関数はRedmineAPIClientを利用する。
- 例外処理は既存の他ツールと同様にrequests.exceptions.HTTPErrorをcatchし、404の場合はNoneや空dictを返す。
- DocstringはGoogleスタイル、コメントは英語、PEP8準拠。
- テストはtests/Groups/配下に作成する。
