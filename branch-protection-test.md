
# Branch Protection Test

This file is used to test the GitHub branch protection workflow.

## Validation Steps

1. Create a feature branch.
2. Make a change and commit it.
3. Push the feature branch to GitHub.
4. Create a pull request targeting main.
5. Run Pytest, Gitleaks, and Trivy checks.
6. Merge only after all required checks pass.
