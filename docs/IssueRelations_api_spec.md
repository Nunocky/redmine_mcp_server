# IssueRelations API仕様書

## 概要

Redmineの課題間リレーション（Issue Relations）を取得・作成・削除するAPIの仕様を定義する。  
Redmine REST API `/issues/:issue_id/relations.[format]` および `/relations/[id].[format]` をラップし、課題間の関連情報を操作する。

---

## エンドポイント

### 1. 課題リレーション一覧取得

- メソッド: GET
- パス: `/issues/:issue_id/relations.[format]`
- 概要: 指定した課題IDに紐づくリレーション一覧を取得する

### 2. 課題リレーション作成

- メソッド: POST
- パス: `/issues/:issue_id/relations.[format]`
- 概要: 指定した課題IDに対して新しいリレーションを作成する

### 3. 課題リレーション削除

- メソッド: DELETE
- パス: `/relations/:id.[format]`
- 概要: 指定したリレーションIDのリレーションを削除する

---

## リクエスト

### 1. 課題リレーション一覧取得

#### パラメータ

| 名前        | 型     | 必須 | 説明                       |
| ----------- | ------ | ---- | -------------------------- |
| redmine_url | string | 必須 | RedmineのベースURL         |
| api_key     | string | 必須 | Redmine APIキー            |
| issue_id    | int    | 必須 | 対象課題のID               |
| format      | string | 任意 | レスポンス形式（json/xml） |

#### リクエスト例

```
GET https://redmine.example.com/issues/123/relations.json?key=xxxxxxxxxxxxxxxxxxxxxx
```

---

### 2. 課題リレーション作成

#### パラメータ

| 名前          | 型     | 必須 | 説明                                          |
| ------------- | ------ | ---- | --------------------------------------------- |
| redmine_url   | string | 必須 | RedmineのベースURL                            |
| api_key       | string | 必須 | Redmine APIキー                               |
| issue_id      | int    | 必須 | 対象課題のID                                  |
| issue_to_id   | int    | 必須 | 関連先課題のID                                |
| relation_type | string | 必須 | リレーション種別（例: relates, blocks, etc.） |
| delay         | int    | 任意 | 遅延日数（relation_typeがprecedes等の場合）   |
| format        | string | 任意 | レスポンス形式（json/xml）                    |

#### リクエスト例

```json
POST https://redmine.example.com/issues/123/relations.json?key=xxxxxxxxxxxxxxxxxxxxxx
Content-Type: application/json

{
  "relation": {
    "issue_to_id": 456,
    "relation_type": "relates"
  }
}
```

---

### 3. 課題リレーション削除

#### パラメータ

| 名前        | 型     | 必須 | 説明                       |
| ----------- | ------ | ---- | -------------------------- |
| redmine_url | string | 必須 | RedmineのベースURL         |
| api_key     | string | 必須 | Redmine APIキー            |
| id          | int    | 必須 | 削除対象リレーションID     |
| format      | string | 任意 | レスポンス形式（json/xml） |

#### リクエスト例

```
DELETE https://redmine.example.com/relations/789.json?key=xxxxxxxxxxxxxxxxxxxxxx
```

---

## レスポンス

### 1. 課題リレーション一覧取得

#### ステータスコード

- 200 OK

#### レスポンスボディ（JSON例）

```json
{
  "relations": [
    {
      "id": 789,
      "issue_id": 123,
      "issue_to_id": 456,
      "relation_type": "relates",
      "delay": null
    }
  ]
}
```

---

### 2. 課題リレーション作成

#### ステータスコード

- 201 Created

#### レスポンスボディ（JSON例）

```json
{
  "relation": {
    "id": 790,
    "issue_id": 123,
    "issue_to_id": 456,
    "relation_type": "relates",
    "delay": null
  }
}
```

---

### 3. 課題リレーション削除

#### ステータスコード

- 204 No Content

---

### エラー時

#### ステータスコード

- 401 Unauthorized（APIキー不正）
- 403 Forbidden（権限不足）
- 404 Not Found（リソース未存在）

#### エラーレスポンス例

```json
{
  "error": {
    "message": "Invalid API key.",
    "code": 401
  }
}
```

---

## 備考

- レスポンス形式はデフォルトでJSON。`format`パラメータでXMLも選択可能。
- relation_typeにはRedmine標準の種別（relates, blocks, precedes, etc.）が利用可能。
- 標準のRedmine REST API仕様に準拠。
