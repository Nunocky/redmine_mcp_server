# 添付ファイルAPI設計書

## チェックリスト

- [ ] API仕様書作成
- [ ] 機能仕様書作成（要件定義・機能一覧・クラス構成）

---

## 1. API仕様書

### 概要

Redmineの添付ファイル（Attachments）に関するREST APIの仕様をまとめる。

### エンドポイント

#### 1.1 GET /attachments/:id.:format

- 概要: 指定したIDの添付ファイル情報を取得する
- メソッド: GET
- パスパラメータ:
  - id: 添付ファイルID
  - format: レスポンスフォーマット（xml, json など）

- レスポンス例（XML）:

```xml
<attachment>
  <id>6243</id>
  <filename>test.txt</filename>
  <filesize>124</filesize>
  <content_type>text/plain</content_type>
  <description>This is an attachment</description>
  <content_url>http://localhost:3000/attachments/download/6243/test.txt</content_url>
  <author name="Jean-Philippe Lang" id="1"/>
  <created_on>2011-07-18T22:58:40+02:00</created_on>
</attachment>
```

- 備考: ファイル本体は `content_url` でダウンロード可能。

#### 1.2 PATCH /attachments/:id.:format

- 概要: 添付ファイル情報の更新
- メソッド: PATCH
- パスパラメータ:
  - id: 添付ファイルID
  - format: レスポンスフォーマット
- 備考: 詳細未記載（Redmine Issue #12181 参照）

#### 1.3 DELETE /attachments/:id.:format

- 概要: 添付ファイルの削除
- メソッド: DELETE
- パスパラメータ:
  - id: 添付ファイルID
  - format: レスポンスフォーマット

- リクエスト例:
```
DELETE /attachments/6243.json
```

---

## 2. 機能仕様書

### 2.1 要件定義

- 添付ファイルの情報取得、削除、（将来的に）更新をREST API経由で行う
- ファイル本体は `content_url` でダウンロード可能
- 添付ファイルはチケット等のリソースに紐付く
- 認証はRedmineのAPIキー等を利用

### 2.2 機能一覧

| 機能名           | 概要                               |
| ---------------- | ---------------------------------- |
| 添付ファイル取得 | 添付ファイルのメタ情報を取得       |
| 添付ファイル削除 | 添付ファイルを削除                 |
| 添付ファイル更新 | 添付ファイル情報を更新（将来対応） |

### 2.3 クラス構成（案）

- `AttachmentApiClient`
  - 添付ファイルAPIへのリクエストを担当
  - メソッド例:
    - `get_attachment(id: int) -> Attachment`
    - `delete_attachment(id: int) -> bool`
    - `update_attachment(id: int, data: dict) -> Attachment`（将来対応）

- `Attachment`
  - 添付ファイルの情報を保持するデータクラス
  - 属性例:
    - id, filename, filesize, content_type, description, content_url, author, created_on

---

## 3. 備考

- 添付ファイルのアップロードは本API仕様には含まれない（別途「Attaching files」参照）
- PATCHメソッドの詳細はRedmine本体のIssue #12181を参照
