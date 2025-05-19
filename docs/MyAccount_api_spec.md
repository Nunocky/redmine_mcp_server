# MyAccount API仕様書

## 概要
自身のアカウント情報を取得・更新するAPI。

---

## エンドポイント

### GET /my/account.:format

- 概要: ログインユーザー自身のアカウント情報を取得する
- 認証: 必須（APIキーまたはセッション）

#### リクエスト例

```
GET /my/account.json
GET /my/account.xml
```

#### パラメータ

| 名前   | 種別   | 必須 | 説明                       |
| ------ | ------ | ---- | -------------------------- |
| format | string | ○    | レスポンス形式（json/xml） |

#### レスポンス例（XML）

```xml
<?xml version="1.0" encoding="UTF-8"?>
<user>
  <id>3</id>
  <login>dlopper</login>
  <admin>false</admin>
  <firstname>Dave</firstname>
  <lastname>Lopper</lastname>
  <mail>dlopper@somenet.foo</mail>
  <created_on>2006-07-19T17:33:19Z</created_on>
  <last_login_on>2020-06-14T13:03:34Z</last_login_on>
  <api_key>c308a59c9dea95920b13522fb3e0fb7fae4f292d</api_key>
  <custom_fields type="array">
    <custom_field id="4" name="Phone number">
      <value/>
    </custom_field>
    <custom_field id="5" name="Money">
      <value/>
    </custom_field>
  </custom_fields>
</user>
```

#### レスポンス項目

| フィールド名  | 型     | 説明                |
| ------------- | ------ | ------------------- |
| id            | int    | ユーザーID          |
| login         | string | ログインID          |
| admin         | bool   | 管理者フラグ        |
| firstname     | string | 名                  |
| lastname      | string | 姓                  |
| mail          | string | メールアドレス      |
| created_on    | string | 作成日時（ISO8601） |
| last_login_on | string | 最終ログイン日時    |
| api_key       | string | APIキー             |
| custom_fields | array  | カスタムフィールド  |

---

### PUT /my/account.:format

- 概要: ログインユーザー自身のアカウント情報を更新する
- 認証: 必須
- ※詳細未記載（TODO）
