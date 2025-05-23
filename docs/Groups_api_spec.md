# Groups API 仕様書

## 概要

RedmineのGroups APIは、グループの一覧取得、作成、詳細取得、更新、削除、ユーザーの追加・削除を行うREST APIです。全てのエンドポイントは管理者権限が必要です。

---

## エンドポイント一覧

### 1. グループ一覧取得

- **GET /groups.:format**
  - グループの一覧を取得します。
  - レスポンス例（XML）:
    ```xml
    <groups type="array">
      <group>
        <id>53</id>
        <name>Managers</name>
      </group>
      <group>
        <id>55</id>
        <name>Developers</name>
      </group>
    </groups>
    ```

---

### 2. グループ作成

- **POST /groups.:format**
  - 新しいグループを作成します。
  - パラメータ:
    - `group` (必須): グループ属性のハッシュ
      - `name` (必須): グループ名
      - `user_ids` (任意): ユーザーIDの配列
  - リクエスト例（JSON）:
    ```json
    {
      "group": {
        "name": "Developers",
        "user_ids": [3, 5]
      }
    }
    ```
  - レスポンス:
    - 201 Created: 作成成功
    - 422 Unprocessable Entity: バリデーションエラー

---

### 3. グループ詳細取得

- **GET /groups/:id.:format**
  - 指定したグループの詳細を取得します。
  - パラメータ:
    - `include` (任意): `users`, `memberships` をカンマ区切りで指定可能
  - レスポンス例（XML）:
    ```xml
    <group>
      <id>20</id>
      <name>Developers</name>
      <users type="array">
        <user id="5" name="John Smith"/>
        <user id="8" name="Dave Loper"/>
      </users>
    </group>
    ```

---

### 4. グループ更新

- **PUT /groups/:id.:format**
  - 指定したグループを更新します。

---

### 5. グループ削除

- **DELETE /groups/:id.:format**
  - 指定したグループを削除します。

---

### 6. グループにユーザー追加

- **POST /groups/:id/users.:format**
  - 指定したグループに既存ユーザーを追加します。
  - パラメータ:
    - `user_id` (必須): 追加するユーザーID
  - レスポンス:
    - 204 No Content: 追加成功

---

### 7. グループからユーザー削除

- **DELETE /groups/:id/users/:user_id.:format**
  - 指定したグループからユーザーを削除します。
  - レスポンス:
    - 204 No Content: 削除成功
