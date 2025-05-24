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
