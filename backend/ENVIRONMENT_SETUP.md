# Environment Variables Setup for Render

## Default Admin Configuration

You can customize the default admin account by setting these environment variables in your Render service:

### Required Variables
- `DATABASE_URL` - Your PostgreSQL connection string (set by Render automatically)

### Optional Variables (for customizing default admin)
- `DEFAULT_ADMIN_EMAIL` - Default: `alusinekuyateh6@gmail.com`
- `DEFAULT_ADMIN_PASSWORD` - Default: `Admin123`
- `DEFAULT_ADMIN_NAME` - Default: `Alusine Kuyateh`
- `DEFAULT_ADMIN_PHONE` - Default: `+23212345678`

## How to Set Environment Variables in Render

1. **Go to your Render dashboard**
2. **Click on your MamaCare backend service**
3. **Go to "Environment" tab**
4. **Add the variables you want to customize**

## Example Configuration

If you want to use different default admin credentials:

```
DEFAULT_ADMIN_EMAIL=your-email@example.com
DEFAULT_ADMIN_PASSWORD=YourSecurePassword123
DEFAULT_ADMIN_NAME=Your Name
DEFAULT_ADMIN_PHONE=+23212345678
```

## What Happens During Deployment

1. **Database tables are created** (if they don't exist)
2. **Default admin is created** (if no verified admins exist)
3. **Admin is automatically verified**
4. **Application starts normally**

## Default Admin Credentials

If you don't set custom environment variables, the default admin will be:

- **Email**: `alusinekuyateh6@gmail.com`
- **Password**: `Admin123`
- **Name**: `Alusine Kuyateh`
- **Phone**: `+23212345678`
- **Status**: Verified ✅

## Security Note

⚠️ **Important**: Change the default password after your first login!

The default admin is created for initial setup only. For production use, always change the password and consider removing the default admin creation after initial setup. 