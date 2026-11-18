# So sánh phương án chuyển mạch tụ chuẩn (Cs) — bảo vệ phương án relay G6K

Mục đích: phản biện với mentor về lựa chọn relay G6K, so sánh định lượng với các phương án khác.

---

## 1. Tiêu chí nào thực sự quyết định độ chính xác?

Trong mạch 2 tụ chuẩn, khóa chuyển Cs nằm **song song trong khung cộng hưởng**, nên chỉ có 3 thông số ảnh hưởng trực tiếp:

| Thông số | Ảnh hưởng | Ngân sách cho ±0,3 pF |
|---|---|---|
| **C_off** (khi hở) | cộng thẳng vào C0 → trôi bao nhiêu thì Cp sai bấy nhiêu (1:1) | **ΔC_off ≤ 0,1 pF** |
| **R_on** (khi đóng) | nối tiếp Cs → làm lệch tần số f2 | **R_on ≤ ~10 Ω** |
| **Nhiễu lật** | spike dòng, back-EMF, từ trường | xử lý được bằng thời điểm + tách vật lý |

> Điểm mấu chốt: **C_off không phải là "giá trị" mà là "độ trôi của nó"**. C_off cố định thì hiệu chuẩn bù hết; C_off **trôi theo nhiệt độ/điện áp** thì phá hiệu chuẩn.

---

## 2. Bảng so sánh định lượng

| Phương án | C_off (hở) | R_on (đóng) | Trôi C_off | Nhiễu lật | Dòng khiển | Tốc độ | Giá | Kết luận ±0,3 pF |
|---|---|---|---|---|---|---|---|---|
| **Relay G6K** | **0,3–0,5 pF** | **~50 mΩ** | **~0** | cuộn + back-EMF + từ trường | 33–37 mA | 2–5 ms | ~2 $ | ✅ **đạt** |
| **Reed relay** | 0,1–0,3 pF | 50–100 mΩ | ~0 | cuộn (nhẹ hơn) | 10–20 mA | 1–3 ms | 3–10 $ | ✅ tốt nhất |
| **PhotoMOS (AQY212)** | 1–3 pF | 1–5 Ω | ±0,1–0,3 pF | không (LED) | 3–5 mA | µs–ms | 1–2 $ | ⚠️ biên |
| **74LVC1G66** | ~5 pF | 5–10 Ω | ±0,25–0,5 pF (±25 °C) | không | µA | ns | 0,1 $ | ❌ vượt ngân sách |
| **TS5A3166** | ~5 pF | ~1 Ω | ±0,25–0,5 pF | không | µA | ns | 0,2 $ | ❌ vượt ngân sách |
| **MOSFET 2N7002** | 10–15 pF | 3–6 Ω | ±2–4 pF (theo Vds) | không | µA | ns | 0,03 $ | ❌❌ tệ nhất |
| **PIN diode** | ~1 pF | 1–6 Ω (@5 mA) | tốt | dòng phân cực | 5 mA | µs | 0,1 $ | mạng phân cực phức tạp |
| **JFET** | ~1 pF | 100–500 Ω | tốt | không | µA | µs | khó mua | ❌ R_on quá cao |

### Phương án KHÔNG dùng khóa
| Phương án | Ưu | Nhược |
|---|---|---|
| **Hai dao động song song** | không khóa, không nhiễu | 2× comparator + 2× tank; DUT phải nối cả 2 → không thực tế |
| **Quét trở kháng (mini-VNA)** | đo trực tiếp Z(ω), không khóa | cần DDS + detector + ADC, nhiều mã, xử lý hài |

---

## 3. Phân tích sai số định lượng

### 3.1 Ảnh hưởng của C_off trôi
Cp được tính: `Cp = C_A − (C0 + Cstray + C_off)`. Nếu C_off trôi ΔC_off thì **Cp sai đúng ΔC_off** (1:1):

- Relay: 0,5 pF × ~0 % → **~0 pF** ✅
- Analog switch: 5 pF × 5–10 % (±25 °C) → **0,25–0,5 pF** ❌ (> 0,3 pF)
- MOSFET: 12 pF × 20–30 % → **2–4 pF** ❌❌

### 3.2 Ảnh hưởng của R_on (lệch tần số f2)
Tụ Cs nối tiếp R_on làm C_eff giảm: `Δf/f ≈ ½(ω·R_on·Cs)²`. Ở f2 ≈ 4,2 MHz, Cs = 100 pF:

| R_on | ωRC | Δf/f | ΔCp ≈ 231,6 pF × Δf/f |
|---|---|---|---|
| 0,05 Ω (relay) | 1,3e-4 | ~0 | **~0 pF** ✅ |
| 5 Ω (analog switch) | 1,3e-2 | 8,7e-5 | **0,02 pF** ✅ |
| 10 Ω | 2,6e-2 | 3,5e-4 | 0,08 pF ✅ |
| 50 Ω | 0,13 | 8,7e-3 | **2,0 pF** ❌ |
| 500 Ω (JFET) | 1,3 | 0,87 | 202 pF ❌❌ |

→ **R_on ≤ 10 Ω là đủ**; relay và analog switch đều đạt, JFET/PhotoMOS R_on cao thì không.

### 3.3 Vì sao C_off của bán dẫn trôi
- C_off của CMOS/MOSFET là **điện dung vùng nghèo (junction)**, phụ thuộc **nhiệt độ** (~+0,3–0,5 %/K) và **điện áp Vds**.
- Tank dao động ±0,3 V → C_off **biến thiên theo tín hiệu** (phi tuyến) → lệch tần phụ thuộc biên độ.
- Relay: C_off là **khe hở cơ khí cố định** → không phụ thuộc nhiệt độ/điện áp.

---

## 4. Cái giá đánh đổi

| | Relay G6K | Analog switch / PhotoMOS |
|---|---|---|
| **Được** | C_off ~0, R_on ~0 → **chính xác nhất** | không cuộn → **không nhiễu**, µA, ns, nhỏ, rẻ |
| **Mất** | cuộn 37 mA, 2–5 ms, to (6,5×10 mm), 2 $, cần driver Q4+D1+R4 | C_off 5 pF trôi 0,25–0,5 pF → **mất độ chính xác** |
| **Chi phí cụ thể** | +2 $, +50 ms/lần đo, +~18 mA trung bình | ±0,25–0,5 pF (vượt ngân sách ±0,3 pF) |

**Tính toán chi phí relay:**
- Cuộn 37 mA, chỉ bật ở trạng thái B (~50 % thời gian đo) → trung bình ~18 mA.
- Pin 500 mAh → vẫn chạy ~27 h. **Không đáng kể.**
- Chậm 50 ms/lần đo → không đáng kể với máy cầm tay.

→ Cái giá của relay **nhỏ và hữu hình** (2 $, 50 ms, 18 mA). Cái giá của bán dẫn **lớn và vô hình** (sai số 0,25–0,5 pF, phụ thuộc nhiệt độ).

---

## 5. Phương án nào tốt nhất?

### Theo mục tiêu ±0,3 pF (độ chính xác là ưu tiên số 1)
**Relay G6K** (hoặc reed relay nếu cần C_off thấp hơn nữa).

### Theo từng trường hợp
| Trường hợp | Phương án tốt nhất | Lý do |
|---|---|---|
| **Độ chính xác cao, dải nhiệt rộng** | **Relay G6K / Reed relay** | C_off ~0, không trôi |
| **Cầm tay, nhiệt độ phòng ổn định, cần rẻ/nhỏ** | **74LVC1G66 / TS5A3166** | C_off trôi chỉ ~0,04 pF nếu ΔT ≤ 2 °C; hiệu chuẩn tại nhiệt độ làm việc |
| **Cần bán dẫn, không cuộn, chính xác khá** | **PhotoMOS AQY212** | C_off 1–3 pF, không nhiễu cuộn |
| **Cần tuyệt đối không khóa** | **Quét trở kháng (mini-VNA)** | đo trực tiếp Z(ω), không có C_off |
| **Chỉ đo L, không cần Cp chính xác** | MOSFET 2N7002 | rẻ nhất, C_oss trôi không quan trọng |

---

## 6. Trả lời trực tiếp mentor

> "Đúng là relay có nhược điểm: cuộn 37 mA, to, 2 $, và khi lật có spike/back-EMF/từ trường. Nhưng **nhiễu đó xử lý được** (rail riêng 3.3VD, diode D1, chỉ lật giữa 2 lần đo, tách vật lý ≥5 mm). Còn **nhược điểm của bán dẫn thì không xử lý được**: C_off 5 pF trôi 0,25–0,5 pF theo nhiệt độ/điện áp — **vượt ngân sách ±0,3 pF** của bài toán. Nên đây là đánh đổi: **relay đổi 2 $ + 50 ms + 18 mA để lấy ±0 pF; bán dẫn đổi 0 $ + nhỏ + không nhiễu để lấy ±0,25–0,5 pF sai số.** Với một *dụng cụ đo*, tôi chọn vế thứ nhất."

> "Nếu mentor muốn bán dẫn, phương án bảo vệ được là **PhotoMOS AQY212** (không cuộn, C_off 1–3 pF), chấp nhận hiệu chuẩn theo nhiệt độ."

---

## 7. Kết luận 1 câu

**Relay G6K thắng vì C_off ~0 và không trôi — đúng thứ quyết định ±0,3 pF; mọi nhược điểm khác của relay đều xử lý được hoặc không đáng kể. Bán dẫn chỉ thắng khi bài toán không cần Cp chính xác, hoặc khi nhiệt độ làm việc ổn định và chấp nhận hiệu chuẩn nhiệt.**
