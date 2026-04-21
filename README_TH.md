# 🤖 Bitkub DCA Bot

[![DCA Bot](https://github.com/PattoMotto/bitkub-dca-bot/actions/workflows/dca_bot.yml/badge.svg)](https://github.com/PattoMotto/bitkub-dca-bot/actions/workflows/dca_bot.yml)

> **[🇹🇭 อ่านภาษาไทย](README_TH.md) | [🇬🇧 Read in English](README.md)**
> **[🎥 ดูวิดีโอสอนการใช้งาน](https://youtu.be/9TbMAWm_qIk)**

> **สะสมคริปโตอัตโนมัติ แม่นยำ และง่ายดาย**

การต้องมานั่งเช็คกราฟทุกวันมันเหนื่อยเกินไป **Bitkub DCA Bot** คือเครื่องมือ Python ขนาดเล็กแต่แข็งแกร่ง ที่ออกแบบมาเพื่อช่วยคุณทำ Dollar-Cost Averaging (DCA) บน [Bitkub Exchange](https://www.bitkub.com/) ได้แบบอัตโนมัติ ไม่ว่าคุณจะสะสม Sats หรือเก็บเหรียญ Altcoins ที่ชื่นชอบ บอทตัวนี้จะช่วยให้คุณมีวินัยในการลงทุนโดยไม่ต้องใช้อารมณ์เข้ามาร่วมด้วย

## ✨ ฟีเจอร์เด่น

- **🚀 การซิงค์เวลาอัจฉริยะ**: ซิงค์เวลากับเซิร์ฟเวอร์ Bitkub อัตโนมัติ เพื่อป้องกันปัญหา "Invalid Timestamp"
- **🔐 ความปลอดภัยระดับองค์กร**: ใช้การยืนยันตัวตนด้วย HMAC-SHA256 มาตรฐานสำหรับการเรียกใช้ API ที่ปลอดภัย
- **⚙️ ตั้งค่าผ่าน Environment Variable**: กำหนดค่าต่างๆ ผ่าน environment variables ทั้งหมด เหมาะสำหรับ CI/CD pipelines (GitHub Actions) หรือ Docker
- **🛡 การจัดการข้อผิดพลาดที่แข็งแกร่ง**: แจ้งเตือนสาเหตุของปัญหาอย่างชัดเจน เช่น ชื่อเหรียญผิด หรือสิทธิ์การเข้าถึงไม่ถูกต้อง
- **⚡️ เบาและรวดเร็ว**: สร้างขึ้นโดยใช้ dependencies น้อยที่สุด เพื่อให้ทำงานได้รวดเร็วและใช้ทรัพยากรน้อย

## 🛠 สิ่งที่ต้องมี

- Python 3.6+
- [บัญชี Bitkub](https://www.bitkub.com/) ที่เปิดใช้งานการเข้าถึง API แล้ว

## ⚙️ การตั้งค่า

บอทจะถูกตั้งค่าผ่าน **Environment Variables** ทั้งหมด ทำให้ปลอดภัยและสามารถ deploy ได้ทุกที่

| ตัวแปร | คำอธิบาย | ค่าเริ่มต้น | จำเป็น |
|----------|-------------|---------|----------|
| `API_KEY` | Public Key ของ Bitkub API | - | **ใช่** |
| `API_SECRET` | Secret Key ของ Bitkub API | - | **ใช่** |
| `BUY_AMOUNT` | จำนวนเงิน (THB) ที่ต้องการซื้อต่อครั้ง | `108` | ไม่ |
| `SYMBOL` | คู่เหรียญที่ต้องการซื้อ (เช่น `ETH_THB`) | `BTC_THB` | ไม่ |

## 🤖 การทำงานอัตโนมัติด้วย GitHub Actions (แนะนำ)

บอทนี้ถูกตั้งค่ามาพร้อมกับ GitHub Actions workflow (`.github/workflows/dca_bot.yml`) ที่รองรับทั้งการตั้งเวลาอัตโนมัติและการกดสั่งงานด้วยตัวเอง

### 1. Fork Repository
คลิกปุ่ม **Fork** ที่มุมขวาบนของหน้านี้ เพื่อคัดลอก repository ไปเป็นของคุณเอง

### 2. ตั้งค่า Secrets & Environment
1. ไปที่เมนู **Settings** > **Environments** ของ repository
2. สร้าง environment ใหม่ชื่อ `production`
3. เพิ่ม `API_KEY` และ `API_SECRET` ใน **Environment Secrets** ภายใต้ `production` environment
4. (ทางเลือก) เพิ่ม `BUY_AMOUNT` และ `SYMBOL` ใน **Environment Variables** หากต้องการเปลี่ยนค่าเริ่มต้น

### 3. ตัวเลือกการตั้งเวลา (Schedule Options)
โดยปกติ บอทจะทำงาน **ทุกวัน** (Daily) คุณสามารถเปลี่ยนการตั้งค่านี้โดยการ uncomment บรรทัดที่ต้องการในไฟล์ `.github/workflows/dca_bot.yml`:

- **รายวัน (Daily)**: `0 2 * * *` (09:00 น. เวลาไทย) <-- **ค่าเริ่มต้น**
- **รายสัปดาห์ (Weekly)**: `0 2 * * 1` (ทุกวันจันทร์ เวลา 09:00 น.)
- **รายชั่วโมง (Hourly)**: `0 * * * *`
- **ทุก 12 ชั่วโมง**: `0 2,14 * * *`

### 4. การสั่งงานด้วยตัวเอง (Manual Trigger)
คุณสามารถสั่งให้บอททำงานทันทีด้วยการกำหนดค่าเอง:
1. ไปที่แท็บ **Actions** ใน repository
2. เลือก **DCA Bot** จากเมนูซ้ายมือ
3. คลิก **Run workflow**
4. (ทางเลือก) ระบุจำนวนเงินม `Amount to Buy` (ค่าเริ่มต้น: 108) และ `Crypto Pair` (ค่าเริ่มต้น: BTC_THB)
5. คลิก **Run workflow**

### 5. ข้อควรจำสำหรับการตั้งค่า ⚠️
- **กฎ Environment**: ตรวจสอบให้แน่ใจว่า environment `production` ถูกตั้งค่าอย่างถูกต้องใน Settings > Environments (หากเป็น Private repo อาจต้องเปิดใช้งาน environment ก่อน)
- **การเปิดใช้งาน Action**: ไปที่ **Settings > Actions > General** และเลือก "Allow all actions and reusable workflows" เพื่อให้บอทสามารถทำงานได้

## 📦 การติดตั้ง

1. **Clone repository**
   ```bash
   git clone https://github.com/PattoMotto/bitkub-dca-bot.git
   cd bitkub-dca-bot
   ```

2. **ติดตั้ง dependencies**
   ```bash
   pip install requests
   ```



## 🚀 การใช้งาน

### 1. การรันบนเครื่องตัวเอง (Local)
คุณสามารถรันบอทผ่าน terminal ได้โดยตรง

**Linux/macOS:**
```bash
export API_KEY="your_actual_api_key"
export API_SECRET="your_actual_api_secret"
export BUY_AMOUNT="1000"
export SYMBOL="ETH_THB"

python main.py
```

**Windows (PowerShell):**
```powershell
$env:API_KEY="your_actual_api_key"
$env:API_SECRET="your_actual_api_secret"
$env:BUY_AMOUNT="1000"
$env:SYMBOL="ETH_THB"

python main.py
```

### 2. ตัวอย่างผลลัพธ์
เมื่อทำงานสำเร็จ บอทจะแสดงสรุปรายการสั่งซื้อ:
```text
🕒 Time: 1703421234567
🚀 Buying 108.0 THB of BTC_THB...
✅ SUCCESS!
   Order ID: 12345678
   Spend Amount: 108
   Full Response: {...}
```

## 🧪 การทดสอบ

คุณสามารถตรวจสอบการทำงานของบอทและ log ได้โดยไม่ต้องทำการซื้อขายจริง โดยใช้สคริปต์ทดสอบที่มีให้:

```bash
python test_main.py
```

คำสั่งนี้จะทำการจำลองสถานการณ์การซื้อขายและตรวจสอบรูปแบบของผลลัพธ์ว่าถูกต้องหรือไม่



## ⚠️ คำเตือน

ซอฟต์แวร์นี้จัดทำขึ้นเพื่อการศึกษาเท่านั้น การเทรดด้วยระบบอัตโนมัติมีความเสี่ยง โปรดมั่นใจว่าคุณได้ทดสอบด้วยจำนวนเงินน้อยๆ และทำความเข้าใจโค้ดก่อนที่จะเริ่มใช้งานจริง ผู้เขียนโปรแกรมไม่รับผิดชอบต่อความสูญเสียทางการเงินใดๆ ที่เกิดขึ้น

## 💰 สนับสนุน (Donate)

หากคุณพบบอทนี้มีประโยชน์ คุณสามารถสนับสนุนการพัฒนาได้โดยการบริจาค:

- **BTC Address:** `bc1qm7ktthfyeghpmdqjcnumfxse4d8h0g3pgujxr6`
- **LN Address:** `mumbledpunch57@walletofsatoshi.com`

---
*Maintained by @PattoMotto*
