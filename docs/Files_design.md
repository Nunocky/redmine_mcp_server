# Files API設計書

## 1. 要件定義書

### 概要
RedmineのREST API「/projects/:project_id/files」エンドポイントをラップするツールを実装する。  
- プロジェクト単位で登録済みファイルの一覧取得（GET）
- プロジェクトへの新規ファイル登録（POST）

### 対象API
- GET /projects/:project_id/files.:format  
  プロジェクトに紐づくファイル一覧を取得
- POST /projects/:project_id/files.:format  
  プロジェクトにファイルを登録

### 想定ユースケース
- プロジェクトのリリースファイル一覧取得
- 新しいリリースファイルの登録

---

## 2. 機能仕様

### 2.1 ファイル一覧取得（GET）

- エンドポイント: `/projects/:project_id/files.:format`
- メソッド: GET
- パラメータ:
  - project_id: プロジェクトIDまたは識別子（必須）
  - redmine_url: RedmineサーバのURL（必須）
  - api_key: Redmine APIキー（必須）
- レスポンス:  
  - ファイル情報のリスト（id, filename, filesize, content_type, description, content_url, author, created_on, version, digest, downloads）

### 2.2 ファイル登録（POST）

- エンドポイント: `/projects/:project_id/files.:format`
- メソッド: POST
- パラメータ:
  - project_id: プロジェクトIDまたは識別子（必須）
  - redmine_url: RedmineサーバのURL（必須）
  - api_key: Redmine APIキー（必須）
  - file:  
    - token: アップロード済みファイルのトークン（必須、/uploads APIで取得）
    - version_id: 紐づけるバージョンID（任意）
    - filename: ファイル名（任意）
    - description: 説明（任意）
- レスポンス:  
  - 登録したファイル情報（token, version_id, filename, description）

---

## 3. クラス構成（案）

- tools/Files/get_files.py  
  - get_files(redmine_url, api_key, project_id)
- tools/Files/GetFilesTool.py  
  - GetFilesTool = Tool.from_function(get_files, ...)
- tools/Files/create_file.py  
  - create_file(redmine_url, api_key, project_id, file)
- tools/Files/CreateFileTool.py  
  - CreateFileTool = Tool.from_function(create_file, ...)

---

## 4. 補足

- ファイルのアップロード自体は /uploads APIで行い、tokenを取得してからPOSTする必要がある
- 添付ファイルAPI（tools/Attachments/）との違いに注意
