# Redmine Issues API設計

## 概要

Redmineの「チケット（Issue）」に関するREST APIの設計ドキュメントです。  
エンドポイントごとに、概要・パラメータ・リクエスト例・レスポンス例・備考をまとめます。

---

## 目次

- [Redmine Issues API設計](#redmine-issues-api設計)
  - [概要](#概要)
  - [目次](#目次)
  - [GET /issues](#get-issues)
    - [概要](#概要-1)
    - [主なパラメータ](#主なパラメータ)
    - [リクエスト例](#リクエスト例)
    - [curl例](#curl例)
  - [GET /issues/:id](#get-issuesid)
    - [概要](#概要-2)
    - [主なパラメータ](#主なパラメータ-1)
    - [リクエスト例](#リクエスト例-1)
    - [curl例](#curl例-1)
  - [POST /issues](#post-issues)
    - [概要](#概要-3)
    - [主なパラメータ](#主なパラメータ-2)
    - [リクエスト例](#リクエスト例-2)
    - [curl例](#curl例-2)
    - [レスポンス](#レスポンス)
  - [PUT /issues/:id](#put-issuesid)
    - [概要](#概要-4)
    - [主なパラメータ](#主なパラメータ-3)
    - [リクエスト例](#リクエスト例-3)
    - [curl例](#curl例-3)
    - [設計・実装方針](#設計実装方針)
  - [DELETE /issues/:id](#delete-issuesid)
    - [概要](#概要-5)
    - [リクエスト例](#リクエスト例-4)
    - [curl例](#curl例-4)
    - [レスポンス](#レスポンス-1)
  - [POST /issues/:id/watchers](#post-issuesidwatchers)
    - [概要](#概要-6)
    - [主なパラメータ](#主なパラメータ-4)
    - [リクエスト例](#リクエスト例-5)
    - [curl例](#curl例-5)
  - [DELETE /issues/:id/watchers/:user\_id](#delete-issuesidwatchersuser_id)
    - [概要](#概要-7)
    - [リクエスト例](#リクエスト例-6)
    - [curl例](#curl例-6)
    - [レスポンス](#レスポンス-2)
  - [備考](#備考)

---

## GET /issues

### 概要

チケット（Issue）の一覧を返します。  
デフォルトではオープンなチケットのみ返します。ページング対応。

### 主なパラメータ

| パラメータ名   | 説明                                         | 例                       |
| -------------- | -------------------------------------------- | ------------------------ |
| offset         | 取得開始位置（省略可）                       | 0                        |
| limit          | 1ページあたりの件数（省略可）                | 100                      |
| sort           | ソートカラム。`:desc`で降順                  | category:desc,updated_on |
| include        | 関連情報をカンマ区切りで指定                 | attachments,relations    |
| issue_id       | 指定IDのチケット（カンマ区切りで複数指定可） | 1,2,3                    |
| project_id     | プロジェクトIDで絞り込み                     | 2                        |
| subproject_id  | サブプロジェクトIDで絞り込み                 | 5                        |
| tracker_id     | トラッカーIDで絞り込み                       | 1                        |
| status_id      | ステータスIDまたは`open`/`closed`/`*`        | open                     |
| assigned_to_id | 担当者IDまたは`me`                           | me                       |
| parent_id      | 親チケットID                                 | 10                       |
| cf_x           | カスタムフィールドID x の値で絞り込み        | cf_1=foo                 |

他にも日付や文字列の範囲指定等、多数のフィルタが利用可能です。

### リクエスト例

```
GET /issues.json?project_id=2&status_id=open&limit=10
```

### curl例

```bash
curl -H "X-Redmine-API-Key: YOUR_API_KEY" -X GET "http://your-redmine-instance/issues.json?project_id=2&status_id=open&limit=10"
```

---

## GET /issues/:id

### 概要

指定したチケット（Issue）の詳細を返します。

### 主なパラメータ

| パラメータ名 | 説明                         | 例                   |
| ------------ | ---------------------------- | -------------------- |
| include      | 関連情報をカンマ区切りで指定 | attachments,journals |

指定可能なinclude:  
`children`, `attachments`, `relations`, `changesets`, `journals`, `watchers`, `allowed_statuses`

### リクエスト例

```
GET /issues/2.json?include=attachments,journals
```

### curl例

```bash
curl -H "X-Redmine-API-Key: YOUR_API_KEY" -X GET "http://your-redmine-instance/issues/2.json?include=attachments,journals"
```

---

## POST /issues

### 概要

新しいチケット（Issue）を作成します。

### 主なパラメータ

| パラメータ名     | 説明                           | 例      |
| ---------------- | ------------------------------ | ------- |
| project_id       | プロジェクトID                 | 1       |
| tracker_id       | トラッカーID                   | 1       |
| status_id        | ステータスID                   | 1       |
| priority_id      | 優先度ID                       | 4       |
| subject          | 件名                           | Example |
| description      | 詳細説明                       | ...     |
| category_id      | カテゴリID                     | 2       |
| fixed_version_id | 対象バージョンID               | 3       |
| assigned_to_id   | 担当者ID                       | 5       |
| parent_issue_id  | 親チケットID                   | 10      |
| custom_fields    | カスタムフィールド             | ...     |
| watcher_user_ids | ウォッチャーのユーザーIDリスト | [1,2,3] |
| is_private       | プライベートチケットか         | true    |
| estimated_hours  | 予定工数（時間）               | 2.5     |

### リクエスト例

```json
POST /issues.json
{
  "issue": {
    "project_id": 1,
    "subject": "Example",
    "priority_id": 4
  }
}
```

### curl例

```bash
curl -H "X-Redmine-API-Key: YOUR_API_KEY" -H "Content-Type: application/json" -X POST -d '{"issue":{"project_id":1,"subject":"Example","priority_id":4}}' http://your-redmine-instance/issues.json
```

### レスポンス

- `201 Created`: チケットが作成されました
- `422 Unprocessable Entity`: バリデーションエラー

---

## PUT /issues/:id

### 概要

指定したチケット（Issue）を更新します。

### 主なパラメータ

POST /issuesと同様。加えて下記が利用可能です。

| パラメータ名  | 説明                       | 例                        |
| ------------- | -------------------------- | ------------------------- |
| notes         | 更新内容のコメント         | "The subject was changed" |
| private_notes | コメントを非公開にする場合 | true                      |

### リクエスト例

```json
PUT /issues/2.json
{
  "issue": {
    "subject": "Subject changed",
    "notes": "The subject was changed"
  }
}
```

### curl例

```bash
curl -H "X-Redmine-API-Key: YOUR_API_KEY" -H "Content-Type: application/json" -X PUT -d '{"issue":{"subject":"Subject changed","notes":"The subject was changed"}}' http://your-redmine-instance/issues/2.json
```

### 設計・実装方針

- fastmcpのToolとして実装する
- APIクライアントはRedmineAPIClientを利用する
- パラメータはNoneを除外し、必要なもののみリクエストボディに含める
- 404エラー時は空辞書を返す
- その他のHTTPエラーは例外送出
- レスポンスはAPIの返却内容をそのまま返す（204の場合はsuccessのみ返す）
- PEP8・GoogleスタイルDocstring・英語コメントを徹底する

---

## DELETE /issues/:id

### 概要

指定したチケット（Issue）を削除します。

### リクエスト例

```
DELETE /issues/2.json
```

### curl例

```bash
curl -H "X-Redmine-API-Key: YOUR_API_KEY" -X DELETE http://your-redmine-instance/issues/2.json
```

### レスポンス

- `204 No Content`: チケットが削除されました

---

## POST /issues/:id/watchers

### 概要

指定したチケットにウォッチャー（監視者）を追加します。

### 主なパラメータ

| パラメータ名 | 説明                 | 例  |
| ------------ | -------------------- | --- |
| user_id      | 追加するユーザーのID | 5   |

### リクエスト例

```json
POST /issues/2/watchers.json
{
  "user_id": 5
}
```

### curl例

```bash
curl -H "X-Redmine-API-Key: YOUR_API_KEY" -H "Content-Type: application/json" -X POST -d '{"user_id":5}' http://your-redmine-instance/issues/2/watchers.json
```

---

## DELETE /issues/:id/watchers/:user_id

### 概要

指定したチケットからウォッチャー（監視者）を削除します。

### リクエスト例

```
DELETE /issues/2/watchers/5.json
```

### curl例

```bash
curl -H "X-Redmine-API-Key: YOUR_API_KEY" -X DELETE http://your-redmine-instance/issues/2/watchers/5.json
```

### レスポンス

- `204 No Content`: ウォッチャーが削除されました

---

## 備考

- 添付ファイルの追加は [Rest API: Attaching files](https://www.redmine.org/projects/redmine/wiki/Rest_api#Attaching-files) を参照
- カスタムフィールドの扱いは [Rest API: Custom fields](https://www.redmine.org/projects/redmine/wiki/Rest_api#Working-with-custom-fields) を参照
- 本ドキュメントは [Redmine公式Rest Issuesドキュメント](https://www.redmine.org/projects/redmine/wiki/Rest_Issues) を参考に作成しています
