# Source Control Management

## Learning Objectives

- Define Source Control Management (SCM) and Version Control Systems (VCS)
- Distinguish between Centralized and Distributed Version Control Systems
- Understand why version control is essential for software development

## Why This Matters

Version control is a fundamental skill for every developer. It enables collaboration, tracks changes, and provides a safety net for your code. Git, the tool you will use throughout this program, is a DVCS that has become the industry standard. Understanding SCM concepts prepares you to work effectively in any development environment.

## The Concept

### What is Source Control Management?

**Source Control Management (SCM)**, also called **Version Control**, is the practice of tracking and managing changes to source code over time. An SCM system records every modification, who made it, and when.

### Why Use Version Control?

- **History:** View the complete history of changes to any file
- **Collaboration:** Multiple developers can work on the same codebase without overwriting each other's work
- **Branching:** Experiment with features in isolation before merging
- **Backup:** Distributed copies protect against data loss
- **Accountability:** Know who made each change and why

### Version Control System (VCS)

A **Version Control System** is the software that implements source control. There are two main types:

---

### Centralized Version Control Systems (CVCS)

**Architecture:** A single central server stores the repository. Developers checkout files, make changes, and commit back to the server.

```
Developer A --> Central Server <-- Developer B
                     |
                     v
              Repository (single copy)
```

**Examples:** Subversion (SVN), CVS, Perforce

**Characteristics:**

- Single source of truth on the server
- Requires network access to commit or view history
- Simpler access control and permissions
- Single point of failure (if the server goes down, work stops)

---

### Distributed Version Control Systems (DVCS)

**Architecture:** Every developer has a full copy of the repository, including the entire history. Changes are synchronized between repositories.

```
Developer A (full repo) <--> Remote Server (full repo) <--> Developer B (full repo)
```

**Examples:** Git, Mercurial

**Characteristics:**

- Full repository on every machine (work offline)
- No single point of failure
- Faster operations (most work is local)
- More complex workflows possible (branching, forking)

---

### CVCS vs DVCS Comparison

| Aspect | CVCS | DVCS |
|--------|------|------|
| Repository Location | Central server only | Every developer has a copy |
| Offline Work | Limited | Full capabilities |
| Speed | Depends on network | Fast (local operations) |
| Backup/Redundancy | Single point of failure | Inherently distributed |
| Branching | Typically heavier | Lightweight, encouraged |

### Git: The Industry Standard DVCS

**Git** is the most widely used version control system today. Created by Linus Torvalds in 2005, Git is:

- Fast and efficient
- Designed for branching and merging
- Distributed, so every clone is a full backup
- Supported by platforms like GitHub, GitLab, and Bitbucket

In the following topics, we will cover how to initialize a Git repository, make commits, create branches, and push changes to a remote repository.

## Summary

- Source Control Management tracks changes to code over time
- VCS can be Centralized (single server) or Distributed (full copies everywhere)
- Git is the industry-standard DVCS, enabling collaboration, branching, and offline work
- Understanding SCM is essential for professional software development

## Additional Resources

- [Git SCM: About Version Control](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control)
- [Atlassian: What is Version Control?](https://www.atlassian.com/git/tutorials/what-is-version-control)
- [GitHub Docs: About Git](https://docs.github.com/en/get-started/using-git/about-git)
