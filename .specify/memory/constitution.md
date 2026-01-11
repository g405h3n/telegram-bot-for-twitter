<!--
Sync Impact Report:
- Version change: 1.1.1 → 1.2.0 (added issue-driven branching principle)
- Modified principles: N/A
- Added sections: Issue-Driven Branching principle
- Removed sections: N/A
- Templates requiring updates:
  ✅ plan-template.md - Constitution Check section uses dynamic references
  ✅ spec-template.md - Aligned with constitution requirements
  ✅ tasks-template.md - Task categorization reflects principles
  ✅ No .specify/templates/commands directory exists, no updates needed
- Follow-up TODOs: None
-->

# Telegram Bot for Twitter Constitution

## Core Principles

### Borrow Proven Functionality
The system MUST borrow all core functionalities from the original project, which have been verified in production, to avoid too-early over-engineering.

**Rationale**: Leveraging existing, tested code ensures reliability, reduces development time, and maintains the project's focus on proven patterns rather than reinventing the wheel.

### Issue-Driven Branching
All development work MUST start from a GitHub Issue. Branches MUST follow the naming convention '{feat, or fix, or ...}/#{Issue ID}/{short-description}', where Issue ID is specified by the user and ensures traceability.

**Rationale**: Public GitHub projects rely on Issues for collaboration and tracking; this convention maintains project continuity, prevents untracked changes, and aligns with standard GitHub workflows.

### Simplicity & Maintainability
The system MUST remain simple and focused, following the original project's single-script pattern. Code MUST be readable, well-documented, and use standard Python libraries where possible. GitHub Actions workflow MUST be straightforward and easy to understand.

**Rationale**: The original project succeeds because of its simplicity. Over-engineering a monitoring bot creates unnecessary complexity and maintenance burden. The multi-account enhancement should not introduce bloat.

### Multi-Account First
The system MUST support tracking multiple Twitter/X accounts from inception, not as an afterthought. State management MUST be account-specific to prevent cross-account contamination. Configuration MUST allow easy addition/removal of accounts without code changes.

**Rationale**: The core enhancement over the original project is multi-account support; designing this capability from the start ensures proper separation of concerns and prevents architectural debt.

### API Resilience
All external API calls (Twitter/X API v2, Telegram Bot API) MUST include robust error handling, retry logic with exponential backoff, and clear error logging. The system MUST degrade gracefully if one account fails, continuing to monitor other accounts.

**Rationale**: External APIs are unreliable by nature; rate limits, temporary outages, and API changes are common. Single-account failures should not break the entire monitoring system.

### State Consistency
The system MUST maintain persistent state for each tracked account, recording the last seen tweet ID to avoid duplicate notifications. State files MUST be committed to the repository for transparency and recovery. State updates MUST be atomic to prevent corruption.

**Rationale**: Preventing duplicate notifications is critical for user experience. Persistent state ensures continuity across GitHub Actions runs and enables recovery from failures.

### Notification Purity
The system MUST send Telegram messages ONLY for new original tweets, explicitly filtering out replies, retweets, and quotes. On first run for any account, the system MUST initialize state WITHOUT sending messages (to avoid spamming historical posts).

**Rationale**: Original project requirement and user expectation. Users want notifications of new content, not noise from engagement activities or historical tweets.

### Observability & Logging
All monitoring activities MUST be logged with timestamps, account identifiers, and outcome details. Logs MUST distinguish between normal operation, warnings, and errors. The system MUST provide visibility into which accounts are being monitored, when checks occur, and what actions were taken.

**Rationale**: With multiple accounts, transparency is essential for debugging, verifying correct operation, and identifying issues. Users need to know what the bot is doing and why.

## Security Requirements

All secrets (Twitter Bearer Tokens, Telegram Bot Tokens, Chat IDs) MUST be stored in GitHub Secrets or environment variables, never committed to the repository. The system MUST validate that required secrets are present before attempting API calls.

**Rationale**: Exposing API tokens would compromise security and violate best practices. GitHub Secrets provides secure storage for sensitive configuration.

## Development Workflow

All changes MUST include logging and error handling appropriate to the multi-account context. State file format MUST be backward compatible or include migration logic. GitHub Actions workflow MUST be tested with sample accounts before deployment.

**Rationale**: Ensuring quality and preventing regressions is critical for a service that runs automatically. Testing with sample accounts validates the multi-account logic without affecting production monitoring.

## Governance

This constitution governs all development decisions for the Telegram Bot for Twitter project. All features, refactoring, and bug fixes MUST align with these principles. Amendments MUST update this document with version increment and clear rationale. Code reviews MUST verify compliance with these principles.

**Rationale**: A clear governance structure ensures the project maintains its focus on reliable, simple multi-account monitoring as it evolves.

**Version**: 1.2.0 | **Ratified**: 2026-01-11 | **Last Amended**: 2026-01-11
