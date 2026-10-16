import os
import json
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

# ==============================================================================
# DATA DEFINITIONS BASED ON TOURNAMENT SCHEDULE & BTC FLEET PLAN
# ==============================================================================

FLEET_OVERVIEW = [
    {
        "buoi": "Chiều 27/10/2026",
        "ks": "Mr. Tiệp + Ms. Thu Trang & Ms. Dương",
        "teddy": "Nhung & Quốc Anh",
        "ntd": "Giang & Phương",
        "golf": "---",
        "xe": "15 xe 7, 1 xe 16 và 2 xe 29 chỗ (Tổng 179 chỗ)",
        "ghichu": "Ưu tiên VĐV đi trước, CĐV đi sau nếu có xe"
    },
    {
        "buoi": "Sáng 28/10/2026",
        "ks": "---",
        "teddy": "---",
        "ntd": "---",
        "golf": "Mr. Tiệp, Thu Trang, Dương, Giang, Phương, Nhung, Quốc Anh",
        "xe": "8 xe 45 chỗ, 2 xe 16 và 26 xe 7 chỗ (Tổng 450+ chỗ)",
        "ghichu": "450 người tham gia giải chạy Fun Run Tràng An (cách 32 km)"
    },
    {
        "buoi": "Chiều 28/10/2026",
        "ks": "Mr. Tiệp + Ms. Thu Trang & Ms. Dương",
        "teddy": "Giang & Hải",
        "ntd": "Nhung & Quốc Anh",
        "golf": "---",
        "xe": "15 xe 7, 1 xe 16 (Tổng 121 chỗ)",
        "ghichu": "Ưu tiên VĐV đi trước, CĐV đi sau nếu có xe"
    },
    {
        "buoi": "Sáng 29/10/2026",
        "ks": "Mr. Tiệp + Ms. Thu Trang & Ms. Dương",
        "teddy": "Giang & Phương",
        "ntd": "Nhung & Quốc Anh",
        "golf": "---",
        "xe": "15 xe 7, 1 xe 16 (Tổng 121 chỗ)",
        "ghichu": "Ưu tiên VĐV đi trước, CĐV đi sau nếu có xe"
    }
]

DAY_27_TRIPS = [
    ("Chuyến #1", "12:30", "Khách sạn Mường Thanh ➔ Nhà thi đấu", 82, "02 xe 29 chỗ + 01 xe 16 chỗ + 02 xe 7 chỗ", "Kéo co (13:00)", "Đưa toàn bộ các đội Kéo co đi khai mạc thi đấu"),
    ("Chuyến #2", "13:30", "Khách sạn Mường Thanh ➔ Nhà thi đấu", 37, "01 xe 29 chỗ + 01 xe 16 chỗ", "Bóng bàn, Cầu lông (14:00)", "Đưa VĐV thi ca 14h"),
    ("Chuyến #3", "14:00", "Nhà thi đấu ➔ Khách sạn Mường Thanh", 75, "02 xe 29 chỗ + 01 xe 16 chỗ + 01 xe 7 chỗ", "Kéo co (13:00)", "Đón các đội Kéo co thi xong về KS nghỉ"),
    ("Chuyến #4", "14:00", "Nhà thi đấu ➔ Sân bóng Teddy", 6, "01 xe 7 chỗ", "Bóng đá (15:00)", "🔥 TRUNG CHUYỂN LIÊN SÂN: VĐV kéo co sang đá bóng"),
    ("Chuyến #5", "14:30", "Khách sạn Mường Thanh ➔ Nhà thi đấu", 21, "01 xe 29 chỗ", "Cầu lông, Bóng bàn (15:00)", "Đưa VĐV thi ca 15h"),
    ("Chuyến #6", "14:30", "Khách sạn Mường Thanh ➔ Sân bóng Teddy", 97, "02 xe 29 chỗ + 01 xe 16 chỗ + 04 xe 7 chỗ", "Bóng đá Nam & Nữ (15:00)", "Đưa các đội bóng đá ra sân Teddy"),
    ("Chuyến #7", "15:00", "Nhà thi đấu ➔ Khách sạn Mường Thanh", 11, "02 xe 7 chỗ", "Cầu lông, Bóng bàn", "Đón VĐV đã thi xong về KS"),
    ("Chuyến #8", "15:00", "Nhà thi đấu ➔ Sân bóng Teddy", 3, "01 xe 7 chỗ", "Bóng đá (15:00)", "🔥 TRUNG CHUYỂN LIÊN SÂN: VĐV sang đá bóng"),
    ("Chuyến #9", "16:30", "Khách sạn Mường Thanh ➔ Nhà thi đấu", 9, "02 xe 7 chỗ", "Bóng bàn (17:00)", "Đưa VĐV thi lượt 17h"),
    ("Chuyến #10", "17:00", "Nhà thi đấu ➔ Khách sạn Mường Thanh", 27, "01 xe 29 chỗ", "Cầu lông, Bóng bàn", "Đón VĐV kết thúc về KS"),
    ("Chuyến #11", "17:00", "Sân bóng Teddy ➔ Khách sạn Mường Thanh", 106, "02 xe 29 chỗ + 01 xe 16 chỗ + 05 xe 7 chỗ", "Bóng đá (17:00)", "Đón toàn bộ các đội bóng đá về KS ăn tối"),
    ("Chuyến #12", "17:00", "Nhà thi đấu ➔ Sân bóng Teddy", 1, "01 xe 7 chỗ", "Bóng đá (15:00)", "🔥 TRUNG CHUYỂN LIÊN SÂN"),
    ("Chuyến #13", "17:00", "Sân bóng Teddy ➔ Nhà thi đấu", 1, "01 xe 7 chỗ", "Bóng bàn (15:00)", "🔥 TRUNG CHUYỂN LIÊN SÂN"),
    ("Chuyến #14", "18:00", "Nhà thi đấu ➔ Khách sạn Mường Thanh", 27, "01 xe 29 chỗ", "Bóng bàn, Cầu lông (18:00)", "Đón lượt cuối về Khách sạn")
]

DAY_28_TRIPS = [
    ("Sáng Fun Run", "05:30", "Khách sạn Mường Thanh ➔ Sân Golf Tràng An", 450, "8 xe 45 chỗ + 2 xe 16 chỗ + 26 xe 7 chỗ", "Fun Run (06:00 - 10:30)", "Cự ly 32 km. Phục vụ 450 VĐV & CĐV"),
    ("Chuyến #1", "14:30", "Khách sạn Mường Thanh ➔ Sân bóng Teddy", 42, "01 xe 16 chỗ + 04 xe 7 chỗ", "Bán kết Bóng đá Nam & Nữ (15:00)", "Đưa 2 đội Bán kết 1 ra sân"),
    ("Chuyến #2", "15:30", "Sân bóng Teddy ➔ Khách sạn Mường Thanh", 21, "01 xe 16 chỗ + 01 xe 7 chỗ", "Bóng đá (kết thúc trận 1)", "Đón đội kết thúc trận về KS nghỉ"),
    ("Chuyến #3", "15:30", "Khách sạn Mường Thanh ➔ Sân bóng Teddy", 44, "01 xe 16 chỗ + 04 xe 7 chỗ", "Bán kết Bóng đá Nam & Nữ (16:00)", "Đưa 2 đội Bán kết 2 ra sân"),
    ("Chuyến #4", "16:30", "Sân bóng Teddy ➔ Khách sạn Mường Thanh", 44, "01 xe 16 chỗ + 04 xe 7 chỗ", "Bóng đá (kết thúc)", "Đón các đội về Khách sạn"),
    ("Chuyến #5", "16:30", "Khách sạn Mường Thanh ➔ Sân bóng Teddy", 21, "01 xe 16 chỗ + 01 xe 7 chỗ", "Bán kết Bóng đá (17:00)", "Đưa đội thi ca cuối"),
    ("Chuyến #6", "17:30", "Sân bóng Teddy ➔ Khách sạn Mường Thanh", 42, "01 xe 16 chỗ + 04 xe 7 chỗ", "Bóng đá (kết thúc toàn bộ)", "Đón toàn bộ các đội về KS chuẩn bị Gala")
]

DAY_29_TRIPS = [
    ("Chuyến #1", "06:30", "Khách sạn Mường Thanh ➔ Sân bóng Teddy", 44, "01 xe 16 chỗ + 04 xe 7 chỗ", "CK & Tranh 3-4 Bóng đá (07:00)", "Đưa 4 đội bóng đá nam & nữ ra sân"),
    ("Chuyến #2", "07:00", "Khách sạn Mường Thanh ➔ Nhà thi đấu", 20, "01 xe 16 chỗ + 01 xe 7 chỗ", "CK Bóng bàn, Cầu lông (07:30)", "Đưa VĐV thi chung kết ca 1"),
    ("Chuyến #3", "07:30", "Sân bóng Teddy ➔ Khách sạn Mường Thanh", 44, "01 xe 16 chỗ + 04 xe 7 chỗ", "Bóng đá (kết thúc)", "Xe quay vòng đón VĐV về KS"),
    ("Chuyến #4", "07:30", "Khách sạn Mường Thanh ➔ Nhà thi đấu", 18, "01 xe 16 chỗ + 01 xe 7 chỗ", "CK Cầu lông, Bóng bàn (08:00)", "Đưa VĐV thi ca 2"),
    ("Chuyến #5", "07:30", "Khách sạn Mường Thanh ➔ Sân bóng Teddy", 44, "01 xe 16 chỗ + 04 xe 7 chỗ", "Bóng đá (08:00)", "Đưa các lượt trận bóng đá tiếp theo"),
    ("Chuyến #6", "08:00", "Nhà thi đấu ➔ Khách sạn Mường Thanh", 20, "01 xe 16 chỗ + 01 xe 7 chỗ", "Bóng bàn, Cầu lông", "Đón VĐV thi xong ca 1 về KS"),
    ("Chuyến #7", "08:00", "Khách sạn Mường Thanh ➔ Nhà thi đấu", 20, "01 xe 16 chỗ + 01 xe 7 chỗ", "CK Cầu lông, Bóng bàn (08:30)", "Đưa VĐV thi ca 3"),
    ("Chuyến #8", "08:30", "Nhà thi đấu ➔ Khách sạn Mường Thanh", 17, "01 xe 16 chỗ + 01 xe 7 chỗ", "Bóng bàn, Cầu lông", "Đón VĐV về KS"),
    ("Chuyến #9", "08:30", "Sân bóng Teddy ➔ Khách sạn Mường Thanh", 44, "01 xe 16 chỗ + 04 xe 7 chỗ", "Bóng đá (08:30)", "Đón các đội bóng đá về KS"),
    ("Chuyến #10", "08:30", "Khách sạn Mường Thanh ➔ Nhà thi đấu", 17, "01 xe 16 chỗ + 01 xe 7 chỗ", "CK Cầu lông, Bóng bàn (09:00)", "Đưa VĐV thi ca 4"),
    ("Chuyến #11", "09:00", "Nhà thi đấu ➔ Khách sạn Mường Thanh", 20, "01 xe 16 chỗ + 01 xe 7 chỗ", "Bóng bàn, Cầu lông", "Đón VĐV ca 3 về KS"),
    ("Chuyến #12", "09:00", "Khách sạn Mường Thanh ➔ Nhà thi đấu", 5, "01 xe 7 chỗ", "CK Cầu lông (09:30)", "Chở VĐV trận bán kết cầu lông"),
    ("Chuyến #13", "09:30", "Nhà thi đấu ➔ Khách sạn Mường Thanh", 17, "01 xe 16 chỗ + 01 xe 7 chỗ", "Bóng bàn, Cầu lông", "Đón VĐV ca 4 về KS"),
    ("Chuyến #14", "09:30", "Khách sạn Mường Thanh ➔ Nhà thi đấu", 2, "01 xe 7 chỗ", "CK Cầu lông (10:00)", "Chở 2 VĐV Chung kết đơn nam"),
    ("Chuyến #15", "10:00", "Nhà thi đấu ➔ Khách sạn Mường Thanh", 4, "01 xe 7 chỗ", "Bóng bàn, Cầu lông", "Đón VĐV về KS"),
    ("Chuyến #16", "10:00", "Khách sạn Mường Thanh ➔ Nhà thi đấu", 2, "01 xe 7 chỗ", "CK Cầu lông (10:30)", "Chở 2 VĐV Chung kết đôi"),
    ("Chuyến #17", "10:30", "Nhà thi đấu ➔ Khách sạn Mường Thanh", 2, "01 xe 7 chỗ", "Cầu lông", "Đón VĐV về KS"),
    ("Chuyến #18", "10:30", "Khách sạn Mường Thanh ➔ Nhà thi đấu", 96, "01 xe 16 chỗ + 12 xe 7 chỗ", "Bán kết & CK Kéo co (11:00)", "⚡ Tổng lực đoàn xe chở 8 đội kéo co (96 VĐV)"),
    ("Chuyến #19", "11:00", "Nhà thi đấu ➔ Khách sạn Mường Thanh", 4, "01 xe 7 chỗ", "Cầu lông", "Đón VĐV về KS"),
    ("Chuyến #20", "11:30", "Nhà thi đấu ➔ Khách sạn Mường Thanh", 96, "01 xe 16 chỗ + 12 xe 7 chỗ", "Kéo co kết thúc (11:30)", "⚡ Tổng lực đón toàn bộ VĐV kéo co về KS ăn trưa")
]

# ==============================================================================
# EXPORT TO EXCEL (.XLSX)
# ==============================================================================
def create_excel():
    wb = openpyxl.Workbook()
    
    # Common styles
    font_title = Font(name="Calibri", size=15, bold=True, color="1E3A8A")
    font_subtitle = Font(name="Calibri", size=11, italic=True, color="475569")
    font_sec = Font(name="Calibri", size=12, bold=True, color="0F172A")
    font_header = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    font_data = Font(name="Calibri", size=10)
    font_bold = Font(name="Calibri", size=10, bold=True)
    
    fill_header = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
    fill_header_day28 = PatternFill(start_color="0D9488", end_color="0D9488", fill_type="solid")
    fill_header_day29 = PatternFill(start_color="4F46E5", end_color="4F46E5", fill_type="solid")
    fill_zebra = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    fill_highlight = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")
    
    border_thin = Side(border_style="thin", color="CBD5E1")
    cell_border = Border(left=border_thin, right=border_thin, top=border_thin, bottom=border_thin)
    
    align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    align_left = Alignment(horizontal="left", vertical="center", wrap_text=True)
    align_right = Alignment(horizontal="right", vertical="center", wrap_text=True)

    # ----------------------------------------------------
    # SHEET 1: ĐỘI XE & CÁN BỘ TRỰC ĐIỂM
    # ----------------------------------------------------
    ws1 = wb.active
    ws1.title = "1. Doi xe & Truc diem"
    ws1.views.sheetView[0].showGridLines = True
    
    ws1.merge_cells("A1:G1")
    ws1["A1"] = "ĐẠI HỘI MƯỜNG THANH 2026 - KẾ HOẠCH ĐIỀU PHỐI XE & CÁN BỘ TRỰC ĐIỂM"
    ws1["A1"].font = font_title
    ws1["A1"].alignment = align_center
    ws1.row_dimensions[1].height = 30
    
    ws1.merge_cells("A2:G2")
    ws1["A2"] = "Thời gian: 27/10 - 29/10/2026 · Địa điểm: KS Mường Thanh, Nhà thi đấu Ninh Bình, Sân bóng Teddy, Sân Golf Tràng An"
    ws1["A2"].font = font_subtitle
    ws1["A2"].alignment = align_center
    ws1.row_dimensions[2].height = 20
    
    headers_ws1 = [
        "Thời gian", "Trực tại KS Ninh Bình", "Trực Sân Teddy (cách 3km)", 
        "Trực Nhà thi đấu (cách 2.6km)", "Sân Golf Tràng An (cách 32km)", 
        "Số lượng xe sẵn có", "Ghi chú vận hành"
    ]
    
    ws1.row_dimensions[4].height = 28
    for col_idx, h in enumerate(headers_ws1, 1):
        cell = ws1.cell(row=4, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = align_center
        cell.border = cell_border
        
    for r_idx, row in enumerate(FLEET_OVERVIEW, 5):
        ws1.row_dimensions[r_idx].height = 35
        data_cells = [
            (row["buoi"], align_center, True),
            (row["ks"], align_left, False),
            (row["teddy"], align_left, False),
            (row["ntd"], align_left, False),
            (row["golf"], align_left, False),
            (row["xe"], align_left, True),
            (row["ghichu"], align_left, False)
        ]
        for c_idx, (val, al, is_b) in enumerate(data_cells, 1):
            c = ws1.cell(row=r_idx, column=c_idx, value=val)
            c.font = font_bold if is_b else font_data
            c.alignment = al
            c.border = cell_border
            if r_idx % 2 == 0:
                c.fill = fill_zebra
                
    ws1.column_dimensions["A"].width = 18
    ws1.column_dimensions["B"].width = 28
    ws1.column_dimensions["C"].width = 22
    ws1.column_dimensions["D"].width = 22
    ws1.column_dimensions["E"].width = 32
    ws1.column_dimensions["F"].width = 30
    ws1.column_dimensions["G"].width = 35

    # ----------------------------------------------------
    # FUNCTION TO BUILD TRIP SHEET
    # ----------------------------------------------------
    def build_trip_sheet(ws, title, day_label, fleet_str, trips, fill_hdr):
        ws.views.sheetView[0].showGridLines = True
        
        ws.merge_cells("A1:G1")
        ws["A1"] = f"LỊCH ĐIỀU XE CHI TIẾT - {title.upper()}"
        ws["A1"].font = font_title
        ws["A1"].alignment = align_center
        ws.row_dimensions[1].height = 28
        
        ws.merge_cells("A2:G2")
        ws["A2"] = f"Ngày thi đấu: {day_label} · Đội xe sẵn có: {fleet_str}"
        ws["A2"].font = font_subtitle
        ws["A2"].alignment = align_center
        ws.row_dimensions[2].height = 20
        
        trip_headers = ["Chuyến", "Giờ đón", "Lộ trình di chuyển", "Số VĐV", "Gợi ý bố trí loại xe", "Môn thi & Giờ thi đấu", "Ghi chú điều hành"]
        ws.row_dimensions[4].height = 26
        for c_idx, h in enumerate(trip_headers, 1):
            c = ws.cell(row=4, column=c_idx, value=h)
            c.font = font_header
            c.fill = fill_hdr
            c.alignment = align_center
            c.border = cell_border
            
        for idx, t in enumerate(trips, 5):
            ws.row_dimensions[idx].height = 26
            chuyen, gio, lotrinh, vdv, xe, mon, ghichu = t
            is_cross = "TRUNG CHUYỂN" in ghichu
            is_huge = vdv >= 80
            
            row_data = [
                (chuyen, align_center, True),
                (gio, align_center, True),
                (lotrinh, align_left, True if is_cross else False),
                (vdv, align_center, True),
                (xe, align_left, True),
                (mon, align_left, False),
                (ghichu, align_left, False)
            ]
            for c_idx, (val, al, is_b) in enumerate(row_data, 1):
                c = ws.cell(row=idx, column=c_idx, value=val)
                c.font = font_bold if is_b else font_data
                c.alignment = al
                c.border = cell_border
                if is_cross or is_huge:
                    c.fill = fill_highlight
                elif idx % 2 == 0:
                    c.fill = fill_zebra
                    
        # Summary row
        tot_row = len(trips) + 5
        ws.cell(row=tot_row, column=1, value="TỔNG CỘNG").font = font_bold
        ws.cell(row=tot_row, column=1).alignment = align_center
        ws.cell(row=tot_row, column=1).border = cell_border
        
        ws.cell(row=tot_row, column=4, value=f"=SUM(D5:D{tot_row-1})").font = font_bold
        ws.cell(row=tot_row, column=4).alignment = align_center
        ws.cell(row=tot_row, column=4).border = cell_border
        
        for c_idx in [2, 3, 5, 6, 7]:
            c = ws.cell(row=tot_row, column=c_idx, value="")
            c.border = cell_border
            
        ws.column_dimensions["A"].width = 14
        ws.column_dimensions["B"].width = 12
        ws.column_dimensions["C"].width = 38
        ws.column_dimensions["D"].width = 12
        ws.column_dimensions["E"].width = 36
        ws.column_dimensions["F"].width = 30
        ws.column_dimensions["G"].width = 42

    ws2 = wb.create_sheet("2. Chieu 27-10")
    build_trip_sheet(ws2, "Chiều 27/10/2026 (Vòng bảng)", "27/10/2026", "15 xe 7 chỗ, 1 xe 16 chỗ, 2 xe 29 chỗ (179 chỗ)", DAY_27_TRIPS, fill_header)

    ws3 = wb.create_sheet("3. Ngay 28-10")
    build_trip_sheet(ws3, "Ngày 28/10/2026 (Fun Run & Bán kết Bóng đá)", "28/10/2026", "Sáng: 8 xe 45, 2 xe 16, 26 xe 7 · Chiều: 15 xe 7, 1 xe 16 chỗ", DAY_28_TRIPS, fill_header_day28)

    ws4 = wb.create_sheet("4. Sang 29-10 (Chung ket)")
    build_trip_sheet(ws4, "Sáng 29/10/2026 (Chung kết các môn)", "29/10/2026", "15 xe 7 chỗ, 1 xe 16 chỗ (121 chỗ)", DAY_29_TRIPS, fill_header_day29)

    excel_path = "d:\\App quan ly lich thi dau DHMT\\Ke_hoach_dieu_xe_DHMT_2026.xlsx"
    wb.save(excel_path)
    print(f"Excel saved successfully: {excel_path}")

# ==============================================================================
# EXPORT TO WORD (.DOCX)
# ==============================================================================
def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_word():
    doc = docx.Document()
    
    # Page setup: Landscape for wide tables
    for section in doc.sections:
        section.orientation = docx.enum.section.WD_ORIENTATION.LANDSCAPE
        section.page_width = Inches(11.69) # A4 Landscape width
        section.page_height = Inches(8.27) # A4 Landscape height
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.5)
        section.right_margin = Inches(0.5)
        
    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_org = p_title.add_run("TẬP ĐOÀN MƯỜNG THANH - BAN TỔ CHỨC ĐẠI HỘI 2026\n")
    r_org.font.size = Pt(11)
    r_org.font.bold = True
    r_org.font.color.rgb = RGBColor(71, 85, 105)
    
    r_title = p_title.add_run("KẾ HOẠCH ĐIỀU PHỐI XE & LỊCH TRÌNH DI CHUYỂN VẬN ĐỘNG VIÊN\n")
    r_title.font.size = Pt(16)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(30, 58, 138)
    
    r_sub = p_title.add_run("Ninh Bình · 27 - 29/10/2026 · Căn cứ theo cơ cấu đội xe & cán bộ điều hành của Ban Tổ Chức")
    r_sub.font.size = Pt(10)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(100, 116, 139)
    
    # Section 1
    doc.add_heading("I. BẢNG PHÂN CÔNG ĐỘI XE & CÁN BỘ TRỰC ĐIỂM (THEO PHƯƠNG ÁN BTC)", level=2)
    
    t_fleet = doc.add_table(rows=1, cols=7)
    t_fleet.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_fleet.autofit = False
    
    hdr_cells = t_fleet.rows[0].cells
    hdr_titles = ["Thời gian", "Trực tại KS Ninh Bình", "Trực Sân Teddy (3km)", "Trực Nhà thi đấu (2.6km)", "Sân Golf Tràng An (32km)", "Số lượng xe sẵn có", "Ghi chú vận hành"]
    col_widths_f = [Inches(1.2), Inches(1.8), Inches(1.5), Inches(1.5), Inches(1.8), Inches(1.6), Inches(1.8)]
    
    for i, title in enumerate(hdr_titles):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], "1E3A8A")
        set_cell_margins(hdr_cells[i], 120, 120, 100, 100)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.bold = True
            run.font.size = Pt(9.5)
            run.font.color.rgb = RGBColor(255, 255, 255)
            
    for row in FLEET_OVERVIEW:
        row_cells = t_fleet.add_row().cells
        data = [row["buoi"], row["ks"], row["teddy"], row["ntd"], row["golf"], row["xe"], row["ghichu"]]
        for j, text in enumerate(data):
            row_cells[j].text = text
            set_cell_margins(row_cells[j], 100, 100, 100, 100)
            p = row_cells[j].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j == 0 else WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.size = Pt(9)
                if j in [0, 5]:
                    run.font.bold = True
                    
    for row in t_fleet.rows:
        for i, w in enumerate(col_widths_f):
            row.cells[i].width = w

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Function to add a day table in Word
    def add_day_word_table(day_title, day_meta, trips, header_hex):
        h = doc.add_heading(day_title, level=2)
        p_sub = doc.add_paragraph(day_meta)
        p_sub.runs[0].font.italic = True
        p_sub.runs[0].font.size = Pt(9.5)
        p_sub.paragraph_format.space_after = Pt(6)
        
        t_trips = doc.add_table(rows=1, cols=7)
        t_trips.alignment = WD_TABLE_ALIGNMENT.CENTER
        t_trips.autofit = False
        
        h_cells = t_trips.rows[0].cells
        h_names = ["Chuyến", "Giờ đón", "Lộ trình di chuyển", "Số VĐV", "Gợi ý bố trí loại xe", "Môn thi & Giờ thi", "Ghi chú điều hành"]
        col_w = [Inches(1.0), Inches(0.9), Inches(2.2), Inches(0.8), Inches(2.2), Inches(1.8), Inches(2.3)]
        
        for i, name in enumerate(h_names):
            h_cells[i].text = name
            set_cell_background(h_cells[i], header_hex)
            set_cell_margins(h_cells[i], 120, 120, 80, 80)
            p = h_cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.bold = True
                run.font.size = Pt(9.5)
                run.font.color.rgb = RGBColor(255, 255, 255)
                
        for t in trips:
            r_cells = t_trips.add_row().cells
            chuyen, gio, lotrinh, vdv, xe, mon, ghichu = t
            is_cross = "TRUNG CHUYỂN" in ghichu
            is_huge = vdv >= 80
            
            data = [chuyen, gio, lotrinh, str(vdv), xe, mon, ghichu]
            for j, val in enumerate(data):
                r_cells[j].text = val
                set_cell_margins(r_cells[j], 80, 80, 80, 80)
                if is_cross or is_huge:
                    set_cell_background(r_cells[j], "FEF3C7")
                p = r_cells[j].paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j in [0, 1, 3] else WD_ALIGN_PARAGRAPH.LEFT
                for run in p.runs:
                    run.font.size = Pt(8.5)
                    if j in [0, 1, 3, 4] or (j == 2 and is_cross):
                        run.font.bold = True
                        if is_cross and j == 6:
                            run.font.color.rgb = RGBColor(180, 83, 9)
                            
        for row in t_trips.rows:
            for i, w in enumerate(col_w):
                row.cells[i].width = w
                
        doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # Section 2, 3, 4
    add_day_word_table(
        "II. CHIỀU 27/10/2026: LỊCH ĐIỀU XE VÒNG BẢNG (14 CHUYẾN)",
        "Đội xe: 15 xe 7 chỗ, 1 xe 16 chỗ, 2 xe 29 chỗ (179 chỗ) · Trực: KS Mường Thanh, Sân Teddy, Nhà thi đấu",
        DAY_27_TRIPS,
        "1E3A8A"
    )
    
    doc.add_page_break()

    add_day_word_table(
        "III. NGÀY 28/10/2026: LỊCH ĐIỀU XE FUN RUN & BÁN KẾT BÓNG ĐÁ (7 CHUYẾN)",
        "Sáng: 8 xe 45, 2 xe 16, 26 xe 7 chỗ (Fun Run 450 người) · Chiều: 15 xe 7, 1 xe 16 chỗ (Bán kết bóng đá)",
        DAY_28_TRIPS,
        "0D9488"
    )

    doc.add_page_break()

    add_day_word_table(
        "IV. SÁNG 29/10/2026: LỊCH ĐIỀU XE CHUNG KẾT TOÀN ĐẠI HỘI (20 CHUYẾN)",
        "Đội xe: 15 xe 7 chỗ, 1 xe 16 chỗ (121 chỗ) · Điểm nhấn: Trận Kéo co 10:30 & 11:30 điều động 1 xe 16 + 12 xe 7 chỗ",
        DAY_29_TRIPS,
        "4F46E5"
    )

    # Signatures
    p_sign = doc.add_paragraph()
    p_sign.paragraph_format.space_before = Pt(20)
    p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_date = p_sign.add_run("Ninh Bình, ngày 16 tháng 10 năm 2026\n")
    r_date.font.italic = True
    r_date.font.size = Pt(10)
    
    t_sign = doc.add_table(rows=2, cols=3)
    t_sign.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_sign.autofit = False
    
    for i, w in enumerate([Inches(3.5), Inches(3.5), Inches(3.5)]):
        for r in t_sign.rows:
            r.cells[i].width = w
            
    cell_s0 = t_sign.rows[0].cells[0].paragraphs[0]
    cell_s0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r0 = cell_s0.add_run("NGƯỜI LẬP KẾ HOẠCH\n(Ký, ghi rõ họ tên)")
    r0.font.bold = True
    r0.font.size = Pt(10)
    
    cell_s1 = t_sign.rows[0].cells[1].paragraphs[0]
    cell_s1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = cell_s1.add_run("ĐẠI DIỆN ĐỘI XE ĐƯA ĐÓN\n(Ký, ghi rõ họ tên)")
    r1.font.bold = True
    r1.font.size = Pt(10)

    cell_s2 = t_sign.rows[0].cells[2].paragraphs[0]
    cell_s2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = cell_s2.add_run("TRƯỞNG BAN TỔ CHỨC\n(Ký duyệt)")
    r2.font.bold = True
    r2.font.size = Pt(10)

    for cell in t_sign.rows[1].cells:
        p = cell.paragraphs[0]
        p.add_run("\n\n\n")

    word_path = "d:\\App quan ly lich thi dau DHMT\\Ke_hoach_dieu_xe_DHMT_2026.docx"
    doc.save(word_path)
    print(f"Word document saved successfully: {word_path}")

if __name__ == "__main__":
    create_excel()
    create_word()
