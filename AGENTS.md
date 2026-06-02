# OpenShift LightSpeed RAG Content - Development Guide for AI

## Git and PR Workflow

### Commit Messages
- Start with the Jira ticket reference: `OLS-XXXX description`
- Keep the first line under 72 characters
- Use imperative mood

### Pull Requests
This repo uses a **fork-based workflow**:

1. **Push to your fork**, not to `origin` (openshift/lightspeed-rag-content)
2. **Create the PR** against `origin/main` using your fork's branch:
   ```bash
   git push <your-fork-remote> <branch>
   gh pr create --repo openshift/lightspeed-rag-content --head <your-github-user>:<branch> --base main
   ```
3. **PR title** must start with the Jira reference: `OLS-XXXX description`
4. **Squash commits** before pushing -- one logical commit per PR unless the PR explicitly tracks multiple independent changes

### Branch Completion
When finishing a development branch:
1. Remove any process artifacts (design docs, plans in `docs/superpowers/`)
2. Squash commits with the Jira-prefixed message
3. Push to the contributor's fork remote (not `origin`)
4. Create the PR against `origin/main` using `--head <user>:<branch>`

## Risk Levels

When creating Jira tickets for this repo, assign a risk level in the description.

| Level | Customer Impact | Review Requirements | Automation |
|-------|----------------|---------------------|------------|
| Risk 1 | Very little impact if change goes wrong | No human code review required | Fully automated implementation |
| Risk 2 | Medium impact if change causes problems | 1 human reviewer required | Automated implementation with human review gate |
| Risk 3 | Major impact — risk of losing customers if a bug is introduced | 2+ human reviewers required | Human-driven implementation |

### Classification Examples

| Change Type | Risk Level |
|-------------|------------|
| Doc source URL updates | 1 |
| Dependency version bump | 1 |
| Embedding pipeline parameter tuning | 2 |
| Chunking strategy changes | 2 |
| Vector store schema/index changes | 3 |
| Embedding model changes | 3 |

### Jira Description Format

Include this section in every ticket description:

```
## Risk Level

Risk {1|2|3} — {one-line impact summary}
Rationale: {why this classification, referencing the rubric}
```
