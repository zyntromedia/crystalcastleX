#!/bin/bash
set -euo pipefail

echo "🚀 เริ่มต้น Migration Agent..."

# 1. โหลดสภาพแวดล้อม
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# 2. ตรวจสอบโฟลเดอร์ชั่วคราว
TMP_DIR="./tmp"
mkdir -p "$TMP_DIR"

# 3. เรียก Planner → สร้างแผน
echo "🧠 ขั้น 1: วางแผน"
python src/planner.py

# 4. ตรวจสอบความถูกต้อง
echo "✅ ขั้น 2: ตรวจสอบสภาพ"
python src/validator.py

# 5. Clone/Mirror
echo "🔄 ขั้น 3: Clone/Mirror"
python src/git_migrator.py

# 6. LFS + Push + ตั้งค่า + ตรวจสอบ
echo "📦 ขั้น 4: LFS & Push"
python src/lfs.py
python src/github_client.py

echo "🧪 ขั้น 5: ตรวจสอบผลลัพธ์"
python src/verifier.py

echo "✅ เสร็จสิ้นการทำงานของ Agent"
