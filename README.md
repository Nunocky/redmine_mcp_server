# Redmine MCP Server

**UNDER CONSTRUCTION**

## API Refecence
- [Redmine API](https://www.redmine.org/projects/redmine/wiki/Rest_api)
- [MCP Specification](https://modelcontextprotocol.io/specification/2025-03-26)

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



## Cline

```json
    "Local Redmine": {
      "disabled": false,
      "timeout": 60,
      "command": "uv",
      "args": [
        "--directory",
        "<path_to_mcp_server>",
        "run",
        "main.py"
      ],
      "env": {
        "REDMINE_URL": "http://***",
        "REDMINE_API_KEY": "***"
      },
      "transportType": "stdio"
    }
```

## Example

### users

```sh
curl -H "X-Redmine-API-Key: ..." "http://...:8082/users.json?limit=25&amp;offset=0"
```

### membership
```sh
curl -H "X-Redmine-API-Key: ..." "http://.../projects/123/memberships.json?limit=25&amp;offset=0"
```
