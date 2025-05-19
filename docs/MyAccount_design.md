# MyAccount機能設計書

## 実装タスクチェックリスト

- [ ] API仕様書作成
- [ ] 機能設計書作成
- [ ] GET /my/account 実装
- [ ] テストコード作成
- [ ] ドキュメント更新

---

## 1. 要件定義

### 機能概要
- ログインユーザー自身のアカウント情報を取得するAPI(GET)を提供する。
- 将来的にアカウント情報の更新API(PUT)も実装予定。

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
- 実装予定（現状は未対応）

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
