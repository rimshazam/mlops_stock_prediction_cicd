# CI/CD Setup Guide

## Quick Summary
You have **TWO options** for CI/CD:
1. **Jenkins** (Local) - Running on http://localhost:8090
2. **GitHub Actions** (Cloud) - Already configured in `.github/workflows/ci-cd.yml`

---

## Option 1: Jenkins Setup (Local CI/CD)

### Step 1: Access Jenkins
```bash
# Jenkins is already running!
# Open in browser: http://localhost:8090
```

### Step 2: Initial Setup (If First Time)
1. Go to http://localhost:8090
2. Get unlock password:
   ```bash
   docker logs jenkins 2>&1 | grep -A 5 "Jenkins initial setup"
   # OR manually get it:
   docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
   ```
3. Install suggested plugins
4. Create admin user

### Step 3: Install Required Plugins
**Dashboard → Manage Jenkins → Manage Plugins → Available**
- Docker Pipeline
- GitHub Integration Plugin
- Pipeline

### Step 4: Add DockerHub Credentials
1. **Manage Jenkins → Credentials → System → Global credentials → Add Credentials**
2. **Kind**: Username with password
3. **Username**: Your DockerHub username
4. **Password**: Your DockerHub password/token
5. **ID**: `dockerhub-credentials` (IMPORTANT - matches Jenkinsfile)
6. Click **OK**

### Step 5: Create Pipeline Job
1. Click **New Item**
2. **Name**: `stock-prediction-pipeline`
3. **Type**: Pipeline
4. Click **OK**
5. **Configure**:
   - **Build Triggers**: Check "GitHub hook trigger for GITScm polling"
   - **Pipeline**:
     - **Definition**: Pipeline script from SCM
     - **SCM**: Git
     - **Repository URL**: `https://github.com/rimshazam/mlops_stock_prediction_cicd.git`
     - **Branch**: `*/main` (or `*/master` depending on your default branch)
     - **Script Path**: `Jenkinsfile`
6. Click **Save**

### Step 6: Configure GitHub Webhook
1. Go to: https://github.com/rimshazam/mlops_stock_prediction_cicd/settings/hooks
2. Click **Add webhook**
3. **Payload URL**: `http://<YOUR_PUBLIC_IP>:8090/github-webhook/`
   - Note: For local testing, you'll need ngrok or similar to expose Jenkins
4. **Content type**: `application/json`
5. **Which events**: Just the push event
6. Click **Add webhook**

### Step 7: Test Jenkins Pipeline
```bash
# Trigger manually first
# Go to Jenkins → stock-prediction-pipeline → Build Now

# OR push to GitHub to trigger webhook
git add .
git commit -m "Test Jenkins pipeline"
git push origin main
```

---

## Option 2: GitHub Actions (Recommended - Easier)

### Step 1: Add GitHub Secrets
1. Go to: https://github.com/rimshazam/mlops_stock_prediction_cicd/settings/secrets/actions
2. Click **New repository secret**
3. Add these secrets:

**Secret 1:**
- **Name**: `DOCKERHUB_USERNAME`
- **Value**: Your DockerHub username

**Secret 2:**
- **Name**: `DOCKERHUB_TOKEN`
- **Value**: Your DockerHub access token
  - Get token from: https://hub.docker.com/settings/security
  - Click "New Access Token"
  - Name: "GitHub Actions"
  - Copy the token

### Step 2: Push GitHub Actions Workflow
```bash
# The workflow file is already created at: .github/workflows/ci-cd.yml
# Just commit and push it

git add .github/workflows/ci-cd.yml
git commit -m "Add GitHub Actions CI/CD workflow"
git push origin main
```

### Step 3: Verify GitHub Actions
1. Go to: https://github.com/rimshazam/mlops_stock_prediction_cicd/actions
2. You should see the workflow running
3. Click on it to see details

### Step 4: Test the Pipeline
```bash
# Make any change and push
echo "# Test" >> README.md
git add README.md
git commit -m "Test GitHub Actions pipeline"
git push origin main

# Go to GitHub Actions tab to see it running
```

---

## Demo Commands

### Check Running Services
```bash
# Check Jenkins
docker ps | grep jenkins

# Check app containers
docker-compose ps
```

### View Pipeline Logs

**Jenkins:**
```bash
# In browser: http://localhost:8090
# Click on job → Build History → Console Output
```

**GitHub Actions:**
```bash
# In browser: https://github.com/rimshazam/mlops_stock_prediction_cicd/actions
```

### Manual Pipeline Trigger

**Jenkins:**
- Browser: http://localhost:8090 → Job → Build Now

**GitHub Actions:**
```bash
# Push any change
git commit --allow-empty -m "Trigger pipeline"
git push origin main
```

---

## Pipeline Stages (Both Jenkins & GitHub Actions)

1. **Checkout Code** - Clone repository
2. **Install Dependencies** - Install Python packages
3. **Run Tests** - Execute pytest tests
4. **Build Docker Images** - Build backend, frontend, database images
5. **Push to DockerHub** - Upload images to registry
6. **Deploy** - Deploy using docker-compose

---

## Troubleshooting

### Jenkins Issues

**Can't access Jenkins:**
```bash
# Check if running
docker ps | grep jenkins

# Restart
docker restart jenkins

# View logs
docker logs jenkins
```

**Pipeline fails on Docker commands:**
```bash
# Jenkins container needs Docker access
docker run -d --name jenkins \
  -p 8090:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  jenkins/jenkins:lts
```

**Credentials not working:**
- Verify ID is exactly `dockerhub-credentials`
- Check DockerHub token hasn't expired

### GitHub Actions Issues

**Secrets not working:**
- Names must be EXACTLY: `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN`
- Check token has write permissions

**Workflow not triggering:**
- File must be in `.github/workflows/` directory
- Must be pushed to repository
- Check Actions tab is enabled in repo settings

---

## Demo Talking Points

### For Jenkins:
- "We use Jenkins for local CI/CD with full control"
- "Pipeline defined in Jenkinsfile with 5 stages"
- "Automatically triggers on GitHub push via webhooks"
- "Builds Docker images and pushes to DockerHub"
- "Can see build history and logs in Jenkins UI"

### For GitHub Actions:
- "Cloud-native CI/CD with GitHub Actions"
- "YAML-based workflow configuration"
- "Runs on GitHub's infrastructure"
- "Free for public repositories"
- "Automatic triggers on push/PR"
- "Matrix builds for multiple platforms possible"

---

## Quick Reference

| Feature | Jenkins | GitHub Actions |
|---------|---------|----------------|
| Location | http://localhost:8090 | GitHub Actions tab |
| Config File | `Jenkinsfile` | `.github/workflows/ci-cd.yml` |
| Secrets | Jenkins Credentials | GitHub Secrets |
| Trigger | Webhook | Automatic on push |
| Cost | Free (self-hosted) | Free (public repo) |
