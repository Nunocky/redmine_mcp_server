# Redmine MCP Server ツール設計指針

## 機能の実装手順


- 実装方針: tools/IssueStatuses/GetIssueStatusesTool.py と同様に、Tool.from_function で get_trackers 関数をラップして GetTrackersTool を生成する


## Tool実装方針

各 APIは toolsディレクトリ下にカテゴリを作り、その下に実装する。

API一つにつき

- 関数
- 関数を使用するツール

を定義する。

1. docs から 関連する html ファイルを読み、API仕様書、実装仕様書を作成
2. それらを元に ツール、及びそれで使用する関数を実装する
   1. ツールは TrackerToolなどのように、最後に Toolを付けた名前とする。
   2. ツールは以下の GetNewsToolのように、Tool.from_function を利用して実装する。
3. 関数を評価するテストコードを実装する。テストは pytestで確認すること。
4. すべてが完了したら main.py に ツールを登録する。


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
- 必須の環境変数が設定されていないときはテストを failすること
- テストコードにおいてモックオブジェクトは作らないこと

## テスト実施のルール

- pytest実行のときには -s オプションをつけて、標準出力を表示すること。
