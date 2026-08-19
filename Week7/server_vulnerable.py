"""
Server Machine 1 : ระบบที่มีช่องโหว่ (ไม่มี Lock)

วิธีรัน (ต้องใส่ --host 0.0.0.0 ไม่งั้นเพื่อนในวง LAN ต่อเข้ามาไม่ได้):
    uvicorn server_vulnerable:app --host 0.0.0.0 --port 8088 --reload
"""
import asyncio
from typing import Dict, List
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Coupon Hunting - VULNERABLE (No Lock)")

STUDENTS = ["6710301004", "6710301006", "6710301023", "6710301025", "6710301022"]
GROUP_SIZE = len(STUDENTS)
TOTAL_COUPONS = (GROUP_SIZE * 2) - 1

coupons_db: List[str] = [f"COUPON-{i:02d}" for i in range(1, TOTAL_COUPONS + 1)]

# ใช้ Pointer ชี้ตำแหน่งคูปองใบถัดไปที่จะจ่ายแจก
current_coupon_index = 0

student_claims: Dict[str, List[str]] = {student_id: [] for student_id in STUDENTS}


class ClaimRequest(BaseModel):
    student_id: str


@app.post("/claim")
async def claim_coupon(req: ClaimRequest):
    global current_coupon_index
    student_id = req.student_id

    if student_id not in student_claims:
        return {"status": "INVALID_STUDENT", "message": "ไม่พบรายชื่อในระบบ"}

    # ── โซนอันตรายจุดที่ 1: อ่านโควตาส่วนตัว ─────────────────────────
    # เช็คตรงนี้ผ่านแล้ว แต่ยังไม่ได้จองสิทธิ์ ระหว่างที่หลับที่ await ข้างล่าง
    # request ใบอื่นของคนเดียวกันก็เช็คผ่านได้อีก -> ได้เกิน 2 ใบ
    if len(student_claims[student_id]) >= 2:
        return {"status": "LIMIT_REACHED", "message": "คุณรับคูปองครบ 2 ใบแล้ว"}

    # ── โซนอันตรายจุดที่ 2: Read - Modify - Write คร่อม await ────────
    if current_coupon_index < len(coupons_db):

        # READ : จำตำแหน่งคูปองที่จะหยิบไว้ "ก่อน" จะหลับ
        index_to_claim = current_coupon_index

        # PAUSE : จุดสลับงานของ Event Loop
        # ระหว่างนี้ task อื่นเข้ามาอ่าน current_coupon_index ตัวเดิมได้
        # เพราะยังไม่มีใครขยับ Pointer เลยสักคน
        await asyncio.sleep(0.1)

        # WRITE : ตื่นมาแล้วใช้ค่าเก่าที่ค้างอยู่ในมือ
        # ทุกคนที่อ่าน index เดียวกันไว้ จะได้ "คูปองใบเดียวกัน" ทั้งหมด
        coupon = coupons_db[index_to_claim]
        student_claims[student_id].append(coupon)

        # Pointer ขยับแค่ทีละ 1 ทั้งที่จ่ายคูปองออกไปหลายใบ -> แจกเกินสต็อก
        current_coupon_index = index_to_claim + 1

        return {
            "status": "SUCCESS",
            "claimed_coupon": coupon,
            "total_owned": len(student_claims[student_id])
        }

    return {
        "status": "OUT_OF_STOCK",
        "message": "คูปองหมดแล้ว"
    }


@app.get("/my-coupons/{student_id}")
async def get_my_coupons(student_id: str):
    """ดูคูปองเฉพาะของนักเรียนคนเดียว (client.py เรียกใช้ตอนจบภารกิจ)"""
    if student_id not in student_claims:
        return {"status": "INVALID_STUDENT", "message": "ไม่พบรายชื่อในระบบ"}

    my_coupons = student_claims[student_id]
    return {
        "student_id": student_id,
        "total_claimed": len(my_coupons),
        "claimed_coupons": my_coupons
    }


@app.get("/summary")
async def get_summary():
    # รวมคูปองที่จ่ายออกไปจริงทั้งหมด เพื่อเทียบกับสต็อกที่ควรจะมี
    all_issued = [c for coupons in student_claims.values() for c in coupons]

    # หารหัสที่ถูกแจกซ้ำ (อาการของ Race Condition ที่เห็นชัดที่สุด)
    duplicated = sorted({c for c in all_issued if all_issued.count(c) > 1})

    return {
        "remaining_stock": len(coupons_db) - current_coupon_index,
        "total_coupons_in_stock": TOTAL_COUPONS,
        "total_issued": len(all_issued),
        "over_issued": len(all_issued) - TOTAL_COUPONS,
        "duplicated_coupons": duplicated,
        "student_claims": student_claims
    }
