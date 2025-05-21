# Redmine MCP Server ツール設計指針

## 機能の実装手順

1. API仕様の解析
   - docs以下にあるhtmlを解析してAPI仕様書を作成
2. 1をもとに設計仕様書を作成
   - ファイルの先頭にチェックボックス付きの実行項目リストを作る。実装が完了したらチェックを入れる。
3. 実装を行う。
   - まずAPIを実行するツール関数と Toolを継承したクラスの作成
   - それをMCPサーバから扱うための main.pyの実装
   - テストコードの作成
     - 環境変数 .env を読み込んで必要な情報を取得してから各種テストを実施すること。
     - ツール向けテストコードの作成
     - MCPサーバ化したときのテストの作成

実装の際に redmineにあらかじめデータを用意する必要があるときはユーザーに要求すること。

## Tool実装方針

各 APIは toolsディレクトリ下にカテゴリを作り、その下に実装する。

API一つにつき

- 関数
- 関数を使用するツール

を定義する。

### 例: get_newsとそのツール GetNewsTool

get_news.py

```py
def get_news(
    redmine_url: str,
    api_key: str,
    project_id: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
) -> Dict[str, Any]:
...
```

GetNewsTool.py

```py
from fastmcp.tools.tool import Tool

from tools.News.get_news import get_news

GetNewsTool = Tool.from_function(
    get_news,
    name="get_news",
    description="Get a list of news from Redmine.",
)
```

## テスト実装の指針

- テストは pytest を使用する。
- 各ツールのテストは tests/ 以下のカテゴリのディレクトリに分ける。
- テストでは *Toolを 使わない。必ずそこで用いられる get_news といった関数を使用する。
- REDMINE_URL, REDMINE_ADMIN_API_KEY, REDMINE_PROJECT_ID は環境変数から取得する。

## テスト実施のルール

- pytest実行のときには -s オプションをつけて、標準出力を表示すること。
