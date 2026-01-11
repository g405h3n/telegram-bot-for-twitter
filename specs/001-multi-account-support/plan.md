# Implementation Plan: Multi-Account Twitter Bot Support

**Branch**: `001-multi-account-support` | **Date**: 2026-01-11 | **Spec**: D:/Projects/telegram-bot-for-twitter/specs/001-multi-account-support/spec.md
**Input**: Feature specification from `/specs/001-multi-account-support/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Support configuration and monitoring of multiple Twitter/X accounts for sending Telegram notifications of new original tweets. Implementation borrows and adapts code from https://github.com/EleftheriaBatsou/cosineai-x-telegram-notifier/tree/main, uses Twitter list API for efficient multi-account retrieval via a user-managed list, stores persistent state in a single JSON file, and schedules daily runs at 6:00 AM Asia/Shanghai via GitHub Actions to stay within free Twitter API limits.

## Technical Context

**Language/Version**: Python 3.10+  
**Primary Dependencies**: requests>=2.31.0,<3  
**Storage**: JSON file  
**Testing**: Not required for initial implementation; focus on making it work first  
**Target Platform**: GitHub Actions (Linux)  
**Project Type**: single  
**Performance Goals**: Daily notifications for multiple accounts within free Twitter API limits (1,500 tweets/month, 500 users/month) using list API for efficiency  
**Constraints**: Stay within free Twitter API plan, no real-time polling, manage Twitter list for accounts with user-controlled size to minimize pagination  
**Scale/Scope**: Multiple Twitter accounts in a user-managed list  

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

All principles align:
- Borrow Proven Functionality: Copying and adapting verified code from the original repo.
- Issue-Driven Branching: Branch follows convention feat/#1/core-functionalities based on GitHub Issue #1.
- Simplicity & Maintainability: Single-script pattern using standard Python libraries.
- Multi-Account First: State management designed for account-specific isolation from inception.
- API Resilience: Robust error handling, retry logic, and exponential backoff included.
- State Consistency: Persistent JSON state with atomic updates and backward compatibility.
- Notification Purity: Filters out replies, retweets, and quotes; initializes without spamming history.
- Observability & Logging: Logs all activities with timestamps, account IDs, and outcomes.
- Security Requirements: Secrets in GitHub Secrets, validation before API calls.
- Development Workflow: State file migration logic, testing with sample accounts.

One justified violation: Skipping initial testing to prioritize making it work first, as per user preference.

## Project Structure

### Documentation (this feature)

```text
specs/001-multi-account-support/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
src/
└── monitor.py          # Adapted script for multi-account monitoring

.github/
└── workflows/
    └── monitor.yml     # GitHub Actions workflow for daily runs
```

**Structure Decision**: Single project structure chosen to maintain simplicity and follow the original repo's pattern. Source code adapted in src/monitor.py, with tests added for reliability without over-engineering.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Skipping testing initially | User prioritizes "make it work first" approach | Testing with mocks/samples rejected due to focus on quick implementation |

