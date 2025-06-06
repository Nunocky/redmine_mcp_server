# News API 仕様書

## ✅ 実行項目リスト

- [x] API仕様の解析（news_api.htmlより）
- [x] 設計仕様書の修正案作成
- [x] コード・テスト実装
- [x] テスト実行・確認

---

## 1. 要件定義

Redmineのニュース情報を取得するためのAPIを提供する。  
プロジェクトを指定しない場合は全てのプロジェクトのニュースを、プロジェクトを指定した場合はそのプロジェクトのニュースを取得できるようにする。

---

## 2. 設計書

### 2.1. 概略設計

RedmineのREST APIを利用してニュース情報を取得する。  
以下の2つのエンドポイントを提供する。

- 全プロジェクトのニュースを取得
- 指定したプロジェクトのニュースを取得

---

### 2.2. APIリファレンス

#### 2.2.1. 全プロジェクトニュース取得機能

- **エンドポイント**: `/news.:format`
- **HTTPメソッド**: GET
- **説明**: 全てのプロジェクトに登録されているニュースをページネーション付きで取得する
- **リクエストパラメータ**:
    - `format`: レスポンス形式 (xml, jsonなど)
    - `offset`: 取得開始位置 (ページネーション用、任意)
    - `limit`: 取得件数 (ページネーション用、任意、デフォルト25)
- **レスポンス**:
    - ニュースの配列
    - 各ニュースには以下の情報が含まれる:
        - `id`: ニュースID
        - `project`: プロジェクト情報 (name, id)
        - `author`: 作成者情報 (name, id)
        - `title`: タイトル
        - `summary`: 概要
        - `description`: 詳細
        - `created_on`: 作成日時
    - ページネーション情報: `limit`, `total_count`, `offset`
- **レスポンス例 (XML)**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<news type="array" limit="25" total_count="X" offset="0">
  <news>
    <id>...</id>
    <project name="..." id="..."/>
    <author name="..." id="..."/>
    <title>...</title>
    <summary/>
    <description>...</description>
    <created_on>...</created_on>
  </news>
  ...
</news>
- **エラー例**:
    - 不正なproject_id: `ValueError` が発生し、メッセージ「Invalid project_id」が返される
    - 不正なパラメータ: 400 Bad Request
    - Redmine API接続失敗: 502 Bad Gateway

---

#### 2.2.2. プロジェクト指定ニュース取得機能

- **エンドポイント**: `/projects/:project_id/news.:format`
- **HTTPメソッド**: GET
- **説明**: 指定されたプロジェクトIDまたは識別子に登録されているニュースをページネーション付きで取得する
- **リクエストパラメータ**:
    - `project_id`: プロジェクトIDまたは識別子 (必須)
    - `format`: レスポンス形式 (xml, jsonなど)
    - `offset`: 取得開始位置 (ページネーション用、任意)
    - `limit`: 取得件数 (ページネーション用、任意、デフォルト25)
- **レスポンス**:
    - ニュースの配列
    - 各ニュースには以下の情報が含まれる:
        - `id`: ニュースID
        - `project`: プロジェクト情報 (name, id)
        - `author`: 作成者情報 (name, id)
        - `title`: タイトル
        - `summary`: 概要
        - `description`: 詳細
        - `created_on`: 作成日時
    - ページネーション情報: `limit`, `total_count`, `offset`
- **レスポンス例 (XML)**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<news type="array" limit="25" total_count="2" offset="0">
  <news>
    <id>54</id>
    <project name="Redmine" id="1"/>
    <author name="Jean-Philippe Lang" id="1"/>
    <title>Redmine 1.1.3 released</title>
    <summary/>
    <description>Redmine 1.1.3 has been released</description>
    <created_on>2011-04-29T14:00:25+02:00</created_on>
  </news>
  <news>
    <id>53</id>
    <project name="Redmine" id="1"/>
    <author name="Jean-Philippe Lang" id="1"/>
    <title>Redmine 1.1.2 bug/security fix released</title>
    <summary/>
    <description>Redmine 1.1.2 has been released</description>
    <created_on>2011-03-07T21:07:03+01:00</created_on>
  </news>
</news>
```
- **エラー例**:
    - 不正なproject_id: 404 Not Found
    - 不正なパラメータ: 400 Bad Request
    - Redmine API接続失敗: 502 Bad Gateway

---

### 2.3. クラス構成

Redmine APIクライアントライブラリ (例: `python-redmine`) を利用することを想定。  
本API仕様書では特定のクラス構成は定義しない。

---

## 3. 機能仕様書

### 3.1. 機能一覧

| No. | 機能名                       | 概要                                                     |
| --- | ---------------------------- | -------------------------------------------------------- |
| 1   | 全プロジェクトニュース取得   | Redmineに登録されている全てのニュースを取得する。        |
| 2   | プロジェクト指定ニュース取得 | 指定したプロジェクトに登録されているニュースを取得する。 |

---

### 3.2. 機能詳細

#### 3.2.1. 全プロジェクトニュース取得

- **ID**: NEWS-001
- **機能名**: 全プロジェクトニュース取得
- **概要**: Redmineシステム内の全プロジェクトからニュース記事を取得する。
- **ユースケース**:
    - システム全体の最新情報を一覧表示する。
    - 複数のプロジェクトを横断してニュースを検索・分析する。
- **入力**:
    - (任意) `offset`: 取得開始オフセット（数値）
    - (任意) `limit`: 取得件数（数値）
    - (任意) `format`: 出力形式（`xml` または `json`）
- **出力**:
    - ニュース記事のリスト。各記事には以下の情報が含まれる:
        - ニュースID
        - プロジェクト名とID
        - 作成者名とID
        - タイトル
        - 概要 (存在する場合)
        - 詳細説明
        - 作成日時
    - 取得件数 (`limit`)
    - 総件数 (`total_count`)
    - オフセット (`offset`)
- **処理フロー**:
    1. APIリクエスト `/news.:format` を受信する。
    2. (任意) `offset`, `limit` パラメータを解釈する。
    3. Redmineデータベースから全てのニュースを取得する。
    4. 指定されたフォーマットでレスポンスを生成する。
- **エラー処理**:
    - Redmine APIへの接続に失敗した場合、エラーを返す。
    - 不正なパラメータが指定された場合、エラーを返す。
- **制限事項**:
    - 一度に取得できる件数には上限がある場合がある (Redmine側の設定による)。

---

#### 3.2.2. プロジェクト指定ニュース取得

- **ID**: NEWS-002
- **機能名**: プロジェクト指定ニュース取得
- **概要**: 特定のプロジェクトIDまたは識別子を指定して、そのプロジェクトのニュース記事を取得する。
- **ユースケース**:
    - 特定のプロジェクトの最新情報を表示する。
    - プロジェクトごとのニュースフィードを作成する。
- **入力**:
    - `project_id`: プロジェクトIDまたは識別子（必須）
    - (任意) `offset`: 取得開始オフセット（数値）
    - (任意) `limit`: 取得件数（数値）
    - (任意) `format`: 出力形式（`xml` または `json`）
- **出力**:
    - 指定されたプロジェクトのニュース記事のリスト。各記事には以下の情報が含まれる:
        - ニュースID
        - プロジェクト名とID
        - 作成者名とID
        - タイトル
        - 概要 (存在する場合)
        - 詳細説明
        - 作成日時
    - 取得件数 (`limit`)
    - 総件数 (`total_count`)
    - オフセット (`offset`)
- **処理フロー**:
    1. APIリクエスト `/projects/:project_id/news.:format` を受信する。
    2. `project_id` パラメータを解釈する。
    3. (任意) `offset`, `limit` パラメータを解釈する。
    4. Redmineデータベースから指定されたプロジェクトのニュースを取得する。
    5. 指定されたフォーマットでレスポンスを生成する。
- **エラー処理**:
    - Redmine APIへの接続に失敗した場合、エラーを返す。
    - 指定された `project_id` が存在しない場合、エラーを返す。
    - 不正なパラメータが指定された場合、エラーを返す。
- **制限事項**:
    - 一度に取得できる件数には上限がある場合がある (Redmine側の設定による)。
