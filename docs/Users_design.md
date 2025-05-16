# Redmine Users API


## 残り実装

- [ ] レスポンス内容の管理者/非管理者による差分対応
- [ ] エラーハンドリングの強化
- [ ] テストケースの拡充

## 拡充計画

### get_user_tool.py の拡充
- **目的**: /users/current エンドポイント対応と管理者/非管理者による差分対応
- **実装方法**:
  - /users/current エンドポイント対応の確認と必要に応じた実装
  - レスポンス内容の管理者/非管理者による差分対応

### エラーハンドリングの強化
- **目的**: より詳細なエラー情報の提供
- **実装方法**:
  - 各ツールのエラーハンドリングを強化
  - HTTPステータスコードに応じた適切なエラーメッセージの提供

### テストケースの拡充
- **目的**: 新機能のテスト網羅性向上
- **実装方法**:
  - 新機能に対応するテストケースの追加
  - エッジケースのテスト追加


## API仕様詳細

### GET /users
- **説明**: ユーザーの一覧を返します。管理者権限が必要です。
- **パラメータ**:
  - `status`: ユーザーステータスでフィルタリングします。
    - `1`: アクティブ (ログイン可能)
    - `2`: 登録済み (メールアドレス未確認または管理者未アクティブ)
    - `3`: ロック済み (ログイン不可)
    - `(指定なし)`: 全てのステータスのユーザー
  - `name`: ログイン名、名、姓、メールアドレスでフィルタリングします。スペースを含む場合、名または姓が一致するユーザーも返します。
  - `group_id`: 特定のグループに所属するユーザーでフィルタリングします。
  - `limit`: 取得するユーザーの最大数。
  - `offset`: 取得するユーザーのオフセット。
- **例**:
  - `/users.xml`
- **curl 例**:
  ```bash
  curl -H "X-Redmine-API-Key: YOUR_API_KEY" -X GET http://your-redmine-instance/users.xml
  ```

### GET /users/:id
- **説明**: 特定のユーザーの詳細を返します。
  - `/users/current.:format` で、APIにアクセスするために使用される認証情報を持つユーザーを取得できます。
- **パラメータ**:
  - `include`: レスポンスに含める関連情報。カンマ区切りで複数指定できます。
    - `memberships`: ユーザーのプロジェクトメンバーシップとロールに関する情報を追加します。
    - `groups`: ユーザーのグループに関する情報を追加します (Redmine 2.1 以降)。
- **例**:
  - `/users/current.xml`
  - `/users/3.xml?include=memberships,groups`
- **curl 例**:
  ```bash
  curl -H "X-Redmine-API-Key: YOUR_API_KEY" -X GET http://your-redmine-instance/users/3.xml?include=memberships,groups
  ```

### POST /users
- **説明**: ユーザーを作成します。管理者権限が必要です。
- **パラメータ**:
  - `user`: ユーザー属性のハッシュ (必須)。
    - `login`: ログイン名 (必須)。
    - `password`: パスワード。
    - `firstname`: 名 (必須)。
    - `lastname`: 姓 (必須)。
    - `mail`: メールアドレス (必須)。
    - `auth_source_id`: 認証モード ID。
    - `mail_notification`: メール通知設定 (only_my_events, none など)。
    - `must_change_passwd`: パスワード変更が必要かどうか (true または false)。
    - `generate_password`: パスワードを自動生成するかどうか (true または false)。
    - `custom_fields`: カスタムフィールド (詳細は [Custom fields](https://www.redmine.org/projects/redmine/wiki/Rest_api#Working-with-custom-fields) を参照)。
  - `send_information`: アカウント情報をユーザーに送信するかどうか (true または false)。
- **例**:
  - XML:
    ```xml
    <user>
      <login>jplang</login>
      <firstname>Jean-Philippe</firstname>
      <lastname>Lang</lastname>
      <password>secret</password>
      <mail>jp_lang@yahoo.fr</mail>
      <auth_source_id>2</auth_source_id>
    </user>
    ```
  - JSON:
    ```json
    {
      "user": {
        "login": "jplang",
        "firstname": "Jean-Philippe",
        "lastname": "Lang",
        "mail": "jp_lang@yahoo.fr",
        "password": "secret"
      }
    }
    ```
- **レスポンス**:
  - `201 Created`: ユーザーが作成されました。
  - `422 Unprocessable Entity`: バリデーションエラーによりユーザーが作成されませんでした (レスポンスボディにエラーメッセージが含まれます)。
- **curl 例**:
  ```bash
  curl -H "X-Redmine-API-Key: YOUR_API_KEY" -H "Content-Type: application/xml" -X POST -d '<user><login>test</login><firstname>Test</firstname><lastname>User</lastname><mail>test@example.com</mail><password>password</password></user>' http://your-redmine-instance/users.xml
  ```
  または JSON:
  ```bash
  curl -H "X-Redmine-API-Key: YOUR_API_KEY" -H "Content-Type: application/json" -X POST -d '{"user":{"login":"test","firstname":"Test","lastname":"User","mail":"test@example.com","password":"password"}}' http://your-redmine-instance/users.json
  ```

### PUT /users/:id
- **説明**: ユーザーを更新します。管理者権限が必要です。
- **パラメータ**:
  - `user`: ユーザー属性のハッシュ (必須)。POST /users と同じ属性を使用します。
  - `admin`: ユーザーに管理者権限を付与するかどうか (true または false)。
  - `custom_fields`: カスタムフィールド (詳細は [Custom fields](https://www.redmine.org/projects/redmine/wiki/Rest_api#Working-with-custom-fields) を参照)。
- **例**:
  - `/users/20.xml`
- **curl 例**:
  ```bash
  curl -H "X-Redmine-API-Key: YOUR_API_KEY" -H "Content-Type: application/xml" -X PUT -d '<user><firstname>New</firstname></user>' http://your-redmine-instance/users/20.xml
  ```

### DELETE /users/:id
- **説明**: ユーザーを削除します。管理者権限が必要です。
- **パラメータ**:
  - `id`: 削除するユーザーのID。
- **例**:
  - `/users/20.xml`
- **レスポンス**:
  - `204 No Content`: ユーザーが削除されました。
- **curl 例**:
  ```bash
  curl -H "X-Redmine-API-Key: YOUR_API_KEY" -X DELETE http://your-redmine-instance/users/20.xml
  ```
