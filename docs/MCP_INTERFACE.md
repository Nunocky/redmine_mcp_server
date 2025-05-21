# MCPインターフェース ドキュメント

このサーバは [Model Context Protocol (MCP)](https://modelcontextprotocol.io/specification/2025-03-26) に準拠したAPIを提供します。

## サーバ情報
- サーバ名: `redmine-mcp-server`
- 説明: Redmine APIにアクセスするMCPサーバ

## 提供ツール

### get_issues
Redmineの課題一覧を取得します。

#### 引数
| 名前         | 型      | 必須 | 説明                                      |
|--------------|---------|------|-------------------------------------------|
| redmine_url  | string  | ○    | RedmineのベースURL（例: https://redmine.example.com） |
| api_key      | string  | ○    | RedmineのAPIキー                          |
| project_id   | string  | ×    | プロジェクトID（省略時は全プロジェクト）   |

#### 出力
| 名前   | 型    | 説明     |
|--------|-------|----------|
| issues | array | 課題一覧 |

- `issues`はRedmine APIの`/issues.json`エンドポイントのレスポンスと同等です。

## 参考
- [Redmine API](https://www.redmine.org/projects/redmine/wiki/Rest_api)
- [MCP Specification](https://modelcontextprotocol.io/specification/2025-03-26)
