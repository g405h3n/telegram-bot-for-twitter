# Implementation Tasks: Multi-Account Twitter Bot Support

**Branch**: `001-multi-account-support` | **Date**: 2026-01-11 | **Plan**: D:/Projects/telegram-bot-for-twitter/specs/001-multi-account-support/plan.md

## Implementation Strategy

**MVP Scope**: User Story 1 (Configure Multiple Twitter Accounts) - enables basic list creation and account management.

**Incremental Delivery**: Implement US1 first for core functionality, then add notifications (US2), then error handling (US3). Testing deferred per user preference.

**Parallel Opportunities**: Within each story, API-related tasks can be parallelized where dependencies allow.

## Dependencies

User Story 1 (P1) → User Story 2 (P1) → User Story 3 (P2)

No cross-dependencies; each story can be implemented independently after foundational setup.

## Phase 1: Setup (Project Initialization)

Goal: Initialize project structure and copy/adapt base code.

- [X] T001 Create src/ directory structure
- [X] T002 Create state/ directory for persistent files
- [X] T003 Copy monitor.py from original repo to src/monitor.py and adapt imports
- [X] T004 Create requirements.txt with requests>=2.31.0,<3
- [X] T005 Create .github/workflows/ directory
- [X] T006 Create .github/workflows/monitor.yml for daily scheduling at 6:00 AM Asia/Shanghai

## Phase 2: Foundational (Prerequisites)

Goal: Set up core infrastructure before user stories.

- [X] T007 Add state file management for last_seen.json in src/monitor.py
- [X] T008 Implement basic logging with timestamps and account identifiers in src/monitor.py
- [X] T009 Add secret validation for Twitter Bearer, Access tokens, Telegram tokens at startup in src/monitor.py

## Phase 3: User Story 1 - Configure Multiple Twitter Accounts (P1)

Goal: Enable configuration of multiple accounts and list management.

Independent Test: Configure 2+ usernames, verify list configuration and validation without errors.

- [X] T010 [US1] Add configuration parsing for TWITTER_USERNAMES comma-delimited string in src/monitor.py
- [X] T013 [US1] Add list configuration loading from GitHub secrets
- [X] T014 [US1] Add validation for account usernames and list management in src/monitor.py

## Phase 4: User Story 2 - Receive Notifications for New Tweets (P1)

Goal: Fetch tweets from list and send Telegram notifications.

Independent Test: Post test tweet to monitored account, verify daily notification at 6 AM Asia/Shanghai.

- [ ] T015 [US2] Implement list tweets fetching in src/monitor.py (GET /2/lists/{id}/tweets)
- [ ] T016 [US2] Add filtering for original tweets (exclude replies, retweets, quotes) in src/monitor.py
- [ ] T017 [US2] Implement Telegram message sending in src/monitor.py (POST /bot{token}/sendMessage)
- [ ] T018 [US2] Add state update for last seen tweet ID in src/monitor.py
- [ ] T019 [US2] Add initialization logic to skip historical tweets on first run in src/monitor.py

## Phase 5: User Story 3 - Graceful Error Handling for Multiple Accounts (P2)

Goal: Ensure system continues monitoring despite failures.

Independent Test: Simulate API failure for one account, verify others continue and errors are logged.

- [ ] T020 [US3] Add retry logic with exponential backoff for all API calls in src/monitor.py
- [ ] T021 [US3] Implement error isolation per account/list operation in src/monitor.py
- [ ] T022 [US3] Add comprehensive error logging for rate limits, network issues, invalid tokens in src/monitor.py
- [ ] T023 [US3] Add graceful degradation when list API fails (fallback or skip) in src/monitor.py

## Final Phase: Polish & Cross-Cutting Concerns

Goal: Finalize implementation with quality improvements.

- [ ] T024 Add README.md with setup instructions from quickstart.md
- [ ] T025 Update .github/workflows/monitor.yml with proper secrets and environment variables
- [ ] T026 Add pagination handling for large lists if needed in src/monitor.py
- [ ] T027 Final validation of free API limits compliance in implementation</content>
<parameter name="filePath">D:/Projects/telegram-bot-for-twitter/specs/001-multi-account-support/tasks.md