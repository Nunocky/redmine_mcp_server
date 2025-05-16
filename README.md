# Redmine MCP Server

## API Refecence
- [Redmine API](https://www.redmine.org/projects/redmine/wiki/Rest_api)
- [MCP Specification](https://modelcontextprotocol.io/specification/2025-03-26)

## setup

```sh
uv sync
```

### Cline

```json
    "Local Redmine": {
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
- [ ] News
- [ ] Issue Relations
- [ ] Versions
- [ ] Wiki Pages
- [ ] Queries
- [ ] Attachments
- [ ] Issue Statuses
- [ ] Trackers
- [ ] Enumerations
- [ ] Issue Categories
- [ ] Roles
- [ ] Groups
- [ ] Custom Fields
- [ ] Search
- [ ] Files
- [ ] My account
- [ ] Journals
