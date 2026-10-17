import json
import sys
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from vptd_directory import DIRECTORY

sys.stdout.reconfigure(encoding='utf-8')

def build_excel():
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    vehicles = data.get('funrun', {}).get('vehicles', [])
    all_runners = data.get('funrun', {}).get('runners', [])
    runners_by_bib = {r['bib']: r for r in all_runners}

    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)

    # Styles
    font_family = "Arial"
    title_font = Font(name=font_family, size=16, bold=True, color="1E3A8A")
    subtitle_font = Font(name=font_family, size=11, italic=True, color="475569")
    header_font = Font(name=font_family, size=10, bold=True, color="FFFFFF")
    sec_header_font = Font(name=font_family, size=11, bold=True, color="FFFFFF")
    sec_sub_font = Font(name=font_family, size=10, bold=True, color="0F172A")
    data_font = Font(name=font_family, size=10, color="000000")
    bold_data_font = Font(name=font_family, size=10, bold=True, color="000000")
    italic_font = Font(name=font_family, size=9, italic=True, color="64748B")

    # Fills
    header_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid") # Dark Blue
    sub_header_fill = PatternFill(start_color="0284C7", end_color="0284C7", fill_type="solid") # Light Blue / Cyan
    sec_fill_vip = PatternFill(start_color="7E22CE", end_color="7E22CE", fill_type="solid") # Purple VIP
    sec_fill_btc = PatternFill(start_color="991B1B", end_color="991B1B", fill_type="solid") # Dark Red BTC
    sec_fill_bus = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid") # Navy Blue 45c
    sec_fill_7c = PatternFill(start_color="0D9488", end_color="0D9488", fill_type="solid") # Teal 7c
    sec_fill_tudi = PatternFill(start_color="334155", end_color="334155", fill_type="solid") # Slate
    info_bar_fill = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
    zebra_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")

    # Borders
    thin_line = Side(border_style="thin", color="CBD5E1")
    thick_line = Side(border_style="medium", color="1E3A8A")
    double_line = Side(border_style="double", color="1E3A8A")
    all_border = Border(left=thin_line, right=thin_line, top=thin_line, bottom=thin_line)
    top_thick_border = Border(top=thick_line, left=thin_line, right=thin_line, bottom=thin_line)

    # Alignments
    center_align = Alignment(horizontal="center", vertical="center")
    left_align = Alignment(horizontal="left", vertical="center")
    right_align = Alignment(horizontal="right", vertical="center")
    wrap_left_align = Alignment(horizontal="left", vertical="center", wrap_text=True)

    # =========================================================================
    # SHEET 1: TỔNG HỢP ĐIỀU XE FUN RUN
    # =========================================================================
    ws1 = wb.create_sheet(title="Tổng hợp điều xe Fun Run")
    ws1.views.sheetView[0].showGridLines = True

    # Title
    ws1.merge_cells("A1:M1")
    ws1["A1"] = "BẢNG TỔNG HỢP KẾ HOẠCH ĐIỀU XE GIẢI CHẠY MƯỜNG THANH FUN RUN 2026"
    ws1["A1"].font = title_font
    ws1["A1"].alignment = center_align
    ws1.row_dimensions[1].height = 30

    ws1.merge_cells("A2:M2")
    ws1["A2"] = "Thời gian: Sáng 28/10/2026 · Điểm đón: Sảnh KS Mường Thanh Luxury Ninh Bình ➔ Điểm đến: Sân Golf Tràng An & Resort (32km)"
    ws1["A2"].font = subtitle_font
    ws1["A2"].alignment = center_align
    ws1.row_dimensions[2].height = 20

    # Headers for Sheet 1
    s1_headers = [
        "STT", "Mã xe", "Tên xe & Chủng loại", "Sức chứa", "Quân số nội bộ",
        "Giờ xuất phát", "Điểm đón & Lộ trình", "Trưởng xe phụ trách", "SĐT Trưởng xe",
        "Lái xe", "Dải số BIB / Đối tượng", "Cự ly", "Ghi chú điều hành"
    ]
    ws1.row_dimensions[4].height = 28
    for col_idx, h_text in enumerate(s1_headers, start=1):
        cell = ws1.cell(row=4, column=col_idx, value=h_text)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_align
        cell.border = all_border

    # Populate Sheet 1
    for r_idx, v in enumerate(vehicles, start=5):
        ws1.row_dimensions[r_idx].height = 24
        is_even = (r_idx % 2 == 0)
        curr_fill = zebra_fill if is_even else PatternFill(fill_type=None)

        drv = v.get('driver')
        drv_str = f"{drv['name']} (VĐV tự lái)" if drv else "Lái xe hợp đồng"
        cpt = v.get('captain', {})
        cpt_name = cpt.get('name', '')
        cpt_phone = cpt.get('phone', '')
        if v.get('id') == 'XE-VIP-01':
            cpt_phone = "Bảo mật (LH Thư ký)"

        pax_str = f"{v.get('paxCount', len(v.get('runners', [])))} người"
        if v.get('isSelfTransport'):
            cap_str = "Tự túc"
        else:
            cap_str = f"{v.get('capacity', 0)} chỗ"

        row_data = [
            r_idx - 4,
            v.get('id', ''),
            v.get('label', ''),
            cap_str,
            pax_str,
            v.get('departTime', '05:00'),
            f"{v.get('pickupLoc', '')} ➔ {v.get('destLoc', '')}",
            cpt_name,
            cpt_phone,
            drv_str,
            v.get('bibRange', ''),
            v.get('distance', ''),
            v.get('note', '')
        ]

        for col_idx, val in enumerate(row_data, start=1):
            cell = ws1.cell(row=r_idx, column=col_idx, value=val)
            cell.font = data_font
            cell.border = all_border
            if curr_fill.fill_type:
                cell.fill = curr_fill

            # Alignments
            if col_idx in [1, 2, 4, 5, 6, 9]:
                cell.alignment = center_align
            elif col_idx in [3, 8, 10]:
                cell.alignment = left_align
            else:
                cell.alignment = wrap_left_align

    # Auto-adjust column widths for Sheet 1
    s1_widths = {
        1: 6, 2: 14, 3: 32, 4: 12, 5: 15,
        6: 14, 7: 35, 8: 22, 9: 16,
        10: 24, 11: 30, 12: 18, 13: 45
    }
    for col_idx, w in s1_widths.items():
        col_letter = get_column_letter(col_idx)
        ws1.column_dimensions[col_letter].width = w

    # =========================================================================
    # SHEET 2: CHI TIẾT DANH SÁCH NGƯỜI TỪNG XE
    # =========================================================================
    ws2 = wb.create_sheet(title="Chi tiết danh sách từng xe")
    ws2.views.sheetView[0].showGridLines = True

    # Title
    ws2.merge_cells("A1:J1")
    ws2["A1"] = "DANH SÁCH CHI TIẾT CÁN BỘ & VẬN ĐỘNG VIÊN THEO TỪNG XE - MƯỜNG THANH FUN RUN 2026"
    ws2["A1"].font = title_font
    ws2["A1"].alignment = center_align
    ws2.row_dimensions[1].height = 30

    ws2.merge_cells("A2:J2")
    ws2["A2"] = "Tổng số xe: 23 xe · Tổng số VĐV: 434 người · Thành phần: Ban Lãnh đạo, BTC, Tổ Y tế, Khối VĐV & Lái xe kiêm VĐV"
    ws2["A2"].font = subtitle_font
    ws2["A2"].alignment = center_align
    ws2.row_dimensions[2].height = 20

    curr_row = 4

    for v in vehicles:
        v_id = v.get('id', '')
        v_label = v.get('label', '')
        v_type = v.get('type', '')
        capacity = v.get('capacity', 0)
        pax_count = v.get('paxCount', 0)
        cpt = v.get('captain', {})
        cpt_name = cpt.get('name', '')
        cpt_phone = cpt.get('phone', '')
        if v_id == 'XE-VIP-01':
            cpt_phone = "Bảo mật (LH Thư ký: 0968 449 690)"
        cpt_title = cpt.get('title', '')
        cpt_unit = cpt.get('unit', '')

        drv = v.get('driver')
        drv_str = f"{drv['name']} (BIB {drv['bib']} - VĐV tự lái)" if drv else "Lái xe hợp đồng phục vụ"

        # Determine section banner color
        if 'VIP' in v_id:
            banner_fill = sec_fill_vip
        elif v_id in ['XE-00-BTC', 'XE-CHOT-DOAN', 'XE-BAN-SU-KIEN', 'XE-16-YTE']:
            banner_fill = sec_fill_btc
        elif 'TU-DI' in v_id:
            banner_fill = sec_fill_tudi
        elif 'XE-0' in v_id or v_id in ['XE-07', 'XE-08']:
            banner_fill = sec_fill_bus
        else:
            banner_fill = sec_fill_7c

        # 1. Major Section Header (Banner)
        ws2.merge_cells(start_row=curr_row, start_column=1, end_row=curr_row, end_column=10)
        banner_cell = ws2.cell(row=curr_row, column=1)
        seat_desc = f"{pax_count}/{capacity} chỗ" if not v.get('isSelfTransport') else f"{pax_count} người (Tự túc)"
        if drv:
            seat_desc += " [VĐV TỰ LÁI]"
        banner_cell.value = f"MÃ XE: {v_id} — {v_label.upper()}  |  SỨC CHỨA: {seat_desc}"
        banner_cell.font = sec_header_font
        banner_cell.fill = banner_fill
        banner_cell.alignment = left_align
        ws2.row_dimensions[curr_row].height = 26
        curr_row += 1

        # 2. Sub-info row 1: Trưởng xe & Lái xe & Thời gian
        ws2.merge_cells(start_row=curr_row, start_column=1, end_row=curr_row, end_column=10)
        info_cell_1 = ws2.cell(row=curr_row, column=1)
        info_cell_1.value = f"👤 Trưởng xe: {cpt_name} - {cpt_title} ({cpt_unit}) - ĐT: {cpt_phone}  |  🚗 Lái xe: {drv_str}  |  ⏰ Giờ xuất phát: {v.get('departTime', '')}"
        info_cell_1.font = sec_sub_font
        info_cell_1.fill = info_bar_fill
        info_cell_1.alignment = left_align
        ws2.row_dimensions[curr_row].height = 20
        curr_row += 1

        # 3. Sub-info row 2: Lộ trình & Ghi chú
        ws2.merge_cells(start_row=curr_row, start_column=1, end_row=curr_row, end_column=10)
        info_cell_2 = ws2.cell(row=curr_row, column=1)
        info_cell_2.value = f"📍 Lộ trình: {v.get('pickupLoc', '')} ➔ {v.get('destLoc', '')}  |  💡 Ghi chú: {v.get('note', '')}"
        info_cell_2.font = italic_font
        info_cell_2.fill = info_bar_fill
        info_cell_2.alignment = left_align
        ws2.row_dimensions[curr_row].height = 20
        curr_row += 1

        # 4. Table Header
        t_headers = [
            "STT", "Số BIB", "Họ và tên", "Giới tính", "Chức danh",
            "Đơn vị công tác", "Cự ly chạy", "Size áo", "Số điện thoại", "Vai trò / Nhiệm vụ trên xe"
        ]
        ws2.row_dimensions[curr_row].height = 22
        for col_idx, h_text in enumerate(t_headers, start=1):
            cell = ws2.cell(row=curr_row, column=col_idx, value=h_text)
            cell.font = header_font
            cell.fill = sub_header_fill
            cell.alignment = center_align
            cell.border = all_border
        curr_row += 1

        staff_genders = {
            'Vũ Minh Tuấn': 'Nam', 'Nguyễn Tuấn Long': 'Nam', 'Phạm Văn Nhất': 'Nam',
            'Lê Hoàng': 'Nam', 'Nguyễn Huy Nhân': 'Nam', 'Vũ Chiến Thắng': 'Nam',
            'Đỗ Thị Thanh Huyền': 'Nữ', 'Hoàng Thị Huyền Trang': 'Nữ', 'Lương Tú Anh': 'Nữ',
            'Phạm Thị Thu Thủy': 'Nữ', 'Tạ Diệp Anh': 'Nữ', 'Lê Đức Tuấn Định': 'Nam',
            'Nguyễn Huy Quỳnh': 'Nam', 'Phạm Hoàng Hiệp': 'Nam', 'Trần Hồng Hạnh': 'Nữ',
            'Nguyễn Thị Vân Anh': 'Nữ', 'Võ Tuấn Dương': 'Nam', 'Vũ Thị Hoàng Nhung': 'Nữ',
            'Nguyễn Minh Hiếu': 'Nam', 'Nguyễn Thị Lan': 'Nữ', 'BS Lê Kim Vũ': 'Nam',
            'BS Võ Thị Mai Anh': 'Nữ', 'BS Quang Tuấn Anh': 'Nam', 'Hoàng Thanh Hải': 'Nam',
            'Dương Thị Hải Anh': 'Nữ', 'Nguyễn Thu Mai': 'Nữ', 'Nguyễn Thái Mỹ': 'Nam',
            'Nguyễn Duy Hoạt': 'Nam', 'Phạm Minh Hiếu': 'Nam', 'Trần Đình Thông': 'Nam',
            'Võ Thị Mai Trang': 'Nữ', 'Phạm Hà An': 'Nữ', 'Đoàn Thế Cương': 'Nam',
            'Lưu Quốc Việt': 'Nam', 'Nguyễn Bá Lãm': 'Nam', 'Đào Minh Anh': 'Nữ',
            'Hoàng Kim Chính': 'Nam', 'Trần Đại Nghĩa': 'Nam', 'Lê Thị Thu Nguyệt': 'Nữ',
            'Lê Thị Thanh Trà': 'Nữ', 'Lê Thị Hoàng Yến': 'Nữ', 'Nguyễn Thanh Tuấn': 'Nam',
            'Trần Thị Minh Anh': 'Nữ', 'Phạm Hồng Dũng': 'Nam'
        }

        # 5. Compile Persons on this Vehicle
        # Order:
        # a) Driver (if VĐV kiêm lái xe)
        # b) Captain / BTC Staff / Doctors (if not VĐV already listed)
        # c) Runners
        persons = []

        # List of runner BIBs already in this vehicle
        v_runners = v.get('runners', [])
        v_runner_bibs = set(r['bib'] for r in v_runners)

        # Check BTC Staff who are NOT registered runners
        for stf in v.get('btcStaff', []):
            stf_name = stf.get('name', '')
            matching_runner = next((r for r in v_runners if r['name'] == stf_name), None)
            if not matching_runner:
                phone_stf = stf.get('phone', '')
                if not phone_stf and stf_name in DIRECTORY:
                    phone_stf = DIRECTORY[stf_name].get('phone', '')
                g = staff_genders.get(stf_name, '-')
                persons.append({
                    'bib': 'BTC',
                    'name': stf_name,
                    'gender': g,
                    'title': stf.get('title', ''),
                    'unit': stf.get('dept', 'Văn phòng Tập đoàn'),
                    'dist': 'Không chạy (BTC)',
                    'size': '-',
                    'phone': phone_stf,
                    'role': stf.get('duty', 'Cán bộ Ban Tổ Chức')
                })

        # Add runners
        for r in v_runners:
            role = "Vận động viên"
            # Check if this runner is driver
            if drv and r['bib'] == drv.get('bib'):
                role = "Lái xe kiêm VĐV"
            # Check if this runner is captain
            elif r['name'] == cpt_name:
                if v_id == 'XE-15':
                    role = "Vận động viên Trưởng xe #15"
                elif v_id == 'XE-14':
                    role = "Vận động viên Trưởng xe #14"
                elif v_id == 'XE-16-YTE':
                    role = "Vận động viên - Trưởng xe Y tế & Hậu cần cứu thương"
                else:
                    role = f"Trưởng xe #{v_id.replace('XE-', '')} & VĐV"
            # Check if special role
            elif r['name'] == 'Lê Thị Hoàng Yến':
                role = "Tổng Giám Đốc (Trưởng BTC)"
            elif r['name'] in ['Nguyễn Thanh Tuấn', 'Trần Thị Minh Anh']:
                role = "Phó Tổng Giám Đốc (Phó BTC)"
            elif r['name'] == 'Nguyễn Tuấn Long':
                role = "TP Đào tạo & Điều phối XP/Đích (BTC)"
            elif r['name'] == 'Lưu Quốc Việt':
                role = "Trưởng Team Điều phối xe (BTC)"
            elif r['name'] in ['Đỗ Thị Thanh Huyền', 'Hoàng Thị Huyền Trang']:
                role = "Team Điều phối xe (BTC)"
            elif r['name'] == 'Lê Đức Tuấn Định':
                role = "Trưởng đoàn Ban Sự kiện (BTC)"
            elif r['name'] == 'Hoàng Roãn Cường':
                role = "Lái xe kiêm VĐV 5km"

            persons.append({
                'bib': r.get('bib', ''),
                'name': r.get('name', ''),
                'gender': r.get('gender', staff_genders.get(r.get('name'), '')),
                'title': r.get('title', ''),
                'unit': r.get('unit', ''),
                'dist': r.get('dist', ''),
                'size': r.get('size', ''),
                'phone': r.get('phone', ''),
                'role': role
            })

        # Sort so that Driver / Captain / BTC staff appear first, followed by other runners
        def sort_key(p):
            r_str = str(p['role']).lower()
            if 'lái xe' in r_str:
                return 0
            if 'trưởng' in r_str or 'tổng giám đốc' in r_str or 'phó tổng' in r_str:
                return 1
            if 'btc' in r_str or p['bib'] == 'BTC':
                return 2
            return 3

        persons.sort(key=sort_key)

        # Write persons to Sheet 2
        for p_idx, p in enumerate(persons, start=1):
            ws2.row_dimensions[curr_row].height = 20
            is_even = (p_idx % 2 == 0)
            curr_fill = zebra_fill if is_even else PatternFill(fill_type=None)

            row_vals = [
                p_idx,
                p['bib'],
                p['name'],
                p['gender'],
                p['title'],
                p['unit'],
                p['dist'],
                p['size'],
                p['phone'],
                p['role']
            ]

            for col_idx, val in enumerate(row_vals, start=1):
                cell = ws2.cell(row=curr_row, column=col_idx, value=val)
                cell.font = data_font
                cell.border = all_border
                if curr_fill.fill_type:
                    cell.fill = curr_fill

                # Alignment
                if col_idx in [1, 2, 4, 7, 8, 9]:
                    cell.alignment = center_align
                elif col_idx in [3, 5, 6, 10]:
                    cell.alignment = left_align

                # Bold for key roles or captain
                if "Lái xe" in str(p['role']) or "Trưởng" in str(p['role']) or "Tổng Giám Đốc" in str(p['role']):
                    cell.font = bold_data_font

            curr_row += 1

        # Empty row between vehicles
        curr_row += 1

    # Auto-adjust column widths for Sheet 2
    s2_widths = {
        1: 6, 2: 12, 3: 24, 4: 10, 5: 32,
        6: 35, 7: 18, 8: 10, 9: 16, 10: 38
    }
    for col_idx, w in s2_widths.items():
        col_letter = get_column_letter(col_idx)
        ws2.column_dimensions[col_letter].width = w

    # Save to disk
    out_filename = "Danh_sach_xep_xe_Fun_Run_DHMT_2026.xlsx"
    try:
        wb.save(out_filename)
        print(f"Successfully generated Excel file: {out_filename}")
    except PermissionError:
        backup_filename = "Danh_sach_xep_xe_Fun_Run_DHMT_2026_MoiNhat.xlsx"
        wb.save(backup_filename)
        print(f"[THÔNG BÁO]: File '{out_filename}' đang được mở trong Microsoft Excel nên bị khóa ghi.")
        print(f"Đã lưu bản cập nhật chuẩn 100% ra file: '{backup_filename}'. Vui lòng đóng Excel và chạy lại nếu muốn ghi đè vào file gốc.")

if __name__ == '__main__':
    build_excel()
