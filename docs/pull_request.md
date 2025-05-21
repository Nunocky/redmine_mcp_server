# プルリクエスト作成指針

## PR作成時

- PRを要望されたら、gitコマンドで差分を確認したうえで、`gh pr` コマンドを使ってPRを作成してください
- PRの descriptionは [[.github/pull_request_template.md]] を読み取ってフォーマットを合わせてください。**これは絶対です**


## PRレビュー時

以下の手順でファイルごとにコメントを付けてください：

1. チェックする観点は .github/pull_request_template.md を参照してください。
2. PRの差分を確認:

```bash
gh pr diff <PR番号>
```

3. ファイルごとに、変更後のファイル全体とPRの差分を確認した上でレビューコメントを追加:

```bash
   gh api repos/<owner>/<repo>/pulls/<PR番号>/comments \
     -F body="レビューコメント" \
     -F commit_id="$(gh pr view <PR番号> --json headRefOid --jq .headRefOid)" \
     -F path="対象ファイルのパス" \
     -F position=<diffの行番号>
```

パラメータの説明：

- position: diffの行番号（新規ファイルの場合は1から開始）
- commit_id: PRの最新のコミットIDを自動取得
