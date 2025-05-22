# Enumerations API 設計書

## 1. 要件定義書

RedmineのEnumerations APIは、Redmineシステム内で定義されている各種列挙型データを取得するためのインターフェースを提供する。
具体的には、以下の情報を取得できる必要がある。

- チケットの優先度 (Issue Priorities)
- 作業分類 (Time Entry Activities)
- 文書カテゴリ (Document Categories)

取得形式はXMLまたはJSONを選択できる。

## 2. 設計書

### 2.1. 概略

RedmineのEnumerations APIをMCPサーバーのツールとして実装する。
各列挙型データ取得に対応するツールを作成し、Redmine APIへのリクエストとレスポンス処理を行う。

### 2.2. 機能

以下の機能を提供する。

- **チケットの優先度一覧取得機能**
  - エンドポイント: `/enumerations/issue_priorities.:format`
  - HTTPメソッド: GET
  - 説明: チケットの優先度一覧を取得する。
  - レスポンス (XML例):
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <issue_priorities type="array">
      <issue_priority>
        <id>3</id>
        <name>Low</name>
        <is_default>false</is_default>
      </issue_priority>
      <issue_priority>
        <id>4</id>
        <name>Normal</name>
        <is_default>true</is_default>
      </issue_priority>
      ...
    </issue_priorities>
    ```
- **作業分類一覧取得機能**
  - エンドポイント: `/enumerations/time_entry_activities.:format`
  - HTTPメソッド: GET
  - 説明: 作業分類の一覧を取得する。
  - レスポンス (XML例):
    ```xml
    <time_entry_activities type="array">
      <time_entry_activity>
        <id>8</id>
        <name>Design</name>
        <is_default>false</is_default>
      </time_entry_activity>
      ...
    </time_entry_activities>
    ```
- **文書カテゴリ一覧取得機能**
  - エンドポイント: `/enumerations/document_categories.:format`
  - HTTPメソッド: GET
  - 説明: 文書カテゴリの一覧を取得する。
  - レスポンス (XML例):
    ```xml
    <document_categories type="array">
      <document_category>
        <id>1</id>
        <name>Uncategorized</name>
        <is_default>false</is_default>
      </document_category>
      <document_category>
        <id>2</id>
        <name>User documentation</name>
        <is_default>false</is_default>
      </document_category>
      <document_category>
        <id>3</id>
        <name>Technical documentation</name>
        <is_default>false</is_default>
      </document_category>
    </document_categories>
    ```

### 2.3. クラス構成案

各APIエンドポイントに対応するツールクラスを作成する。

- `GetIssuePrioritiesTool`
  - `redmine_url`: RedmineのURL
  - `api_key`: RedmineのAPIキー
  - `format`: レスポンス形式 (xml or json) - オプション、デフォルトはjson
- `GetTimeEntryActivitiesTool`
  - `redmine_url`: RedmineのURL
  - `api_key`: RedmineのAPIキー
  - `format`: レスポンス形式 (xml or json) - オプション、デフォルトはjson
- `GetDocumentCategoriesTool`
  - `redmine_url`: RedmineのURL
