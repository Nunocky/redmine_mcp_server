# Redmine Users API 拡充計画

## 現状の実装状況

### 1. GET /users (get_users_tool.py)
- 現状: 基本的な一覧取得のみ実装（limit, offsetパラメータのみ対応）
- 未対応: フィルタリング機能（status, name, group_id）

### 2. GET /users/:id (get_user_tool.py)
- 現状: 基本的なユーザー詳細取得は実装済み、includeパラメータも対応
- 未対応: /users/current エンドポイント対応の確認

### 3. POST /users (create_user_tool.py)
- 現状: 必須パラメータ（login, firstname, lastname, mail）および多くのオプションパラメータに対応済み
- 対応済み: password, auth_source_id, mail_notification, must_change_passwd, generate_password, custom_fields, send_information

### 4. PUT /users/:id (update_user_tool.py)
- 現状: 基本的な更新機能は実装済み
- 対応済み: admin権限付与（adminパラメータ）、custom_fields

### 5. DELETE /users/:id (delete_user_tool.py)
- 現状: 基本的な削除機能は実装済み

## 拡充計画

### 1. get_users_tool.py の拡充
- **目的**: ユーザー一覧取得時のフィルタリング機能を追加
- **追加パラメータ**:
  - `status`: ユーザーステータスでフィルタリング（1: アクティブ、2: 登録済み、3: ロック済み）
  - `name`: ログイン名、姓名、メールアドレスでフィルタリング
  - `group_id`: 特定グループに所属するユーザーでフィルタリング
- **実装方法**:
  - パラメータをAPIリクエストに追加
  - レスポンス形式の確認と調整

### 2. get_user_tool.py の拡充
- **目的**: /users/current エンドポイント対応と管理者/非管理者による差分対応
- **実装方法**:
  - /users/current エンドポイント対応の確認と必要に応じた実装
  - レスポンス内容の管理者/非管理者による差分対応

### 3. エラーハンドリングの強化
- **目的**: より詳細なエラー情報の提供
- **実装方法**:
  - 各ツールのエラーハンドリングを強化
  - HTTPステータスコードに応じた適切なエラーメッセージの提供

### 4. テストケースの拡充
- **目的**: 新機能のテスト網羅性向上
- **実装方法**:
  - 新機能に対応するテストケースの追加
  - エッジケースのテスト追加

## 実装スケジュール

1. get_users_tool.py のフィルタリング機能追加
2. get_user_tool.py の /users/current 対応確認と実装
3. レスポンス内容の管理者/非管理者による差分対応
4. エラーハンドリングの強化
5. テストケースの拡充

## API仕様詳細

### GET /users
- **パラメータ**:
  - `status`: ユーザーステータス（1: アクティブ、2: 登録済み、3: ロック済み）
  - `name`: ログイン名、姓名、メールアドレスでフィルタリング
  - `group_id`: 特定グループに所属するユーザーでフィルタリング
  - `limit`: 取得件数
  - `offset`: スキップ件数

### GET /users/:id
- **パラメータ**:
  - `include`: レスポンスに含める関連情報（memberships, groups）

### POST /users
- **パラメータ**:
  - `login`: ログイン名（必須）
  - `firstname`: 名（必須）
  - `lastname`: 姓（必須）
  - `mail`: メールアドレス（必須）
  - `password`: パスワード
  - `auth_source_id`: 認証モードID
  - `mail_notification`: メール通知設定
  - `must_change_passwd`: パスワード変更要求
  - `generate_password`: パスワード自動生成
  - `custom_fields`: カスタムフィールド
  - `send_information`: アカウント情報送信

### PUT /users/:id
- **パラメータ**:
  - `login`: ログイン名
  - `firstname`: 名
  - `lastname`: 姓
  - `mail`: メールアドレス
  - `password`: パスワード
  - `auth_source_id`: 認証モードID
  - `mail_notification`: メール通知設定
  - `must_change_passwd`: パスワード変更要求
  - `generate_password`: パスワード自動生成
  - `custom_fields`: カスタムフィールド
  - `admin`: 管理者権限付与

### DELETE /users/:id
- **パラメータ**:
  - `user_id`: 削除するユーザーID
