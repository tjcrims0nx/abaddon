---
name: code-review
description: Perform thorough code review with security, performance, and style analysis
---

When asked to review code, follow this enhanced protocol:

1. Check for security vulnerabilities first: SQL injection, XSS, hardcoded secrets, unsafe eval/exec calls, path traversal.
2. Review performance: identify N+1 queries, unnecessary loops, blocking I/O, memory leaks.
3. Check code style and readability: naming conventions, function length, comments, dead code.
4. Suggest specific, actionable improvements with corrected code snippets.
5. Rate the severity of each issue: CRITICAL / HIGH / MEDIUM / LOW.
