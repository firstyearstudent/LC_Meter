# Hướng dẫn layout PCB — LCR/EPC Meter (STM32F401 + TLV3601 + G6K, 2 lớp)

Trạng thái PCB hiện tại (06/11 14:47): đã sync footprint từ schematic, nhưng **0 track, 0 via, 0 zone, 0 Edge.Cuts**, 138 pad chưa nối, DRC 56 vi phạm.

---

## 1. Board setup — hiện trạng & cần sửa

| Hạng mục | Hiện tại | Cần làm |
|---|---|---|
| Stackup | 2 lớp F.Cu/B.Cu, FR4 1.6 mm, 35 µm Cu | Giữ nguyên ✅ |
| Clearance | 0.15 mm | Giữ (có thể 0.2 mm cho dễ ăn) |
| Min track | 0.15 mm | Giữ |
| Via | 0.6/0.3 mm | Giữ; qua 0.8/0.4 cho power |
| **Net class** | **Chỉ Default** | **Tạo 5–6 class (mục 2)** |
| **Board outline** | **Trống (DRC báo malformed)** | **Vẽ Edge.Cuts trước tiên** |
| **Zone** | **0 zone** | **Đổ GND 2 lớp** |
| Footprint | Rải rác x 78–268 mm | Gom lại ~60×80 mm |

> **Lưu ý:** phải vẽ **Edge.Cuts** và tạo **net class** trước khi route, nếu không DRC sẽ luôn báo lỗi.

---

## 2. Net class đề xuất

| Class | Nets | Clearance | Track | Via |
|---|---|---|---|---|
| **Power** | /VBUS, /BAT, /VSYS | 0.25 mm | **0.8 mm** | 0.8/0.4 |
| **3V3** | 3.3VD, 3.3VA | 0.2 mm | **0.4 mm** | 0.6/0.3 |
| **Analog** | /LC_TANK, /V_BIAS, /LC_PULSE | 0.2 mm | 0.25 mm | 0.6/0.3 (trừ tank: cấm via) |
| **USB** | /D+, /D− | 0.2 mm | 0.3 mm (diff 90 Ω) | 0.6/0.3 (cả cặp) |
| **Crystal** | /HSE_IN, /HSE_OUT | 0.2 mm | 0.2 mm | **cấm via** |
| Default | còn lại (SWD, I2C, relay, nút) | 0.15 mm | 0.2 mm | 0.6/0.3 |

---

## 3. Net cần đổ zone

| Net | Zone | Ghi chú |
|---|---|---|
| **GND** | **F.Cu + B.Cu** | Zone chính ở B.Cu (mặt phẳng tham chiếu), stitch via 1–2 mm |
| **3.3VA** | Local pour (F.Cu) quanh U5/U3 | **Tách biệt** khỏi 3.3VD |
| **3.3VD** | Local pour dưới U2 (tùy chọn) | Chỉ khi còn chỗ |
| /VBUS, /VSYS | Không cần zone | Dùng track to thay thế |

---

## 4. Net đi dây to

| Net | Dòng | Track |
|---|---|---|
| /VBUS | ≤1.5 A (USB-C) | **0.8 mm** |
| /BAT | ≤1.5 A (pin) | **0.8 mm** |
| /VSYS | ~600 mA | **0.6 mm** |
| 3.3VD | ~66 mA | 0.4 mm |
| 3.3VA | ~1.2 mA | 0.3–0.4 mm |
| GND | — | zone (không track) |

---

## 5. Differential pair

- **/D+ và /D−**: USB Full Speed.
- **0.3 mm width / 0.2 mm gap** (gần 90 Ω trên 2 lớp 1.6 mm — USB FS dung sai rộng).
- **Cùng layer (F.Cu)**, **bằng chiều dài** (±0.1 mm), chạy **trên nền GND B.Cu**.
- **Không đổi layer** (nếu bắt buộc phải via thì via cả 2 tại cùng điểm).

---

## 6. Net phải cùng layer / cấm via

| Net | Yêu cầu | Lý do |
|---|---|---|
| **/LC_TANK** (+ C18, C12, K2, J5, J7) | **F.Cu, không via** | Nút tank nhạy nhất; via thêm ~0.3–1 pF + cảm kháng |
| **/HSE_IN, /HSE_OUT** | F.Cu, không via, ngắn | Thạch anh 8 MHz |
| **/V_BIAS** | F.Cu preferred, hạn chế via | Chuẩn analog 1.65 V |
| **/D+, /D−** | F.Cu, không via (hoặc via cùng lúc) | Diff pair |

---

## 7. Net được phép via

| Net | Via |
|---|---|
| GND | Thoải mái (stitching 1–2 mm) |
| 3.3VD, 3.3VA | Có (1–2 via) |
| /VBUS, /VSYS, /BAT | Có (dùng nhiều via cho dòng lớn) |
| /RELAY_CTRL, /SWDIO, /SWCLK | Có |
| /BOOT0, /NRST | Có |
| /OLED_SCL, /OLED_SDA | Có |

---

## 8. Bố trí linh kiện (placement)

### 8.1 Cụm tank (quan trọng nhất — đặt gần nhau ≤10 mm)
| Linh kiện | Gần |
|---|---|
| **U5 (TLV3601)** | pin 3 (IN+) ↔ C18, C12, R12, R14, J5, J7 |
| **C18 (33 pF)** | sát U5 pin 3 và GND via ngắn |
| **C12 (100 pF)** | sát K2 và U5 pin 3 |
| **K2 (relay)** | sát C12 |
| **R12, R14** | sát U5 pin 3 |
| **J5/J7 (SMD pads)** | sát tank node, khe **1.5–2 mm** |
| **J6/J8 (banana)** | mép board, dây ngắn về tank |
| **C14 (V_BIAS 100 nF)** | sát U5 pin 4 và J7/J8 |

> Vòng tank (U5 pin3 → C18/C12 → GND) phải **nhỏ nhất có thể**; tránh cắt GND dưới tank.

### 8.2 Cụm MCU
| Linh kiện | Gần |
|---|---|
| **X1 + C21/C22** | U2 PH0/PH1 (pin 5/6), ngắn, guard GND |
| **C11 (VCAP 2.2 µF)** | U2 pin 30 |
| **C1/C2/C3/C10/C20** | các chân VDD (19/32/48/64), mỗi chân 1 tụ 100 nF |
| **R1 (BOOT0 10k)** | U2 pin 60 |
| **C19 (NRST 100 nF)** | U2 pin 7 |
| **J1 (SWD)** | gần U2 |
| **R2/R5 (22 Ω)** | gần PA11/PA12 |
| **R6 (100 Ω)** | gần PA0 |

### 8.3 Cụm USB
- **J3 (USB-C)** ở mép board.
- /D+/− ngắn, đối xứng → U2 PA11/PA12.
- R2/R5 đặt gần U2 (hoặc gần J3 — chọn một, giữ ngắn).

### 8.4 Cụm nguồn
| Linh kiện | Gần |
|---|---|
| **U4 (MCP73832)** | J3, C4 (VBUS), C5 (BAT), R11, LED1 |
| **D2 + Q1 + R15** | đường VBUS/BAT |
| **U1 (3.3VD)** | C7, C10, C6 |
| **U3 (3.3VA)** | C9, C13, C15, C6 |
| **J2/J4 (BAT pads)** | mép board |

### 8.5 Cụm relay driver
- **Q4 + D1 + R4** gần K2 **nhưng xa tank/analog** (tránh nhiễu coil 36 mA).

### 8.6 Khác
- **DS1 (OLED)** ở mép board, xa tank.
- **SW1 (nút)** mặt trước.
- **SW4 (công tắc nguồn)** mép board.

---

## 9. Lưu ý 2 lớp

1. **B.Cu = mặt phẳng GND** (zone), stitch via 1–2 mm; F.Cu đặt linh kiện + route.
2. USB diff pair chạy F.Cu, tham chiếu B.Cu GND (không cắt zone dưới USB).
3. **Không cắt GND** dưới tank, dưới U5, dưới thạch anh.
4. Giữ khoảng cách tank ↔ relay coil/U4 (nguồn) ≥5 mm.
5. Đặt test point ở mép để dễ đo.

---

## 10. Thứ tự thực hiện

1. Vẽ **Edge.Cuts** (board outline ~60×80 mm).
2. Tạo **net class** (mục 2).
3. **Placement** theo mục 8.
4. Đổ **GND zone** 2 lớp + stitch via.
5. Route **power** (0.6–0.8 mm) → **USB diff** → **analog/tank** → còn lại.
6. Chạy **DRC**, sửa đến 0 lỗi (trừ "unconnected" của pad không dùng).
7. Kiểm tra **3D** + xuất Gerber.
