# Redmine API

Redmineは一部のデータをREST API経由で公開しています。このAPIは、以下に記載するリソースに対する基本的なCRUD操作（作成・更新・削除）を提供します。APIは[XML](http://en.wikipedia.org/wiki/Xml)と[JSON](http://en.wikipedia.org/wiki/JSON)の両フォーマットをサポートしています。

## API概要

| リソース | ステータス | 備考 | 利用可能バージョン |
| --- | --- | --- | --- |
| [Issues](Rest_Issues) | Stable | | 1.0 |
| [Projects](Rest_Projects) | Stable | | 1.0 |
| [Project Memberships](Rest_Memberships) | Alpha | | 1.4 |
| [Users](Rest_Users) | Stable | | 1.1 |
| [Time Entries](Rest_TimeEntries) | Stable | | 1.1 |
| [News](Rest_News) | Prototype | @index@のみプロトタイプ実装 | 1.1 |
| [Issue Relations](Rest_IssueRelations) | Alpha | | 1.3 |
| [Versions](Rest_Versions) | Alpha | | 1.3 |
| [Wiki Pages](Rest_WikiPages) | Alpha | | 2.2 |
| [Queries](Rest_Queries) | Alpha | | 1.3 |
| [Attachments](Rest_Attachments) | Beta | API経由の添付追加は1.4で追加 | 1.3 |
| [Issue Statuses](Rest_IssueStatuses) | Alpha | 全ステータス一覧を提供 | 1.3 |
| [Trackers](Rest_Trackers) | Alpha | 全トラッカー一覧を提供 | 1.3 |
| [Enumerations](Rest_Enumerations) | Alpha | 優先度・作業分類一覧を提供 | 2.2 |
| [Issue Categories](Rest_IssueCategories) | Alpha | | 1.3 |
| [Roles](Rest_Roles) | Alpha | | 1.4 |
| [Groups](Rest_Groups) | Alpha | | 2.1 |
| [Custom Fields](Rest_CustomFields) | Alpha | | 2.4 |
| [Search](Rest_Search) | Alpha | | 3.3 |
| [Files](Rest_Files) | Alpha | | 3.4 |
| [My account](Rest_MyAccount) | Alpha | | 4.1 |
| [Journals](Rest_Journals) | Alpha | | 5.0 |

**ステータス凡例:**

- Stable: 機能完成、主要な変更予定なし
- Beta: 統合利用可能だが一部バグや小機能未実装
- Alpha: 主要機能あり、ユーザーからのフィードバック募集中
- Prototype: 粗い実装、バージョン途中で大きな変更の可能性あり（統合非推奨）
- Planned: 今後のバージョンで計画中

API各バージョンの変更点一覧は[こちら](/projects/redmine/issues?set_filter=1&status_id=c&fixed_version_id=*&category_id=32&c[]=tracker&c[]=subject&c[]=author&group_by=fixed_version&sort=fixed_version:desc,id)を参照。

## 一般トピック

### POST/PUTリクエスト時のContent-Type指定

リモート要素の作成・更新時は、URL末尾にフォーマットを付与しても**Content-Type**ヘッダーの指定が必須です。

- JSON: `Content-Type: application/json`
- XML: `Content-Type: application/xml`

### 認証

API利用時は認証が必要です。管理画面→設定→APIで「REST APIを有効化」してください。認証方法は以下の2通りです。

- HTTP Basic認証で通常のログイン/パスワードを利用
- APIキーを利用（リクエストにkeyパラメータ、ユーザー名、または`X-Redmine-API-Key`ヘッダーで指定）

APIキーはアカウントページ（/my/account）で確認できます。

### ユーザーなりすまし

Redmine 2.2.0以降、管理者アカウントで`X-Redmine-Switch-User`ヘッダーを指定することで他ユーザーになりすまし可能です。

例:  
`X-Redmine-Switch-User: jsmith`

該当ユーザーが存在しない場合や無効の場合は412エラーとなります。

### コレクションリソースとページネーション

GETリクエストでコレクションリソース（例: `/issues.xml`, `/users.xml`）を取得する際、全件は返りません。  
`offset`と`limit`パラメータで取得範囲を指定できます（デフォルト25件、最大100件）。

例:

```http
GET /issues.xml
=> 先頭25件取得

GET /issues.xml?limit=100
=> 先頭100件取得

GET /issues.xml?offset=30&limit=10
=> 30件目から10件取得
```

レスポンス例（XML）:

```xml
<issues type="array" total_count="2595" limit="25" offset="0">
  ...
</issues>
```

レスポンス例（JSON）:

```json
{ "issues":[...], "total_count":2595, "limit":25, "offset":0 }
```

`nometa`パラメータまたは`X-Redmine-Nometa`ヘッダーでメタ情報を省略可能。

### 関連データの取得

1.1.0以降、`include`パラメータで関連データを明示的に指定可能。

例:

```http
GET /issues/296.xml?include=journals
```

```xml
<issue>
  <id>296</id>
  ...
  <journals type="array">
    ...
  </journals>
</issue>
```

複数指定もカンマ区切りで可能。

### カスタムフィールドの扱い

多くのRedmineオブジェクトはカスタムフィールドをサポートします。値は`custom_fields`属性に含まれます。

XML例:

```xml
<issue>
  <id>296</id>
  ...
  <custom_fields type="array">
    <custom_field name="Affected version" id="1">
      <value>1.0.1</value>
    </custom_field>
    <custom_field name="Resolution" id="2">
      <value>Fixed</value>
    </custom_field>
  </custom_fields>
</issue>
```

JSON例:

```json
{
  "issue": {
    "id": 296,
    "custom_fields": [
      {
        "name": "Affected version",
        "id": 1,
        "value": "1.0.1"
      },
      {
        "name": "Resolution",
        "id": 2,
        "value": "Fixed"
      }
    ]
  }
}
```

...
