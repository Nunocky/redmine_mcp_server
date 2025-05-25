#!/usr/bin/env python3
"""
MCPサーバに登録されているツールの一覧を取得して、その名前と解説を表示するスクリプト

Usage:
    python util/list_mcp_tools.py

標準出力に「Tool Name: ...」「Description: ...」形式で一覧を表示します。

# ref: https://zenn.dev/ohke/articles/mcp-quick-study-2025
# このコメントは、MCPサーバとの通信手順の参考例です。
# 1. initializeリクエストを送信し、サーバのバージョンや機能を取得
# 2. notifications/initialized通知を送信（必要な場合）
# 3. tools/listリクエストを送信し、ツール一覧を取得
# 例:
# [info] [Demo] Message from client: {"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"claude-ai","version":"0.1.0"}},"jsonrpc":"2.0","id":0}
# [info] [Demo] Message from server: {"jsonrpc":"2.0","id":0,"result":{"protocolVersion":"2024-11-05","capabilities":{"experimental":{},"prompts":{"listChanged":false},"resources":{"subscribe":false,"listChanged":false},"tools":{"listChanged":false}},"serverInfo":{"name":"Demo","version":"1.6.0"}}}
# [info] [Demo] Message from client: {"method":"notifications/initialized","jsonrpc":"2.0"}
# [info] [Demo] Message from client: {"method":"tools/list","params":{},"jsonrpc":"2.0","id":1}
# [info] [Demo] Message from server: {"jsonrpc":"2.0","id":1,"result":{"tools":[{"name":"add","description":"Add two numbers","inputSchema":{"properties":{"a":{"title":"A","type":"integer"},"b":{"title":"B","type":"integer"}},"required":["a","b"],"title":"addArguments","type":"object"}}]}}

# main.pyにパイプでAPIを渡してツール一覧を取得するには以下のようにする。
# "notifications/initialized"に idが付いていないのは、これが正しいみたい
 (echo '{"jsonrpc":"2.0", "id":0, "method":"initialize"' ; \
  echo '{"jsonrpc":"2.0",         "method":"notifications/initialized"}' ; \
  echo '{"jsonrpc":"2.0", "id":2, "method":"tools/list"}') | python main.py
"""

import json
import os
import subprocess
import sys
import threading
import time


def main():
    """
    Get the list of tools registered in the MCP server and print their names and descriptions.

    Raises:
        SystemExit: If any error occurs during communication or parsing.
    """
    # Prepare JSON-RPC requests
    initialize_req = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "list_mcp_tools", "version": "1.0"}
        }
    }
    notifications_initialized = {
        "jsonrpc": "2.0",
        "method": "notifications/initialized"
    }
    tools_list_req = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    main_py_path = os.path.join(os.path.dirname(__file__), "..", "main.py")
    main_py_path = os.path.abspath(main_py_path)

    try:
        # Start MCP server process
        proc = subprocess.Popen(
            [sys.executable, main_py_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=0
        )

        # stderrを別スレッドで読み続ける
        def stderr_reader(stderr):
            pass
            # for line in iter(stderr.readline, ''):
            #     if line:
            #         print(f"[stderr] {line.strip()}", file=sys.stderr)

        stderr_thread = threading.Thread(target=stderr_reader, args=(proc.stderr,), daemon=True)
        stderr_thread.start()

        def read_response(proc, expected_id, timeout=5):
            """
            Read lines from proc.stdout until a JSON with 'id'==expected_id is found or timeout.
            Additionally, print all received lines for debugging.
            """
            start = time.time()
            while True:
                if proc.stdout and not proc.stdout.closed:
                    line = proc.stdout.readline()
                    if line:
                        # print(f"[stdout] {line.strip()}", file=sys.stdout)
                        try:
                            resp = json.loads(line)
                            if resp.get("id") == expected_id:
                                return resp
                        except Exception:
                            continue
                    else:
                        if time.time() - start > timeout:
                            raise RuntimeError(f"No response from MCP server (id={expected_id}).")
                        # time.sleep(0.1)
                        continue
                if time.time() - start > timeout:
                    raise RuntimeError(f"No response from MCP server (id={expected_id}).")

        # Wait a moment for main.py to be ready
        # time.sleep(0.5)

        # 1. initializeリクエスト送信
        proc.stdin.write(json.dumps(initialize_req) + "\n")
        proc.stdin.flush()
        resp1 = read_response(proc, 1, timeout=5)

        # 2. notifications/initialized通知送信
        proc.stdin.write(json.dumps(notifications_initialized) + "\n")
        proc.stdin.flush()
        # 通知なのでレスポンスは不要

        # 3. tools/listリクエスト送信
        proc.stdin.write(json.dumps(tools_list_req) + "\n")
        proc.stdin.flush()
        resp2 = read_response(proc, 2, timeout=5)
        proc.stdin.close()  # すべて書き終わったらstdinを閉じる

        tools_list = resp2.get("result", {}).get("tools", [])

        # Print tool names and descriptions
        for tool in tools_list:
            name = tool.get("name", "")
            desc = tool.get("description", "")
            print("-------------------------")
            print(f"Tool Name: {name}")
            print(f"Description: {desc}\n")

        proc.terminate()
        proc.wait(timeout=2)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
