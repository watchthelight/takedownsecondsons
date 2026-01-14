# RECON SUMMARY: secondsons.org
**Date:** 2026-01-13
**Phase:** 2 - Reconnaissance
**Status:** Complete

---

## Subdomains (11 found, 3 confirmed live)

| Subdomain | Status | Technology | Notes |
|-----------|--------|------------|-------|
| `www.secondsons.org` | **LIVE (200)** | WordPress 6.9, LiteSpeed, Elementor, PHP | Main site |
| `secondsons.club.secondsons.org` | **LIVE (200)** | Ruby on Rails, Bootstrap, jQuery 3.7.1 | **Separate app stack!** |
| `www.secondsons.club.secondsons.org` | **LIVE (200)** | Ruby on Rails, Bootstrap | Mirror of above |
| `matrix.secondsons.org` | Unknown | - | Matrix chat server |
| `pay.secondsons.org` | Unknown | - | **Payment portal** |
| `www.pay.secondsons.org` | Unknown | - | Payment portal mirror |
| `preview.secondsons.org` | Unknown | - | Preview/staging |
| `secondsons-preview-880917626.secondsons.org` | Unknown | - | **Numbered staging instance** |
| `openpgpkey.secondsons.org` | Unknown | - | PGP key distribution |
| `*.secondsons.org` | Wildcard | - | Wildcard cert exists |

---

## Tech Stack

### Main Site (www.secondsons.org)

| Component | Value |
|-----------|-------|
| CMS | WordPress 6.9 (Latest - 2025-12-02) |
| Theme | Skelementor 1.1.4 |
| Page Builder | **Elementor Pro** |
| E-Commerce | **WooCommerce** (detected in archives) |
| Server | LiteSpeed |
| Cache | LiteSpeed Cache |
| Protocol | HTTP/3 (QUIC) |
| WAF | **Wordfence (Defiant)** |
| Security Headers | CSP: `object-src 'none'`, HSTS |
| Language | PHP |
| JS Libraries | jQuery, jQuery Migrate, Swiper, SmartMenus |

### Secondary Site (secondsons.club subdomain)

| Component | Value |
|-----------|-------|
| Framework | Ruby on Rails |
| CSS | Bootstrap |
| JS | jQuery 3.7.1 |
| Server | LiteSpeed |

---

## Interesting URLs (477 unique found)

### CRITICAL - Hidden Directories Discovered

| Path | Description |
|------|-------------|
| `/d0n0tc0ncede/` | **Renamed wp-admin directory** (admin-ajax.php found) |
| `/1dev1/` | **Development/staging WordPress instance** |
| `/members/` | Members-only area |

### WordPress Paths

- `/wp-admin/` (standard, likely redirects)
- `/wp-content/`
- `/wp-json/` (REST API)
- `/wp-cron.php` (externally accessible)
- `/readme.html` (exposed)
- `/wp-sitemap.xml`

### Well-Known Endpoints

| URL | Status |
|-----|--------|
| `/.well-known/security.txt` | Check for contact info |
| `/.well-known/openid-configuration` | OpenID config |
| `/.well-known/ai-plugin.json` | AI plugin manifest |
| `/.well-known/gpc.json` | Global Privacy Control |

### Potential Sensitive Files

- `/robots.txt` - Empty (no disallow rules = everything crawlable)
- `/ads.txt`, `/app-ads.txt` - Advertising config
- `/feed.xml`, `/atom.xml` - RSS feeds

### E-Commerce Evidence (WooCommerce)

```
/core/modules/39d10ee62c/assets/css/woocommerce.css
/core/modules/39d10ee62c/assets/js/frontend/add-to-cart.min.js
/core/modules/39d10ee62c/assets/js/frontend/woocommerce.min.js
```

### Interesting Hashed Paths

- `/z0f76a1d14fd21a8fb5fd0d03e0fdc3d3cedae52f` - Unknown hash-based URL
- `/a9bc224bd710f56d27affffddc764239b58c3faa0/` - Another hash directory

---

## DNS Records

```
A Record:      66.223.49.32
MX Record:     mail.secondsons.org (priority 0) - Self-hosted mail
NS Records:    epsilon1.kc.epik.com, epsilon2.kc.epik.com (Epik hosting)
SPF:           v=spf1 ip4:66.223.49.32 ip4:66.223.49.33 include:_spf.epikwebhosting.com +a +mx ~all
CNAME (www):   secondsons.org
```

### Email Security Assessment

- ✅ SPF configured
- ❓ DKIM - Not checked
- ❓ DMARC - Not checked
- ⚠️ Self-hosted mail server (mail.secondsons.org)

---

## Site Structure (from crawler)

### Public Pages

- `/` - Homepage
- `/faq/` - FAQ
- `/contact/` - Contact form
- `/index.php/join-us/` - Membership signup
- `/members/` - Members area

### Social Media Links

- Telegram: t.me/secondsonscanada
- Twitter/X: x.com/SecondSonsCA
- Facebook: facebook.com/profile.php?id=61574436783539
- Instagram: instagram.com/secondsonsca

### robots.txt
Empty (only comment, no rules)

### Sitemap
WordPress default at `/wp-sitemap.xml`

---

## Attack Surface Priority List

### 🔴 HIGH PRIORITY

| Finding | Risk | Action |
|---------|------|--------|
| **Hidden admin at `/d0n0tc0ncede/`** | Admin panel discovery | Probe for login, test default creds |
| **Dev instance at `/1dev1/`** | May have debug enabled, weaker security | Full scan, check for exposed config |
| **`pay.secondsons.org`** | Payment processing = sensitive data | Full assessment when live |
| **External WP-Cron enabled** | DDoS amplification vector | Check for abuse potential |
| **Ruby on Rails app** on club subdomain | Separate attack surface, different vulns | Rails-specific testing |
| **Self-hosted mail server** | Potential phishing/spoofing vector | Check open relay, DMARC |

### 🟡 MEDIUM PRIORITY

| Finding | Risk | Action |
|---------|------|--------|
| `/wp-json/` REST API | Information disclosure, potential vulns | Enumerate endpoints |
| `readme.html` exposed | WordPress version disclosure | Minor info leak |
| Must Use Plugins directory | Plugin enumeration | List and research plugins |
| WooCommerce installed | E-commerce vulns, payment testing | Test checkout flow |
| Hash-based URLs | Unknown functionality | Investigate purpose |
| `/members/` area | Auth bypass potential | Test access controls |
| Staging subdomains | May have weaker security | Probe when discovered |

### 🟢 LOW PRIORITY

| Finding | Risk | Action |
|---------|------|--------|
| Empty robots.txt | Full site indexable | Note for report |
| Social media links | OSINT vectors | Social engineering intel |
| `.well-known` endpoints | Standard configs | Review for misconfig |
| Multiple JS libraries | Potential outdated versions | Version check |

---

## Recommended Phase 3 Focus Areas

### 1. Probe hidden admin `/d0n0tc0ncede/`

```bash
curl -I https://www.secondsons.org/d0n0tc0ncede/
curl -I https://www.secondsons.org/d0n0tc0ncede/wp-login.php
```

### 2. Investigate dev instance `/1dev1/`

```bash
gobuster dir -u https://www.secondsons.org/1dev1/ -w $SECLISTS/Discovery/Web-Content/common.txt
```

### 3. Full WPScan with plugin enumeration

```bash
wpscan --url https://www.secondsons.org -e ap,at,cb,dbe --plugins-detection aggressive
```

### 4. Probe inactive subdomains

```bash
for sub in pay matrix preview; do
  curl -sI "https://$sub.secondsons.org" | head -5
done
```

### 5. Ruby on Rails assessment on club subdomain

```bash
nuclei -u https://secondsons.club.secondsons.org -t cves/,vulnerabilities/
```

### 6. REST API enumeration

```bash
curl -s https://www.secondsons.org/wp-json/ | jq '.routes | keys'
```

---

## Files Generated

| File | Size | Contents |
|------|------|----------|
| subfinder.txt | 242B | 9 subdomains |
| crt_sh.json | 21KB | Certificate transparency |
| wayback_urls.txt | 40KB | 475 historical URLs |
| gau_urls.txt | 40KB | 477 URLs |
| dns_records.txt | 321B | DNS records |
| httpx_live.txt | 603B | 3 live hosts with tech |
| hakrawler.txt | 4.8KB | Crawled links |
| wafw00f.txt | 877B | Wordfence detected |
| wpscan.txt | 3.7KB | WordPress enumeration |
| whatweb.txt | 144B | Error (SSL issue) |
| robots_sitemap.txt | 140B | Empty robots.txt |

---

## API Usage

**WPScan API:** 2/25 calls used today (23 remaining)

---

## Output Location

All raw scan data saved to:
```
~/Documents/Projects/pentesting/tools/output/secondsons/recon/
```
