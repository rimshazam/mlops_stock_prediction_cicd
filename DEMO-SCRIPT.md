# CI/CD Demo Script

## FASTEST PATH: GitHub Actions (5 minutes)

### Setup (Do this BEFORE demo)
```bash
# 1. Add GitHub Secrets (1 minute)
# Go to: https://github.com/rimshazam/mlops_stock_prediction_cicd/settings/secrets/actions
# Add: DOCKERHUB_USERNAME and DOCKERHUB_TOKEN

# 2. Push the workflow file (1 minute)
git add .github/workflows/ci-cd.yml
git commit -m "Add GitHub Actions CI/CD workflow"
git push origin main

# 3. Verify it ran successfully
# Check: https://github.com/rimshazam/mlops_stock_prediction_cicd/actions
```

### During Demo (3 minutes)

**1. Show the Workflow File** (30 seconds)
```bash
# Open .github/workflows/ci-cd.yml
# Explain: "This YAML file defines our CI/CD pipeline"
# Point out: test → build → push → deploy stages
```

**2. Show GitHub Actions Running** (1 minute)
```bash
# Open: https://github.com/rimshazam/mlops_stock_prediction_cicd/actions
# Click on latest workflow run
# Show: All green checks
# Click "Run Tests" → Show pytest output
# Click "Build and Push Docker Images" → Show builds
```

**3. Trigger Live Pipeline** (1.5 minutes)
```bash
# Make a small change
echo "## CI/CD Demo - $(date)" >> README.md
git add README.md
git commit -m "Demo: Trigger CI/CD pipeline"
git push origin main

# Immediately go to Actions tab
# Show: New workflow starting in real-time
# Explain each stage as it runs
```

**Key Points to Mention:**
- ✅ Automatic trigger on every push
- ✅ Runs tests before building
- ✅ Builds 3 Docker images in parallel
- ✅ Pushes to DockerHub for deployment
- ✅ All running in GitHub's cloud infrastructure

---

## ALTERNATIVE: Jenkins Demo (10 minutes)

### Setup (Do this BEFORE demo)

**1. Start Jenkins** (1 minute)
```bash
# Already running on: http://localhost:8090
docker ps | grep jenkins
```

**2. Configure Jenkins** (5 minutes)
```bash
# Open: http://localhost:8090
# - Create pipeline job named "stock-prediction-pipeline"
# - Add DockerHub credentials (ID: dockerhub-credentials)
# - Point to GitHub repo: https://github.com/rimshazam/mlops_stock_prediction_cicd.git
# - Set Script Path: Jenkinsfile
```

**3. Verify DockerHub Access** (1 minute)
```bash
# Make sure DockerHub credentials are working
# Test build manually first
```

### During Demo (4 minutes)

**1. Show Jenkins Dashboard** (30 seconds)
```bash
# Open: http://localhost:8090
# Show: Job list and build history
```

**2. Show Jenkinsfile** (30 seconds)
```bash
# Open Jenkinsfile in editor
# Explain stages:
#   1. Checkout Code
#   2. Install Dependencies
#   3. Run Tests
#   4. Build Docker Images (parallel)
#   5. Push Docker Images
#   6. Deploy Containers
```

**3. Trigger Build** (1 minute)
```bash
# In Jenkins: Click "Build Now"
# Show: Build progress in real-time
# Click "Console Output" to show live logs
```

**4. Show Results** (2 minutes)
```bash
# Once complete, show:
# - Stage View (visual pipeline)
# - Test Results
# - Build artifacts

# Verify images pushed to DockerHub:
# https://hub.docker.com/u/<YOUR_USERNAME>
```

**Key Points to Mention:**
- ✅ Self-hosted on local infrastructure
- ✅ Full control over build environment
- ✅ Detailed logging and history
- ✅ Parallel Docker builds for efficiency
- ✅ Integrated with GitHub webhooks

---

## Combined Demo (Best of Both - 7 minutes)

**1. Show Both Approaches** (2 minutes)
```bash
# "We have two CI/CD options configured"

# Jenkins (Local):
# Open: http://localhost:8090
# "Self-hosted, full control, runs on our infrastructure"

# GitHub Actions (Cloud):
# Open: https://github.com/rimshazam/mlops_stock_prediction_cicd/actions
# "Cloud-native, zero maintenance, free for public repos"
```

**2. Show Configuration Files** (2 minutes)
```bash
# Jenkinsfile
code Jenkinsfile
# "Groovy-based, declarative pipeline"

# GitHub Actions
code .github/workflows/ci-cd.yml
# "YAML-based, similar stages but different syntax"
```

**3. Live Trigger** (3 minutes)
```bash
# Push a change
echo "# Demo $(date)" >> README.md
git add README.md
git commit -m "CI/CD Demo"
git push origin main

# Show BOTH running simultaneously:
# Jenkins: http://localhost:8090
# GitHub Actions: https://github.com/rimshazam/mlops_stock_prediction_cicd/actions

# "Same code, two different CI/CD platforms, both working!"
```

---

## Expected Questions & Answers

**Q: Why have both Jenkins and GitHub Actions?**
A: Jenkins for local/enterprise control, GitHub Actions for cloud simplicity. Demonstrates knowledge of both approaches.

**Q: What happens if tests fail?**
A: Pipeline stops immediately, no images built or deployed. Let me show you:
```bash
# Temporarily break a test in backend/test_app.py
# Push and show pipeline failing
```

**Q: How do you handle secrets?**
A:
- Jenkins: Credentials manager (stored encrypted)
- GitHub Actions: Repository secrets (encrypted at rest)
- Never hardcoded in code

**Q: Can you show a failed build?**
A: Sure! [Point to any red X in build history]
- Click Console Output
- Show error message
- Explain how to debug

**Q: How do you deploy to production?**
A:
- Current: docker-compose on deployment server
- Better: Kubernetes with Helm charts
- Could add: ArgoCD for GitOps

**Q: What about monitoring?**
A: Can add:
- Prometheus for metrics
- Grafana for visualization
- Jenkins/GitHub Actions notifications (Slack, email)

---

## Backup Plan (If Live Demo Fails)

**Show Previous Successful Runs:**
```bash
# Jenkins: Build history with green checks
# GitHub Actions: Previous workflow runs
# "Here's one we ran earlier that succeeded"
```

**Explain What Would Happen:**
```bash
# Walk through each stage
# Show Jenkinsfile/workflow file
# Explain expected output
# "In production, this runs automatically on every merge"
```

---

## One-Liner Summary

**For resume/interview:**
"Implemented dual CI/CD pipeline using Jenkins and GitHub Actions with automated testing, parallel Docker builds, and DockerHub integration for MLOps stock prediction application"

## Time Estimates

| Demo Type | Setup Time | Demo Time | Total |
|-----------|------------|-----------|-------|
| GitHub Actions Only | 2 min | 3 min | 5 min |
| Jenkins Only | 6 min | 4 min | 10 min |
| Both (Recommended) | 8 min | 7 min | 15 min |
