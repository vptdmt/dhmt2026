import sys
import os
import json
import csv
import re

sys.stdout.reconfigure(encoding='utf-8')

def clean_phone(p):
    if not p:
        return ''
    p = str(p).strip()
    digits = re.sub(r'\D', '', p)
    if len(digits) == 9 and digits[0] in '35789':
        digits = '0' + digits
    if len(digits) == 10 and digits.startswith('0'):
        return f"{digits[:4]} {digits[4:7]} {digits[7:]}"
    if len(digits) == 11 and digits.startswith('84'):
        d0 = '0' + digits[2:]
        return f"{d0[:4]} {d0[4:7]} {d0[7:]}"
    return p

# 1. Load data.json
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

old_runners_map = {r['bib']: r for r in data['funrun']['runners']}
old_vehicles_map = {v['num']: v for v in data['funrun']['vehicles']}

# Known license plates
KNOWN_PLATES = {
    2: '30L 218.10',
    3: '30E 412.72',
    5: '19A 647.63',
    6: '29A 926.18',
    7: '30L 337.90',
    8: '90A 229.87',
    9: '36A 991.46',
    10: '24A 280.49',
    11: '73A-048.52',
    12: '74A-258.46',
    13: '37K-228.43',
    14: '75A-334.40',
    15: '37K-336.27',
    16: '30L 187.76',
    17: '14A-89642',
    18: '14A-89663',
    19: '11A-11772',
    20: '37K-281.42',
    21: '73A-319.98',
    22: '37B - 007.70',
    23: 'ກດ5103',
    33: '30L 211.60',
    34: '29B 612.19', # 16 chỗ Media xe của Nguyễn An Khang
}

# 2. Parse danh_sach_xe_funrun_23.10.csv
with open('danh_sach_xe_funrun_23.10.csv', mode='r', encoding='utf-8') as f:
    rows = list(csv.reader(f))

raw_vehicles = []
cur_v = None

for i, r in enumerate(rows):
    if not r:
        continue
    c0 = r[0].strip() if len(r) > 0 else ''
    if c0.startswith('XE '):
        if cur_v:
            raw_vehicles.append(cur_v)
        cur_v = {'header': c0, 'rows': []}
        continue
    if cur_v and (c0 == 'STT' or (len(r) > 1 and r[1].strip() == 'Xe số')):
        continue
    if cur_v and any(c.strip() for c in r):
        cur_v['rows'].append(r)

if cur_v:
    raw_vehicles.append(cur_v)

print(f"Parsed {len(raw_vehicles)} vehicle blocks from CSV.")

# 3. Process each vehicle block
vehicles = []
all_runners = []

for v_raw in raw_vehicles:
    h = v_raw['header']
    m = re.search(r'XE\s*(\d+)', h)
    num = int(m.group(1)) if m else 0
    v_id = f"XE-{num:02d}"

    # Departure time
    if '04:30' in h or num in [3, 34]:
        dep_time = '04:30'
    elif '05:15' in h or num == 33:
        dep_time = '05:15'
    elif 'TỰ TÚC' in h.upper() or num in [30, 31]:
        dep_time = 'Tự túc phương tiện'
    else:
        dep_time = '05:00'

    # Capacity and Type
    if num == 1:
        v_type = '4 chỗ'
        cap = 4
        v_label = 'Xe 01 - Tổng Giám Đốc'
    elif num == 2:
        v_type = '7 chỗ'
        cap = 7
        v_label = 'Xe 02 - Ban Phó Tổng & Các Giám Đốc (7 chỗ)'
    elif num == 3:
        v_type = '7 chỗ'
        cap = 7
        v_label = 'Xe 03 - Ban Tổ Chức (Đi sớm 04h30) (7 chỗ)'
    elif num == 34:
        v_type = '16 chỗ'
        cap = 16
        v_label = 'Xe 34 - Ekip Media (Đi sớm 04h30) (16 chỗ)'
    elif 4 <= num <= 21:
        v_type = '7 chỗ'
        cap = 7
        v_label = f"Xe {num:02d} - Vận động viên (7 chỗ)"
    elif num in [22, 23]:
        v_type = '16 chỗ'
        cap = 16
        v_label = f"Xe {num:02d} - Vận động viên (16 chỗ)"
    elif 24 <= num <= 29:
        v_type = '45 chỗ'
        cap = 45
        v_label = f"Xe {num:02d} - Vận động viên (45 chỗ)"
    elif num == 30:
        v_type = 'Tự túc'
        cap = len(v_raw['rows'])
        v_label = 'Xe 30 - Khối Siêu Thị Mường Thanh (Tự di chuyển)'
    elif num == 31:
        v_type = 'Tự túc'
        cap = len(v_raw['rows'])
        v_label = 'Xe 31 - Công ty Cienco5 & Thang máy DHE (Tự di chuyển)'
    elif num == 32:
        v_type = '7 chỗ'
        cap = 7
        v_label = 'Xe 32 - Tổ Y Tế BV Phủ Diễn (7 chỗ)'
    elif num == 33:
        v_type = '7 chỗ'
        cap = 7
        v_label = 'Xe 33 - Xe Chốt Đoàn (Xuất phát 05h15) (7 chỗ)'
    else:
        v_type = '7 chỗ'
        cap = 7
        v_label = f"Xe {num:02d}"

    # Extract Captain & Driver from rows
    cap_name = ''
    cap_phone = ''
    cap_title = ''
    cap_unit = ''

    driver_name = ''
    driver_phone = ''

    # First pass for captain and driver
    for r in v_raw['rows']:
        # r columns:
        # 0: STT, 1: Xe số, 2: Số BIB, 3: Họ và tên, 4: Giới tính, 5: Chức danh, 6: Đơn vị công tác,
        # 7: Cự ly chạy, 8: Size áo, 9: Số điện thoại, 10: Vai trò / Nhiệm vụ trên xe
        name = r[3].strip() if len(r) > 3 else ''
        gender = r[4].strip() if len(r) > 4 else ''
        title = r[5].strip() if len(r) > 5 else ''
        unit = r[6].strip() if len(r) > 6 else ''
        phone = clean_phone(r[9].strip() if len(r) > 9 else '')
        role = r[10].strip() if len(r) > 10 else ''

        if ('trưởng xe' in role.lower() or 'trưởng đoàn' in role.lower()) and not cap_name:
            cap_name = name
            cap_phone = phone
            cap_title = title
            cap_unit = unit

        if ('lái xe' in role.lower() or 'lái xe' in title.lower()) and not driver_name:
            driver_name = name
            driver_phone = phone

    # Fallbacks for Captain if not explicitly labeled
    if not cap_name:
        if num == 1:
            cap_name = 'Lê Thị Hoàng Yến'
            cap_title = 'Tổng Giám đốc'
            cap_unit = 'Văn phòng Tập đoàn Mường Thanh'
        elif num == 34:
            cap_name = 'Phạm Lê Khánh Duy'
            cap_title = 'Phụ trách ekip quay phim'
            cap_unit = 'Ekip Media BTC'
            cap_phone = '0972 554 172'
        elif num == 31:
            cap_name = 'Võ Thanh Hoài'
            cap_title = 'Nhân viên Hành chính - Nhân sự'
            cap_unit = 'Công ty CP Phát triển Địa ốc Cienco5'
            cap_phone = '0839 629 629'
        elif len(v_raw['rows']) > 0:
            first_r = v_raw['rows'][0]
            cap_name = first_r[3].strip() if len(first_r) > 3 else ''
            cap_title = first_r[5].strip() if len(first_r) > 5 else ''
            cap_unit = first_r[6].strip() if len(first_r) > 6 else ''
            cap_phone = clean_phone(first_r[9].strip() if len(first_r) > 9 else '')

    # License plate
    plate = KNOWN_PLATES.get(num, '')

    # Calculate BIB range for label/summary
    numeric_bibs = [int(r[2].strip()) for r in v_raw['rows'] if len(r) > 2 and r[2].strip().isdigit()]
    if numeric_bibs:
        if num == 1:
            bib_range = 'BIB 5001'
        elif num == 2:
            bib_range = '5002, 5003, 5306, 5010, 15005'
        elif num == 3:
            bib_range = 'BIB 5380 & BTC Đi Sớm'
        elif num == 32:
            bib_range = 'BIB 5018 & Tổ Y Tế'
        elif num == 33:
            bib_range = f"BIB {min(numeric_bibs)} – {max(numeric_bibs)} & BTC Chốt Đoàn"
        elif num in [30, 31]:
            bib_range = f"{len(numeric_bibs)} VĐV Tự túc"
        else:
            bib_range = f"BIB {min(numeric_bibs)} – {max(numeric_bibs)}"
    else:
        if num == 34:
            bib_range = 'Ekip Media, Quay phim & MC'
        else:
            bib_range = ''

    # Build Vehicle Object
    v_obj = {
        'id': v_id,
        'num': num,
        'code': f"XE-{num:02d}",
        'label': v_label,
        'type': v_type,
        'capacity': cap,
        'paxCount': len(v_raw['rows']),
        'paxSummary': f"{len(v_raw['rows'])} người",
        'departTime': dep_time,
        'pickupLoc': 'Sảnh Khách sạn Mường Thanh Luxury Ninh Bình',
        'destLoc': 'Sân Golf Tràng An & Resort',
        'returnTime': '11:00',
        'captain': {
            'name': cap_name,
            'title': cap_title,
            'unit': cap_unit,
            'phone': cap_phone
        },
        'driver': {
            'name': driver_name,
            'phone': driver_phone
        },
        'plate': plate,
        'bibRange': bib_range,
        'note': '',
        'isVIP': (num in [1, 2]),
        'isEarly': (num in [3, 34]),
        'isEventTeam': (num == 34),
        'isSelfTransport': (num in [30, 31]),
        'isMedical': (num == 32),
        'isCoordination': (num == 33),
        'members': [],
        'runners': [],
        'btcStaff': [],
        'drivers': []
    }

    # Second pass: process each member
    for row_idx, r in enumerate(v_raw['rows']):
        raw_stt = r[0].strip() if len(r) > 0 else str(row_idx + 1)
        raw_bib = r[2].strip() if len(r) > 2 else ''
        name = r[3].strip() if len(r) > 3 else ''
        gender = r[4].strip() if len(r) > 4 else ''
        title = r[5].strip() if len(r) > 5 else ''
        unit = r[6].strip() if len(r) > 6 else ''
        dist = r[7].strip() if len(r) > 7 else ''
        size = r[8].strip() if len(r) > 8 else ''
        phone = clean_phone(r[9].strip() if len(r) > 9 else '')
        role = r[10].strip() if len(r) > 10 else ''

        bib_val = int(raw_bib) if raw_bib.isdigit() else None
        is_btc = (raw_bib.upper() == 'BTC' or 'không chạy' in dist.lower() or 'btc' in role.lower())

        mem_obj = {
            'stt': raw_stt,
            'bib': bib_val,
            'name': name,
            'gender': gender,
            'title': title,
            'unit': unit,
            'dist': dist,
            'size': size,
            'phone': phone,
            'role': role,
            'vehicleId': v_id,
            'vehicleNum': num,
            'vehicleLabel': v_label,
            'captainName': cap_name,
            'captainPhone': cap_phone,
            'driverName': driver_name,
            'driverPhone': driver_phone,
            'plate': plate
        }
        v_obj['members'].append(mem_obj)

        if bib_val is not None:
            # Runner
            old_r = old_runners_map.get(bib_val, {})
            cat = old_r.get('category', '')
            if not cat:
                if '15' in dist: cat = f"15km {gender}"
                elif '10' in dist: cat = f"10km {gender}"
                elif '5' in dist: cat = f"5km {gender}"
                else: cat = '5km'

            runner_dist = '5km'
            if '10' in dist: runner_dist = '10km'
            elif '15' in dist: runner_dist = '15km'

            # Preserve phone & size if CSV was empty
            phone_val = phone or old_r.get('phone', '')
            size_val = size or old_r.get('size', 'M')

            is_btc_role = ('BTC' in role or 'Trưởng xe' in role or old_r.get('btc'))
            btc_badge = role if ('BTC' in role or 'Trưởng xe' in role) else (old_r.get('btc', '') if is_btc_role else '')

            runner_obj = {
                'stt': len(all_runners) + 1,
                'bib': bib_val,
                'name': name,
                'gender': gender,
                'title': title,
                'unit': unit,
                'distance': runner_dist,
                'dist': dist,
                'category': cat,
                'size': size_val,
                'phone': phone_val,
                'role': role,
                'btc': btc_badge,
                'note': '',
                'vehicleId': v_id,
                'vehicleNum': num,
                'vehicleLabel': v_label,
                'captainName': cap_name,
                'captainPhone': cap_phone,
                'captainTitle': cap_title,
                'captainUnit': cap_unit,
                'driverName': driver_name,
                'driverPhone': driver_phone,
                'plate': plate
            }
            v_obj['runners'].append(runner_obj)
            all_runners.append(runner_obj)

        elif is_btc or num == 34:
            # BTC staff or Media on Xe 34
            if ('lái xe' in role.lower() or 'lái xe' in title.lower()):
                v_obj['drivers'].append({
                    'name': name,
                    'gender': gender,
                    'title': title,
                    'phone': phone,
                    'role': role
                })
            else:
                v_obj['btcStaff'].append({
                    'name': name,
                    'gender': gender,
                    'title': title,
                    'unit': unit,
                    'phone': phone,
                    'role': role
                })
        else:
            v_obj['drivers'].append({
                'name': name,
                'gender': gender,
                'title': title,
                'phone': phone,
                'role': role
            })

    vehicles.append(v_obj)

# Sort vehicles by vehicle number
vehicles.sort(key=lambda v: v['num'])

# Sort runners by bib
all_runners.sort(key=lambda r: r['bib'])
for idx, r in enumerate(all_runners):
    r['stt'] = idx + 1

print(f"Total vehicles: {len(vehicles)}")
print(f"Total runners with numeric BIB: {len(all_runners)}")

# 4. Update data['funrun']
data['funrun']['vehicles'] = vehicles
data['funrun']['runners'] = all_runners
data['funrun']['overview']['totalRunners'] = len(all_runners)
data['funrun']['overview']['totalVehicles'] = len(vehicles)

# Recompute summary counts
c5 = [r for r in all_runners if r['distance'] == '5km']
c10 = [r for r in all_runners if r['distance'] == '10km']
c15 = [r for r in all_runners if r['distance'] == '15km']

data['funrun']['overview']['summaryCounts'] = {
    'total': len(all_runners),
    'c5k': len(c5),
    'c5k_m_lt35': sum(1 for r in c5 if r['category'] == '5km Nam dưới 35 tuổi'),
    'c5k_m_gte35': sum(1 for r in c5 if r['category'] == '5km Nam trên 35 tuổi'),
    'c5k_f_lt35': sum(1 for r in c5 if r['category'] == '5km Nữ dưới 35 tuổi'),
    'c5k_f_gte35': sum(1 for r in c5 if r['category'] == '5km Nữ trên 35 tuổi'),
    'c10k': len(c10),
    'c10k_m': sum(1 for r in c10 if r['gender'] == 'Nam'),
    'c10k_f': sum(1 for r in c10 if r['gender'] == 'Nữ'),
    'c15k': len(c15),
    'c15k_m': sum(1 for r in c15 if r['gender'] == 'Nam'),
    'c15k_f': sum(1 for r in c15 if r['gender'] == 'Nữ')
}

print("Summary counts:", data['funrun']['overview']['summaryCounts'])

# Recompute category counts
cat_counts = {}
for r in all_runners:
    cat = r['category']
    cat_counts[cat] = cat_counts.get(cat, 0) + 1

for c in data['funrun'].get('categories', []):
    c['count'] = cat_counts.get(c['name'], 0)

# 5. Cross-reference athletes with Fun Run runners
UNIT_MAP = {
    'Bệnh Viện Phủ Diễn': ['Bệnh viện Phủ Diễn'],
    'Trường Nguyễn Du': ['Trường THPT Nguyễn Du'],
    'Chung cư Thanh Hà': ['Chi nhánh DVNO Thanh Hà'],
    'Cienco5 và DHE': ['Công ty CP Phát triển Địa ốc Cienco5', 'Công ty CP Phát triển địa ốc Cienco5', 'Công ty TNHH Thang máy DHE'],
    'Cụm Chung cư Hà Nội': ['Chi nhánh DVNO Linh Đàm', 'Chung cư Mường Thanh Khánh Hòa', 'Chung cư Mường Thanh Viễn Triều'],
    'Cụm siêu thị MT Mart': ['Ban Điều hành Siêu thị Mường Thanh', 'Siêu thị Mường Thanh HH1', 'Siêu thị Mường Thanh HH2', 'Siêu thị Mường Thanh Hoàng Mai', 'Siêu thị Mường Thanh Con Cuông'],
    'Văn Phòng Tập Đoàn': ['Văn phòng Tập đoàn Mường Thanh', 'Văn Phòng Tập Đoàn Mường Thanh', 'Ban Nhân sự', 'Ban Kiểm toán nội bộ', 'Công ty TNHH ĐTTC và Vàng Mường Thanh'],
    'Mường Thanh Luxury Diễn Lâm': ['Mường Thanh Luxury Diễn Lâm', 'Mường Thanh Golf Club Diễn Lâm', 'Khu sinh thái Mường Thanh Diễn Lâm'],
}

def is_unit_match(ath_unit, run_unit):
    u_a = ath_unit.strip()
    u_r = run_unit.strip()
    if u_a.lower() == u_r.lower():
        return True
    if u_a in UNIT_MAP:
        for allowed in UNIT_MAP[u_a]:
            if u_r.lower() == allowed.lower():
                return True
    return False

runners_by_name = {}
for r in all_runners:
    k = r['name'].strip().lower()
    if k not in runners_by_name:
        runners_by_name[k] = []
    runners_by_name[k].append(r)

matched_athletes_count = 0
for a in data.get('athletes', []):
    # Strip old Chạy events
    a['monThi'] = [m for m in a['monThi'] if not m.startswith('Chạy') and 'Fun Run' not in m]
    if 'chay' in a:
        del a['chay']

    a_name = a['hoVaTen'].strip().lower()
    a_unit = a['donVi'].strip()
    a_gen = a.get('gioiTinh', '').strip().lower()

    candidates = runners_by_name.get(a_name, [])
    matched_r = None
    for r in candidates:
        r_unit = r['unit'].strip()
        r_gen = r.get('gender', '').strip().lower()
        if is_unit_match(a_unit, r_unit):
            if a_gen and r_gen and a_gen != r_gen:
                continue
            matched_r = r
            break

    if matched_r:
        matched_athletes_count += 1
        cat = matched_r['category']
        run_event = f"Chạy {cat}" if not cat.startswith('Chạy') else cat
        a['monThi'].append(run_event)
        a['chay'] = {
            'bib': matched_r['bib'],
            'dist': matched_r['dist'],
            'category': matched_r['category'],
            'runEvent': run_event,
            'vehicle': matched_r['vehicleLabel'],
            'vehicleNum': matched_r['vehicleNum'],
            'role': matched_r['role']
        }

    a['soMon'] = len(a['monThi'])

print(f"Cross-referenced {matched_athletes_count} athletes with Fun Run runners.")

# 6. Save data.json
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Saved updated data.json successfully!")
