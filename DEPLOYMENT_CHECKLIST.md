# MamaCare Deployment Checklist

## Pre-Deployment Setup ✅

- [ ] Backend code updated to use environment variables for database
- [ ] CORS configured for Netlify domains
- [ ] gunicorn added to requirements.txt
- [ ] render.yaml file created and configured
- [ ] config.js created for frontend API URL configuration

## Render Backend Deployment

### Step 1: Create Render Account
- [ ] Sign up at https://render.com
- [ ] Connect GitHub account

### Step 2: Deploy Web Service
- [ ] Create new Web Service
- [ ] Select MamaCare repository
- [ ] Configure settings:
  - [ ] Name: `mamacare-backend`
  - [ ] Environment: Python 3
  - [ ] Region: Frankfurt (or closest)
  - [ ] Build Command: `pip install -r backend/requirements.txt && pip install gunicorn`
  - [ ] Start Command: `cd backend && gunicorn --bind 0.0.0.0:$PORT app:app`

### Step 3: Create PostgreSQL Database
- [ ] Create new PostgreSQL service
- [ ] Configure:
  - [ ] Name: `mamacare-db`
  - [ ] Database: `mamacare`
  - [ ] User: `mamacare`
  - [ ] Plan: Free
  - [ ] Region: Same as web service

### Step 4: Set Environment Variables
- [ ] SECRET_KEY (auto-generated)
- [ ] DATABASE_URL (auto-linked from PostgreSQL)
- [ ] FLASK_ENV = production
- [ ] PYTHONUNBUFFERED = 1
- [ ] TIMEZONE = Africa/Freetown
- [ ] EMAIL_USER = your-gmail@gmail.com
- [ ] EMAIL_PASSWORD = your-gmail-app-password
- [ ] TWILIO_ACCOUNT_SID = your-twilio-sid (optional)
- [ ] TWILIO_AUTH_TOKEN = your-twilio-token (optional)
- [ ] TWILIO_PHONE_NUMBER = your-twilio-number (optional)

### Step 5: Deploy and Test
- [ ] Deploy web service
- [ ] Wait for build completion
- [ ] Test health endpoint: `https://your-app.onrender.com/health`
- [ ] Test API endpoints:
  - [ ] GET /api/hospitals
  - [ ] GET /api/doctors
  - [ ] GET /api/pharmacies

## Frontend Updates

### Step 1: Update Configuration
- [ ] Update config.js with actual Render URL
- [ ] Add config.js script to all HTML files
- [ ] Test configuration in browser console

### Step 2: Update API Calls
- [ ] Replace hardcoded localhost:5000 URLs
- [ ] Use configurable base URL or apiFetch helper
- [ ] Test all API calls work with new configuration

### Step 3: Deploy to Netlify
- [ ] Push updated code to GitHub
- [ ] Deploy to Netlify
- [ ] Test frontend-backend communication
- [ ] Check for CORS errors in browser console

## Post-Deployment Verification

### Backend Tests
- [ ] Health check endpoint responds
- [ ] Database connection working
- [ ] All API endpoints accessible
- [ ] Email functionality working (if configured)
- [ ] SMS functionality working (if configured)

### Frontend Tests
- [ ] All pages load correctly
- [ ] API calls work from frontend
- [ ] No CORS errors in console
- [ ] All forms submit successfully
- [ ] File uploads work (if applicable)

### Integration Tests
- [ ] User registration works
- [ ] Login functionality works
- [ ] Medical records can be created/viewed
- [ ] Hospital/doctor/pharmacy listings work
- [ ] Admin dashboard accessible

## Monitoring Setup

- [ ] Check Render logs for errors
- [ ] Monitor database connections
- [ ] Set up error tracking (optional)
- [ ] Configure performance monitoring (optional)

## Security Checklist

- [ ] Environment variables are secure
- [ ] No sensitive data in code
- [ ] CORS properly configured
- [ ] Database credentials secure
- [ ] API endpoints properly protected

## Documentation

- [ ] Update README with deployment info
- [ ] Document environment variables
- [ ] Create troubleshooting guide
- [ ] Document API endpoints

## Final Steps

- [ ] Test complete user journey
- [ ] Verify all features work in production
- [ ] Set up backup strategy
- [ ] Plan for scaling (if needed)
- [ ] Consider custom domain setup

---

**Deployment URL:** https://your-app-name.onrender.com
**Frontend URL:** https://your-app-name.netlify.app

**Notes:**
- Free tier services sleep after 15 minutes of inactivity
- First request after sleep may take 30-60 seconds
- Consider upgrading to paid plan for production use 