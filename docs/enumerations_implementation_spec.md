# Enumerations API 実装仕様書

## 1. 概要

RedmineのEnumerations API（チケットの優先度、作業分類、文書カテゴリ）をMCPサーバーのツールとして実装する。
本文書は、各ツールの具体的な入力、出力、および処理フローを定義する。

## 2. 共通事項

- 各ツールは `tools.redmine_api_client.RedmineApiClient` を利用してRedmine APIにアクセスする。
- APIキー (`api_key`) とRedmineのURL (`redmine_url`) は必須パラメータとする。
- レスポンス形式 (`format`) はオプションとし、デフォルトは `json` とする。`xml` も選択可能とする。
- エラーハンドリング:
    - `format` パラメータが `json` または `xml` 以外の場合は `ValueError` を発生させる。
    - Redmine APIからのエラーレスポンスは、`RedmineApiClient` が適切に処理し、呼び出し元に例外を伝播させる。

## 3. ツール別仕様

### 3.1. GetIssuePrioritiesTool

- **機能**: チケットの優先度一覧を取得する。
- **ファイル**:
    - `tools/Enumerations/get_issue_priorities.py`
    - `tools/Enumerations/GetIssuePrioritiesTool.py`
- **入力 (Pydanticモデル: `GetIssuePrioritiesParams`)**:
    - `redmine_url: str`: RedmineサーバーのURL (例: `https://my.redmine.jp`)
    - `api_key: str`: Redmine APIキー
    - `format: Optional[str]`: レスポンス形式 (`json` または `xml`)。デフォルト: `json`
- **処理フロー (`get_issue_priorities`関数)**:
    1. `format` パラメータを検証する。不正な場合は `ValueError` を送出する。
    2. Redmine APIのエンドポイントURLを構築する: `{redmine_url}/enumerations/issue_priorities.{format}`
    3. HTTPヘッダーを設定する:
        - `X-Redmine-API-Key`: `api_key`
        - `Content-Type`: `application/{format}`
    4. `RedmineApiClient.get()` を呼び出し、APIリクエストを実行する。
    5. APIレスポンスをそのまま返す。
- **出力**:
    - Redmine APIからのレスポンス (JSONまたはXML形式の文字列を含む辞書)
- **ツールクラス (`GetIssuePrioritiesTool`)**:
    - `name`: `get_issue_priorities`
    - `description`: "Redmineからチケットの優先度一覧を取得します"
    - `args_schema`: `GetIssuePrioritiesParams`
    - `_run` メソッド:
        1. `RedmineApiClient` のインスタンスを生成する。
        2. `get_issue_priorities` 関数を呼び出す。
        3. 結果を返す。

### 3.2. GetTimeEntryActivitiesTool

- **機能**: 作業分類の一覧を取得する。
- **ファイル**:
    - `tools/Enumerations/get_time_entry_activities.py`
    - `tools/Enumerations/GetTimeEntryActivitiesTool.py`
- **入力 (Pydanticモデル: `GetTimeEntryActivitiesParams`)**:
    - `redmine_url: str`: RedmineサーバーのURL
    - `api_key: str`: Redmine APIキー
    - `format: Optional[str]`: レスポンス形式 (`json` または `xml`)。デフォルト: `json`
- **処理フロー (`get_time_entry_activities`関数)**:
    1. `format` パラメータを検証する。
    2. Redmine APIのエンドポイントURLを構築する: `{redmine_url}/enumerations/time_entry_activities.{format}`
    3. HTTPヘッダーを設定する。
    4. `RedmineApiClient.get()` を呼び出し、APIリクエストを実行する。
    5. APIレスポンスをそのまま返す。
- **出力**:
    - Redmine APIからのレスポンス
- **ツールクラス (`GetTimeEntryActivitiesTool`)**:
    - `name`: `get_time_entry_activities`
    - `description`: "Redmineから作業分類の一覧を取得します"
    - `args_schema`: `GetTimeEntryActivitiesParams`
    - `_run` メソッド:
        1. `RedmineApiClient` のインスタンスを生成する。
        2. `get_time_entry_activities` 関数を呼び出す。
        3. 結果を返す。

### 3.3. GetDocumentCategoriesTool

- **機能**: 文書カテゴリの一覧を取得する。
- **ファイル**:
    - `tools/Enumerations/get_document_categories.py`
    - `tools/Enumerations/GetDocumentCategoriesTool.py`
- **入力 (Pydanticモデル: `GetDocumentCategoriesParams`)**:
    - `redmine_url: str`: RedmineサーバーのURL
    - `api_key: str`: Redmine APIキー
    - `format: Optional[str]`: レスポンス形式 (`json` または `xml`)。デフォルト: `json`
- **処理フロー (`get_document_categories`関数)**:
    1. `format` パラメータを検証する。
    2. Redmine APIのエンドポイントURLを構築する: `{redmine_url}/enumerations/document_categories.{format}`
    3. HTTPヘッダーを設定する。
    4. `RedmineApiClient.get()` を呼び出し、APIリクエストを実行する。
    5. APIレスポンスをそのまま返す。
- **出力**:
    - Redmine APIからのレスポンス
- **ツールクラス (`GetDocumentCategoriesTool`)**:
    - `name`: `get_document_categories`
    - `description`: "Redmineから文書カテゴリの一覧を取得します"
    - `args_schema`: `GetDocumentCategoriesParams`
    - `_run` メソッド:
        1. `RedmineApiClient` のインスタンスを生成する。
        2. `get_document_categories` 関数を呼び出す。
        3. 結果を返す。

## 4. `main.py` への登録

作成した各ツールクラス (`GetIssuePrioritiesTool`, `GetTimeEntryActivitiesTool`, `GetDocumentCategoriesTool`) を `main.py` の `TOOL_CLASSES` リストに追加する。
