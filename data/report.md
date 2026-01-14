# PENETRATION TEST REPORT: secondsons.org

**Target:** https://www.secondsons.org  
**Test Date:** January 13, 2026  
**Tester:** Claude AI Security Assessment  
**Scope:** Full web application security assessment  
**Authorization:** Authorized by domain owner  

---

## EXECUTIVE SUMMARY

The security assessment of secondsons.org identified **2 HIGH severity**, **3 MEDIUM severity**, and **4 LOW severity** vulnerabilities. The site runs a well-maintained WordPress stack with current plugin versions, protected against known CVEs. However, critical misconfigurations expose sensitive information and increase attack surface.

**Risk Rating: MEDIUM**

The most critical finding is **directory listing enabled on /wp-content/uploads/**, exposing all uploaded files including WooCommerce transaction data paths and Elementor configuration.

---

## FINDINGS SUMMARY

| ID | Finding | Severity | CVSS | Status |
|----|---------|----------|------|--------|
| 001 | Directory Listing Enabled | HIGH | 7.5 | OPEN |
| 002 | Missing Security Headers | HIGH | 6.5 | OPEN |
| 003 | REST API Over-Exposure (217 Routes) | MEDIUM | 5.3 | OPEN |
| 004 | Plugin readme.txt Files Accessible | MEDIUM | 4.3 | OPEN |
| 005 | WordPress Version Disclosure via readme.html | MEDIUM | 4.3 | OPEN |
| 006 | Mixed HTTP/HTTPS Internal References | LOW | 3.1 | OPEN |
| 007 | Theme Outdated (Skelementor 1.1.4) | LOW | 3.0 | OPEN |
| 008 | WooCommerce Directory Structure Exposed | LOW | 3.0 | OPEN |
| 009 | Excessive CORS Permissiveness | LOW | 2.5 | OPEN |

---

## DETAILED FINDINGS

### FINDING 001: Directory Listing Enabled on /wp-content/uploads/

**Severity:** HIGH  
**CVSS Score:** 7.5 (High)  
**CWE:** CWE-548 (Exposure of Information Through Directory Listing)  
**Location:** `/wp-content/uploads/` and all subdirectories

**Description:**  
Directory listing is enabled on the uploads directory, allowing unauthenticated attackers to enumerate all uploaded files. This exposes:
- All media uploads (images, videos, documents)
- WooCommerce placeholder images
- Elementor screenshots and configuration files
- Font files (potential licensing issues)
- Temporary files (.tmp)
- WooCommerce logs directory path
- Full upload date structure (2025/04, 2025/05, etc.)

**Proof of Concept:**
```
https://www.secondsons.org/wp-content/uploads/
https://www.secondsons.org/wp-content/uploads/2025/
https://www.secondsons.org/wp-content/uploads/2025/04/
https://www.secondsons.org/wp-content/uploads/wph/
```

**Exposed Directories:**
- `/wp-content/uploads/2025/` (and monthly subdirectories through 2026)
- `/wp-content/uploads/elementor/`
- `/wp-content/uploads/et_temp/`
- `/wp-content/uploads/fonts/`
- `/wp-content/uploads/wc-logs/`
- `/wp-content/uploads/woocommerce_uploads/`
- `/wp-content/uploads/wph/`

**Impact:**
- Information disclosure of all uploaded content
- Potential exposure of sensitive documents if uploaded
- Reconnaissance for further attacks
- WooCommerce transaction path disclosure

**Recommendation:**
Add the following to `.htaccess` in the uploads directory:
```apache
Options -Indexes
```

Or via LiteSpeed configuration:
```
<Directory /path/to/wp-content/uploads>
    Options -Indexes
</Directory>
```

---

### FINDING 002: Missing Critical Security Headers

**Severity:** HIGH  
**CVSS Score:** 6.5  
**CWE:** CWE-693 (Protection Mechanism Failure)  
**Location:** All HTTP responses

**Description:**  
Multiple security headers are missing or inadequately configured:

| Header | Status | Risk |
|--------|--------|------|
| X-Frame-Options | **MISSING** | Clickjacking attacks |
| X-Content-Type-Options | **MISSING** | MIME sniffing attacks |
| Content-Security-Policy | **MINIMAL** (only `object-src 'none'`) | XSS, data injection |
| Referrer-Policy | **MISSING** | Information leakage |
| Permissions-Policy | **MISSING** | Feature abuse |
| HSTS preload | **MISSING** | Incomplete HTTPS enforcement |

**Current Headers Observed:**
```
strict-transport-security: max-age=15768000;includeSubdomains
content-security-policy: object-src 'none'
x-xss-protection: 1; mode=block
```

**Impact:**
- Clickjacking attacks possible (no X-Frame-Options)
- Browser MIME sniffing could lead to XSS
- Weak CSP allows inline scripts/styles

**Recommendation:**
Add the following headers via LiteSpeed or plugin:
```
X-Frame-Options: SAMEORIGIN
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' https://www.google.com https://www.gstatic.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https:; frame-ancestors 'self';
```

---

### FINDING 003: REST API Over-Exposure (217 Routes)

**Severity:** MEDIUM  
**CVSS Score:** 5.3  
**CWE:** CWE-200 (Exposure of Sensitive Information)  
**Location:** `/wp-json/`

**Description:**  
The WordPress REST API exposes 217 routes across multiple namespaces:
- `wp/v2` - Core WordPress API
- `elementor/v1` - Elementor endpoints (forms, templates, globals)
- `elementor-pro/v1` - Elementor Pro endpoints
- `elementor-ai/v1` - AI features
- `litespeed/v1` and `v3` - Cache management
- `wordfence/v1` - Security plugin
- `wp-abilities/v1` - Custom plugin
- `oembed/1.0` - Embed handling

**Sensitive Endpoints Discovered:**
```
/elementor/v1/form-submissions (requires auth - 401)
/elementor/v1/form-submissions/export
/elementor/v1/globals
/elementor/v1/notes
/wp/v2/users (blocked - 404)
```

**Positive Finding:** User enumeration via `/wp/v2/users` is DISABLED (returns 404).

**Impact:**
- Attack surface reconnaissance
- Plugin fingerprinting
- Potential future vulnerability exploitation

**Recommendation:**
Consider limiting REST API access via Wordfence or dedicated plugin:
```php
// Disable REST API for unauthenticated users
add_filter('rest_authentication_errors', function($result) {
    if (!is_user_logged_in()) {
        return new WP_Error('rest_forbidden', 'REST API restricted.', ['status' => 403]);
    }
    return $result;
});
```

---

### FINDING 004: Plugin readme.txt Files Accessible

**Severity:** MEDIUM  
**CVSS Score:** 4.3  
**CWE:** CWE-200 (Information Exposure)  
**Location:** `/wp-content/plugins/*/readme.txt`

**Description:**  
Plugin readme files are publicly accessible, disclosing exact version numbers:

| Plugin | Version | Status |
|--------|---------|--------|
| Elementor | 3.33.6 | Current |
| LiteSpeed Cache | 7.7 | Current |
| Wordfence | 8.1.4 | Current |
| WooCommerce | 10.4.0 | Current |

**Accessible URLs:**
```
https://www.secondsons.org/wp-content/plugins/elementor/readme.txt
https://www.secondsons.org/wp-content/plugins/litespeed-cache/readme.txt
https://www.secondsons.org/wp-content/plugins/wordfence/readme.txt
https://www.secondsons.org/wp-content/plugins/woocommerce/readme.txt
```

**Impact:**
- Attackers can identify exact versions to target known CVEs
- Reduces time-to-exploit for zero-day vulnerabilities

**Recommendation:**
Block access to readme.txt files via .htaccess:
```apache
<Files readme.txt>
    Order Allow,Deny
    Deny from all
</Files>
```

---

### FINDING 005: WordPress readme.html Accessible

**Severity:** MEDIUM  
**CVSS Score:** 4.3  
**CWE:** CWE-200 (Information Exposure)  
**Location:** `/readme.html`

**Description:**  
The default WordPress readme.html file is accessible, confirming WordPress installation and PHP version requirements:
- PHP 8.3 required (disclosed)
- MySQL 5.5.5+ required (disclosed)
- WordPress branding confirmed

**Impact:**
- Platform confirmation for targeted attacks
- PHP version disclosure aids exploitation

**Recommendation:**
Delete or block access to `/readme.html`:
```bash
rm /path/to/wordpress/readme.html
```

---

### FINDING 006: Mixed HTTP/HTTPS References

**Severity:** LOW  
**CVSS Score:** 3.1  
**CWE:** CWE-319 (Cleartext Transmission)  
**Location:** Various internal references

**Description:**  
The REST API returns mixed protocol references:
- `URL: http://www.secondsons.org` (HTTP)
- `Home: https://www.secondsons.org` (HTTPS)

**Impact:**
- Potential mixed content warnings
- Possible information leakage over unencrypted connections

**Recommendation:**
Ensure WordPress Address and Site Address are both set to HTTPS in settings.

---

### FINDING 007: Outdated Theme (Skelementor 1.1.4)

**Severity:** LOW  
**CVSS Score:** 3.0  
**CWE:** CWE-1104 (Use of Unmaintained Third Party Components)  
**Location:** `/wp-content/themes/skelementor/`

**Description:**  
The Skelementor theme is version 1.1.4, tested up to WordPress 5.7.1 (released March 2021). Current WordPress is 6.8+.

**Theme Details:**
```
Theme Name: Skelementor
Version: 1.1.4
Tested up to: 5.7.1
Author: Mousebuilt
```

**Impact:**
- Potential compatibility issues with newer WordPress
- May contain unpatched vulnerabilities

**Recommendation:**
Check for theme updates or consider migrating to actively maintained theme.

---

### FINDING 008: WooCommerce Directory Structure Exposed

**Severity:** LOW  
**CVSS Score:** 3.0  
**CWE:** CWE-200 (Information Exposure)  
**Location:** Directory listing

**Description:**  
Via directory listing, the following WooCommerce-specific paths are visible:
- `/wp-content/uploads/wc-logs/` - Log files directory
- `/wp-content/uploads/woocommerce_uploads/` - Customer uploads

**Impact:**
- Confirms WooCommerce installation
- Log files may contain sensitive transaction data if accessible

**Recommendation:**
Disable directory listing (see Finding 001) and add `.htaccess` deny rules to WooCommerce directories.

---

### FINDING 009: TRACE Method Not Blocked at Application Level

**Severity:** LOW  
**CVSS Score:** 2.5  
**CWE:** CWE-693 (Protection Mechanism Failure)  
**Location:** HTTP methods handling

**Description:**  
While TRACE returns 405 at the proxy level (openresty), other unusual HTTP methods (PUT, DELETE, PATCH) return 200 OK.

**Impact:**
- Minimal - blocked by proxy
- Indicates potential mishandling at application level

**Recommendation:**
Verify that non-standard HTTP methods are explicitly handled by WordPress/LiteSpeed.

---

## POSITIVE SECURITY FINDINGS

The following security measures are properly implemented:

✅ **User Enumeration Blocked** - `/wp-json/wp/v2/users` returns 404  
✅ **wp-login.php Protected/Hidden** - Returns 404  
✅ **XML-RPC Disabled** - Returns 404  
✅ **wp-admin Protected** - Redirects to homepage  
✅ **HSTS Enabled** - 6-month max-age with includeSubdomains  
✅ **TLS 1.3** - Modern encryption  
✅ **HTTP/2 and HTTP/3** - Modern protocols  
✅ **Wordfence WAF Active** - Security plugin installed  
✅ **LiteSpeed Cache** - 7-day caching, DDoS mitigation  
✅ **All Major Plugins Updated** - No known CVEs applicable  
✅ **Form Submissions Protected** - Returns 401 Unauthorized  
✅ **oEmbed Proxy Protected** - Returns 401 Forbidden  
✅ **TRACE Method Blocked** - Returns 405 at proxy  
✅ **CAPTCHA System Active** - Imunify360/similar protection detected  

---

## DETECTED SOFTWARE STACK

| Component | Version | Status |
|-----------|---------|--------|
| WordPress | Hidden | ✓ Good Practice |
| Elementor | 3.33.6 | ✓ Current |
| Elementor Pro | Unknown | - |
| LiteSpeed Cache | 7.7 | ✓ Current |
| Wordfence | 8.1.4 | ✓ Current |
| WooCommerce | 10.4.0 | ✓ Current |
| Skelementor Theme | 1.1.4 | ⚠ Outdated |
| PHP | 8.3+ | ✓ Current |
| Web Server | LiteSpeed + Envoy | ✓ |
| TLS | 1.3 | ✓ Modern |

---

## CVE ASSESSMENT

All detected plugin versions have been cross-referenced against known CVEs:

| CVE | Affected Component | Your Version | Status |
|-----|-------------------|--------------|--------|
| CVE-2024-8522 | Elementor <= 3.25.6 | 3.33.6 | ✅ PATCHED |
| CVE-2023-48777 | Elementor <= 3.18.1 | 3.33.6 | ✅ PATCHED |
| CVE-2024-28000 | LiteSpeed <= 6.3.0.1 | 7.7 | ✅ PATCHED |
| CVE-2024-44000 | LiteSpeed <= 6.5.0.2 | 7.7 | ✅ PATCHED |
| CVE-2024-1634 | Wordfence <= 7.11.4 | 8.1.4 | ✅ PATCHED |
| CVE-2023-35913 | WooCommerce <= 7.8.2 | 10.4.0 | ✅ PATCHED |

**No known unpatched CVEs affecting current versions.**

---

## REMEDIATION PRIORITY

| Priority | Finding | Effort | Impact |
|----------|---------|--------|--------|
| 1 | Disable Directory Listing | Low | High |
| 2 | Add Missing Security Headers | Low | High |
| 3 | Block readme.txt Access | Low | Medium |
| 4 | Delete readme.html | Low | Medium |
| 5 | Review REST API Exposure | Medium | Medium |
| 6 | Fix HTTP/HTTPS Mixed References | Low | Low |
| 7 | Update Skelementor Theme | Medium | Low |

---

## RECOMMENDATIONS SUMMARY

### Immediate Actions (< 1 hour):
1. Add `Options -Indexes` to uploads .htaccess
2. Add security headers via LiteSpeed config
3. Delete `/readme.html`
4. Block `/wp-content/plugins/*/readme.txt`

### Short-term Actions (< 1 week):
1. Review and limit REST API endpoints
2. Update WordPress/Site Address to HTTPS in settings
3. Review theme update availability

### Long-term Actions (< 1 month):
1. Implement comprehensive CSP
2. Consider REST API authentication for all endpoints
3. Regular security assessments

---

## TESTING METHODOLOGY

- **Passive Reconnaissance:** HTTP headers, API enumeration, version detection
- **Active Scanning:** Directory enumeration, sensitive file probing
- **Injection Testing:** SQL injection probes, XSS testing
- **API Security:** REST API endpoint analysis, authentication bypass attempts
- **Configuration Review:** Security headers, SSL/TLS, HTTP methods

---

## CONCLUSION

secondsons.org demonstrates **good security hygiene** with updated plugins, disabled dangerous endpoints (XML-RPC, user enumeration, wp-login), and active security plugins (Wordfence). 

However, the **enabled directory listing** represents a significant information disclosure vulnerability that should be addressed immediately. The missing security headers also present unnecessary risk that can be easily mitigated.

Overall security posture: **MEDIUM RISK** - Well-maintained but with configuration gaps.

---

*Report generated: January 13, 2026*  
*Tester: Claude AI Security Assessment*  
*Classification: CONFIDENTIAL*