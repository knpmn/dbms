# HR Oracle Dashboard

A PHP/Apache web dashboard that connects to an Oracle database and displays 10 HR views.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and **running**
- Network access to the Oracle server (must be on campus/VPN)

---

## Quick Start (one command)

```powershell
# In the project folder:
docker compose up -d --build
```

Then open → **http://localhost:8080**

To stop:
```powershell
docker compose down
```

---

## Fully Automated — use the startup script

A `start.ps1` script is included. Double-click it or right-click → *Run with PowerShell*.  
It will:
1. Check Docker is running
2. Build the image (only rebuilds if something changed)
3. Start the container
4. Open the browser automatically

---

## Changing Oracle Credentials

Edit **`docker-compose.yml`** (the `environment:` section):

```yaml
environment:
  ORA_USER: AI_683380317_6   # ← your Oracle username
  ORA_PASS: p1234            # ← your password
  ORA_HOST: 10.199.8.14      # ← Oracle server IP
  ORA_PORT: 1726             # ← port
  ORA_SID:  ORCLCDB          # ← SID
```

After editing, run: `docker compose up -d --build`

---

## First-time Setup (only once)

The Oracle **views** must exist in your database before the app can display data.  
Run `oracledatabase.sql` against your Oracle server once using SQL*Plus or SQL Developer:

```sql
-- In SQL*Plus:
@oracledatabase.sql
```

---

## Project Structure

```
dbweb/
├── docker-compose.yml   ← credentials & port config
├── Dockerfile           ← builds PHP + OCI8 image
├── oracledatabase.sql   ← creates tables, inserts data, creates views
├── start.ps1            ← one-click startup script
└── www/
    ├── config.php       ← Oracle connection helper
    ├── navbar.php       ← sidebar + shared CSS
    ├── footer.php
    ├── index.php        ← redirects to view1
    ├── view1.php        ← Dept Headcount
    ├── view2.php        ← Monthly Bonus Summary
    ├── view3.php        ← Top Performance Bonus
    ├── view4.php        ← Employee Directory
    ├── view5.php        ← Contract Expiry Alert
    ├── view6.php        ← Penalty History
    ├── view7.php        ← Today's Attendance
    ├── view8.php        ← Monthly Attendance Summary
    ├── view9.php        ← Active Recruitment
    └── view10.php       ← Yearly Bonus Overview
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Page shows `oci_connect() undefined` | Docker image wasn't rebuilt — run `docker compose up -d --build` |
| Page shows Oracle connection error | Wrong credentials in `docker-compose.yml`, or not on campus network |
| Port 8080 already in use | Change `"8080:80"` to e.g. `"8081:80"` in `docker-compose.yml` |
| Container won't start | Make sure Docker Desktop is open and running |
