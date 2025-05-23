# Files API 機能仕様書・実装計画書

## 1. 機能仕様書

### 1.1 ファイル一覧取得ツール（GetFilesTool）

- 機能: 指定したプロジェクトIDのファイル一覧を取得する
- 引数:
  - redmine_url: RedmineサーバのURL（必須）
  - api_key: Redmine APIキー（必須）
  - project_id: プロジェクトIDまたは識別子（必須）
- 出力: ファイル情報のリスト（id, filename, filesize, content_type, description, content_url, author, created_on, version, digest, downloads）
- エラー時: 404の場合は空リスト、その他は例外

### 1.2 ファイル登録ツール（CreateFileTool）

- 機能: 指定したプロジェクトに新規ファイルを登録する
- 引数:
  - redmine_url: RedmineサーバのURL（必須）
  - api_key: Redmine APIキー（必須）
  - project_id: プロジェクトIDまたは識別子（必須）
  - file:
    - token: /uploads APIで取得したファイルトークン（必須）
    - version_id: 紐づけるバージョンID（任意）
    - filename: ファイル名（任意）
    - description: 説明（任意）
- 出力: 登録したファイル情報（token, version_id, filename, description）
- エラー時: 例外

---

## 2. 実装計画書

### 2.1 ディレクトリ構成

- tools/Files/get_files.py
- tools/Files/GetFilesTool.py
- tools/Files/create_file.py
- tools/Files/CreateFileTool.py

### 2.2 実装手順

1. **get_files.py**  
   - RedmineAPIClientを利用し、GET /projects/:project_id/files.json を呼び出す関数 `get_files` を実装
   - 404時は {"files": []} を返す
2. **GetFilesTool.py**  
   - 上記関数をTool化し、引数・説明を付与
3. **create_file.py**  
   - RedmineAPIClientを利用し、POST /projects/:project_id/files.json を呼び出す関数 `create_file` を実装
   - fileパラメータのバリデーションを行う
4. **CreateFileTool.py**  
   - 上記関数をTool化し、引数・説明を付与
5. **テスト**  
   - tests/Files/test_get_files_tool.py, tests/Files/test_create_file_tool.py を作成し、正常系・異常系を検証
6. **設計書更新**  
   - 実装後、設計書・仕様書を必要に応じて修正

---

## 3. 注意事項

- ファイルアップロードは /uploads API で事前に行い、tokenを取得してから本APIを呼ぶ
- 添付ファイルAPI（tools/Attachments/）との混同に注意
- PEP8・GoogleスタイルDocstring・日本語コメント・ruff自動整形を遵守
