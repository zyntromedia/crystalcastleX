import os
import subprocess
import requests
from typing import Tuple, List

class MigrationValidator:
    def __init__(self, token: str, session_id: str):
        self.token = token
        self.session_id = session_id
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def check_git_tools(self) -> bool:
        """ตรวจ Git + Git LFS ติดตั้งหรือไม่"""
        try:
            subprocess.run(["git", "--version"], check=True, capture_output=True)
            subprocess.run(["git", "lfs", "--version"], check=True, capture_output=True)
            return True
        except Exception:
            self.errors.append("Git หรือ Git LFS ไม่พบในระบบ")
            return False

    def check_github_auth(self) -> bool:
        """ตรวจ Token & ขอบเขตสิทธิ์"""
        headers = {"Authorization": f"Bearer {self.token}", "Accept": "application/vnd.github.v3+json"}
        resp = requests.get("https://api.github.com/user", headers=headers)
        if resp.status_code != 200:
            self.errors.append(f"Token ไม่ถูกต้องหรือหมดอายุ (HTTP {resp.status_code})")
            return False
        
        # ตรวจสิทธิ์เพิ่มเติม
        scopes = resp.headers.get("X-OAuth-Scopes", "")
        required = ["repo", "admin:org"]
        missing = [s for s in required if s not in scopes]
        if missing:
            self.errors.append(f"สิทธิ์ขาด: {', '.join(missing)}")
            return False
        return True

    def check_repo_access(self, url: str) -> bool:
        """ตรวจสอบการเข้าถึงคลังต้นทาง"""
        try:
            result = subprocess.run(
                ["git", "ls-remote", url],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode != 0:
                self.errors.append(f"เข้าถึงคลังไม่ได้: {url}")
                return False
            return True
        except Exception:
            self.errors.append("หมดเวลาหรือผิดพลาดในการเชื่อมต่อ")
            return False

    def validate_all(self, source_url: str) -> Tuple[bool, dict]:
        """รันการตรวจสอบทั้งหมด"""
        git_ok = self.check_git_tools()
        auth_ok = self.check_github_auth()
        repo_ok = self.check_repo_access(source_url)

        return all([git_ok, auth_ok, repo_ok]), {
            "session_id": self.session_id,
            "valid": all([git_ok, auth_ok, repo_ok]),
            "errors": self.errors,
            "warnings": self.warnings
        }

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    val = MigrationValidator(os.getenv("GITHUB_TOKEN", ""), "test-session")
    ok, res = val.validate_all("https://github.com/example/source")
    print(json.dumps(res, indent=2))
