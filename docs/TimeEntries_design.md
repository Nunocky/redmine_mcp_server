# TimeEntries機能設計書

## 実装タスクチェックリスト

- [ ] 要件定義・API仕様確認
- [ ] MCPツール用APIクライアント関数実装
- [ ] MCPツールクラス実装（Tool継承）
- [ ] main.pyへの組み込み
- [ ] ユニットテスト作成（tools/TimeEntries, tests/TimeEntries）
- [ ] MCPサーバ統合テスト作成
- [ ] ドキュメント更新

---

## 1. 要件定義

- RedmineのTimeEntry（工数）情報をMCPツールとして操作可能にする
- 工数の一覧取得・単一取得・作成・更新・削除をサポート
- 必要なパラメータ・バリデーションはRedmine API仕様に準拠
- MCPサーバ経由で外部から呼び出し可能なツールとして提供
- テスト容易性・保守性を考慮した設計

---

## 2. 概略設計

- tools/TimeEntries/配下に各APIエンドポイントごとにツールクラスを実装
- main.pyでMCPツールとして登録
- テストはtests/TimeEntries/配下にAPIごとに作成

---

## 3. 機能設計

### 3.1 MCPツール

| ツール名               | 概要         | 引数例・備考                |
| ---------------------- | ------------ | --------------------------- |
| get_time_entries_tool  | 工数一覧取得 | offset, limit, user_id, ... |
| get_time_entry_tool    | 工数単一取得 | id                          |
| create_time_entry_tool | 工数作成     | time_entry(dict)            |
| update_time_entry_tool | 工数更新     | id, time_entry(dict)        |
| delete_time_entry_tool | 工数削除     | id                          |

### 3.2 パラメータ・バリデーション

- API仕様書（docs/TimeEntries_api_reference.md）に準拠
- 必須・任意パラメータ、型、バリデーション内容を明記

---

## 4. クラス構成

- tools/TimeEntries/get_time_entries_tool.py
- tools/TimeEntries/get_time_entry_tool.py
- tools/TimeEntries/create_time_entry_tool.py
- tools/TimeEntries/update_time_entry_tool.py
- tools/TimeEntries/delete_time_entry_tool.py

---

## 5. テスト設計

- tests/TimeEntries/test_get_time_entries_tool.py
- tests/TimeEntries/test_get_time_entry_tool.py
- tests/TimeEntries/test_create_time_entry_tool.py
- tests/TimeEntries/test_update_time_entry_tool.py
- tests/TimeEntries/test_delete_time_entry_tool.py

---

## 6. 備考

- PEP8/GoogleスタイルDocstring/英語コメント遵守
- ruffによる自動整形前提
- 既存のtools/Issues, tools/Projects等の実装・テストを参考にする

---

以上の設計内容で問題なければご指摘ください。修正要望がなければこの設計に基づき実装を進めます。
