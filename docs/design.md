# Redmine MCP Server ツール設計指針

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
