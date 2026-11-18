# Mô phỏng SPICE — Proof of Concept: Khối dao động LC + Relay hiệu chuẩn

Mô phỏng 2 khối của máy đo LCR/EPC bằng ngspice (đi kèm KiCad) hoặc LTspice,
để chứng minh phương pháp **cộng hưởng 2 tụ chuẩn** hoạt động.

## 1. File

| File | Vai trò |
|---|---|
| `lcr_osc_relay_ngspice.cir` | Netlist chính (ngspice / KiCad) — chạy 2 trạng thái relay |
| `lcr_osc_relay_ltspice.cir` | Bản tương đương cho LTspice (dùng `.step`) |
| `solve.py` | Giải Lx, Cp, SRF từ f1, f2 |
| `waveform.cir` | Xuất dạng sóng 2 trạng thái ra `waveA.txt` / `waveB.txt` |
| `plot_waveform.py` | Vẽ `oscillator_states.png` |

## 2. Cách chạy

### ngspice (Linux / KiCad)
```bash
ngspice -b lcr_osc_relay_ngspice.cir
```
In ra:
```
f1 = 7.667830e+06    (relay MỞ — chỉ C0 = 33 pF)
f2 = 4.198656e+06    (relay ĐÓNG — C0 + Cs = 133 pF)
```

Sau đó giải 3 ẩn:
```bash
python3 solve.py 7.667830e6 4.198656e6
```
Kết quả (so với giá trị đặt Lx=10 µH, Cp=5 pF):
```
C_A = 42.823 pF     (lý tưởng 43 pF)
Cp  =  4.823 pF     (đặt 5 pF, sai ~3.5 %)
Lx  = 10.061 µH     (đặt 10 µH, sai ~0.6 %)
SRF = 22.85 MHz     (lý tưởng 22.5 MHz)
```

### LTspice (Windows)
1. Mở `lcr_osc_relay_ltspice.cir` (File → Open).
2. Chạy (biểu tượng "Run").
3. Mở **SPICE Error Log** (Ctrl+L) → xem 2 giá trị `f` của 2 bước `.step`.
4. Đưa 2 giá trị đó vào `solve.py`.

## 3. Đổi cuộn cảm cần đo

Sửa 3 dòng `.param` ở đầu file:
```
.param Lx=10u      * độ tự cảm
.param Rs=16       * điện trở dây quấn AC (Rs ≈ 2πf·L/Q)
.param Cp=5p       * điện dung ký sinh EPC
```

Ví dụ cuộn 100 µH (Q≈50, Cp=10 pF): `Lx=100u`, `Rs=30`, `Cp=10p`.

## 4. Mô hình (cần biết)

- **Comparator TLV3601**: mô hình hành vi `tanh` (rail-to-rail, gain 2000), **chưa** mô hình độ trễ 2,5 ns.
  - Độ trễ `tpd` thực tế sẽ kéo tần số xuống thêm ~0,1–0,2 % (bù bằng firmware, xem bảng sai số tpd trong review).
  - Muốn chính xác hơn, thay bằng model TLV3601 của TI.
- **Relay G6K**: mô hình switch `Ron=0.05 Ω, Roff=1 GΩ`, điều khiển bằng nguồn `Vctrl` (0 V = mở, 3.3 V = đóng).
- **DUT**: `Lx + Rs` nối tiếp, `Cp` song song (đầu nóng = tank, đầu lạnh = V_BIAS — đúng topology **phương án B**).

## 5. Vì sao kết quả lệch vài %

Mô hình comparator dùng hàm `tanh` mềm + đo tần bằng điểm cắt ngưỡng → có lệch pha nhỏ,
làm tần số hơi thấp hơn lý tưởng. Sai số này **khuếch đại vào Cp** (do Cp được suy từ hiệu
`C_A − 38 pF`). Đây là giới hạn của mô hình hành vi, **không phải** lỗi phương pháp —
với comparator thật + hiệu chuẩn, sai số về mức ±0,3–1 pF như đã phân tích.

## 6. Ý nghĩa Proof-of-Concept

Kết quả cho thấy:
1. Mạch **tự dao động bền vững** ở tần số cộng hưởng (phương án B).
2. Relay đóng/mở làm tần số **đổi rõ rệt** (7,67 → 4,20 MHz).
3. Từ 2 tần số đo được, công thức `K=(f1/f2)² → C_A=Cs/(K−1)` **khôi phục đúng Lx và Cp**.
