# GitHub-only submission

The uploaded brief asks for a dedicated repository URL containing all lab materials. A ZIP, HTML download or cloud document is useful for preparation, but does not replace the repository URL. No repository has been created or uploaded by this package.

## Finish before uploading

- [ ] Open and check both Tableau workbooks. Complete the native data, chart and filter checks in `tableau_open_and_verify.md`.
- [ ] Save the verified main dashboard as `evaluation_score_dashboard.twbx`.
- [ ] Capture a real Tableau view as `dashboard_screenshot.png`.
- [ ] For the optional extension, save the verified judge workbook and capture `judge_agreement_screenshot.png`.
- [ ] Review `reflection.md` and personalise it to your own observations.
- [ ] Update the README status and requirements checklist to distinguish what you have now verified.

## Upload using the GitHub website

1. Create a repository called `lab-evaluation-dashboard-walid-barakat` in your GitHub account. Choose a visibility that allows your instructor to access it.
2. Extract this package. Upload the contents of `lab_evaluation_dashboard_walid_barakat` into that repository, preserving folders. Do not upload an enclosing ZIP as the only source.
3. Include README, both native files, data, notebook, scripts, documentation, previews and the new native screenshots. Keep this lab separate from the EU tender project repository.
4. Exclude virtual environments, package caches, `node_modules`, personal documents, credentials and unrelated projects.
5. Check that the README renders, CSV files open, native files download and screenshots are visible. Download the TWBX from the repository and open it once more to confirm its data travel with it.
6. Submit the repository's actual URL in the course lab submission field. Do not submit the example repository name or a made-up URL.

## Upload using Git locally (optional)

After creating the remote repository in your account, run from the extracted folder:

```bash
git init
git add .
git commit -m "Add evaluation dashboard lab solution"
git branch -M main
# Replace the following with the real URL of the repository you created.
git remote add origin YOUR_ACTUAL_REPOSITORY_URL
git push -u origin main
```

The remote URL is a placeholder until you create the repository. This package contains only synthetic lab data and no API keys.

Reference: the uploaded lab's Deliverables and Submission hygiene sections.
