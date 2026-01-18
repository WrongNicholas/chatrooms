## Contributing

We're using a structured workflow inspired by Scrum, as required for the course.

Helpful links:
- [What is Scrum?](https://www.scrum.org/resources/what-scrum-module)
- [What is an Issue?](https://docs.github.com/en/issues)

---
## Code Standards

These guidelines are meant to keep the codebase consistent and easy to work with.
Since we're all contributing to the same project, the goal is for everyone to be able to understand each other's code without extra effort.

- Write clear, readable, and maintainable code
- Use meaningful variable, function, class names
- Include docstrings for functions and classes
- Use [Python type hints](https://docs.python.org/3/library/typing.html) where it makes sense
- Follow [PEP 8](https://peps.python.org/pep-0008/) style conventions
- Avoid committing commented-out or unused code
- Keep commits focused and related to a single Issue

If you're unsure, just follow existing patterns in the codebase.

---

## Working on an Issue

The project board reflects the current state of work and should be kept reasonably up to date.

### 1. Create a Branch and Check It Out Locally
- Open the assigned Issue on GitHub
- On the right side, under **Development**, click **Create a branch**
- Use the default branch name provided by GitHub
- The base branch must be `main`

Once the branch is created, pull it locally:

```sh
git fetch origin
git checkout <branch-name>
```

Verify you are on the correct branch:
```sh
git branch
```

Please for the love of God do not work on `main`.

### 2. Move the Issue to "In Progress" and Push Your Work
- After creating the branch, move the Issue to **In Progress**
    - This indicates you are actively working on it.
Make your code changes on the branch.

Stage and commit your changes:
```sh
git status
git add .
git commit -m "Brief description of changes"
```

Push your branch to GitHub:
```sh
git push
```
Please don't nuke `main` on accident.

### 3. Move to "Peer Review" and Open a Pull Request

When you are done and ready to merge:
  - Move the Issue to **Peer Review**
  - Create a pull request
A Pull Request is how you request review and merging of your changes into `main`.

Helpful link:
- [Creating a Pull Request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)

Once approved and merged, the Issue will be moved to **Done**.

---

## Handling Merge Conflicts
Merge conflicts happen when Git cannot automatically combine changes.

Helpful links:
- [Addressing merge conflicts](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts)
- [Oh Shit, Git!?!](https://ohshitgit.com/)
