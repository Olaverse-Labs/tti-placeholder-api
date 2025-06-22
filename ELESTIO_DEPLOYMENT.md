# Elestio Deployment Guide

This guide will help you deploy your Text-to-Image Placeholder API on Elestio.

## Prerequisites

1. An Elestio account
2. Your code pushed to a Git repository (GitHub, GitLab, or Bitbucket)
3. Docker installed locally (for testing)

## Step 1: Prepare Your Repository

Make sure your repository contains these files:
- `main.py` - Your FastAPI application
- `requirements.txt` - Python dependencies
- `Dockerfile` - Docker configuration
- `.dockerignore` - Docker ignore file
- `docker-compose.yml` - Docker Compose configuration (optional)

## Step 2: Deploy on Elestio

### Option A: Using Elestio Dashboard

1. **Login to Elestio Dashboard**
   - Go to [elest.io](https://elest.io)
   - Sign in to your account

2. **Create New Service**
   - Click "Create New Service"
   - Select "Docker" as the service type

3. **Configure Service**
   - **Service Name**: `tti-placeholder-api` (or your preferred name)
   - **Repository**: Select your Git repository
   - **Branch**: `main` (or your default branch)
   - **Port**: `8000`
   - **Build Command**: Leave empty (Dockerfile will handle this)
   - **Start Command**: Leave empty (Dockerfile CMD will handle this)

4. **Environment Variables** (Optional)
   - Add any environment variables if needed
   - For this API, no additional environment variables are required

5. **Deploy**
   - Click "Create Service"
   - Elestio will automatically build and deploy your application

### Option B: Using Elestio CLI

1. **Install Elestio CLI**
   ```bash
   npm install -g @elestio/cli
   ```

2. **Login to Elestio**
   ```bash
   elestio login
   ```

3. **Deploy Service**
   ```bash
   elestio deploy --repo your-username/your-repo --port 8000 --name tti-placeholder-api
   ```

## Step 3: Verify Deployment

1. **Check Service Status**
   - Go to your Elestio dashboard
   - Check that your service shows "Running" status

2. **Test the API**
   - Your API will be available at: `https://your-service-name.elestio.app`
   - Test the health endpoint: `https://your-service-name.elestio.app/health`
   - Test image generation: `https://your-service-name.elestio.app/generate?text=Hello%20World`

3. **Check Logs**
   - In the Elestio dashboard, click on your service
   - Go to the "Logs" tab to monitor application logs

## Step 4: Custom Domain (Optional)

1. **Add Custom Domain**
   - In your Elestio dashboard, go to your service
   - Click "Settings" → "Custom Domain"
   - Add your domain (e.g., `api.yourdomain.com`)

2. **Configure DNS**
   - Point your domain to Elestio's servers
   - Add the CNAME record provided by Elestio

## Step 5: SSL Certificate

Elestio automatically provides SSL certificates for your services, so your API will be available over HTTPS.

## Testing Your Deployed API

Once deployed, test these endpoints:

### Health Check
```bash
curl https://your-service-name.elestio.app/health
```

### Basic Image Generation
```bash
curl "https://your-service-name.elestio.app/generate?text=Hello%20World&width=800&height=400"
```

### Advanced Image with Gradient
```bash
curl "https://your-service-name.elestio.app/generate/advanced?text=Gradient%20Test&gradient=true&gradient_color1=%23ff0000&gradient_color2=%2300ff00"
```

### API Documentation
- Swagger UI: `https://your-service-name.elestio.app/docs`
- ReDoc: `https://your-service-name.elestio.app/redoc`

## Monitoring and Maintenance

1. **Monitor Logs**
   - Regularly check the logs in Elestio dashboard
   - Set up alerts for any errors

2. **Scale if Needed**
   - Elestio allows you to scale your service up or down
   - Adjust resources based on your usage

3. **Updates**
   - Push changes to your repository
   - Elestio will automatically redeploy with the new code

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Check the build logs in Elestio dashboard
   - Ensure all dependencies are in `requirements.txt`
   - Verify the Dockerfile is correct

2. **Service Not Starting**
   - Check the application logs
   - Verify the port configuration (should be 8000)
   - Ensure the health check endpoint is working

3. **Image Generation Issues**
   - Check if Pillow is properly installed
   - Verify font availability on the server
   - Check memory usage for large images

### Support

- Elestio Documentation: [docs.elest.io](https://docs.elest.io)
- Elestio Support: Available through the dashboard

## Cost Optimization

- Start with the smallest plan and scale up as needed
- Monitor resource usage in the Elestio dashboard
- Consider using Elestio's free tier for testing

## Security Considerations

- The Dockerfile runs the application as a non-root user
- Health checks are enabled for monitoring
- All traffic is served over HTTPS
- Consider adding rate limiting for production use 