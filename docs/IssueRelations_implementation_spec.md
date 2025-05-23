# IssueRelations API 実装仕様書

## 1. 概要

Redmineの課題間リレーション（Issue Relations）APIをMCPサーバーのツールとして実装する。  
本仕様書は、課題リレーションの取得・作成・削除ツールの入力、出力、処理フロー、エラーハンドリング等を定義する。

## 2. 共通事項

- 各ツールは `tools.redmine_api_client.RedmineApiClient` を利用してRedmine APIにアクセスする。
- APIキー (`api_key`) とRedmineのURL (`redmine_url`) は必須パラメータとする。
- レスポンス形式 (`format`) はオプションで、デフォルトは `json`。`xml` も選択可能。
- エラーハンドリング:
    - `format` パラメータが `json` または `xml` 以外の場合は `ValueError` を発生させる。
    - Redmine APIからのエラーは `RedmineApiClient` が例外として伝播する。
    - 必須パラメータが不足している場合は `ValidationError` を発生させる。

## 3. ツール別仕様

### 3.1. GetIssueRelationsTool

- **機能**: 指定課題IDのリレーション一覧を取得する。
- **ファイル**:
    - `tools/Issues/get_issue_relations.py`
    - `tools/Issues/GetIssueRelationsTool.py`
- **入力 (Pydanticモデル: `GetIssueRelationsParams`)**:
    - `redmine_url: str`: RedmineサーバーのURL
    - `api_key: str`: Redmine APIキー
    - `issue_id: int`: 対象課題ID
    - `format: Optional[str]`: レスポンス形式（json/xml）。デフォルト: json
- **処理フロー (`get_issue_relations`関数)**:
    1. `format` パラメータを検証。不正な場合は `ValueError`。
    2. エンドポイントURLを構築: `{redmine_url}/issues/{issue_id}/relations.{format}`
    3. HTTPヘッダーを設定:
        - `X-Redmine-API-Key`: `api_key`
        - `Content-Type`: `application/{format}`
    4. `RedmineApiClient.get()` を呼び出しAPIリクエストを実行。
    5. レスポンスをそのまま返す。
- **出力**:
    - Redmine APIからのレスポンス（JSONまたはXML形式の辞書）
- **ツールクラス (`GetIssueRelationsTool`)**:
    - `name`: `get_issue_relations`
    - `description`: "Redmineから課題リレーション一覧を取得します"
    - `args_schema`: `GetIssueRelationsParams`
    - `_run` メソッド:
        1. `RedmineApiClient` インスタンス生成
        2. `get_issue_relations` 関数呼び出し
        3. 結果を返す

### 3.2. CreateIssueRelationTool

- **機能**: 指定課題IDにリレーションを新規作成する。
- **ファイル**:
    - `tools/Issues/create_issue_relation.py`
    - `tools/Issues/CreateIssueRelationTool.py`
- **入力 (Pydanticモデル: `CreateIssueRelationParams`)**:
    - `redmine_url: str`: RedmineサーバーのURL
    - `api_key: str`: Redmine APIキー
    - `issue_id: int`: 対象課題ID
    - `issue_to_id: int`: 関連先課題ID
    - `relation_type: str`: リレーション種別（relates, blocks, precedes等）
    - `delay: Optional[int]`: 遅延日数（precedes等の場合）
    - `format: Optional[str]`: レスポンス形式（json/xml）。デフォルト: json
- **処理フロー (`create_issue_relation`関数)**:
    1. `format` パラメータを検証。不正な場合は `ValueError`。
    2. エンドポイントURLを構築: `{redmine_url}/issues/{issue_id}/relations.{format}`
    3. HTTPヘッダーを設定。
    4. POSTボディを作成:
        ```json
        {
          "relation": {
            "issue_to_id": ...,
            "relation_type": ...,
            "delay": ... // 任意
          }
        }
        ```
    5. `RedmineApiClient.post()` を呼び出しAPIリクエストを実行。
    6. レスポンスをそのまま返す。
- **出力**:
    - Redmine APIからのレスポンス（作成したリレーション情報）
- **ツールクラス (`CreateIssueRelationTool`)**:
    - `name`: `create_issue_relation`
    - `description`: "Redmineに課題リレーションを新規作成します"
    - `args_schema`: `CreateIssueRelationParams`
    - `_run` メソッド:
        1. `RedmineApiClient` インスタンス生成
        2. `create_issue_relation` 関数呼び出し
        3. 結果を返す

### 3.3. DeleteIssueRelationTool

- **機能**: 指定リレーションIDのリレーションを削除する。
- **ファイル**:
    - `tools/Issues/delete_issue_relation.py`
    - `tools/Issues/DeleteIssueRelationTool.py`
- **入力 (Pydanticモデル: `DeleteIssueRelationParams`)**:
    - `redmine_url: str`: RedmineサーバーのURL
    - `api_key: str`: Redmine APIキー
    - `id: int`: 削除対象リレーションID
    - `format: Optional[str]`: レスポンス形式（json/xml）。デフォルト: json
- **処理フロー (`delete_issue_relation`関数)**:
    1. `format` パラメータを検証。不正な場合は `ValueError`。
    2. エンドポイントURLを構築: `{redmine_url}/relations/{id}.{format}`
    3. HTTPヘッダーを設定。
    4. `RedmineApiClient.delete()` を呼び出しAPIリクエストを実行。
    5. ステータス204の場合は空辞書を返す。
    6. それ以外はAPIレスポンスを返す。
- **出力**:
    - 削除成功時は空辞書、失敗時はエラー内容
- **ツールクラス (`DeleteIssueRelationTool`)**:
    - `name`: `delete_issue_relation`
    - `description`: "Redmineの課題リレーションを削除します"
    - `args_schema`: `DeleteIssueRelationParams`
    - `_run` メソッド:
        1. `RedmineApiClient` インスタンス生成
        2. `delete_issue_relation` 関数呼び出し
        3. 結果を返す

## 4. `main.py` への登録

作成した各ツールクラス（`GetIssueRelationsTool`, `CreateIssueRelationTool`, `DeleteIssueRelationTool`）を `main.py` の `TOOL_CLASSES` リストに追加すること。
