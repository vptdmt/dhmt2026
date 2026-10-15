import sys
sys.stdout.reconfigure(encoding='utf-8')
import openpyxl, json, datetime, re

wb = openpyxl.load_workbook('Tong hop The thao.xlsx', data_only=True)

# ============================================================
# 1. AGENDA
# ============================================================
agenda = [
    # Ngày 27/10/2026
    {"ngay": "2026-10-27", "batdau": "05:30", "ketthuc": "08:30", "hoatdong": "Ăn sáng", "diadiem": "Nhà hàng Tràng An - Tầng 2, Mường Thanh Ninh Bình", "loai": "an_uong"},
    {"ngay": "2026-10-27", "batdau": "09:00", "ketthuc": "12:00", "hoatdong": "Check In", "diadiem": "Mường Thanh Ninh Bình", "loai": "su_kien"},
    {"ngay": "2026-10-27", "batdau": "10:30", "ketthuc": "13:00", "hoatdong": "Ăn trưa", "diadiem": "Nhà hàng Tràng An - Tầng 2, Mường Thanh Ninh Bình", "loai": "an_uong"},
    {"ngay": "2026-10-27", "batdau": "13:00", "ketthuc": "14:00", "hoatdong": "Thể thao - Kéo co (Vòng loại 2 làn)", "diadiem": "Nhà thi đấu Ninh Bình", "loai": "the_thao"},
    {"ngay": "2026-10-27", "batdau": "14:00", "ketthuc": "14:30", "hoatdong": "Thể thao - Bơi (12 lượt vòng loại)", "diadiem": "Bể bơi Mường Thanh Ninh Bình", "loai": "the_thao"},
    {"ngay": "2026-10-27", "batdau": "13:00", "ketthuc": "17:00", "hoatdong": "Tham quan Tràng An", "diadiem": "Thắng cảnh Tràng An", "loai": "tham_quan"},
    {"ngay": "2026-10-27", "batdau": "14:00", "ketthuc": "18:00", "hoatdong": "Thể thao - Bóng bàn (Vòng loại Đơn Nam & Nữ)", "diadiem": "Nhà thi đấu Ninh Bình", "loai": "the_thao"},
    {"ngay": "2026-10-27", "batdau": "14:00", "ketthuc": "17:00", "hoatdong": "Thể thao - Cầu lông (Tứ kết & Vòng loại)", "diadiem": "Nhà thi đấu Ninh Bình", "loai": "the_thao"},
    {"ngay": "2026-10-27", "batdau": "15:00", "ketthuc": "18:00", "hoatdong": "Thể thao - Bóng đá Nam/Nữ (Tứ kết & Vòng bảng 3 sân)", "diadiem": "Sân Teddy", "loai": "the_thao"},
    {"ngay": "2026-10-27", "batdau": "18:00", "ketthuc": "18:30", "hoatdong": "Lucky Draw", "diadiem": "Nhà hàng Tràng An - Tầng 2, Mường Thanh Ninh Bình", "loai": "su_kien"},
    {"ngay": "2026-10-27", "batdau": "18:00", "ketthuc": "18:30", "hoatdong": "Ăn tối", "diadiem": "Nhà hàng Tràng An - Tầng 2, Mường Thanh Ninh Bình", "loai": "an_uong"},
    {"ngay": "2026-10-27", "batdau": "19:00", "ketthuc": "22:00", "hoatdong": "Khai mạc Đại hội Mường Thanh", "diadiem": "Ballroom Hoa Lư - Tầng 1, Mường Thanh Ninh Bình", "loai": "su_kien"},
    {"ngay": "2026-10-27", "batdau": "19:30", "ketthuc": "20:30", "hoatdong": "Chung kết Miss Mường Thanh - Hương Sắc Mường Thanh", "diadiem": "Ballroom Hoa Lư - Tầng 1, Mường Thanh Ninh Bình", "loai": "su_kien"},
    {"ngay": "2026-10-27", "batdau": "20:30", "ketthuc": "21:30", "hoatdong": "Chung kết Văn nghệ - Việt Nam Gấm Hoa", "diadiem": "Ballroom Hoa Lư - Tầng 1, Mường Thanh Ninh Bình", "loai": "su_kien"},
    {"ngay": "2026-10-27", "batdau": "22:00", "ketthuc": "00:00", "hoatdong": "Ăn đêm", "diadiem": "Nhà hàng Tràng An - Tầng 2, Mường Thanh Ninh Bình", "loai": "an_uong"},

    # Ngày 28/10/2026
    {"ngay": "2026-10-28", "batdau": "04:30", "ketthuc": "05:00", "hoatdong": "Ăn sáng nhẹ (Fun Run)", "diadiem": "Nhà hàng Tràng An - Tầng 2, Mường Thanh Ninh Bình", "loai": "an_uong"},
    {"ngay": "2026-10-28", "batdau": "06:00", "ketthuc": "10:30", "hoatdong": "Fun Run - Giải chạy", "diadiem": "Sân Golf Tràng An", "loai": "the_thao"},
    {"ngay": "2026-10-28", "batdau": "05:30", "ketthuc": "08:30", "hoatdong": "Ăn sáng (không tham gia chạy)", "diadiem": "Nhà hàng Tràng An - Tầng 2, Mường Thanh Ninh Bình", "loai": "an_uong"},
    {"ngay": "2026-10-28", "batdau": "10:30", "ketthuc": "13:00", "hoatdong": "Ăn trưa", "diadiem": "Nhà hàng Tràng An - Tầng 2, Mường Thanh Ninh Bình", "loai": "an_uong"},
    {"ngay": "2026-10-28", "batdau": "13:30", "ketthuc": "14:00", "hoatdong": "Khai mạc Thi nghiệp vụ", "diadiem": "Phòng VIP 1 - Tầng 3, Mường Thanh Ninh Bình", "loai": "nghiep_vu"},
    {"ngay": "2026-10-28", "batdau": "14:00", "ketthuc": "17:00", "hoatdong": "Thi nghiệp vụ (Bếp, Nhà hàng, AKT, Buồng, KT-NS, LKM)", "diadiem": "Tầng 3, Mường Thanh Ninh Bình", "loai": "nghiep_vu"},
    {"ngay": "2026-10-28", "batdau": "15:00", "ketthuc": "18:00", "hoatdong": "Thể thao - Bóng đá Nam (Bán kết) / Nữ (Vòng bảng 3 sân)", "diadiem": "Sân Teddy", "loai": "the_thao"},
    {"ngay": "2026-10-28", "batdau": "17:30", "ketthuc": "20:00", "hoatdong": "Ăn tối", "diadiem": "Nhà hàng Tràng An - Tầng 2, Mường Thanh Ninh Bình", "loai": "an_uong"},
    {"ngay": "2026-10-28", "batdau": "18:00", "ketthuc": "19:30", "hoatdong": "Mini Games / Lucky Draw / Trao giải nghiệp vụ", "diadiem": "Nhà hàng Tràng An - Tầng 2, Mường Thanh Ninh Bình", "loai": "su_kien"},
    {"ngay": "2026-10-28", "batdau": "18:00", "ketthuc": "21:00", "hoatdong": "Thể thao - Pickleball (Tứ kết Đôi Nữ, Đôi Nam, Đôi Nam-Nữ tại 2 sân KS)", "diadiem": "Mường Thanh Ninh Bình", "loai": "the_thao"},
    {"ngay": "2026-10-28", "batdau": "21:00", "ketthuc": "00:00", "hoatdong": "Ăn đêm", "diadiem": "Nhà hàng Tràng An - Tầng 2, Mường Thanh Ninh Bình", "loai": "an_uong"},

    # Ngày 29/10/2026
    {"ngay": "2026-10-29", "batdau": "05:30", "ketthuc": "08:30", "hoatdong": "Ăn sáng", "diadiem": "Nhà hàng Tràng An - Tầng 2, Mường Thanh Ninh Bình", "loai": "an_uong"},
    {"ngay": "2026-10-29", "batdau": "07:00", "ketthuc": "09:00", "hoatdong": "Thể thao - Bóng đá (Tranh 3-4 & CK Nam/Nữ tại Sân 1 & 3)", "diadiem": "Sân Teddy", "loai": "the_thao"},
    {"ngay": "2026-10-29", "batdau": "09:00", "ketthuc": "09:30", "hoatdong": "Trao giải Bóng đá tại sân", "diadiem": "Sân Teddy", "loai": "su_kien"},
    {"ngay": "2026-10-29", "batdau": "07:00", "ketthuc": "11:00", "hoatdong": "Thể thao - Bóng bàn, Pickleball, Cầu lông (Bán kết & Chung kết)", "diadiem": "Nhà thi đấu Ninh Bình & Mường Thanh Ninh Bình", "loai": "the_thao"},
    {"ngay": "2026-10-29", "batdau": "07:00", "ketthuc": "11:00", "hoatdong": "Tham quan Tràng An", "diadiem": "Thắng cảnh Tràng An", "loai": "tham_quan"},
    {"ngay": "2026-10-29", "batdau": "10:00", "ketthuc": "10:30", "hoatdong": "Thể thao - Bơi (6 lượt Chung kết 6 làn)", "diadiem": "Bể bơi Mường Thanh Ninh Bình", "loai": "the_thao"},
    {"ngay": "2026-10-29", "batdau": "11:00", "ketthuc": "11:30", "hoatdong": "Thể thao - Kéo co (Bán kết, Tranh 3-4 & Chung kết)", "diadiem": "Nhà thi đấu Ninh Bình", "loai": "the_thao"},
    {"ngay": "2026-10-29", "batdau": "10:30", "ketthuc": "13:00", "hoatdong": "Ăn trưa", "diadiem": "Nhà hàng Tràng An - Tầng 2, Mường Thanh Ninh Bình", "loai": "an_uong"},
    {"ngay": "2026-10-29", "batdau": "13:00", "ketthuc": "15:00", "hoatdong": "Mini Games / Lucky Draw / Trao giải thể thao", "diadiem": "Nhà hàng Tràng An - Tầng 2, Mường Thanh Ninh Bình", "loai": "su_kien"},
    {"ngay": "2026-10-29", "batdau": "13:00", "ketthuc": "17:00", "hoatdong": "Tham quan Tràng An", "diadiem": "Thắng cảnh Tràng An", "loai": "tham_quan"},
    {"ngay": "2026-10-29", "batdau": "17:30", "ketthuc": "20:00", "hoatdong": "Ăn tối", "diadiem": "Nhà hàng Tràng An - Tầng 2, Mường Thanh Ninh Bình", "loai": "an_uong"},
    {"ngay": "2026-10-29", "batdau": "18:30", "ketthuc": "22:00", "hoatdong": "Bế mạc Đại hội Mường Thanh", "diadiem": "Ballroom Hoa Lư - Tầng 1, Mường Thanh Ninh Bình", "loai": "su_kien"},
    {"ngay": "2026-10-29", "batdau": "21:00", "ketthuc": "00:00", "hoatdong": "Ăn đêm", "diadiem": "Nhà hàng Tràng An - Tầng 2, Mường Thanh Ninh Bình", "loai": "an_uong"},
]

# ============================================================
# 2. ATHLETES (Full name sheet)
# ============================================================
ws_full = wb['Full name']
mon_cols = {
    5: 'Bơi tự do Nữ 40m', 6: 'Bơi ếch Nữ 40m', 7: 'Bơi tự do Nam 40m', 8: 'Bơi tự do Nam 80m',
    9: 'Bơi ếch Nam 40m', 10: 'Bơi ếch Nam 80m', 11: 'Pickleball đôi Nữ', 12: 'Pickleball đôi Nam-Nữ',
    13: 'Pickleball đôi Nam', 14: 'Cầu lông đơn Nữ', 15: 'Cầu lông đôi Nữ', 16: 'Cầu lông đôi Nam-Nữ',
    17: 'Cầu lông đơn Nam', 18: 'Cầu lông đôi Nam', 19: 'Bóng bàn đơn Nữ', 20: 'Bóng bàn đơn Nam',
    21: 'Kéo co', 22: 'Bóng đá Nam', 23: 'Bóng đá Nữ'
}
athletes = []
for r in range(3, ws_full.max_row+1):
    stt = ws_full.cell(r, 1).value
    if not stt or not str(stt).strip().isdigit():
        continue
    dv = str(ws_full.cell(r, 2).value or '').strip()
    ten = str(ws_full.cell(r, 3).value or '').strip()
    gt = str(ws_full.cell(r, 4).value or '').strip()
    if not ten: continue
    mons = []
    for c, mname in mon_cols.items():
        v = ws_full.cell(r, c).value
        if v and str(v).strip().lower() in ['x', '1']:
            mons.append(mname)
    athletes.append({'stt': int(stt), 'donVi': dv, 'hoVaTen': ten, 'gioiTinh': gt, 'monThi': mons, 'soMon': len(mons)})

# ============================================================
# 3. STRUCTURED SPORT UNITS (PAIRS & TEAMS) FOR EXACT ROSTER MATCHING
# ============================================================
sport_units = []

# --- 3.1 Cầu lông (Đôi & Đơn) ---
ws = wb['Cầu lông']
def parse_cl(r_start, r_end, is_double, ma_mon, mon_name):
    step = 2 if is_double else 1
    r = r_start
    while r <= r_end:
        ten1 = ws.cell(r, 3).value
        dv1 = ws.cell(r, 4).value
        cd1 = ws.cell(r, 5).value
        code = str(ws.cell(r, 6).value or '').strip()
        if ten1 and code:
            ath = [{'hoVaTen': str(ten1).strip(), 'donVi': str(dv1 or '').strip(), 'chucDanh': str(cd1 or '').strip()}]
            if is_double:
                ten2 = ws.cell(r+1, 3).value
                dv2 = ws.cell(r+1, 4).value
                cd2 = ws.cell(r+1, 5).value
                if ten2:
                    ath.append({'hoVaTen': str(ten2).strip(), 'donVi': str(dv2 or '').strip(), 'chucDanh': str(cd2 or '').strip()})
            sub = code.split('_')[-1].strip()
            b = re.search(r'\(([^)]+)\)', sub)
            b_names = [n.strip().lower() for n in b.group(1).split('-')] if b else []
            sport_units.append({
                'code': code,
                'sub': sub,
                'bracketNames': b_names,
                'mon': mon_name,
                'maMon': ma_mon,
                'type': 'pair' if is_double else 'single',
                'athletes': ath
            })
        r += step

parse_cl(6, 21, True, 'CL.2M', 'Cầu lông đôi Nam')
parse_cl(26, 41, True, 'CL.2F', 'Cầu lông đôi Nữ')
parse_cl(46, 53, False, 'CL.M', 'Cầu lông đơn Nam')
parse_cl(58, 65, False, 'CL.F', 'Cầu lông đơn Nữ')
parse_cl(71, 88, True, 'CL.MF', 'Cầu lông đôi Nam - Nữ')

# --- 3.2 Pickleball (Đôi) ---
ws = wb['Pickle ball']
def parse_pk(r_start, r_end, ma_mon, mon_name):
    r = r_start
    while r <= r_end:
        ten1 = ws.cell(r, 3).value
        dv1 = ws.cell(r, 4).value
        cd1 = ws.cell(r, 5).value
        code = str(ws.cell(r, 6).value or '').strip()
        if ten1 and code:
            ath = [{'hoVaTen': str(ten1).strip(), 'donVi': str(dv1 or '').strip(), 'chucDanh': str(cd1 or '').strip()}]
            ten2 = ws.cell(r+1, 3).value
            dv2 = ws.cell(r+1, 4).value
            cd2 = ws.cell(r+1, 5).value
            if ten2:
                ath.append({'hoVaTen': str(ten2).strip(), 'donVi': str(dv2 or '').strip(), 'chucDanh': str(cd2 or '').strip()})
            sub = code.split('_')[-1].strip()
            b = re.search(r'\(([^)]+)\)', sub)
            b_names = [n.strip().lower() for n in b.group(1).split('-')] if b else []
            sport_units.append({
                'code': code,
                'sub': sub,
                'bracketNames': b_names,
                'mon': mon_name,
                'maMon': ma_mon,
                'type': 'pair',
                'athletes': ath
            })
        r += 2

parse_pk(6, 21, 'PK.MF', 'Pickleball đôi Nam - Nữ')
parse_pk(26, 41, 'PK.2F', 'Pickleball đôi Nữ')
parse_pk(46, 61, 'PK.2M', 'Pickleball đôi Nam')

# --- 3.3 Bóng bàn (Đơn Nam & Đơn Nữ) ---
ws = wb['Bóng bàn']
for r in range(6, 16):
    ten = ws.cell(r, 2).value
    dv = ws.cell(r, 3).value
    cd = ws.cell(r, 4).value
    code = str(ws.cell(r, 5).value or '').strip()
    if ten and code:
        sub = code.split('_')[-1].strip()
        b = re.search(r'\(([^)]+)\)', sub)
        b_names = [n.strip().lower() for n in b.group(1).split('-')] if b else []
        sport_units.append({
            'code': code,
            'sub': sub,
            'bracketNames': b_names,
            'mon': 'Bóng bàn đơn Nam',
            'maMon': 'BB.M',
            'type': 'single',
            'athletes': [{'hoVaTen': str(ten).strip(), 'donVi': str(dv or '').strip(), 'chucDanh': str(cd or '').strip()}]
        })

for r in range(21, 32):
    ten = ws.cell(r, 2).value
    dv = ws.cell(r, 3).value
    cd = ws.cell(r, 4).value
    code = str(ws.cell(r, 5).value or '').strip()
    if ten and code:
        sub = code.split('_')[-1].strip()
        b = re.search(r'\(([^)]+)\)', sub)
        b_names = [n.strip().lower() for n in b.group(1).split('-')] if b else []
        sport_units.append({
            'code': code,
            'sub': sub,
            'bracketNames': b_names,
            'mon': 'Bóng bàn đơn Nữ',
            'maMon': 'BB.F',
            'type': 'single',
            'athletes': [{'hoVaTen': str(ten).strip(), 'donVi': str(dv or '').strip(), 'chucDanh': str(cd or '').strip()}]
        })

# --- 3.4 Bóng đá Nam ---
ws = wb['B.Đ nam']
bd_m_aliases = {
    'BĐ.M.01_Liên quân PDO-CDO-VRC': ['LQ.PDO', 'PDO-CDO-VRC', 'PDO'],
    'BĐ.M.02_Cienco5 và DHE': ['Cienco5', 'Cienco5 và DHE'],
    'BĐ.M.03_CTH': ['CTH'],
    'BĐ.M.04_DNA': ['ĐNA', 'DNA'],
    'BĐ.M.05_Liên quân SLA-MCH': ['LQ.SLA', 'SLA-MCH'],
    'BĐ.M.06_Liên quân SMO-HLC-HLR ': ['LQ.HLO', 'SMO-HLC-HLR'],
    'BĐ.M.07_Liên quân VTR-NTR': ['LQ.NTR', 'VTR-NTR'],
    'BĐ.M.08_Liên quân XLA-HNC-HNO': ['LQ.HNO', 'LQ.Vinh', 'XLA-HNC-HNO']
}
code, current_members, team_name = '', [], ''
for r in range(6, ws.max_row+1):
    v5 = str(ws.cell(r, 5).value or '').strip()
    v1 = str(ws.cell(r, 1).value or '').strip()
    if v5.startswith('BĐ.M.'):
        if code and current_members:
            sub = code.split('_')[-1].strip()
            sport_units.append({
                'code': code,
                'sub': sub,
                'teamName': team_name,
                'aliases': bd_m_aliases.get(code, [sub]),
                'mon': 'Bóng đá Nam',
                'maMon': 'BĐ.M',
                'type': 'team',
                'athletes': current_members
            })
            current_members = []
        code = v5
        team_name = v1 if 'Đội:' in v1 else code
    stt = ws.cell(r, 1).value
    ten = ws.cell(r, 2).value
    dv = ws.cell(r, 3).value
    cd = ws.cell(r, 4).value
    if ten and str(stt).strip().isdigit():
        current_members.append({'hoVaTen': str(ten).strip(), 'donVi': str(dv or '').strip(), 'chucDanh': str(cd or '').strip()})
if code and current_members:
    sub = code.split('_')[-1].strip()
    sport_units.append({
        'code': code,
        'sub': sub,
        'teamName': team_name,
        'aliases': bd_m_aliases.get(code, [sub]),
        'mon': 'Bóng đá Nam',
        'maMon': 'BĐ.M',
        'type': 'team',
        'athletes': current_members
    })

# --- 3.5 Bóng đá Nữ ---
ws = wb['B.Đ nữ']
bd_f_aliases = {
    'BĐ.F.01_DLR': ['LQ.DLR', 'DLR'],
    'BĐ.F.02_Liên quân GXT-XTH': ['LQ.XTH', 'GXT-XTH'],
    'BĐ.F.03_Liên quân LSG-PQU': ['LQ.SGO', 'LSG-PQU'],
    'BĐ.F.04_Liên quân QNA-HAN': ['LQ.QNA', 'QNA-HAN'],
    'BĐ.F.05_Cụm siêu thị MT Mart': ['LQ.MT Mart', 'MT Mart'],
    'BĐ.F.06_Liên quân SLA-MCH': ['LQ.SLA', 'SLA-MCH']
}
code, current_members, team_name = '', [], ''
for r in range(6, ws.max_row+1):
    v5 = str(ws.cell(r, 5).value or '').strip()
    v1 = str(ws.cell(r, 1).value or '').strip()
    if v5.startswith('BĐ.F.'):
        if code and current_members:
            sub = code.split('_')[-1].strip()
            sport_units.append({
                'code': code,
                'sub': sub,
                'teamName': team_name,
                'aliases': bd_f_aliases.get(code, [sub]),
                'mon': 'Bóng đá Nữ',
                'maMon': 'BĐ.F',
                'type': 'team',
                'athletes': current_members
            })
            current_members = []
        code = v5
        team_name = v1 if 'Đội:' in v1 else code
    stt = ws.cell(r, 1).value
    ten = ws.cell(r, 2).value
    dv = ws.cell(r, 3).value
    cd = ws.cell(r, 4).value
    if ten and str(stt).strip().isdigit():
        current_members.append({'hoVaTen': str(ten).strip(), 'donVi': str(dv or '').strip(), 'chucDanh': str(cd or '').strip()})
if code and current_members:
    sub = code.split('_')[-1].strip()
    sport_units.append({
        'code': code,
        'sub': sub,
        'teamName': team_name,
        'aliases': bd_f_aliases.get(code, [sub]),
        'mon': 'Bóng đá Nữ',
        'maMon': 'BĐ.F',
        'type': 'team',
        'athletes': current_members
    })

# --- 3.6 Kéo co ---
ws = wb['Kéo co']
kc_aliases = {
    'KC.01_CMA': ['CMA'],
    'KC.02_DLR': ['LQ.DLR', 'DLR'],
    'KC.03_Liên quân LDB-DBP': ['LQ.ĐBP', 'LQ.DBP', 'LDB-DBP'],
    'KC.04_LYS': ['LYS'],
    'KC.05_Liên quân NTR -VTR': ['LQ.NTR', 'NTR-VTR'],
    'KC.06_ Liên quân SMO-HLC-HLR ': ['LQ.HLO', 'SMO-HLC-HLR'],
    'KC.07_VPTĐ': ['VPTĐ', 'VPTD'],
    'KC.08_VTI': ['VTI']
}
code, current_members, team_name = '', [], ''
for r in range(6, ws.max_row+1):
    v5 = str(ws.cell(r, 5).value or '').strip()
    v1 = str(ws.cell(r, 1).value or '').strip()
    if v5.startswith('KC.'):
        if code and current_members:
            sub = code.split('_')[-1].strip()
            sport_units.append({
                'code': code,
                'sub': sub,
                'teamName': team_name,
                'aliases': kc_aliases.get(code, [sub]),
                'mon': 'Kéo co',
                'maMon': 'KC',
                'type': 'team',
                'athletes': current_members
            })
            current_members = []
        code = v5
        team_name = v1 if 'Đội:' in v1 else code
    stt = ws.cell(r, 1).value
    ten = ws.cell(r, 2).value
    dv = ws.cell(r, 3).value
    cd = ws.cell(r, 4).value
    if ten and str(stt).strip().isdigit():
        current_members.append({'hoVaTen': str(ten).strip(), 'donVi': str(dv or '').strip(), 'chucDanh': str(cd or '').strip()})
if code and current_members:
    sub = code.split('_')[-1].strip()
    sport_units.append({
        'code': code,
        'sub': sub,
        'teamName': team_name,
        'aliases': kc_aliases.get(code, [sub]),
        'mon': 'Kéo co',
        'maMon': 'KC',
        'type': 'team',
        'athletes': current_members
    })

# --- 3.7 Bơi lội ---
for sh, mcode, mname in [('BTD Nam', 'BTD.M', 'Bơi tự do Nam'), ('BE Nam', 'BE.M', 'Bơi ếch Nam'), ('Bơi Nữ', 'BƠI.F', 'Bơi Nữ')]:
    ws = wb[sh]
    for r in range(6, ws.max_row+1):
        stt = ws.cell(r, 1).value
        ten = ws.cell(r, 2).value
        dv = ws.cell(r, 3).value
        cd = ws.cell(r, 4).value
        code = str(ws.cell(r, 5).value or '').strip()
        if ten and code and str(stt).strip().isdigit():
            sub = code.split('_')[-1].strip()
            sport_units.append({
                'code': code,
                'sub': sub,
                'bracketNames': [],
                'mon': mname,
                'maMon': mcode,
                'type': 'single',
                'athletes': [{'hoVaTen': str(ten).strip(), 'donVi': str(dv or '').strip(), 'chucDanh': str(cd or '').strip()}]
            })

# --- 3.8 Chi tiết 12 lượt vòng loại & 6 lượt chung kết môn Bơi ---
swim_heats = [
    # --- 12 LƯỢT VÒNG LOẠI (NGÀY 27/10/2026, 14:00 - 14:30) ---
    {
        'id': 'swim_ql_01', 'maTran': 'BTD.M40.L1', 'ngay': '2026-10-27', 'gio': '14:00 - 14:30', 'vong': 'Vòng loại', 'luot': 1,
        'noiDung': 'Bơi Tự Do Nam 40m - Vòng loại Lượt 1', 'mon': 'Bơi Tự Do Nam 40m', 'cuLy': '40m', 'kieu': 'Tự do', 'gioiTinh': 'Nam',
        'lanes': [
            {'lan': 1, 'hoVaTen': 'Nguyễn Văn Sơn', 'donVi': 'MT LCH (Lai Châu)'},
            {'lan': 2, 'hoVaTen': 'Vũ Đức Dũng', 'donVi': 'Cienco5 và DHE'},
            {'lan': 3, 'hoVaTen': 'Trần Xuân Vinh', 'donVi': 'MT SGO (Sài Gòn)'},
            {'lan': 4, 'hoVaTen': 'Lê Quang Trường', 'donVi': 'MT CTH (Cần Thơ)'},
            {'lan': 5, 'hoVaTen': 'Lê Tuấn Kha', 'donVi': 'MT HUE (Huế)'},
            {'lan': 6, 'hoVaTen': '', 'donVi': 'Trống'}
        ]
    },
    {
        'id': 'swim_ql_02', 'maTran': 'BTD.M40.L2', 'ngay': '2026-10-27', 'gio': '14:00 - 14:30', 'vong': 'Vòng loại', 'luot': 2,
        'noiDung': 'Bơi Tự Do Nam 40m - Vòng loại Lượt 2', 'mon': 'Bơi Tự Do Nam 40m', 'cuLy': '40m', 'kieu': 'Tự do', 'gioiTinh': 'Nam',
        'lanes': [
            {'lan': 1, 'hoVaTen': 'Lê Mạnh Hùng', 'donVi': 'THPT Nguyễn Du'},
            {'lan': 2, 'hoVaTen': 'Trần Văn Quân', 'donVi': 'MT HAN (Hà Nội)'},
            {'lan': 3, 'hoVaTen': 'Hoàng Việt Dũng', 'donVi': 'MT CLO (Cửa Lò)'},
            {'lan': 4, 'hoVaTen': 'Trần Xuân Thuỷ', 'donVi': 'VRC'},
            {'lan': 5, 'hoVaTen': 'Trần Lê Quốc Khánh', 'donVi': 'MT LDN (Lâm Đồng)'},
            {'lan': 6, 'hoVaTen': '', 'donVi': 'Trống'}
        ]
    },
    {
        'id': 'swim_ql_03', 'maTran': 'BTD.M80.L1', 'ngay': '2026-10-27', 'gio': '14:00 - 14:30', 'vong': 'Vòng loại', 'luot': 3,
        'noiDung': 'Bơi Tự Do Nam 80m - Vòng loại Lượt 1', 'mon': 'Bơi Tự Do Nam 80m', 'cuLy': '80m', 'kieu': 'Tự do', 'gioiTinh': 'Nam',
        'lanes': [
            {'lan': 1, 'hoVaTen': 'Lương Văn Châu', 'donVi': 'MT CBA (Cát Bà)'},
            {'lan': 2, 'hoVaTen': 'Trần Văn Anh', 'donVi': 'MT BGI (Bắc Giang)'},
            {'lan': 3, 'hoVaTen': 'Lèo Bá Linh', 'donVi': 'MT SLA (Sơn La)'},
            {'lan': 4, 'hoVaTen': 'Lê Văn Tài', 'donVi': 'VRC'},
            {'lan': 5, 'hoVaTen': 'Phạm Minh Hải', 'donVi': 'MT HLC1 (Hạ Long)'},
            {'lan': 6, 'hoVaTen': '', 'donVi': 'Trống'}
        ]
    },
    {
        'id': 'swim_ql_04', 'maTran': 'BTD.M80.L2', 'ngay': '2026-10-27', 'gio': '14:00 - 14:30', 'vong': 'Vòng loại', 'luot': 4,
        'noiDung': 'Bơi Tự Do Nam 80m - Vòng loại Lượt 2', 'mon': 'Bơi Tự Do Nam 80m', 'cuLy': '80m', 'kieu': 'Tự do', 'gioiTinh': 'Nam',
        'lanes': [
            {'lan': 1, 'hoVaTen': 'Lê Văn Duệ', 'donVi': 'MT HAN (Hà Nội)'},
            {'lan': 2, 'hoVaTen': 'Nguyễn Văn Sơn', 'donVi': 'MT LCH (Lai Châu)'},
            {'lan': 3, 'hoVaTen': 'Hoàng Việt Dũng', 'donVi': 'MT CLO (Cửa Lò)'},
            {'lan': 4, 'hoVaTen': 'Ngô Quý Doanh', 'donVi': 'MT HNC (Hà Nội Center)'},
            {'lan': 5, 'hoVaTen': 'Bá Văn Việt', 'donVi': 'MT PDO (Phú Quốc)'},
            {'lan': 6, 'hoVaTen': '', 'donVi': 'Trống'}
        ]
    },
    {
        'id': 'swim_ql_05', 'maTran': 'BE.M40.L1', 'ngay': '2026-10-27', 'gio': '14:00 - 14:30', 'vong': 'Vòng loại', 'luot': 5,
        'noiDung': 'Bơi Ếch Nam 40m - Vòng loại Lượt 1', 'mon': 'Bơi Ếch Nam 40m', 'cuLy': '40m', 'kieu': 'Ếch', 'gioiTinh': 'Nam',
        'lanes': [
            {'lan': 1, 'hoVaTen': 'Dương Thanh Tú', 'donVi': 'MT SHA (Sông Hàn)'},
            {'lan': 2, 'hoVaTen': 'Nguyễn Duy Nhật Nam', 'donVi': 'MT SGO (Sài Gòn)'},
            {'lan': 3, 'hoVaTen': 'Nguyễn Văn Đàn', 'donVi': 'MT LCH (Lai Châu)'},
            {'lan': 4, 'hoVaTen': 'Nguyễn Viết Minh', 'donVi': 'MT BMT (Buôn Ma Thuột)'},
            {'lan': 5, 'hoVaTen': 'Đặng Văn Thắng', 'donVi': 'MT HNO (Hà Nội)'},
            {'lan': 6, 'hoVaTen': '', 'donVi': 'Trống'}
        ]
    },
    {
        'id': 'swim_ql_06', 'maTran': 'BE.M40.L2', 'ngay': '2026-10-27', 'gio': '14:00 - 14:30', 'vong': 'Vòng loại', 'luot': 6,
        'noiDung': 'Bơi Ếch Nam 40m - Vòng loại Lượt 2', 'mon': 'Bơi Ếch Nam 40m', 'cuLy': '40m', 'kieu': 'Ếch', 'gioiTinh': 'Nam',
        'lanes': [
            {'lan': 1, 'hoVaTen': 'Nguyễn Khắc Thống', 'donVi': 'THPT Nguyễn Du'},
            {'lan': 2, 'hoVaTen': 'Nguyễn Hữu Đương', 'donVi': 'LQ Chung cư Hà Nội'},
            {'lan': 3, 'hoVaTen': 'Lê Văn Tài', 'donVi': 'VRC'},
            {'lan': 4, 'hoVaTen': 'Võ Đình Lưu', 'donVi': 'MT QNH (Quảng Ninh)'},
            {'lan': 5, 'hoVaTen': 'Lê Bá Hải', 'donVi': 'MT SGO (Sài Gòn)'},
            {'lan': 6, 'hoVaTen': '', 'donVi': 'Trống'}
        ]
    },
    {
        'id': 'swim_ql_07', 'maTran': 'BE.M80.L1', 'ngay': '2026-10-27', 'gio': '14:00 - 14:30', 'vong': 'Vòng loại', 'luot': 7,
        'noiDung': 'Bơi Ếch Nam 80m - Vòng loại Lượt 1', 'mon': 'Bơi Ếch Nam 80m', 'cuLy': '80m', 'kieu': 'Ếch', 'gioiTinh': 'Nam',
        'lanes': [
            {'lan': 1, 'hoVaTen': 'Phạm Xuân Thanh', 'donVi': 'NLE'},
            {'lan': 2, 'hoVaTen': 'Tăng Văn Thuận', 'donVi': 'Cienco5 và DHE'},
            {'lan': 3, 'hoVaTen': 'Trần Quốc Anh', 'donVi': 'LSG'},
            {'lan': 4, 'hoVaTen': 'Nguyễn Hữu Đương', 'donVi': 'Cụm CC Hà Nội'},
            {'lan': 5, 'hoVaTen': 'Nguyễn Văn Đàn', 'donVi': 'LCH (Lai Châu)'},
            {'lan': 6, 'hoVaTen': 'Vũ Đức Dũng', 'donVi': 'Cienco5 và DHE'}
        ]
    },
    {
        'id': 'swim_ql_08', 'maTran': 'BE.M80.L2', 'ngay': '2026-10-27', 'gio': '14:00 - 14:30', 'vong': 'Vòng loại', 'luot': 8,
        'noiDung': 'Bơi Ếch Nam 80m - Vòng loại Lượt 2', 'mon': 'Bơi Ếch Nam 80m', 'cuLy': '80m', 'kieu': 'Ếch', 'gioiTinh': 'Nam',
        'lanes': [
            {'lan': 1, 'hoVaTen': 'Võ Minh Tuấn', 'donVi': 'VTR'},
            {'lan': 2, 'hoVaTen': 'Đặng Văn Thắng', 'donVi': 'HNO (Hà Nội)'},
            {'lan': 3, 'hoVaTen': 'Trần Xuân Thuỷ', 'donVi': 'VRC'},
            {'lan': 4, 'hoVaTen': 'Nguyễn Văn Linh', 'donVi': 'CMA (Cà Mau)'},
            {'lan': 5, 'hoVaTen': 'Lê Mạnh Hùng', 'donVi': 'Trường Nguyễn Du'},
            {'lan': 6, 'hoVaTen': '', 'donVi': 'Trống'}
        ]
    },
    {
        'id': 'swim_ql_09', 'maTran': 'BTD.F40.L1', 'ngay': '2026-10-27', 'gio': '14:00 - 14:30', 'vong': 'Vòng loại', 'luot': 9,
        'noiDung': 'Bơi Tự Do Nữ 40m - Vòng loại Lượt 1', 'mon': 'Bơi Tự Do Nữ 40m', 'cuLy': '40m', 'kieu': 'Tự do', 'gioiTinh': 'Nữ',
        'lanes': [
            {'lan': 1, 'hoVaTen': '', 'donVi': 'Trống'},
            {'lan': 2, 'hoVaTen': 'Trần Thị Hoa', 'donVi': 'HMA'},
            {'lan': 3, 'hoVaTen': 'Phạm Thị Bốn', 'donVi': 'Cienco5 và DHE'},
            {'lan': 4, 'hoVaTen': 'Nguyễn Hương Ly', 'donVi': 'BGI (Bắc Giang)'},
            {'lan': 5, 'hoVaTen': 'Nguyễn Thị Loan', 'donVi': 'QTR (Quảng Trị)'},
            {'lan': 6, 'hoVaTen': '', 'donVi': 'Trống'}
        ]
    },
    {
        'id': 'swim_ql_10', 'maTran': 'BTD.F40.L2', 'ngay': '2026-10-27', 'gio': '14:00 - 14:30', 'vong': 'Vòng loại', 'luot': 10,
        'noiDung': 'Bơi Tự Do Nữ 40m - Vòng loại Lượt 2', 'mon': 'Bơi Tự Do Nữ 40m', 'cuLy': '40m', 'kieu': 'Tự do', 'gioiTinh': 'Nữ',
        'lanes': [
            {'lan': 1, 'hoVaTen': '', 'donVi': 'Trống'},
            {'lan': 2, 'hoVaTen': 'Lô Thị Hằng', 'donVi': 'CCU'},
            {'lan': 3, 'hoVaTen': 'Lò Thị Thắm', 'donVi': 'DBP (Điện Biên Phủ)'},
            {'lan': 4, 'hoVaTen': 'Hoàng Thị La', 'donVi': 'Cienco5 và DHE'},
            {'lan': 5, 'hoVaTen': 'Trần Bích Ngọc', 'donVi': 'VPTĐ'},
            {'lan': 6, 'hoVaTen': '', 'donVi': 'Trống'}
        ]
    },
    {
        'id': 'swim_ql_11', 'maTran': 'BE.F40.L1', 'ngay': '2026-10-27', 'gio': '14:00 - 14:30', 'vong': 'Vòng loại', 'luot': 11,
        'noiDung': 'Bơi Ếch Nữ 40m - Vòng loại Lượt 1', 'mon': 'Bơi Ếch Nữ 40m', 'cuLy': '40m', 'kieu': 'Ếch', 'gioiTinh': 'Nữ',
        'lanes': [
            {'lan': 1, 'hoVaTen': 'Phạm Thị Bốn', 'donVi': 'Cienco5 và DHE'},
            {'lan': 2, 'hoVaTen': 'Nguyễn Thị Như Quỳnh', 'donVi': 'Cienco5 và DHE'},
            {'lan': 3, 'hoVaTen': 'Nguyễn Thị Vân', 'donVi': 'VPTĐ'},
            {'lan': 4, 'hoVaTen': 'Nguyễn Thị Thu Ngọc', 'donVi': 'QNA (Quảng Nam)'},
            {'lan': 5, 'hoVaTen': 'Lưu Quỳnh Hương', 'donVi': 'HLC (Hạ Long)'},
            {'lan': 6, 'hoVaTen': '', 'donVi': 'Trống'}
        ]
    },
    {
        'id': 'swim_ql_12', 'maTran': 'BE.F40.L2', 'ngay': '2026-10-27', 'gio': '14:00 - 14:30', 'vong': 'Vòng loại', 'luot': 12,
        'noiDung': 'Bơi Ếch Nữ 40m - Vòng loại Lượt 2', 'mon': 'Bơi Ếch Nữ 40m', 'cuLy': '40m', 'kieu': 'Ếch', 'gioiTinh': 'Nữ',
        'lanes': [
            {'lan': 1, 'hoVaTen': '', 'donVi': 'Trống'},
            {'lan': 2, 'hoVaTen': 'Trần Bích Ngọc', 'donVi': 'VPTĐ'},
            {'lan': 3, 'hoVaTen': 'Đặng Thị Ánh Phượng', 'donVi': 'VRC'},
            {'lan': 4, 'hoVaTen': 'Phạm Thị Hương', 'donVi': 'Cienco5 và DHE'},
            {'lan': 5, 'hoVaTen': 'Dương Thị Thùy Linh', 'donVi': 'LSG'},
            {'lan': 6, 'hoVaTen': '', 'donVi': 'Trống'}
        ]
    },

    # --- 6 LƯỢT CHUNG KẾT (NGÀY 29/10/2026, 10:00 - 10:30) ---
    {
        'id': 'swim_fn_01', 'maTran': 'BTD.M40.CK', 'ngay': '2026-10-29', 'gio': '10:00 - 10:30', 'vong': 'Chung kết', 'luot': 1,
        'noiDung': 'Chung kết Bơi Tự Do Nam 40m', 'mon': 'Bơi Tự Do Nam 40m', 'cuLy': '40m', 'kieu': 'Tự do', 'gioiTinh': 'Nam',
        'lanes': [
            {'lan': 1, 'hoVaTen': 'Top 1 Vòng loại', 'donVi': 'TBD'},
            {'lan': 2, 'hoVaTen': 'Top 2 Vòng loại', 'donVi': 'TBD'},
            {'lan': 3, 'hoVaTen': 'Top 3 Vòng loại', 'donVi': 'TBD'},
            {'lan': 4, 'hoVaTen': 'Top 4 Vòng loại', 'donVi': 'TBD'},
            {'lan': 5, 'hoVaTen': 'Top 5 Vòng loại', 'donVi': 'TBD'},
            {'lan': 6, 'hoVaTen': 'Top 6 Vòng loại', 'donVi': 'TBD'}
        ]
    },
    {
        'id': 'swim_fn_02', 'maTran': 'BTD.M80.CK', 'ngay': '2026-10-29', 'gio': '10:00 - 10:30', 'vong': 'Chung kết', 'luot': 2,
        'noiDung': 'Chung kết Bơi Tự Do Nam 80m', 'mon': 'Bơi Tự Do Nam 80m', 'cuLy': '80m', 'kieu': 'Tự do', 'gioiTinh': 'Nam',
        'lanes': [
            {'lan': 1, 'hoVaTen': 'Top 1 Vòng loại', 'donVi': 'TBD'},
            {'lan': 2, 'hoVaTen': 'Top 2 Vòng loại', 'donVi': 'TBD'},
            {'lan': 3, 'hoVaTen': 'Top 3 Vòng loại', 'donVi': 'TBD'},
            {'lan': 4, 'hoVaTen': 'Top 4 Vòng loại', 'donVi': 'TBD'},
            {'lan': 5, 'hoVaTen': 'Top 5 Vòng loại', 'donVi': 'TBD'},
            {'lan': 6, 'hoVaTen': 'Top 6 Vòng loại', 'donVi': 'TBD'}
        ]
    },
    {
        'id': 'swim_fn_03', 'maTran': 'BE.M40.CK', 'ngay': '2026-10-29', 'gio': '10:00 - 10:30', 'vong': 'Chung kết', 'luot': 3,
        'noiDung': 'Chung kết Bơi Ếch Nam 40m', 'mon': 'Bơi Ếch Nam 40m', 'cuLy': '40m', 'kieu': 'Ếch', 'gioiTinh': 'Nam',
        'lanes': [
            {'lan': 1, 'hoVaTen': 'Top 1 Vòng loại', 'donVi': 'TBD'},
            {'lan': 2, 'hoVaTen': 'Top 2 Vòng loại', 'donVi': 'TBD'},
            {'lan': 3, 'hoVaTen': 'Top 3 Vòng loại', 'donVi': 'TBD'},
            {'lan': 4, 'hoVaTen': 'Top 4 Vòng loại', 'donVi': 'TBD'},
            {'lan': 5, 'hoVaTen': 'Top 5 Vòng loại', 'donVi': 'TBD'},
            {'lan': 6, 'hoVaTen': 'Top 6 Vòng loại', 'donVi': 'TBD'}
        ]
    },
    {
        'id': 'swim_fn_04', 'maTran': 'BE.M80.CK', 'ngay': '2026-10-29', 'gio': '10:00 - 10:30', 'vong': 'Chung kết', 'luot': 4,
        'noiDung': 'Chung kết Bơi Ếch Nam 80m', 'mon': 'Bơi Ếch Nam 80m', 'cuLy': '80m', 'kieu': 'Ếch', 'gioiTinh': 'Nam',
        'lanes': [
            {'lan': 1, 'hoVaTen': 'Top 1 Vòng loại', 'donVi': 'TBD'},
            {'lan': 2, 'hoVaTen': 'Top 2 Vòng loại', 'donVi': 'TBD'},
            {'lan': 3, 'hoVaTen': 'Top 3 Vòng loại', 'donVi': 'TBD'},
            {'lan': 4, 'hoVaTen': 'Top 4 Vòng loại', 'donVi': 'TBD'},
            {'lan': 5, 'hoVaTen': 'Top 5 Vòng loại', 'donVi': 'TBD'},
            {'lan': 6, 'hoVaTen': 'Top 6 Vòng loại', 'donVi': 'TBD'}
        ]
    },
    {
        'id': 'swim_fn_05', 'maTran': 'BTD.F40.CK', 'ngay': '2026-10-29', 'gio': '10:00 - 10:30', 'vong': 'Chung kết', 'luot': 5,
        'noiDung': 'Chung kết Bơi Tự Do Nữ 40m', 'mon': 'Bơi Tự Do Nữ 40m', 'cuLy': '40m', 'kieu': 'Tự do', 'gioiTinh': 'Nữ',
        'lanes': [
            {'lan': 1, 'hoVaTen': 'Top 1 Vòng loại', 'donVi': 'TBD'},
            {'lan': 2, 'hoVaTen': 'Top 2 Vòng loại', 'donVi': 'TBD'},
            {'lan': 3, 'hoVaTen': 'Top 3 Vòng loại', 'donVi': 'TBD'},
            {'lan': 4, 'hoVaTen': 'Top 4 Vòng loại', 'donVi': 'TBD'},
            {'lan': 5, 'hoVaTen': 'Top 5 Vòng loại', 'donVi': 'TBD'},
            {'lan': 6, 'hoVaTen': 'Top 6 Vòng loại', 'donVi': 'TBD'}
        ]
    },
    {
        'id': 'swim_fn_06', 'maTran': 'BE.F40.CK', 'ngay': '2026-10-29', 'gio': '10:00 - 10:30', 'vong': 'Chung kết', 'luot': 6,
        'noiDung': 'Chung kết Bơi Ếch Nữ 40m', 'mon': 'Bơi Ếch Nữ 40m', 'cuLy': '40m', 'kieu': 'Ếch', 'gioiTinh': 'Nữ',
        'lanes': [
            {'lan': 1, 'hoVaTen': 'Top 1 Vòng loại', 'donVi': 'TBD'},
            {'lan': 2, 'hoVaTen': 'Top 2 Vòng loại', 'donVi': 'TBD'},
            {'lan': 3, 'hoVaTen': 'Top 3 Vòng loại', 'donVi': 'TBD'},
            {'lan': 4, 'hoVaTen': 'Top 4 Vòng loại', 'donVi': 'TBD'},
            {'lan': 5, 'hoVaTen': 'Top 5 Vòng loại', 'donVi': 'TBD'},
            {'lan': 6, 'hoVaTen': 'Top 6 Vòng loại', 'donVi': 'TBD'}
        ]
    }
]

# Traditional flat teams list for athlete modal search
flat_teams = []
for u in sport_units:
    for a in u['athletes']:
        flat_teams.append({
            'mon': u['mon'],
            'maMon': u['maMon'],
            'hoVaTen': a['hoVaTen'],
            'donVi': a['donVi'],
            'chucDanh': a.get('chucDanh', ''),
            'maDoi': u['code']
        })

# ============================================================
# 4. SCHEDULE (A-Chi tiết sheet)
# ============================================================
ws_sch = wb['A-Chi tiết']

col_specs = {
    3:  {'mon': 'Thi nghiệp vụ', 'maMon': 'NV', 'san': 'NV.Casino-T3',        'sanGoc': 'Khu Dự án Casino - T3',         'khuVuc': 'Khu Vực Thi Nghiệp Vụ (Tầng 3 KS)', 'cumDiaDiem': 'Khách sạn Mường Thanh'},
    4:  {'mon': 'Thi nghiệp vụ', 'maMon': 'NV', 'san': 'NV.Nhà hàng',        'sanGoc': 'Nhà hàng (T3)',                 'khuVuc': 'Khu Vực Thi Nghiệp Vụ (Tầng 3 KS)', 'cumDiaDiem': 'Khách sạn Mường Thanh'},
    5:  {'mon': 'Thi nghiệp vụ', 'maMon': 'NV', 'san': 'NV.VIP3-Ngoài trời',  'sanGoc': 'Ngoài trời hoặc VIP3 (T3-80m)', 'khuVuc': 'Khu Vực Thi Nghiệp Vụ (Tầng 3 KS)', 'cumDiaDiem': 'Khách sạn Mường Thanh'},
    6:  {'mon': 'Thi nghiệp vụ', 'maMon': 'NV', 'san': 'NV.VIP1-T3',          'sanGoc': 'VIP1 - T3 (200m)',              'khuVuc': 'Khu Vực Thi Nghiệp Vụ (Tầng 3 KS)', 'cumDiaDiem': 'Khách sạn Mường Thanh'},
    7:  {'mon': 'Thi nghiệp vụ', 'maMon': 'NV', 'san': 'NV.VIP2-T3',          'sanGoc': 'VIP2 - T3 (130m)',              'khuVuc': 'Khu Vực Thi Nghiệp Vụ (Tầng 3 KS)', 'cumDiaDiem': 'Khách sạn Mường Thanh'},
    8:  {'mon': 'Bơi',          'maMon': 'BƠI','san': 'BƠI.6 làn bơi',       'sanGoc': '6 làn bơi',                     'khuVuc': 'Bể bơi Khách sạn',                  'cumDiaDiem': 'Khách sạn Mường Thanh'},
    9:  {'mon': 'Bóng bàn',     'maMon': 'BB', 'san': 'BB.Bàn 01',           'sanGoc': 'Bàn 1',                         'khuVuc': 'Nhà thi đấu Ninh Bình',             'cumDiaDiem': 'Nhà thi đấu Ninh Bình'},
    10: {'mon': 'Bóng bàn',     'maMon': 'BB', 'san': 'BB.Bàn 02',           'sanGoc': 'Bàn 2',                         'khuVuc': 'Nhà thi đấu Ninh Bình',             'cumDiaDiem': 'Nhà thi đấu Ninh Bình'},
    11: {'mon': 'Kéo co',       'maMon': 'KC', 'san': 'KC.Làn 01',           'sanGoc': 'Làn kéo 1',                     'khuVuc': 'Nhà thi đấu Ninh Bình',             'cumDiaDiem': 'Nhà thi đấu Ninh Bình'},
    12: {'mon': 'Kéo co',       'maMon': 'KC', 'san': 'KC.Làn 02',           'sanGoc': 'Làn kéo 2',                     'khuVuc': 'Nhà thi đấu Ninh Bình',             'cumDiaDiem': 'Nhà thi đấu Ninh Bình'},
    13: {'mon': 'Cầu lông',     'maMon': 'CL', 'san': 'CL.Sân 01',           'sanGoc': 'Sân 01',                        'khuVuc': 'Nhà thi đấu Ninh Bình',             'cumDiaDiem': 'Nhà thi đấu Ninh Bình'},
    14: {'mon': 'Cầu lông',     'maMon': 'CL', 'san': 'CL.Sân 02',           'sanGoc': 'Sân 02',                        'khuVuc': 'Nhà thi đấu Ninh Bình',             'cumDiaDiem': 'Nhà thi đấu Ninh Bình'},
    15: {'mon': 'Cầu lông',     'maMon': 'CL', 'san': 'CL.Sân 03',           'sanGoc': 'Sân 03',                        'khuVuc': 'Nhà thi đấu Ninh Bình',             'cumDiaDiem': 'Nhà thi đấu Ninh Bình'},
    16: {'mon': 'Cầu lông',     'maMon': 'CL', 'san': 'CL.Sân 04',           'sanGoc': 'Sân 04',                        'khuVuc': 'Nhà thi đấu Ninh Bình',             'cumDiaDiem': 'Nhà thi đấu Ninh Bình'},
    17: {'mon': 'Pickleball',   'maMon': 'PK', 'san': 'PK.Sân 01',           'sanGoc': 'Sân số 01',                     'khuVuc': 'Sân Khách sạn',                     'cumDiaDiem': 'Khách sạn Mường Thanh'},
    18: {'mon': 'Pickleball',   'maMon': 'PK', 'san': 'PK.Sân 02',           'sanGoc': 'Sân số 02',                     'khuVuc': 'Sân Khách sạn',                     'cumDiaDiem': 'Khách sạn Mường Thanh'},
    19: {'mon': 'Bóng đá',      'maMon': 'BĐ', 'san': 'BĐ.Sân 01',           'sanGoc': 'Sân 1',                         'khuVuc': 'Sân Bóng Teddy',                    'cumDiaDiem': 'Sân Bóng Teddy'},
    20: {'mon': 'Bóng đá',      'maMon': 'BĐ', 'san': 'BĐ.Sân 02',           'sanGoc': 'Sân 2',                         'khuVuc': 'Sân Bóng Teddy',                    'cumDiaDiem': 'Sân Bóng Teddy'},
    21: {'mon': 'Bóng đá',      'maMon': 'BĐ', 'san': 'BĐ.Sân 03',           'sanGoc': 'Sân 3',                         'khuVuc': 'Sân Bóng Teddy',                    'cumDiaDiem': 'Sân Bóng Teddy'}
}

schedule = []

# Day 1: 27/10/2026 (Rows 7 to 27)
for r in range(7, 28):
    if 7 <= r <= 12:
        t0, t1, luot = '13:00', '14:00', f'Lượt {r-6}'
    elif 13 <= r <= 14:
        t0, t1, luot = '14:00', '15:00', f'Lượt {r-12}'
    elif 15 <= r <= 18:
        t0, t1, luot = '15:00', '17:00', f'Lượt {r-14}'
    elif 19 <= r <= 27:
        t0, t1, luot = '17:00', '18:00', f'Lượt {r-18}'
    
    for c in range(3, 22):
        val = ws_sch.cell(r, c).value
        if val is not None and str(val).strip() not in ['', 'nan', 'None']:
            info = col_specs[c]
            nd = str(val).strip().replace('\n', ' / ')
            if info['mon'] == 'Bơi':
                # Mở rộng toàn bộ 12 lượt vòng loại môn Bơi với chi tiết từng làn và VĐV
                for h in swim_heats:
                    if h['vong'] == 'Vòng loại':
                        athletes_str = ', '.join([f"Làn {l['lan']}: {l['hoVaTen']} ({l['donVi']})" for l in h['lanes'] if l['hoVaTen'] and l['hoVaTen'] != 'Trống'])
                        schedule.append({
                            'ngay': '2026-10-27',
                            'batdau': '14:00',
                            'ketthuc': '14:30',
                            'luot': f"Lượt {h['luot']}",
                            'mon': 'Bơi',
                            'maMon': 'BƠI',
                            'san': info['san'],
                            'sanGoc': info['sanGoc'],
                            'khuVuc': info['khuVuc'],
                            'cumDiaDiem': info['cumDiaDiem'],
                            'heatId': h['id'],
                            'maTran': h.get('maTran', f"BƠI.L{h['luot']}"),
                            'noiDung': f"{h['noiDung']} ({athletes_str})" if athletes_str else h['noiDung'],
                            'lanes': h['lanes']
                        })
            else:
                schedule.append({
                    'ngay': '2026-10-27',
                    'batdau': t0,
                    'ketthuc': t1,
                    'luot': luot,
                    'mon': info['mon'],
                    'maMon': info['maMon'],
                    'san': info['san'],
                    'sanGoc': info['sanGoc'],
                    'khuVuc': info['khuVuc'],
                    'cumDiaDiem': info['cumDiaDiem'],
                    'noiDung': nd
                })

# Day 2: 28/10/2026 (Rows 32 to 47)
curr_t0 = ''
curr_t1 = ''
for r in range(32, 48):
    t0_val = ws_sch.cell(r, 1).value
    t1_val = ws_sch.cell(r, 2).value
    if isinstance(t0_val, datetime.time):
        curr_t0 = t0_val.strftime('%H:%M')
        curr_t1 = t1_val.strftime('%H:%M') if isinstance(t1_val, datetime.time) else ''
    
    if str(t0_val).strip() == 'TỐI':
        continue
    
    for c in range(3, 22):
        val = ws_sch.cell(r, c).value
        if val is not None and str(val).strip() not in ['', 'nan', 'None']:
            info = col_specs[c]
            nd = str(val).strip().replace('\n', ' / ')
            schedule.append({
                'ngay': '2026-10-28',
                'batdau': curr_t0,
                'ketthuc': curr_t1,
                'luot': '',
                'mon': info['mon'],
                'maMon': info['maMon'],
                'san': info['san'],
                'sanGoc': info['sanGoc'],
                'khuVuc': info['khuVuc'],
                'cumDiaDiem': info['cumDiaDiem'],
                'noiDung': nd
            })

# Day 3: 29/10/2026 (Rows 49 to 60)
curr_t0 = ''
curr_t1 = ''
for r in range(49, 60):
    t0_val = ws_sch.cell(r, 1).value
    t1_val = ws_sch.cell(r, 2).value
    if isinstance(t0_val, datetime.time):
        curr_t0 = t0_val.strftime('%H:%M')
        curr_t1 = t1_val.strftime('%H:%M') if isinstance(t1_val, datetime.time) else ''
    
    for c in range(3, 22):
        val = ws_sch.cell(r, c).value
        if val is not None and str(val).strip() not in ['', 'nan', 'None']:
            info = col_specs[c]
            nd = str(val).strip().replace('\n', ' / ')
            if info['mon'] == 'Bơi':
                # Mở rộng toàn bộ 6 lượt chung kết môn Bơi
                for h in swim_heats:
                    if h['vong'] == 'Chung kết':
                        schedule.append({
                            'ngay': '2026-10-29',
                            'batdau': '10:00',
                            'ketthuc': '10:30',
                            'luot': f"Chung kết {h['luot']}",
                            'mon': 'Bơi',
                            'maMon': 'BƠI',
                            'san': info['san'],
                            'sanGoc': info['sanGoc'],
                            'khuVuc': info['khuVuc'],
                            'cumDiaDiem': info['cumDiaDiem'],
                            'heatId': h['id'],
                            'maTran': h.get('maTran', f"BƠI.CK{h['luot']}"),
                            'noiDung': f"{h['noiDung']} (Top 6 Vòng loại tranh 1-2-3-4)",
                            'lanes': h['lanes']
                        })
            else:
                schedule.append({
                    'ngay': '2026-10-29',
                    'batdau': curr_t0,
                    'ketthuc': curr_t1,
                    'luot': f'Lượt {r-56}' if r in (58, 59) else '',
                    'mon': info['mon'],
                    'maMon': info['maMon'],
                    'san': info['san'],
                    'sanGoc': info['sanGoc'],
                    'khuVuc': info['khuVuc'],
                    'cumDiaDiem': info['cumDiaDiem'],
                    'noiDung': nd
                })

# Sport List
monList = [
    {'ma': 'NV',      'ten': 'Thi nghiệp vụ',   'mau': '#7c3aed', 'bg': 'bg-purple-600', 'badge': 'bg-purple-100 text-purple-800'},
    {'ma': 'PK',      'ten': 'Pickleball',     'mau': '#ea580c', 'bg': 'bg-orange-600', 'badge': 'bg-orange-100 text-orange-800'},
    {'ma': 'BĐ',      'ten': 'Bóng đá',        'mau': '#15803d', 'bg': 'bg-green-600',  'badge': 'bg-green-100 text-green-800'},
    {'ma': 'CL',      'ten': 'Cầu lông',       'mau': '#dc2626', 'bg': 'bg-red-600',    'badge': 'bg-red-100 text-red-800'},
    {'ma': 'BB',      'ten': 'Bóng bàn',       'mau': '#1d4ed8', 'bg': 'bg-blue-600',   'badge': 'bg-blue-100 text-blue-800'},
    {'ma': 'KC',      'ten': 'Kéo co',         'mau': '#b45309', 'bg': 'bg-amber-600',  'badge': 'bg-amber-100 text-amber-800'},
    {'ma': 'BƠI',     'ten': 'Bơi',            'mau': '#0284c7', 'bg': 'bg-sky-600',    'badge': 'bg-sky-100 text-sky-800'},
]

try:
    from add_tournaments import tournaments
except Exception as e:
    tournaments = []

output = {
    'agenda': agenda,
    'athletes': athletes,
    'sportUnits': sport_units,
    'swimHeats': swim_heats,
    'tournaments': tournaments,
    'teams': flat_teams,
    'schedule': schedule,
    'monList': monList
}

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f'Done! Athletes: {len(athletes)}, Schedule: {len(schedule)}, Sport Units: {len(sport_units)}, Teams: {len(flat_teams)}, Swim Heats: {len(swim_heats)}, Tournaments: {len(tournaments)}')
print(f'Agenda events: {len(agenda)}')
