# DevOps Lab Mid - Assignment Submission Portal

## Requirements
- Python 3.10+
- Git
- GitHub account
- For automatic local JSON delivery: Cloudflare Tunnel (`cloudflared`)

## 1. Install and run the portal (Windows PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## 2. Run automated tests
```powershell
pytest -v
```

## 3. Start the local report receiver
Open a second PowerShell window in this project folder:
```powershell
$env:RECEIVER_TOKEN="use-a-long-random-secret"
python receiver.py
```
The receiver listens on port 9000 and saves incoming reports as `test-report.json`.

## 4. Connect GitHub Actions to your computer
Keep the receiver running. In a third terminal run:
```powershell
cloudflared tunnel --url http://localhost:9000
```
Copy the HTTPS trycloudflare.com URL printed by the command. In GitHub:
Settings > Secrets and variables > Actions > New repository secret
- `RECEIVER_URL` = the HTTPS tunnel URL (without `/report`)
- `RECEIVER_TOKEN` = exactly the same token used by receiver.py

Keep both receiver and tunnel running during the demonstration. A Quick Tunnel URL may change when restarted; update the GitHub secret if it changes.

## 5. Push to GitHub
Create an empty GitHub repository, then run:
```powershell
git init
git add .
git commit -m "Create assignment submission portal and CI"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```
Replace the remote URL with your own repository URL. Every push triggers GitHub Actions.

## 6. Demonstrate pass and fail
1. Push the original code: all three tests should pass.
2. Temporarily break URL validation in `app.py` (for example, change the accepted schemes so `https` is rejected), commit and push. The URL test should fail and the workflow should be red.
3. Restore the original validation, commit and push. The workflow should turn green again.
4. After each run, check that your local `test-report.json` has been automatically updated. Also show the Actions run and its uploaded artifact.

## Important
- The GitHub runner cannot directly access its own `localhost` as your computer. The tunnel forwards the report to your computer.
- If the receiver or tunnel is stopped, the local file cannot be updated. The workflow artifact is still uploaded.
- Do not commit your real receiver token. Store it only in GitHub Secrets and your local environment.
