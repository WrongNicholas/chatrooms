## Contributing

We're using a structured workflow (inspired by Scrum), because that's what our professor is asking us to do.

Helpful links:
- [What is Scrum?](https://www.scrum.org/resources/what-scrum-module)
- [What is an Issue?](https://docs.github.com/en/issues)

## Working on an Issue

### 1. Create a Branch and Check It Out Locally
- Open the assigned Issue on GitHub
- On the right side, under **Development**, click **Create a branch**
- Use the default branch name provided by GitHub
- The base branch must be `main`

Once the branch is created, pull it locally:

```sh
git fetch
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
Please make sure you are not on `main`.

### 3. Move to "Peer Review" and Open a Pull Request

When you are done and ready to merge:
  - Move the Issue to **Peer Review**
  - Create a pull request
A Pull Request is how you request review and merging of your changes into `main`.
- See: [Creating a Pull Request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)

Once approved and merged, the Issue will be moved to `Done`.

---

## Merge Conflicts
Merge conflicts happen when Git cannot automatically combine changes.

Helpful links:
- [Addressing merge conflicts](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts)
- [Oh Shit, Git!?!](https://ohshitgit.com/)
