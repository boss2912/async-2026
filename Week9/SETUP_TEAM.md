# Week9 F1 Telemetry — คู่มือติดตั้งสำหรับสมาชิกในกลุ่ม

> **Redis Server รันที่เครื่องเดียวเท่านั้น** (เครื่องที่ลง Docker)
> อีก 4 คน **ไม่ต้องลง Docker** แค่ต่อเข้ามา

---

## ขั้นที่ 1 — ลง Python library (ทุกคน)

```bash
pip install redis rich
```

> ⛔ **ห้ามลง `asyncio` จาก pip** ถึงแม้ใบงานจะเขียนไว้ว่า `pip install redis asyncio rich`
> `asyncio` เป็น stdlib ของ Python อยู่แล้ว แพ็กเกจชื่อซ้ำบน PyPI เป็นของเก่าปี 2015
> ถ้าลงไปจะไปทับ stdlib แล้วพังทั้งโปรเจกต์

---

## ขั้นที่ 2 — แก้ config (ทุกคน)

เปิดไฟล์ **ของบทบาทตัวเองไฟล์เดียว** แล้วแก้ 3 บรรทัดบนสุด

| บทบาท | ไฟล์ที่ต้องแก้ | REDIS_HOST | GROUP_ID | STUDENT_ID |
|---|---|---|---|---|
| Student 1 | `student1_telemetry_producer.py` | บรรทัด 8 | บรรทัด 9 | บรรทัด 10 |
| Student 2 | `student2_pit_strategy_engineer.py` | บรรทัด 5 | บรรทัด 6 | บรรทัด 7 |
| Student 3 | `student3_race_control_engine_safety.py` | บรรทัด 5 | บรรทัด 6 | บรรทัด 7 |
| Student 4 | `student4_DRS_automation_controller.py` | บรรทัด 5 | บรรทัด 6 | บรรทัด 7 |
| Student 5 | `student5_dashboard_broadcaster.py` | บรรทัด 6 | บรรทัด 7 | บรรทัด 8 |
| จอทีม (ใครก็ได้) | `dashboard_listener.py` | บรรทัด 10 | บรรทัด 11 | — (ไม่มี) |

ค่าที่ต้องใส่:

```python
REDIS_HOST = '172.20.56.145'   # ตั้งไว้ให้แล้ว ไม่ต้องแก้ (ยกเว้น IP เปลี่ยน)
GROUP_ID   = 'g01'             # << ต้องตรงกันทั้ง 5 คน
STUDENT_ID = '66010002'        # << รหัสนักศึกษาตัวเอง ห้ามซ้ำกับเพื่อน
```

---

## ขั้นที่ 3 — เทสว่าต่อ Redis ติดไหม (ทุกคน ทำก่อนเสมอ)

```bash
python -c "import redis; print(redis.Redis(host='172.20.56.145',port=6379,socket_connect_timeout=3).ping())"
```

* ได้ `True` → ผ่าน ไปขั้นที่ 4
* ค้างแล้ว error → **โดน Firewall** ให้เจ้าของเครื่อง Redis เปิด port 6379 (ดูท้ายไฟล์)

---

## ขั้นที่ 4 — รันไฟล์ของตัวเอง

**Windows ต้องตั้ง encoding ก่อน** ไม่งั้นจะ crash ตอน print emoji

PowerShell:
```powershell
$env:PYTHONIOENCODING = "utf-8"
python student2_pit_strategy_engineer.py
```

CMD:
```cmd
set PYTHONIOENCODING=utf-8
python student2_pit_strategy_engineer.py
```

หรือใช้ตัวช่วยที่เตรียมไว้ (PowerShell):
```powershell
.\run.ps1 student2_pit_strategy_engineer.py
```

อาการถ้าลืมตั้ง:
```
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f3ce'
```

---

## ขั้นที่ 5 — ลำดับการรันตอนซ้อมในกลุ่ม

> ⚠️ **ลำดับในใบงาน (ข้อ 5.2) ผิด** ใบงานให้ set GREEN ก่อนแล้วค่อยรัน Student 1
> ทำแบบนั้นแล้ว Student 1 จะค้างที่ `Waiting for Teacher to RESET...` ไม่ยอมออกตัว
>
> เพราะโค้ด `wait_for_new_green_light()` บังคับให้เห็นการ**เปลี่ยนสถานะ** STOPPED → GREEN
> ถ้าเจอ GREEN ค้างอยู่ตั้งแต่แรก มันจะรอ reset ตลอดไป
>
> **ใช้ลำดับข้างล่างนี้แทน**

1. เจ้าของเครื่อง Redis สั่ง `docker compose up -d`

2. **รีเซ็ตสถานะเป็น STOPPED ก่อน** (สำคัญ — ทำทุกครั้งก่อนซ้อมรอบใหม่)
   ```bash
   python -c "import redis; redis.Redis(host='172.20.56.145',port=6379).set('f1:race:status','STOPPED')"
   ```

3. เปิดจอทีม → `dashboard_listener.py`

4. Student 2, 3, 4, 5 รันไฟล์ตัวเอง

5. **Student 1 รันตอนนี้** จะต้องขึ้นข้อความนี้ ถึงจะถูกต้อง:
   ```
   🚦 [g01] Ready on Grid! Waiting for Teacher's GREEN LIGHT...
   ```
   ถ้าขึ้น `⏳ Waiting for Teacher to RESET the race status (STOPPED)...` แปลว่าลืมทำข้อ 2

6. **ปล่อยตัว** — ใครก็ได้เปิด terminal ใหม่แล้วสั่ง:
   ```bash
   python -c "import redis; redis.Redis(host='172.20.56.145',port=6379).set('f1:race:status','GREEN')"
   ```

ผลที่ควรเห็น (ทดสอบจริงแล้ว):
```
Student 1 : 🏎️ [g01] Sent ID: ... | Speed: 234.4 km/h | Dist: 3.3 m
Student 4 : 🟢 [DRS SYSTEM] DRS ENABLED! Speed: 281.9 km/h (Gear 7)
Student 2 : 🛞 ⚠️ [PIT STRATEGY] Prepare Soft Compound. Tires at 56.5%
```

### ล้างข้อมูลก่อนซ้อมรอบใหม่

```bash
python -c "import redis; r=redis.Redis(host='172.20.56.145',port=6379); r.delete('f1:telemetry:g01'); r.set('f1:race:status','STOPPED'); print('cleared')"
```
ถ้าไม่ล้าง stream เก่าจะค้าง ทำให้ระยะทางกับ consumer group เพี้ยน

---

## เช็คลิสต์เวลาระบบเงียบ ไม่มีข้อมูลไหล

ไล่ตามลำดับนี้ อย่าข้าม

1. **`GROUP_ID` ตรงกันทุกคนไหม** — ไม่ตรง = คนละ stream, **ไม่มี error ใดๆ เลย** เงียบสนิท เจอบ่อยที่สุด
2. **`STUDENT_ID` ซ้ำกันไหม** — ซ้ำ = consumer name ชน Redis แบ่งงานมั่ว
3. **`REDIS_HOST` ยังเป็น `localhost` อยู่ไหม** — ถ้าใช่ = ต่อเข้าเครื่องตัวเอง ไม่ใช่เครื่องกลาง
4. **ping ผ่านไหม** (ขั้นที่ 3)
5. **`f1:race:status` เป็น `GREEN` หรือยัง** — Student 1 จะไม่ยิงข้อมูลจนกว่าจะได้ไฟเขียว

---

## สำหรับเจ้าของเครื่อง Redis เท่านั้น

```bash
docker compose up -d     # เปิด
docker ps                # ต้องเห็น f1-redis  Up
docker compose down      # ปิด
```

ถ้าเพื่อนต่อไม่ติด → เปิด PowerShell **แบบ Run as Administrator** แล้วสั่ง:
```powershell
New-NetFirewallRule -DisplayName "Redis F1 Lab" -Direction Inbound -LocalPort 6379 -Protocol TCP -Action Allow
```
เสร็จงานแล้วลบทิ้ง:
```powershell
Remove-NetFirewallRule -DisplayName "Redis F1 Lab"
```

> ⚠️ IP `172.20.56.145` มาจาก DHCP ผ่าน Wi-Fi **เปลี่ยนได้เมื่อรีบูตหรือย้ายเน็ต**
> ก่อนเริ่มงานทุกครั้ง เจ้าของเครื่องเช็คด้วย `ipconfig` แล้วแจ้งเพื่อนถ้าเลขเปลี่ยน
