# Git Commit, Branch, Merge, Push, Pull

## Learning Objectives

- Understand the Git workflow for staging, committing, and pushing changes
- Learn how to create and switch branches
- Merge branches and resolve basic conflicts
- Pull changes from a remote repository

## Why This Matters

Mastering the Git workflow is essential for collaboration and code management. These commands form the daily rhythm of professional software development, enabling you to track changes, work on features in isolation, and synchronize with your team.

## The Concept

### The Basic Git Workflow

```
Working Directory --> Staging Area --> Local Repository --> Remote Repository
      (edit)            (git add)       (git commit)          (git push)
```

### Staging Changes

Before committing, you must stage your changes. Staging tells Git which modifications to include in the next commit.

```bash
# Stage a specific file
git add filename.py

# Stage all changes in the current directory
git add .

# Stage all changes in the repository
git add -A
```

Check what is staged:

```bash
git status
```

### Committing Changes

A **commit** is a snapshot of your staged changes with a descriptive message.

```bash
git commit -m "Add user authentication feature"
```

**Best Practices for Commit Messages:**

- Use the imperative mood ("Add feature" not "Added feature")
- Keep the subject line under 50 characters
- Explain what and why, not how

View commit history:

```bash
git log --oneline
```

---

### Branching

A **branch** is an independent line of development. Branches allow you to work on features without affecting the main codebase.

#### Create a New Branch

```bash
git branch feature-login
```

#### Switch to a Branch

```bash
git checkout feature-login
```

#### Create and Switch in One Command

```bash
git checkout -b feature-login
```

Or using the newer syntax:

```bash
git switch -c feature-login
```

#### List All Branches

```bash
git branch
```

The current branch is marked with an asterisk (*).

---

### Merging Branches

Once your feature is complete, you merge it back into the main branch.

#### Switch to the Target Branch

```bash
git checkout main
```

#### Merge the Feature Branch

```bash
git merge feature-login
```

If there are no conflicts, Git performs a **fast-forward** or **three-way merge** automatically.

#### Handling Merge Conflicts

If the same lines were changed in both branches, Git cannot automatically merge. You must:

1. Open the conflicting file(s)
2. Look for conflict markers:

   ```
   <<<<<<< HEAD
   Your changes
   =======
   Their changes
   >>>>>>> feature-login
   ```

3. Edit the file to resolve the conflict
4. Stage the resolved file and commit

```bash
git add resolved-file.py
git commit -m "Resolve merge conflict in resolved-file.py"
```

---

### Pushing Changes

Upload your local commits to the remote repository:

```bash
git push origin main
```

If you set upstream tracking earlier, you can simply:

```bash
git push
```

---

### Pulling Changes

Download and integrate changes from the remote repository:

```bash
git pull origin main
```

This is equivalent to:

```bash
git fetch origin
git merge origin/main
```

**Best Practice:** Always pull before you push to ensure you have the latest changes.

---

### Summary Workflow

```bash
# Start a new feature
git checkout -b feature-new-ui

# Make changes, then stage and commit
git add .
git commit -m "Implement new UI components"

# Switch back to main and merge
git checkout main
git pull origin main
git merge feature-new-ui

# Push merged changes
git push origin main

# Optionally delete the feature branch
git branch -d feature-new-ui
```

## Summary

- **Staging (add):** Select changes to include in the next commit
- **Committing:** Save a snapshot with a descriptive message
- **Branching:** Create isolated lines of development
- **Merging:** Combine branches together
- **Pushing:** Upload commits to a remote repository
- **Pulling:** Download and integrate remote changes

## Additional Resources

- [Git Documentation: Basic Branching and Merging](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging)
- [Atlassian: Git Merge](https://www.atlassian.com/git/tutorials/using-branches/git-merge)
- [GitHub Docs: About Branches](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-branches)
