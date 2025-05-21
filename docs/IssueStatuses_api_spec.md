# IssueStatuses API仕様書

## 概要

Redmineの課題ステータス（Issue Statuses）一覧を取得するAPIの仕様を定義する。  
Redmine REST API `/issue_statuses.[format]` のGETリクエストをラップし、全ての課題ステータス情報（id, name, is_closed）を取得する。

---

## エンドポイント

- メソッド: GET
- パス: `/issue_statuses.[format]`
- 概要: 全ての課題ステータスを取得する

---

## リクエスト

### パラメータ

| 名前        | 型     | 必須 | 説明                       |
| ----------- | ------ | ---- | -------------------------- |
| redmine_url | string | 必須 | RedmineのベースURL         |
| api_key     | string | 必須 | Redmine APIキー            |
| format      | string | 任意 | レスポンス形式（json/xml） |

### リクエスト例

```
GET https://redmine.example.com/issue_statuses.json?key=xxxxxxxxxxxxxxxxxxxxxx
```

---

## レスポンス

### 正常時

#### ステータスコード

- 200 OK

#### レスポンスボディ（JSON例）

```json
{
  "issue_statuses": [
    {
      "id": 1,
      "name": "New",
      "is_closed": false
    },
    {
      "id": 2,
      "name": "Closed",
      "is_closed": true
    }
  ]
}
```

#### レスポンスボディ（XML例）

```xml
<?xml version="1.0" encoding="UTF-8"?>
<issue_statuses type="array">
  <issue_status>
    <id>1</id>
    <name>New</name>
    <is_closed>false</is_closed>
  </issue_status>
  <issue_status>
    <id>2</id>
    <name>Closed</name>
    <is_closed>true</is_closed>
  </issue_status>
</issue_statuses>
```

---

### エラー時

#### ステータスコード

- 401 Unauthorized（APIキー不正）
- 403 Forbidden（権限不足）
- 404 Not Found（URL不正）

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
- 標準のRedmine REST API仕様に準拠。
- 追加パラメータは現時点で不要。
