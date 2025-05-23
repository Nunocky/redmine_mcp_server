# IssueCategoriesツール設計書

## 1. 要件定義

### 概要
Redmineの課題カテゴリ（Issue Categories）情報を取得するツールを実装する。  
Redmine REST API `/projects/:project_id/issue_categories.json` を利用し、指定プロジェクトの課題カテゴリ一覧を取得する。

### 機能要件
- 指定したRedmineプロジェクトの課題カテゴリ一覧を取得できること
- 必須入力：`redmine_url`, `api_key`, `project_id`
- 取得結果はAPIレスポンス（JSON）をそのまま返却する
- 404エラー時は空リストを返却する
- その他のHTTPエラー時は例外を送出する

### 非機能要件
- PEP8準拠
- GoogleスタイルDocstring
- コメントは英語
- ruffによる自動整形対応
- テストはモックを使わず実APIで行う

## 2. API仕様

### 関数: get_issue_categories

| 引数        | 型  | 必須 | 説明                       |
| ----------- | --- | ---- | -------------------------- |
| redmine_url | str | ○    | RedmineサーバのURL         |
| api_key     | str | ○    | Redmine APIキー            |
| project_id  | str | ○    | プロジェクトIDまたは識別子 |

- 戻り値: dict（課題カテゴリ一覧、APIレスポンスそのまま）
- 404: 空リスト返却
- その他: 例外送出

### ツール: GetIssueCategoriesTool
- 上記関数をToolとして登録

## 3. ディレクトリ構成

```
tools/
└── IssueCategories/
    ├── get_issue_categories.py
    └── GetIssueCategoriesTool.py
tests/
└── IssueCategories/
    └── test_get_issue_categories_tool.py
docs/
└── IssueCategories_design.md
```

## 4. 実装手順

1. 本設計書（docs/IssueCategories_design.md）作成
2. `tools/IssueCategories/get_issue_categories.py`  
   - RedmineAPIClientを用いたAPI関数を実装
3. `tools/IssueCategories/GetIssueCategoriesTool.py`  
   - 上記関数をToolとして登録
4. テストコード `tests/IssueCategories/test_get_issue_categories_tool.py` を作成
5. 必要に応じて `__init__.py` 追加
6. ドキュメント修正・追記

## 5. テスト方針

- 実APIを用いた正常系・異常系テスト
- モックは使用しない
- 404時の空リスト返却を確認

## 6. 備考

- 実装・テスト時に追加要件があれば設計書を随時更新する
