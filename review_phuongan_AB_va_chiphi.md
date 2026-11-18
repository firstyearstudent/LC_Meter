# Nghiên cứu 2 cách sửa mạch dao động (A/B) + ước tính chi phí LCSC/JLCPCB

Bổ sung cho `review_LCR_EPC_meter.md`. Kết quả mô phỏng SPICE (ngspice, model hành vi của TLV3501) và ước tính giá.

---

## 1. Quyết định về "IC băm tần số"

**Bỏ qua** (đúng hướng). Khâu tạo dao động vẫn dùng comparator nhanh TLV3501; không thêm prescaler/chia tần/PLL. Lý do vật lý: độ trễ vòng phải ≤ 5–7 ns ở dải 10 µH; IC chia tần đặt *sau* bộ dao động không thay được vai trò này, còn IC dao động+chia tần (74HC4060/4046) có trễ 15–25 ns → sai số Cp > 0,5 pF.

---

## 2. Kết quả nghiên cứu 2 cách (mô phỏng ngspice)

Hai cách sửa lỗi phân cực DC của mạch dao động hiện tại:

- **Cách A**: mắc nối tiếp 1 tụ 10 nF với R12 (phá hồi tiếp dương DC), giữ DUT nối GND qua SMA.
- **Cách B**: nối đầu lạnh DUT vào V_BIAS (1,65 V) thay vì GND, bỏ C17, nối IN− thẳng V_BIAS; DUT nối trực tiếp vào IN+ (kẹp Kelvin 2 chân thay SMA).

Mô hình: TLV3501 = comparator ngắt cứng rail-to-rail (hysteresis ~6 mV), DUT = L nối tiếp Rs + Cp song song. Đo tần số dao động ở trạng thái ổn định.

| Ca | Cách A | Cách B | f lý tưởng |
|---|---|---|---|
| 10 µH, trạng thái A (33 pF) | dao động **tắt dần → chốt** sau ~0,1 ms | **ổn định 8,06 MHz** | 8,16 MHz |
| 10 µH, trạng thái B (33+100 pF) | — | **ổn định 4,27 MHz** | 4,28 MHz |
| 100 µH, trạng thái A | dao động chớp tắt | **ổn định 2,58 MHz** | 2,58 MHz |
| 100 µH, trạng thái B | — | **ổn định 1,36 MHz** | 1,37 MHz |

**Kết luận định lượng:**
- **Cách B dao động bền vững trên toàn dải**, tần số lệch lý tưởng < 1,2 % (số lệch nhỏ này là do góc pha của khâu kích; bù bằng firmware theo `tpd` như báo cáo).
- **Cách A chỉ dao động tạm thời rồi tắt (chốt)** ở 10 µH. Nguyên nhân: vòng có thêm 2 tụ nối tiếp (Cser + C17), làm suy giảm/đổi pha tín hiệu ở nút IN+, khiến độ lợi vòng ở biên Q thấp ≤ 1 → biên độ tắt dần rồi comparator chốt. Nói cách khác, cách A chỉ "dịch" vấn đề chốt, không giải quyết triệt để.

**→ Vì bạn ưu tiên "chính xác + phải chạy được", chọn Cách B.**

Lợi ích thêm của Cách B cho máy handheld:
- Bỏ được C17, R13, C16 (nối IN− thẳng V_BIAS) → ít linh kiện, ít Cstray hơn.
- DUT nối trực tiếp vào IN+ → tín hiệu không qua tụ ghép → ít nguồn sai số hơn.
- Kẹp 2 chân/Kelvin tiện hơn cắm cuộn cảm vào SMA (SMA vốn bất tiện cho handheld).
- V_BIAS trở thành AC-ground của khung cộng hưởng → phải decoupling tốt (4,7 µF ∥ 100 nF sát gá đo).

Lưu ý khi làm Cách B:
1. **V_BIAS phải trở kháng thấp**: dùng cầu phân áp 100k/100k + decoupling 4,7 µF ∥ 100 nF ngay tại gá đo; lý tưởng thêm op-amp buffer nếu muốn chắc.
2. **C16 = 10 µF (IN−→GND) hiện tại gây chậm khởi động τ = R13·C16 = 1 s**. Cách B bỏ luôn R13/C16 → hết vấn đề. Nếu giữ, đổi 10 µF → 100 nF.
3. Tụ chuẩn phải là **C0G/NP0 ±1 %** (C18 = 33 pF, C12 = 100 pF). Tụ ±5 %/±10 % hiện tại không đạt chỉ tiêu Cp ±0,3 pF (sai số C0 truyền 1:1 vào Cp).
4. Không có cuộn chuẩn nội L0 → mô tả OPEN/SHORT-cal trong báo cáo không thực hiện được như đã viết. Cần hiệu chuẩn bằng cuộn chuẩn đã biết Cp (đo VNA) hoặc tụ chuẩn ngoài C_ref.
5. Vẫn phải mô phỏng/chạy thử với **model TLV3501 thật của TI** ở các góc 10 µH/Q=20 → 100 mH/Q=100 trước khi đặt mạch (model hành vi ở đây chỉ để so sánh A/B).

---

## 3. Ước tính chi phí (LCSC + JLCPCB, sang Việt Nam)

Giá tham khảo (USD, mức trung bình; kiểm tra lại trên LCSC/JLCPCB vì giá biến động).

### 3.1 Linh kiện (LCSC) — BOM đề xuất Cách B, handheld có pin

| Nhóm | Linh kiện | SL | Đơn giá | Thành tiền |
|---|---|---|---|---|
| MCU | ESP32-S3-WROOM-1U-N4R2 | 1 | 2,8–3,5 | ~3,0 |
| Comparator | TLV3501AIDBV | 1 | 2,2–3,2 | ~2,5 |
| LDO | AP2112K-3.3 | 2 | 0,08 | 0,16 |
| Sạc pin | MCP73832 | 1 | 0,30 | 0,30 |
| Power path | AO3401A + 1N5819 | 2 | 0,05 | 0,10 |
| Chuyển mạch | G6K-2F DC3 + SS8050 + 1N4148W | 3 | 2,2 / 0,03 / 0,03 | ~2,3 |
| Hiển thị | OLED 1.3" I2C (SH1106) | 1 | 2,5–3,5 | ~3,0 |
| Kết nối | USB-C 16 chân + 3 nút + công tắc gạt + LED | ~6 | 0,03–0,2 | ~0,6 |
| Điện trở | 100k/10k/5,1k/2k/470/100/4,7k (~13 cái) | ~13 | 0,01 | ~0,15 |
| Tụ thường | 4,7µ/10µ/100n/2,2µ (~13 cái) | ~13 | 0,01–0,05 | ~0,35 |
| Tụ chuẩn | 33 pF + 100 pF **C0G 1 %** | 2 | 0,10 | 0,20 |
| Pin | Li-Po 3.7V 500–800 mAh (mua ngoài) | 1 | 3–6 | ~4,0 |

- **Tổng linh kiện trên LCSC (chưa gồm pin): ≈ 12–15 USD.**
- **Cả pin: ≈ 16–19 USD.**

Nếu chuyển relay → NMOS 2N7002/BSS138 + 1 MΩ (đề xuất cũ) thì bớt G6K/SS8050/1N4148W, tiết kiệm ~2,3 USD nhưng đổi lại C_off cao hơn (vẫn hiệu chuẩn được, sai số ~−0,01 %).

### 3.2 PCB (JLCPCB)

- 5 tấm, 2 lớp, ~55×75 mm, HASL, xanh lá: **2–5 USD** (thường 2 USD khuyến mãi + phí ~1–3 USD).

### 3.3 Hàn lắp

| Phương án | Chi phí |
|---|---|
| Tự hàn tay | 0 USD (tốn thời gian) |
| JLCPCB SMT (5 tấm) | setup ~8 USD + phí "extended parts" ~3 USD/mã lạ (~10–15 mã) + hàn theo pad ≈ **40–70 USD** |

### 3.4 Vận chuyển về Việt Nam

- Tiêu chuẩn (15–25 ngày): **8–15 USD**; nhanh DHL/FedEx: **20–35 USD**.

### 3.5 Tổng cộng

| Kịch bản | Tổng (USD) | Ghi chú |
|---|---|---|
| **Tự hàn, ship thường** | **~25–40** | PCB 2–5 + linh kiện 12–15 + ship 8–15 (+pin 4) |
| **JLCPCB hàn sẵn, ship thường** | **~70–110** | thêm 40–70 hàn |
| Chỉ 1–2 bo mẫu, ship nhanh | ~60–90 | ít bo, ship nhanh |

**Nhận xét:** chi phí bị chi phối bởi 4 món đắt: ESP32-S3 (~3), TLV3501 (~2,5), OLED (~3), relay G6K (~2,2) + pin (~4). Phần thụ động (điện trở/tụ) gần như không đáng kể. Nếu muốn rẻ, thay ESP32-S3-WROOM bằng module ESP32-C3/ESP32-S2 (rẻ hơn ~1–1,5 USD) nhưng mất khả năng đếm PCNT/MCPWM 80 MHz đầy đủ — **không nên** vì đang ưu tiên độ chính xác.

---

## 4. Việc cần làm tiếp (theo thứ tự ưu tiên)

1. **Sửa schematic theo Cách B**: DUT nối V_BIAS, bỏ C17/R13/C16, IN− nối thẳng V_BIAS, SMA → kẹp Kelvin 2 chân, decoupling V_BIAS 4,7 µF ∥ 100 nF.
2. Đổi tụ chuẩn sang **C0G 1 %** (33 pF, 100 pF); bổ sung phương án hiệu chuẩn (cuộn chuẩn L0 hoặc tụ chuẩn ngoài C_ref).
3. Cân nhắc relay G6K (chính xác nhất) vs NMOS 2N7002 (rẻ/gọn); với ưu tiên chính xác → **giữ relay**.
4. Mô phỏng lại bằng model TLV3501 thật của TI (các góc L/Q) trước khi đặt mạch.
5. Sửa báo cáo: bỏ bảng số liệu E4980A/Bringup "như đã đo" (board chưa có), cập nhật MCU (WROOM-1U-N4R2), LDO (AP2112K), tụ chuẩn 1 %, và trích bài Fred Lee đúng vai trò (khử EPC, không phải phương pháp đo).
6. Chạy lại ERC/DRC (`kicad-cli`) sau khi sửa schematic/PCB.
