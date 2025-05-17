# Project Memberships API Reference

## /projects/:project_id/memberships.:format

### GET

プロジェクトのメンバーシップのページ分割されたリストを返します。`:project_id` はプロジェクトの数値IDまたはプロジェクト識別子のいずれかです。

**例:**

```
GET /projects/1/memberships.xml
GET /projects/redmine/memberships.xml
```

**レスポンス:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<memberships type="array" limit="25" offset="0" total_count="3">
  <membership>
    <id>1</id>
    <project name="Redmine" id="1"/>
    <user name="David Robert" id="17"/>
    <roles type="array">
      <role name="Manager" id="1"/>
    </roles>
  </membership>
  <membership>
    <id>3</id>
    <project name="Redmine" id="1"/>
    <group name="Contributors" id="24"/>
    <roles type="array">
      <role name="Contributor" id="3"/>
    </roles>
  </membership>
  <membership>
    <id>4</id>
    <project name="Redmine" id="1"/>
    <user name="John Smith" id="27"/>
    <roles type="array">
      <role name="Developer" id="2" />
      <role name="Contributor" id="3" inherited="true" />
    </roles>
  </membership>
</memberships>
```

**注記:**

*   メンバーシップの所有者は、ユーザーまたはグループのいずれかです（グループAPIはRedmine 2.1で追加されました）。
*   上記の例では、最後のロールの `inherited="true"` 属性は、このロールがグループから継承されたことを意味します（例：John SmithはContributorsグループに属しており、このグループはプロジェクトメンバーとして追加されました）。John Smithのメンバーシップは、最初にグループメンバーシップを削除しないと削除できません。
*   特定のユーザーのメンバーシップは、ユーザーAPIから取得できます。

### POST

プロジェクトメンバーを追加します。

**パラメータ:**

*   `membership` (必須): メンバーシップ属性のハッシュ。以下を含みます:
    *   `user_id` (必須): ユーザーまたはグループの数値ID
    *   `role_ids` (必須): ロールの数値IDの配列

**例 (XML):**

```xml
POST /projects/redmine/memberships.xml

<membership>
  <user_id>27</user_id>
  <role_ids type="array">
    <role_id>2</role_id>
  </role_ids>
</membership>
```

**例 (JSON):**

```json
{
  "membership":
  {
    "user_id": 27,
    "role_ids": [ 2 ]
  }
}
```

**レスポンス:**

*   `201 Created`: メンバーシップが作成されました
*   `422 Unprocessable Entity`: 検証エラーのためメンバーシップが作成されませんでした（レスポンスボディにエラーメッセージが含まれます）

## /memberships/:id.:format

### GET

指定された `:id` のメンバーシップを返します。

**例:**

```
GET /memberships/1.xml
```

**レスポンス:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<membership>
  <id>1</id>
  <project name="Redmine" id="1"/>
  <user name="David Robert" id="17"/>
  <roles type="array">
    <role name="Developer" id="2"/>
    <role name="Manager" id="1"/>
  </roles>
</membership>
```

### PUT

指定された `:id` のメンバーシップを更新します。ロールのみ更新可能で、メンバーシップのプロジェクトとユーザーは読み取り専用です。

**パラメータ:**

*   `membership` (必須): メンバーシップ属性のハッシュ。以下を含みます:
    *   `role_ids` (必須): ロールの数値IDの配列

**例:**

```xml
PUT /memberships/2.xml

<membership>
  <role_ids type="array">
    <role_id>3</role_id>
    <role_id>4</role_id>
  </role_ids>
</membership>
```

**レスポンス:**

*   `204 No Content`: メンバーシップが更新されました
*   `422 Unprocessable Entity`: 検証エラーのためメンバーシップが更新されませんでした（レスポンスボディにエラーメッセージが含まれます）

### DELETE

メンバーシップを削除します。

グループメンバーシップから継承されたメンバーシップは削除できません。グループメンバーシップを削除する必要があります。

**パラメータ:**

*   なし

**例:**

```
DELETE /memberships/2.xml
```

**レスポンス:**

*   `204 No Content`: メンバーシップが削除されました
*   `422 Unprocessable Entity`: メンバーシップが削除されませんでした
