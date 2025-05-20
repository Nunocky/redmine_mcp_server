# MyAccount機能設計書

## 実装タスクチェックリスト

- [x] API仕様書作成
- [x] 機能設計書作成
- [x] GET /my/account 実装
- [ ] PUT /my/account 実装
- [ ] テストコード作成
- [ ] ドキュメント更新

---

## 1. 要件定義

### 機能概要
- ログインユーザー自身のアカウント情報を取得するAPI(GET)を提供する。
- ログインユーザー自身のアカウント情報を更新するAPI(PUT)を提供する。

### ユースケース
- ユーザーが自身のプロフィール情報を取得する。
- 外部アプリケーションが認証済みユーザー情報を取得する。

### 非機能要件
- PEP8準拠
- GoogleスタイルDocstring
- テストコード必須（pytest）

---

## 2. 機能設計

### エンドポイント

#### GET /my/account.:format

- 概要: ログインユーザー自身のアカウント情報を返却
- 認証: 必須（APIキーまたはセッション）
- レスポンス: ユーザー情報（id, login, admin, firstname, lastname, mail, created_on, last_login_on, api_key, custom_fields）

#### PUT /my/account.:format

- 概要: ログインユーザー自身のアカウント情報を更新
- 認証: 必須（APIキーまたはセッション）
- リクエスト: 更新可能なユーザー情報（firstname, lastname, mail, custom_fields など）
- レスポンス: 更新後のユーザー情報（GETと同形式）
- エラー: 権限エラー・バリデーションエラー時はエラーメッセージを返却

---

### PUT /my/account.:format 設計詳細

- リクエスト例（JSON）:
  ```json
  {
    "firstname": "Taro",
    "lastname": "Yamada",
    "mail": "taro@example.com",
    "custom_fields": [
      {"id": 4, "value": "090-xxxx-xxxx"}
    ]
  }
  ```

- リクエストパラメータ:
  | 名前          | 型     | 必須 | 説明                       |
  | ------------- | ------ | ---- | -------------------------- |
  | firstname     | string | -    | 名                         |
  | lastname      | string | -    | 姓                         |
  | mail          | string | -    | メールアドレス             |
  | custom_fields | array  | -    | カスタムフィールド（任意） |

- レスポンス例: GET /my/account と同じ

- エラー例:
  - 400: バリデーションエラー
  - 401: 認証エラー
  - 403: 権限エラー

- クラス構成案:
  - `UpdateMyAccountTool`（新規作成）
    - PUT /my/account を実行するツールクラス
    - 認証情報と更新内容を受け取り、ユーザー情報を更新

---

## 3. クラス構成（案）

- `GetMyAccountTool`  
  - GET /my/account を実行するツールクラス
  - 認証情報を受け取り、ユーザー情報を取得
- `RedmineApiClient`  
  - Redmine APIへのリクエスト共通処理

---

## 4. 今後の拡張

- PUTメソッドによるアカウント情報更新機能の追加
- カスタムフィールドの柔軟な対応
- エラーハンドリング強化

---

## 5. 備考

- 詳細なAPI仕様は docs/MyAccount_api_spec.md を参照
- テストは tests/MyAccount/ 以下に配置予定
