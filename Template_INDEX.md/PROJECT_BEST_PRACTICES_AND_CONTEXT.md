# Project Best Practices & Restart Context

## Hardcoded Best Practices
- Always add logging to every function or module.
- Write at least one test for every new feature or bugfix.
- Maintain a control archive (directory or file) listing all log and test files.

## How this is implemented
- Logging and test stubs will be added to every code generation or template.
- A `LOG_AND_TEST_ARCHIVE.md` will be created/updated in the project root, listing all log and test files with a brief description.
- If a feature or module is missing logs or tests, you will be reminded.

## Example Control Archive

```
# Log and Test Archive

## Log Files
- app.log: Main application logs
- payment.log: Payment processing events

## Test Files
- test_user.py: Tests for user registration and login
- test_payment.py: Tests for payment logic

## Last Updated: 2025-04-28
```

## Restart Context
- This project was reopened after a restart on 2025-04-28.
- All key files, documentation, and best practices are now saved in `/Users/danielmelendez/NewFolder/`.
- The MCP project development will resume soon, following the jobs to be done and template previously generated.
- This file and conversation summary will help ensure continuity and onboarding for any team member.

---

*Ready for your next request!*
