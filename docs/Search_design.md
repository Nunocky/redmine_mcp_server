# Searchツール設計書

## 1. 要件定義

### 目的
Redmineの課題・プロジェクト等を対象に、キーワードや条件で横断的に検索できるAPIおよびツールを提供する。

### 機能要件

#### 1. 検索対象
- Redmineの以下リソースを対象とする
  - Issues（課題）
  - Projects（プロジェクト）
  - News（ニュース）
  - WikiPages（Wikiページ）
  - その他拡張可能

#### 2. 検索条件
- キーワード（部分一致・AND/OR指定）
- 検索対象リソースの指定（例: issuesのみ、projectsのみ等）
- 検索対象フィールドの指定（例: subject, description, notes等）
- ページネーション（offset, limit）

#### 3. レスポンス
- 検索結果リスト（各リソースのID, タイトル, 概要, URL等）
- 検索ヒット件数（total_count）
- ページネーション情報（offset, limit）

#### 4. エラー処理
- 必須パラメータ不足時のエラー
- Redmine APIエラー時のエラー返却

### 非機能要件
- PEP8準拠
- GoogleスタイルDocstring
- ruffによる自動整形
- ツールはtools/Search/配下に配置
- テストはtests/Search/配下に配置

## 2. 概略設計

### ディレクトリ構成
- tools/Search/search.py : 検索API本体
- tools/Search/SearchTool.py : Tool定義
- tests/Search/test_search_tool.py : テスト

### API仕様

#### 関数
```python
def search(
    redmine_url: str,
    api_key: str,
    query: str,
    resource_types: list[str] = None,
    fields: list[str] = None,
    offset: int = 0,
    limit: int = 20,
) -> dict:
    """Redmineリソース横断検索API"""
```

#### ツール
- Tool名: SearchTool
- 説明: Redmineリソース横断検索

### クラス構成
- 追加なし（関数ベース）

## 3. 実装方針

- RedmineAPIClientを利用し、各リソースのAPIを呼び出して検索を実現
- resource_typesで指定されたリソースのみ検索
- fieldsで指定されたフィールドのみを対象に部分一致検索
- 各リソースごとにAPIを呼び出し、結果をマージして返却
- ページネーション対応

## 4. テスト方針

- pytestによる自動テスト
- モックは使用せず、実際のRedmineサーバを利用
- 検索条件ごとの正常系・異常系テスト

## 5. 今後の拡張

- 検索対象リソースの追加
- AND/OR等の複雑な条件式対応
- 検索結果のソート指定
