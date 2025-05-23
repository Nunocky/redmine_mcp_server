# Redmine MCPツール CustomFields 設計書

## 1. 要件定義書

- RedmineのREST API `/custom_fields.json` を利用し、全カスタムフィールド定義を取得するMCPツールを作成する。
- 管理者権限のAPIキーが必要。
- MCPツールは `tools/CustomFields/` 配下にAPI関数・ツールクラスとして実装する。
- 取得したカスタムフィールド情報は外部システム連携や管理画面等で利用可能とする。

## 2. 概略設計・機能設計

### 機能概要

- Redmineの全カスタムフィールド定義を取得し、JSON形式で返却する。
- 必須入力: `redmine_url` (str), `api_key` (str)
- 出力: カスタムフィールド定義リスト

### API仕様

- エンドポイント: `GET /custom_fields.json`
- パラメータ: なし（APIキー必須）
- レスポンス例:
  ```json
  {
    "custom_fields": [
      {
        "id": 1,
        "name": "Affected version",
        "customized_type": "issue",
        "field_format": "list",
        "regexp": null,
        "min_length": null,
        "max_length": null,
        "is_required": true,
        "is_filter": true,
        "searchable": true,
        "multiple": true,
        "default_value": null,
        "visible": false,
        "possible_values": [
          {"value": "0.5.x"},
          {"value": "0.6.x"}
        ]
      }
    ]
  }
  ```

- 属性詳細:
    - `id`: カスタムフィールドID
    - `name`: フィールド名
    - `customized_type`: 適用対象（例: issue, project, time_entry）
    - `field_format`: フィールド形式（例: list, string, int）
    - その他: `regexp`, `min_length`, `max_length`, `is_required`, `is_filter`, `searchable`, `multiple`, `default_value`, `visible`, `possible_values`

### ユースケース

- Redmineのカスタムフィールド一覧を取得し、外部システムや管理画面で利用する。

## 3. クラス構成

```
tools/
└── CustomFields/
    ├── get_custom_fields.py         # APIクライアント関数
    └── GetCustomFieldsTool.py      # MCPツール定義
```

- `get_custom_fields.py`: RedmineAPIClientを利用し、APIからデータ取得
- `GetCustomFieldsTool.py`: MCPツールとしてTool.from_functionでツール定義

## 4. 実装手順

1. `tools/CustomFields/get_custom_fields.py` にAPIクライアント関数を実装
2. `tools/CustomFields/GetCustomFieldsTool.py` にMCPツール定義を実装
3. `tests/CustomFields/test_get_custom_fields_tool.py` を作成し、正常系・異常系テストを実施
4. 本設計書を `docs/CustomFields_design.md` として保存

## 5. テスト方針

- 正常系: 管理者APIキーで全カスタムフィールドが取得できること
- 異常系: 権限不足・APIキー不正時のエラー応答を確認

---
