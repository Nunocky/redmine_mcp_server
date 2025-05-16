## 課題詳細取得API

### エンドポイント
GET /issues/{id}.json

### パラメータ
| 名前      | 型     | 必須 | 説明                         |
|-----------|--------|------|------------------------------|
| id        | int    | ○    | 取得対象の課題ID             |
| include   | str    | ×    | 追加情報（カンマ区切り）     |

### レスポンス例
```json
{
  "issue": {
    "id": 1,
    "project": { "id": 1, "name": "Redmine" },
    "tracker": { "id": 1, "name": "バグ" },
    "status": { "id": 1, "name": "新規" },
    "priority": { "id": 2, "name": "通常" },
    "author": { "id": 1, "name": "管理者" },
    "subject": "サンプル課題",
    "description": "詳細説明",
    "start_date": "2025-05-01",
    "due_date": null,
    "done_ratio": 0,
    "estimated_hours": null,
    "custom_fields": [],
    "created_on": "2025-05-01T12:00:00Z",
    "updated_on": "2025-05-01T12:00:00Z"
  }
}
```

### エラー例
- 存在しないIDの場合: 404 Not Found
