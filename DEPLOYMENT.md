# Deployment Guide for Render

This guide will help you deploy the AI Mental Health Support Agent (Sunny) to Render.

## 📋 Prerequisites

Before deploying, ensure you have:

1. **GitHub Account** - Your code must be in a GitHub repository
2. **Render Account** - Sign up at [render.com](https://render.com)
3. **API Keys** - You'll need:
   - `GROQ_API_KEY` - Your Groq API key for LLM access
   - `HUGGINGFACE_API_TOKEN` - Your HuggingFace token for embeddings

## 🚀 Deployment Methods

### Method 1: Using render.yaml (Recommended)

This method uses Infrastructure as Code for automated deployment.

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Create New Web Service on Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml`
   - Click "Apply" to create the service

3. **Set Environment Variables** (if not using sync: false)
   - In Render Dashboard, go to your service
   - Navigate to "Environment" tab
   - Add the following secret variables:
     - `GROQ_API_KEY` = `your_groq_api_key_here`
     - `HUGGINGFACE_API_TOKEN` = `your_huggingface_token_here`

4. **Deploy**
   - Render will automatically deploy your app
   - Wait for the build to complete (5-10 minutes)
   - Your app will be available at: `https://mentalhealth-ai-sunny.onrender.com`

### Method 2: Manual Deployment

1. **Create New Web Service**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your repository and branch

2. **Configure Service**
   - **Name**: `mentalhealth-ai-sunny` (or your preferred name)
   - **Region**: Singapore (or closest to your users)
   - **Branch**: `main`
   - **Runtime**: Python 3
   - **Build Command**: 
     ```
     pip install --upgrade pip && pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```
     gunicorn interface.web.app:app
     ```

3. **Set Environment Variables**
   Click "Advanced" → "Add Environment Variable" and add:
   
   | Key | Value |
   |-----|-------|
   | `PYTHON_VERSION` | `3.11.9` |
   | `GROQ_API_KEY` | Your Groq API key |
   | `HUGGINGFACE_API_TOKEN` | Your HuggingFace token |
   | `FLASK_SECRET_KEY` | Random secure string (or let Render generate) |
   | `RERANKER_ENABLED` | `true` |
   | `RERANKER_MODEL` | `cross-encoder/ms-marco-TinyBERT-L-2-v2` |
   | `RERANKER_THRESHOLD` | `0.0` |
   | `TOKENIZERS_PARALLELISM` | `false` |

4. **Advanced Settings**
   - **Health Check Path**: `/health`
   - **Auto-Deploy**: Yes (recommended)

5. **Create Web Service**
   - Click "Create Web Service"
   - Wait for deployment to complete

## 💰 Pricing Considerations

### Free Tier Limitations
- **Memory**: 512 MB (May be insufficient for PyTorch + sentence-transformers)
- **Build Time**: Services spin down after inactivity
- **Cold Starts**: 30+ seconds to wake up

### Recommended Plan
- **Starter Plan** ($7/month):
  - 512 MB RAM - **Still may be tight**
  - Always online (no cold starts)
  - Custom domains

- **Standard Plan** ($25/month):
  - **2 GB RAM** - **Recommended for this app**
  - Better performance
  - Suitable for production use

⚠️ **Important**: Your app uses PyTorch and sentence-transformers which are memory-intensive. The Standard plan (2GB RAM) is recommended for stable operation.

## 🗄️ Data Persistence Considerations

### ⚠️ Critical: ChromaDB Storage Issue

Render uses **ephemeral filesystem** by default, meaning:
- ChromaDB data stored in `./data/chroma_db` will be **lost on every deploy/restart**
- Your knowledge base will need to be re-initialized each time

### Solutions:

#### Option 1: Render Disks (Recommended for Production)
1. Go to your service in Render Dashboard
2. Navigate to "Disks" tab
3. Add a new disk:
   - **Mount Path**: `/opt/render/project/src/data`
   - **Size**: 1 GB (adjust based on your knowledge base size)
4. Redeploy your service

**Pros**: Data persists across deploys
**Cons**: Costs $0.25/GB/month

#### Option 2: Cloud Vector Database (Best for Scale)
Switch to a hosted vector database service:
- **Pinecone** - Managed vector database
- **Weaviate Cloud** - Open-source vector database
- **Qdrant Cloud** - High-performance vector search

**Pros**: Scalable, reliable, no disk management
**Cons**: Requires code changes, additional service cost

#### Option 3: Accept Re-initialization (Development Only)
Let the app re-initialize ChromaDB on each deploy from your knowledge files.

**Pros**: No additional cost
**Cons**: Slower startup (1-3 minutes), not suitable for production

## 🔍 Monitoring Your Deployment

### Check Deployment Status
1. Go to your service in Render Dashboard
2. View "Logs" tab for real-time logs
3. Check "Events" tab for deployment history

### Health Check
Once deployed, test the health endpoint:
```bash
curl https://your-app-name.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "agent_system": "operational",
  "reranker_enabled": false,
  "timestamp": "2025-11-13T10:30:00.000Z"
}
```

### Test the App
Visit your deployed URL:
```
https://your-app-name.onrender.com
```

You should see the landing page with Sunny's introduction.

## 🐛 Troubleshooting

### Build Fails
**Issue**: `pip install` fails
**Solution**: 
- Check if all dependencies in `requirements.txt` are compatible with Python 3.11
- Review build logs in Render Dashboard
- Try specifying exact versions for problematic packages

### Out of Memory
**Issue**: App crashes with memory errors
**Solution**:
- Upgrade to Standard plan (2GB RAM)
- Disable reranker by setting `RERANKER_ENABLED=false`
- Optimize PyTorch installation (CPU-only version)

### ChromaDB Not Initialized
**Issue**: "Retriever not initialized" errors
**Solution**:
- Ensure knowledge files are committed to repository
- Check build logs for ChromaDB initialization errors
- Consider adding a Render Disk for persistence

### Slow Cold Starts
**Issue**: First request takes 30+ seconds
**Solution**:
- Upgrade to paid plan to keep service always online
- Implement a keep-alive service (ping your app every 10 minutes)

### Environment Variables Not Set
**Issue**: "GROQ_API_KEY not found" error
**Solution**:
- Verify all environment variables are set in Render Dashboard
- Check for typos in variable names
- Redeploy after adding variables

## 🔐 Security Best Practices

1. **Never commit `.env` file** to repository (already in `.gitignore`)
2. **Use Render's Environment Variables** for all secrets
3. **Generate strong FLASK_SECRET_KEY** (use Render's auto-generation)
4. **Enable HTTPS** (Render provides this automatically)
5. **Limit CORS** if adding API endpoints
6. **Monitor logs** for suspicious activity

## 📊 Performance Optimization

### Reduce Memory Usage
If memory is an issue, consider:

1. **Disable Reranker**:
   ```env
   RERANKER_ENABLED=false
   ```

2. **Use CPU-only PyTorch**:
   Update `requirements.txt`:
   ```
   torch>=2.0.0+cpu
   ```

3. **Reduce ChromaDB Collection Size**:
   - Limit knowledge base files
   - Increase chunk size to reduce embeddings

### Improve Response Time
1. **Use caching** for frequently accessed data
2. **Optimize LLM settings** (reduce max_tokens, temperature)
3. **Pre-warm ChromaDB** on startup

## 🔄 Continuous Deployment

### Automatic Deploys
With Auto-Deploy enabled:
1. Push changes to GitHub
2. Render automatically detects and deploys
3. Monitor deployment in Render Dashboard

### Manual Deploys
1. Go to Render Dashboard
2. Select your service
3. Click "Manual Deploy" → "Deploy latest commit"

## 📞 Support Resources

- **Render Documentation**: https://render.com/docs
- **Render Status**: https://status.render.com/
- **Render Community**: https://community.render.com/
- **This Project Issues**: https://github.com/jefflyt/MentalHealth_AI/issues

## ✅ Post-Deployment Checklist

- [ ] App is accessible at deployed URL
- [ ] Landing page loads correctly
- [ ] Chat interface works
- [ ] Assessment tools function
- [ ] Resources page displays
- [ ] Health check endpoint returns healthy status
- [ ] ChromaDB initialized successfully
- [ ] Environment variables are secure
- [ ] Custom domain configured (if applicable)
- [ ] Monitoring/logging set up
- [ ] Data persistence solution implemented

## 🎉 Success!

Your AI Mental Health Support Agent is now live on Render! 

**Next Steps**:
1. Share the URL with test users
2. Monitor performance and logs
3. Gather feedback
4. Iterate and improve

**Your app URL**: `https://your-app-name.onrender.com`

---

**Need Help?** Create an issue on GitHub or contact the development team.

**Built with 💙 for Mental Health Support**
