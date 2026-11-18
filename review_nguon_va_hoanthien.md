# Kiểm tra khối nguồn + hoàn thiện thiết kế (STM32F401RCT6 · TLV3601 · G6K)

Cập nhật theo quyết định: **giữ relay G6K**, **TLV3501 → TLV3601**, **ESP32-S3 → STM32F401RCT6**.
Kiểm tra trên `LCR_Meter.kicad_sch` hiện tại (05/11) và `LCR_Meter.kicad_pcb` (03/11).

---

## 0. Trạng thái schematic hiện tại — QUAN TRỌNG

Schematic đang ở **giữa quá trình thay linh kiện, chưa hoàn thiện**:

| Hạng mục | Tình trạng |
|---|---|
| U2 | Đã đặt **STM32F401RCTx** (LQFP-64) nhưng **chưa nối dây** (64 chân treo) |
| U5 | Đã đặt **TLV3601DBVR** (SOT-23-5) nhưng **chưa nối dây** (5 chân treo) |
| Đã xóa | ESP32-S3, TLV3501, và các linh kiện phụ: R1, R2, R5, R6, C1, C10, C11, SW1, SW2, SW3 |
| Còn nguyên | Khối nguồn, relay K2 + driver, khung LC (C12/C17/C18/R12/R13/R14/C16), OLED, USB-C |
| ERC hiện tại | **90 vi phạm: 80 lỗi, 10 cảnh báo** (chủ yếu là chân treo + đầu dây lơ lửng) |
| PCB | Vẫn là bản ESP32 (03/11) → **lệch hoàn toàn với schematic**, không được đặt PCB lúc này |

→ **Kết luận:** schematic hiện **chưa chạy được**. Cần nối U2 + U5 và bổ sung linh kiện (mục 2) trước khi vẽ lại PCB.

---

## 1. Kiểm tra khối nguồn — KẾT LUẬN: ĐỦ, dư thừa nhiều

### 1.1 Sơ đồ nguồn hiện tại (giữ nguyên, đúng)

```
USB-C 5V (J3) ──► MCP73832 (U4) ──► BAT (Li-Po)  [R11=2k → sạc 500 mA]
USB-C 5V ──► D2 (1N5819) ──► VSYS
BAT ──► Q1 (AO3401, load-share) ──► VSYS
VSYS ──► U1 (AP2112K-3.3) ──► 3.3VD (số)
VSYS ──► U3 (AP2112K-3.3) ──► 3.3VA (tương tự)
```

### 1.2 Bảng dòng tải (theo thiết kế mới: STM32 + TLV3601 + G6K)

| Rail | Tải | I_typ | I_max | Ghi chú |
|---|---|---|---|---|
| 3.3VD | STM32F401RCT6 @84 MHz | 12 mA | 25 mA | thay ESP32 (~35 mA) |
| 3.3VD | OLED SSD1306 1.3" | 15 mA | 25 mA | |
| 3.3VD | Relay G6K-DC3 coil | 36 mA | 36 mA | chỉ khi đóng |
| 3.3VD | LED1 | 2,8 mA | 2,8 mA | R10 = 470 Ω |
| **3.3VD** | **tổng** | **~66 mA** | **~89 mA** | |
| 3.3VA | TLV3601 | 1,2 mA | 2 mA | thay TLV3501 (3,2 mA) |
| 3.3VA | Cầu V_BIAS (R3+R9) | 0,017 mA | 0,017 mA | |
| **3.3VA** | **tổng** | **~1,2 mA** | **~2 mA** | |

### 1.3 Đối chiếu khả năng cấp

| Khối | Định mức | Tải | Kết luận |
|---|---|---|---|
| U1 AP2112K-3.3 | 600 mA | 66 mA (3.3VD) | **dư ~9×** ✅ |
| U3 AP2112K-3.3 | 600 mA | 1,2 mA (3.3VA) | **dư rất nhiều** ✅ |
| D2 1N5819 | 1 A | 66 mA | ✅ |
| Q1 AO3401 | 4 A | 66 mA | ✅ |
| MCP73832 | 500 mA (R11=2k) | sạc | ✅ |
| USB-C 5V | 1,5–3 A | 500 mA sạc + 66 mA hệ ≈ 566 mA | ✅ |
| Pin Li-Po 500 mAh | — | 66 mA | ~7,6 h |

### 1.4 Tổn hao LDO (kiểm tra nhiệt)

- U1 khi cắm USB: VIN = VSYS = 5 − 0,3 = 4,7 V → P = (4,7−3,3)×66 mA ≈ **93 mW** (SOT-23-5, ΔT ~23 °C → OK).
- Khi chạy pin: VIN = 3,7 V → P ≈ 26 mW (OK).

### 1.5 Kết luận khối nguồn

**Khối nguồn cấp đủ và dư thừa lớn.** Việc đổi ESP32→STM32 và TLV3501→TLV3601 làm **tải giảm** (ESP32 35 mA → STM32 12 mA; TLV3501 3,2 mA → TLV3601 1,2 mA). **Không cần thay đổi gì về công suất.**

### 1.6 Các lưu ý (không phải thiếu công suất)

1. **Relay 3 V chạy ở 3,3 V** → dòng 36 mA (quá áp ~10%), trong dung sai nhưng nên thêm **R nối tiếp ~22 Ω** hoặc 1 diode để hạ về ~3,0 V, giảm nhiệt/tăng tuổi thọ.
2. **LDO 3,3 V + pin Li-Po**: dropout ~80–100 mV ở 66 mA → khi pin < 3,4 V, rail 3,3 V bắt đầu tụt theo pin (vẫn trong dải MCU 1,7–3,6 V). Cần ghi rõ trong báo cáo là dùng được ~80 % dung lượng pin, hoặc dùng buck-boost nếu muốn 100 %.

---

## 2. Việc cần hoàn thiện (checklist)

### 2.1 U5 — TLV3601 (SOT-23-5)

| Chân | Tên | Nối vào |
|---|---|---|
| 3 | IN+ | net `Net-(C17-Pad2)` (nút tank: C17.2, R12.1, R14.2) |
| 4 | IN− | `/V_BIAS` |
| 1 | OUT | `/LC_PULSE` (R12.2) **+ thêm R2 100 Ω → chân f_in của MCU** |
| 5 | VCC | `3.3VA` |
| 2 | VEE | `GND` |

> Lưu ý: TLV3601 **không có chân SHDN** (khác TLV3501) → không cần nối SHDN.

### 2.2 U2 — STM32F401RCT6 (LQFP-64) — các chân dùng

| Chức năng | Chân (symbol) | Nối |
|---|---|---|
| VDD | 19, 32, 48, 64 | 3.3VD + 100 nF mỗi chân + 4,7 µF bulk |
| VSS | 18, 31, 47, 63 | GND |
| **VCAP1** | 30 | **2,2 µF → GND (bắt buộc cho F4)** |
| VBAT | 1 | 3,3VD (không dùng pin RTC riêng) |
| VREF+ | 13 | 3,3VD (hoặc 3,3VA nếu sau này dùng ADC) |
| VSSA | 12 | GND |
| NRST | 7 | 100 nF → GND + nút reset |
| BOOT0 | 60 | 10 kΩ → GND |
| OSC_IN / OSC_OUT | PH0 (5) / PH1 (6) | thạch anh 8 MHz + 2× 22 pF |
| SWDIO | PA13 (46) | header/pad SWD |
| SWCLK | PA14 (49) | header/pad SWD |
| USB_DM | PA11 (44) | J3 D− qua **R5 22 Ω** |
| USB_DP | PA12 (45) | J3 D+ qua **R6 22 Ω** |
| f_in (TIM2_CH1) | PA0 (14) | từ `/LC_PULSE` qua **R2 100 Ω** |
| I2C1_SCL | PB6 (58) | DS1 SCL |
| I2C1_SDA | PB7 (59) | DS1 SDA |
| Relay ctrl | PA8 (41) | R4 (chân B của Q4) |
| Nút MEASURE | PB1 (27) | nút nhấn → GND |

*(Số chân lấy từ symbol STM32F401RCTx trong schematic; khi vẽ nên đối chiếu lại datasheet.)*

### 2.3 Linh kiện cần THÊM

- Thạch anh 8 MHz ±10 ppm.
- 2× 22 pF C0G (tụ tải thạch anh).
- 2,2 µF (VCAP1).
- Header 4 chân SWD (hoặc 4 pad pogo).
- 10 kΩ (BOOT0 pull-down) — có thể dùng lại mã 10 k.
- 100 nF (NRST) — dùng lại mã có sẵn.
- R5 / R6 = 22 Ω (USB series) — **cần thêm lại** (đã bị xóa).
- R2 = 100 Ω (f_in series) — **cần thêm lại** (đã bị xóa).
- (tùy chọn) nút MEASURE.

### 2.4 Khung LC — cần quyết định

Schematic hiện **vẫn là topology cũ** (R12/R14/C17 trên IN+, R13/C16 trên IN−) — tức mạch dao động **có nguy cơ chốt** đã phân tích trước đó. Nếu theo **phương án B** (đã khuyến nghị):
- DUT nối đầu lạnh vào `V_BIAS`, bỏ `C17`, `R13`, `C16`.
- IN− nối thẳng `V_BIAS`.
- Kẹp DUT 2 chân thay SMA.

### 2.5 PCB

PCB hiện tại (03/11) là bản ESP32 → **phải vẽ lại hoàn toàn** cho STM32 (LQFP-64, thạch anh, SWD). Quy trình đúng: hoàn thiện schematic → chạy ERC sạch → cập nhật PCB → DRC.

---

## 3. Cảnh báo

1. **Không đặt PCB lúc này** — schematic 80 lỗi ERC, PCB lệch hoàn toàn.
2. **Kiểm tra lại số chân STM32** với datasheet trước khi hàn (symbol có thể khác thực tế).
3. **VCAP1 (2,2 µF) là bắt buộc** — thiếu sẽ hỏng bộ ổn áp nội của F4.
4. **BOOT0 pull-down 10 kΩ** — thiếu có thể không khởi động đúng.
5. **Thạch anh + 2 tụ tải** — thiếu thì phải chạy HSI (±1 % → sai số tần số lớn, phá chỉ tiêu).

---

## 4. Tóm tắt

| Hạng mục | Kết luận |
|---|---|
| Khối nguồn đủ công suất? | **CÓ, dư ~9×** — không cần sửa |
| Schematic hoàn thiện? | **CHƯA** — U2/U5 chưa nối, thiếu thạch anh/SWD/BOOT0/VCAP/USB-R |
| PCB dùng được? | **KHÔNG** — vẫn là bản ESP32, phải vẽ lại |
| Việc ưu tiên | Nối U5 → nối U2 → thêm linh kiện → ERC sạch → vẽ lại PCB |
