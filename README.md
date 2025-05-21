# Redmine MCP Server

## API Reference

- [Redmine API](https://www.redmine.org/projects/redmine/wiki/Rest_api)
- [MCP Specification](https://modelcontextprotocol.io/specification/2025-03-26)

## setup

```sh
uv sync
```

### Cline

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

## APIs

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
- [ ] Enumerations
- [ ] Issue Categories
- [x] Roles
- [ ] Groups
- [ ] Custom Fields
- [ ] Search
- [ ] Files
- [x] My account
- [ ] Journals
