import requests

def send(mobile: str, provider: str = "file"):
    if provider == "file":
        url = "https://api.filemarket.com.tr/v1/otp/send"
        payload = {"mobilePhoneNumber": f"90{mobile}"}
        try:
            r = requests.post(url, json=payload, timeout=5)
            ok_status = (r.status_code == 200)
            try:
                body = r.json()
                ok_body = (body.get("data") == "200 OK")
            except ValueError:
                ok_body = False

            if ok_status and ok_body:
                return {"success": True, "provider": "File", "response": r.text}
            return {"success": False, "provider": "File", "code": r.status_code, "response": r.text}
        except requests.exceptions.RequestException as e:
            return {"success": False, "provider": "File", "error": str(e)}

    elif provider == "kredim":
        url = "https://api.kredim.com.tr/api/v1/Communication/SendOTP"
        headers = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "origin": "https://member.kredim.com.tr",
            "referer": "https://member.kredim.com.tr/",
            "user-agent": "Mozilla/5.0",
        }
        payload = {
            "source": "Register",
            "type": 8,
            "gsmNumber": f"+90{mobile}",
            "templateCode": "VerifyMember",
            "originator": "OTP|KREDIM",
        }
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=10)
            if r.status_code == 200:
                return {"success": True, "provider": "KREDIM", "response": r.text}
            return {"success": False, "provider": "KREDIM", "code": r.status_code, "response": r.text}
        except requests.exceptions.RequestException as e:
            return {"success": False, "provider": "KREDIM", "error": str(e)}

    return {"success": False, "message": "Unknown provider"}
