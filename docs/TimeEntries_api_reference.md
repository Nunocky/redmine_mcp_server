# TimeEntries API仕様書

## 実装項目リスト

- [ ] 一覧取得API(GET /time_entries)
- [ ] 単一取得API(GET /time_entries/[id])
- [ ] 作成API(POST /time_entries)
- [ ] 更新API(PUT /time_entries/[id])
- [ ] 削除API(DELETE /time_entries/[id])

---

## 概要

TimeEntries APIは、Redmineの工数(TimeEntry)情報の取得・作成・更新・削除を行うREST APIです。

---

## エンドポイント一覧

| メソッド | パス               | 概要         |
| -------- | ------------------ | ------------ |
| GET      | /time_entries      | 工数一覧取得 |
| GET      | /time_entries/[id] | 工数単一取得 |
| POST     | /time_entries      | 工数作成     |
| PUT      | /time_entries/[id] | 工数更新     |
| DELETE   | /time_entries/[id] | 工数削除     |

---

## 詳細仕様

### 1. 工数一覧取得

- **エンドポイント**: `GET /time_entries`
- **パラメータ**:
  - `offset` (int, 任意): 取得開始位置
  - `limit` (int, 任意): 取得件数
  - `user_id` (int, 任意): ユーザーIDで絞り込み
  - `project_id` (int or str, 任意): プロジェクトIDまたは識別子で絞り込み
  - `spent_on` (str, 任意): 日付で絞り込み (例: 2020-12-24)
  - `from` (str, 任意): 開始日 (例: 2019-01-01)
  - `to` (str, 任意): 終了日 (例: 2019-01-03)
- **レスポンス**: 工数(TimeEntry)のリスト

---

### 2. 工数単一取得

- **エンドポイント**: `GET /time_entries/[id]`
- **パラメータ**: なし
- **レスポンス**: 指定IDの工数(TimeEntry)情報

---

### 3. 工数作成

- **エンドポイント**: `POST /time_entries`
- **パラメータ**:
  - `time_entry` (必須, オブジェクト)
    - `issue_id` (int, 任意): チケットID
    - `project_id` (int, 任意): プロジェクトID (issue_idとどちらか必須)
    - `spent_on` (str, 任意): 工数日付 (YYYY-MM-DD, デフォルトは当日)
    - `hours` (float, 必須): 工数時間
    - `activity_id` (int, 任意): 作業分類ID (Redmineの設定による)
    - `comments` (str, 任意): コメント(255文字以内)
    - `user_id` (int, 任意): 他ユーザーの代理登録時に指定
- **レスポンス**:
  - `201 Created`: 作成成功
  - `422 Unprocessable Entity`: バリデーションエラー(エラーメッセージ含む)

---

### 4. 工数更新

- **エンドポイント**: `PUT /time_entries/[id]`
- **パラメータ**:
  - `time_entry` (必須, オブジェクト)
    - (作成時と同じ)
- **レスポンス**:
  - `204 No Content`: 更新成功
  - `422 Unprocessable Entity`: バリデーションエラー(エラーメッセージ含む)

---

### 5. 工数削除

- **エンドポイント**: `DELETE /time_entries/[id]`
- **パラメータ**: なし
- **レスポンス**: 削除結果

---

## 備考

- project_idは数値IDまたは文字列識別子のいずれも利用可能
- activity_idはRedmineの設定で必須となる場合がある
- spent_onのフォーマットはYYYY-MM-DD
- バリデーションエラー時は422でエラー内容が返却される
