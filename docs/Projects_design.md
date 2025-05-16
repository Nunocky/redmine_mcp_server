# Projects API設計書

## API仕様詳細

### GET /projects

- **説明**: プロジェクトの一覧を返します。
- **パラメータ**:
  - `include`: 関連情報をカンマ区切りで指定（例: trackers, issue_categories, enabled_modules, time_entry_activities, issue_custom_fields）
  - `limit`: 取得するプロジェクトの最大数
  - `offset`: 取得するプロジェクトのオフセット
- **例**:
  - `/projects.xml?include=trackers,enabled_modules&limit=10&offset=0`
- **curl 例**:

  ```bash
  curl -H "X-Redmine-API-Key: YOUR_API_KEY" -X GET "http://your-redmine-instance/projects.xml?include=trackers,enabled_modules&limit=10&offset=0"
  ```

### GET /projects/:id

- **説明**: 特定のプロジェクトの詳細を返します。
- **パラメータ**:
  - `id` または `identifier`: プロジェクトIDまたは識別子
  - `include`: 関連情報をカンマ区切りで指定
- **例**:
  - `/projects/12.xml?include=trackers,issue_categories`
  - `/projects/redmine.xml`
- **curl 例**:

  ```bash
  curl -H "X-Redmine-API-Key: YOUR_API_KEY" -X GET "http://your-redmine-instance/projects/12.xml?include=trackers,issue_categories"
  ```

### POST /projects

- **説明**: プロジェクトを作成します。
- **パラメータ**:
  - `project`: プロジェクト属性のハッシュ（name, identifier, description, homepage, is_public, parent_id, など）
- **例**:
  - XML:

    ```xml
    <project>
      <name>Example name</name>
      <identifier>example_name</identifier>
      <description>Example project</description>
      <is_public>true</is_public>
    </project>
    ```

  - JSON:

    ```json
    {
      "project": {
        "name": "Example name",
        "identifier": "example_name",
        "description": "Example project",
        "is_public": true
      }
    }
    ```

- **レスポンス**:
  - `201 Created`: プロジェクトが作成されました。
  - `422 Unprocessable Entity`: バリデーションエラー
- **curl 例**:

  ```bash
  curl -H "X-Redmine-API-Key: YOUR_API_KEY" -H "Content-Type: application/xml" -X POST -d '<project><name>Example name</name><identifier>example_name</identifier></project>' http://your-redmine-instance/projects.xml
  ```

  または JSON:

  ```bash
  curl -H "X-Redmine-API-Key: YOUR_API_KEY" -H "Content-Type: application/json" -X POST -d '{"project":{"name":"Example name","identifier":"example_name"}}' http://your-redmine-instance/projects.json
  ```

### PUT /projects/:id

- **説明**: プロジェクトを更新します。
- **パラメータ**:
  - `id` または `identifier`: プロジェクトIDまたは識別子
  - `project`: 更新する属性
- **例**:
  - `/projects/12.xml`
- **curl 例**:

  ```bash
  curl -H "X-Redmine-API-Key: YOUR_API_KEY" -H "Content-Type: application/xml" -X PUT -d '<project><description>Updated description</description></project>' http://your-redmine-instance/projects/12.xml
  ```

### PUT /projects/:id/archive

- **説明**: プロジェクトをアーカイブします（Redmine 5.0以降）。
- **パラメータ**:
  - `id` または `identifier`: プロジェクトIDまたは識別子
- **例**:
  - `/projects/12/archive.xml`
- **curl 例**:

  ```bash
  curl -H "X-Redmine-API-Key: YOUR_API_KEY" -X PUT http://your-redmine-instance/projects/12/archive.xml
  ```

### PUT /projects/:id/unarchive

- **説明**: プロジェクトのアーカイブを解除します（Redmine 5.0以降）。
- **パラメータ**:
  - `id` または `identifier`: プロジェクトIDまたは識別子
- **例**:
  - `/projects/12/unarchive.xml`
- **curl 例**:

  ```bash
  curl -H "X-Redmine-API-Key: YOUR_API_KEY" -X PUT http://your-redmine-instance/projects/12/unarchive.xml
  ```

### DELETE /projects/:id

- **説明**: プロジェクトを削除します。
- **パラメータ**:
  - `id` または `identifier`: プロジェクトIDまたは識別子
- **例**:
  - `/projects/12.xml`
- **レスポンス**:
  - `204 No Content`: プロジェクトが削除されました。
- **curl 例**:

  ```bash
  curl -H "X-Redmine-API-Key: YOUR_API_KEY" -X DELETE http://your-redmine-instance/projects/12.xml
  ```

---

## 設計書

### 概略

RedmineのProjects APIに対応したPythonクライアントツールをtools/配下に実装する。
各機能ごとにツールを分割し、テストはtests/配下に同名ファイルで作成する。

### 機能設計

- get_projects_tool.py: プロジェクト一覧取得
- get_project_tool.py: プロジェクト詳細取得
- create_project_tool.py: プロジェクト作成
- update_project_tool.py: プロジェクト更新
- archive_project_tool.py: プロジェクトアーカイブ
- unarchive_project_tool.py: プロジェクトアーカイブ解除
- delete_project_tool.py: プロジェクト削除

### クラス構成

- RedmineAPIClient
  - APIリクエスト共通処理（認証、リクエスト送信、エラーハンドリング）
- 各ツール（例: GetProjectsTool）
  - RedmineAPIClientを利用し、各APIエンドポイントに対応

### ディレクトリ構成（予定）

```text
tools/
  get_projects_tool.py
  get_project_tool.py
  create_project_tool.py
  update_project_tool.py
  archive_project_tool.py
  unarchive_project_tool.py
  delete_project_tool.py
tests/
  test_get_projects_tool.py
  test_get_project_tool.py
  test_create_project_tool.py
  test_update_project_tool.py
  test_archive_project_tool.py
  test_unarchive_project_tool.py
  test_delete_project_tool.py
```

### テスト

- pytestを用い、正常系・異常系のテストを実装
- モックを活用し、Redmineサーバーがなくてもテスト可能とする
