# Deployment Guide: Antigravity Engine

## 1. GitHub Setup
Since `git` is not currently detected in your terminal, you need to:
1.  **Install Git**: [Download for Windows](https://git-scm.com/download/win)
2.  **Initialize Repository**:
    ```bash
    git init
    git add .
    git commit -m "Initial commit of Antigravity Engine"
    ```
3.  **Push to GitHub**:
    *   Create a new repo on GitHub.
    *   `git remote add origin https://github.com/YOUR_USERNAME/antigravity-vest.git`
    *   `git push -u origin master`

## 2. Vercel Deployment (Frontend Only)
Vercel is perfect for the Next.js Frontend.

1.  Go to [Vercel Dashboard](https://vercel.com/dashboard).
2.  Click **"Add New..."** -> **Project**.
3.  Import your `antigravity-vest` GitHub repo.
4.  **Configure Project**:
    *   **Root Directory**: `frontend` (Important! Click "Edit" next to Root Directory).
    *   **Framework Preset**: Next.js.
    *   **Environment Variables**:
        *   `NEXT_PUBLIC_API_URL`: You will need the URL of your deployed Backend (see below).

## 3. Backend Deployment (Railway/Render)
The Backend **cannot** stream on Vercel standardly because it uses **Celery (Background Tasks)** and **DuckDB (Persistent Files)**. Vercel functions are stateless and time out after 10 seconds.

**Recommended: Deploy Backend to Railway.app**
1.  Login to Railway.
2.  New Project -> Deploy from GitHub Repo.
3.  **Root Directory**: `backend`.
4.  **Variables**: Add the keys from your `.env` (BINANCE_API_KEY, etc.).
5.  **Add Redis**: Railway allows you to add a Redis database easily for Celery.

## 4. Connecting Them
Once Backend is live on Railway (e.g., `https://antigravity-backend.up.railway.app`):
1.  Go back to **Vercel** -> Project Settings -> Environment Variables.
2.  Set `NEXT_PUBLIC_API_URL` to your Railway Backend URL.
3.  Redeploy Frontend.
