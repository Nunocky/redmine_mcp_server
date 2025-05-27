# Redmine MCP Server

## API Reference

- [Redmine API](https://www.redmine.org/projects/redmine/wiki/Rest_api)
- [MCP Specification](https://modelcontextprotocol.io/specification/2025-03-26)

## setup

```sh
uv sync
```

## Using with Cline


```json
    "Redmine": {
      "disabled": false,
      "command": "uv",
      "args": [
        "--directory",
        "<path_to_mcp_server>",
        "run",
        "main.py"
      ],
    }
```

## Note

### Reducing the Number of Tools

`main.py` ですべての Tool を登録すると、 Claude Desktop などの環境では最初のツール一覧の読み取りでトークンの上限に達してしまいます。実際に使うときは管理者権限の必要なAPIを除くなどして、必要なツールだけを登録するようにしてください。

If you register all Tools in `main.py`, environments like Claude Desktop may hit the token limit when reading the initial list of tools. When actually using the server, please register only the necessary tools, such as by excluding APIs that require administrator privileges.

### Interacting with the MCP Server Manually

To retrieve the list of tools by passing API requests to `main.py` via a pipe, use the following method.

```sh
(echo '{"jsonrpc":"2.0","id":0, "method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"mcp-util-list-tools","version":"0.1.0"}}}' ; \
 echo '{"jsonrpc":"2.0",         "method":"notifications/initialized"}' ; \
 echo '{"jsonrpc":"2.0", "id":2, "method":"tools/list"}') | python main.py
```

- [MCPを肌で実感。俺がMCPサーバーだ \#LLM \- Qiita](https://qiita.com/Syuparn/items/92417e0e0b3c67f8e205)

## supported APIs

- [x] Issues
- [x] Projects
- [x] Project Memberships
- [x] Users
- [x] Time Entries
- [x] News
- [ ] Issue Relations
- [x] Versions
- [x] Wiki Pages
- [x] Queries
- [x] Attachments
- [x] Issue Statuses
- [x] Trackers
- [x] Enumerations
- [x] Issue Categories
- [x] Roles
- [x] Groups
- [x] Custom Fields
- [x] Search
- [x] Files
- [x] My account  
~~- [ ] Journals~~

## License

This source code is licensed under the Apache License, Version 2.0. See LICENSE for details.
