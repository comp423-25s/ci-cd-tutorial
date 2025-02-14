# FastAPI Project Starter

This repository has the essential configuration necessary to begin a FastAPI dev container, and it can now be deployed to OKD using a CI/CD pipeline.

Login to `OKD` by going to: <https://console.apps.unc.edu>

Once logged in you sould see **OKD** in the upper-left corner. If you see "Red Hat", be sure you opened the link above.

Now that you are logged in, go to the upper-right corner and click your ONYEN and go to the "Copy Login Command" link. Click Display Token. In this, copy the command in the first text box. Paste it into your dev container's terminal (which has the `oc` command-line application for interfacing with a Red Hat Open-Shift Kubernetes cluster installed).

Before proceeding, switch to your personal OKD project using your ONYEN. For example, if your ONYEN is "jdoe", run:
```bash
oc project comp590-140-25sp-jdoe
```

If the above command fails, restart the steps above! The following will not work until you are able to access your project via `oc`.

## Deploying to OKD using CI/CD (Integrated DeploymentConfig)

This guide shows you how to deploy this FastAPI project to OKD following a successful CI/CD test run using an integrated DeploymentConfig that includes its own BuildConfig and ImageStream. In this setup, after tests pass in GitHub Actions, the build is automatically triggered on OKD. The BuildConfig uses the Dockerfile from the repository (located in the ".production" directory), and the resulting image is deployed automatically with the app name set to "mt12-cicd-demo".

### Prerequisites

- You must be logged into an OKD cluster (`oc login`). You completed this above!
- Your GitHub repository is configured with a test workflow (see `.github/workflows/test.yml`) that runs tests on every push/PR to the `main` branch.
- GitHub Actions is set up with secrets for your OKD token and server URL (e.g., `OKD_TOKEN` and `OKD_SERVER`).
- Since the repository is private, OKD must have access to clone it via a source secret.

### Generating a Personal Access Token for Your Private Repository

Follow these steps to create a Personal Access Token (PAT) with read access for your repository:

1. **Sign in to GitHub**  
   - Go to [GitHub](https://github.com) and log in with your account.

2. **Navigate to Developer Settings**  
   - Click on your profile picture (top-right corner) and select **Settings**.
   - In the left sidebar, click on **Developer settings**.

3. **Access Personal Access Tokens**  
   - Click on **Personal access tokens**.
   - Select **Tokens (classic)**.

4. **Generate a New Token**  
   - Click the **"Generate new token"** button.
   - For classic tokens, click **"Generate new token (classic)"**.
   - Provide a descriptive name for the token (e.g., "OKD-Repo-ReadAccess").

5. **Select the Scope**  
   - Under **"Select scopes"**, check the **`repo`** scope.
   
6. **Generate and Copy the Token**  
   - Click **"Generate token"**.
   - **Copy the generated token immediately.** You won't be able to see it again later.

7. **Store the Token Securely**  
   - Save the token securely as you'll use it to create the OKD source secret.

### Additional Step: Create a Source Secret for Your Private Repo

1. **Create a GitHub access secret**  
   Create a secret in OKD that contains your GitHub username and a personal access token (PAT) with appropriate repo rights. For example, run:
   ```bash
   oc create secret generic mt12-cicd-git-credentials \
       --from-literal=username=<your-github-username> \
       --from-literal=password=<your-github-pat> \
       --type=kubernetes.io/basic-auth
   ```
2. **Label the Secret**  
   Add the label "app=mt12-cicd-demo" to make it easier to delete everything related to this demo later on:
   ```bash
   oc label secret mt12-cicd-git-credentials app=mt12-cicd-demo
   ```

### Steps

#### 1. Create an Integrated Deployment (with BuildConfig, ImageStream, and Source Secret)
Create an application that includes a BuildConfig, ImageStream, and DeploymentConfig. Because the repository is private, include the `--source-secret` flag. Tag every resource with the label "app=mt12-cicd-demo" by adding the `--labels` flag:

```bash
oc new-app . \
--name=mt12-cicd-demo \
--source-secret=mt12-cicd-git-credentials \
--strategy=docker \
--labels=app=mt12-cicd-demo
```

*Explanation*:  
- This command tells OKD to use the repository's Dockerfile located in the ".production" directory.
- The `--source-secret=mt12-cicd-git-credentials` flag directs OKD to use the secret you created to clone the private repo.
- The `--labels=app=mt12-cicd-demo` parameter tags the created BuildConfig, ImageStream, and DeploymentConfig with a common label, "app=mt12-cicd-demo".

#### 2. Expose the Service
Expose your FastAPI service externally by creating a route, also tagging it:
```bash
oc expose svc/mt12-cicd-demo --labels=app=mt12-cicd-demo
```
*Explanation*:  
- This command creates a Route resource with a public URL to your FastAPI application and tags it for bulk deletion later.

#### 3. Set Up CI/CD Integration for Automatic OKD Build
Configure your GitHub Actions workflow so that after tests pass, it automatically starts an OKD build:
```bash
# Log in to OKD using stored token and server URL
oc login --token=${{ secrets.OKD_TOKEN }} --server=${{ secrets.OKD_SERVER }}

# Trigger a new build (integrated with the DeploymentConfig)
oc start-build mt12-cicd-demo --from-dir=. --follow
```
*Explanation*:  
- Your GitHub Actions workflow logs in to OKD using stored secrets.
- When tests pass, this command triggers the build, updating the ImageStream and automatically redeploying the application via the integrated DeploymentConfig.

### Summary

With the Dockerfile read from the repository and a source secret provided:
1. A single command creates the BuildConfig, ImageStream, and DeploymentConfig (all tagged with "app=mt12-cicd-demo").
2. OKD authenticates with GitHub using your source secret.
3. Every push or merge to the `main` branch runs tests via GitHub Actions.
4. On a successful test run, GitHub Actions automatically triggers an OKD build.
5. The integrated configuration updates the deployment automatically.

This setup ensures that only well-tested code is deployed to production, maintaining a robust CI/CD pipeline.

Happy deploying!

---

## Cleaning Up Deployment Components

When you're ready to clean up all the components created by this deployment, you can delete them all in one step by using the label selector:

```bash
oc delete all -l app=mt12-cicd-demo
oc delete secret -l app=mt12-cicd-demo
```

These commands will remove all resources (Deployment, BuildConfig, ImageStream, Service, Route, and secrets) tagged with "app=mt12-cicd-demo" while leaving your OKD project intact for future work.
