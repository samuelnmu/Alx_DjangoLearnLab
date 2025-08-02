# ===============================
# SECURITY CONFIGURATIONS
# ===============================
# These settings are essential for securing your Django application.
# They help protect against common web vulnerabilities like:
# - XSS (Cross-Site Scripting)
# - CSRF (Cross-Site Request Forgery)
# - Clickjacking
# - Cookie theft
# - Host header attacks
# Always enable these in PRODUCTION. In development, you may relax some settings for testing.

# --------------------------------------------------
# 1. Disable DEBUG in production
DEBUG = False  
# WHAT: Turns off Django's debug mode.
# WHY: When True, Django shows detailed error pages with sensitive information.
#      In production, this could leak database passwords, file paths, and server details.
#      Always set to False in production for security.

# --------------------------------------------------
# 2. Restrict allowed hosts
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']  
# WHAT: List of domain names/IP addresses the app will respond to.
# WHY: Prevents HTTP Host header attacks by rejecting requests from unknown hosts.
#      Only allow your actual domain(s) or trusted addresses.

# --------------------------------------------------
# 3. Enable browser-side protections
SECURE_BROWSER_XSS_FILTER = True  
# WHAT: Tells browsers to enable their built-in XSS protection filter.
# WHY: Helps block reflected XSS attacks where malicious code is injected via the URL.
SECURE_CONTENT_TYPE_NOSNIFF = True  
# WHAT: Stops browsers from guessing the MIME type of files.
# WHY: Prevents certain attacks where browsers misinterpret file types (e.g., treating a text file as HTML/JS).
X_FRAME_OPTIONS = 'DENY'  
# WHAT: Prevents the site from being displayed inside an iframe.
# WHY: Protects against clickjacking attacks, where a malicious site overlays invisible buttons over your UI.

# --------------------------------------------------
# 4. Secure cookies
CSRF_COOKIE_SECURE = True  
# WHAT: Ensures the CSRF cookie is sent only over HTTPS.
# WHY: Prevents exposure of CSRF tokens over unsecured HTTP, reducing risk of interception.
SESSION_COOKIE_SECURE = True  
# WHAT: Ensures the session cookie is sent only over HTTPS.
# WHY: Protects session IDs from being stolen over insecure connections.
CSRF_COOKIE_HTTPONLY = True  
# WHAT: Makes the CSRF cookie inaccessible to JavaScript.
# WHY: Reduces the risk of XSS attacks stealing the CSRF token.

# --------------------------------------------------
# 5. Enforce HTTPS using HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000  
# WHAT: Tells browsers to only use HTTPS for the site for 1 year (in seconds).
# WHY: Prevents downgrade attacks where an attacker forces a user to use HTTP instead of HTTPS.
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  
# WHAT: Applies the HSTS rule to all subdomains.
# WHY: Ensures full coverage, so attackers can’t exploit insecure subdomains.
SECURE_HSTS_PRELOAD = True  
# WHAT: Allows your domain to be added to browsers' HSTS preload list.
# WHY: Ensures HTTPS is enforced even on the first visit before HSTS policy is cached.

# --------------------------------------------------
# 6. Content Security Policy (CSP) — optional but recommended
# WHAT: Restricts where content like scripts, styles, and images can be loaded from.
# WHY: Greatly reduces XSS risk by only allowing trusted sources.
# HOW: Either set manually in middleware or use the django-csp package.
# Example configuration if using django-csp:
# INSTALLED_APPS += ['csp']  # Enable django-csp
# MIDDLEWARE += ['csp.middleware.CSPMiddleware']  # Add CSP middleware
# CSP_DEFAULT_SRC = ("'self'",)  # Allow only same-origin content
# CSP_SCRIPT_SRC = ("'self'", 'cdn.jsdelivr.net')  # Allow scripts from self and trusted CDN
# CSP_STYLE_SRC = ("'self'", 'fonts.googleapis.com')  # Allow styles from self and Google Fonts
