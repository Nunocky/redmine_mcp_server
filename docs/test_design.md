# テスト実装方針

- テストは pytest を使用する。
- モックオブジェクトは使わない。実際に Redmineサーバにアクセスして機能を検証する。
- REDMINE_URL, REDMINE_API_KEY, REDMINE_PROJECT_ID は環境変数から取得する。
- 各ツールの機能は tests/ 以下のカテゴリのディレクトリに分ける。
- MCPサーバに対するテストは tests 直下に配置する。
  - レスポンスは標準エラー出力に出力する。