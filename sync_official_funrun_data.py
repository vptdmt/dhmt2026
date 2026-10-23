import sys, json, csv, re

sys.stdout.reconfigure(encoding='utf-8')

def clean_phone(p):
    if not p:
        return ''
    p = str(p).strip().replace('\n', '').replace('\r', '')
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

vehicles_by_num = {v['num']: v for v in data['funrun']['vehicles']}

# 2. Read official danh_sach_dang_ky_chay.csv (434 runners)
with open('danh_sach_dang_ky_chay.csv', mode='r', encoding='utf-8') as f:
    rows = list(csv.reader(f))[1:]

all_runners = []
for idx, r in enumerate(rows):
    stt = int(r[0].strip()) if r[0].strip().isdigit() else (idx + 1)
    bib = int(r[1].strip())
    name = r[2].strip()
    title = r[3].strip()
    unit = r[4].strip()
    raw_phone = r[5].strip()
    phone = clean_phone(raw_phone)
    yob = r[6].strip()
    gender = r[7].strip()
    size = r[8].strip()
    dist_raw = r[9].strip()
    cat = r[10].strip()
    btc_role = r[11].strip()
    car_str = r[12].strip()
    note = r[13].strip() if len(r) > 13 else ''

    car_num = int(car_str) if car_str.isdigit() else None
    v_obj = vehicles_by_num.get(car_num) if car_num else None

    # Dist
    dist = '5km'
    if '10' in dist_raw or '10' in cat:
        dist = '10km'
    elif '15' in dist_raw or '15' in cat:
        dist = '15km'

    v_id = f"XE-{car_num:02d}" if car_num else ''
    v_label = v_obj['label'] if v_obj else ('Không đi xe' if not car_num else f"Xe {car_num:02d}")
    cap_name = v_obj['captain']['name'] if v_obj else ''
    cap_phone = v_obj['captain']['phone'] if v_obj else ''
    cap_title = v_obj['captain']['title'] if v_obj else ''
    cap_unit = v_obj['captain']['unit'] if v_obj else ''
    driver_name = v_obj['driver']['name'] if v_obj else ''
    driver_phone = v_obj['driver']['phone'] if v_obj else ''
    plate = v_obj.get('plate', '') if v_obj else ''

    runner_obj = {
        'stt': stt,
        'bib': bib,
        'name': name,
        'gender': gender,
        'title': title,
        'unit': unit,
        'distance': dist,
        'dist': dist_raw or f"Chạy {dist}",
        'category': cat,
        'size': size,
        'phone': phone,
        'role': 'Vận động viên',
        'btc': btc_role,
        'note': note,
        'vehicleId': v_id,
        'vehicleNum': car_num,
        'vehicleLabel': v_label,
        'captainName': cap_name,
        'captainPhone': cap_phone,
        'captainTitle': cap_title,
        'captainUnit': cap_unit,
        'driverName': driver_name,
        'driverPhone': driver_phone,
        'plate': plate
    }
    all_runners.append(runner_obj)

# 3. Re-assign runners to vehicles['runners']
for v in data['funrun']['vehicles']:
    v['runners'] = []

for r in all_runners:
    if r['vehicleNum'] and r['vehicleNum'] in vehicles_by_num:
        vehicles_by_num[r['vehicleNum']]['runners'].append(r)

# Check and update paxCount for vehicles
for v in data['funrun']['vehicles']:
    total_pax = len(v['runners']) + len(v.get('btcStaff', [])) + len(v.get('drivers', []))
    v['paxCount'] = total_pax
    v['paxSummary'] = f"{total_pax} người"
    bibs = [r['bib'] for r in v['runners']]
    if bibs:
        if v['num'] == 1:
            v['bibRange'] = 'BIB 5001'
        elif v['num'] == 2:
            v['bibRange'] = '5002, 5003, 5306, 5010, 15005'
        elif v['num'] == 3:
            v['bibRange'] = 'BIB 5380 & BTC Đi Sớm'
        elif v['num'] == 32:
            v['bibRange'] = 'BIB 5018 & Tổ Y Tế'
        elif v['num'] == 33:
            v['bibRange'] = f"BIB {min(bibs)} – {max(bibs)} & BTC Chốt Đoàn"
        elif v['num'] in [30, 31]:
            v['bibRange'] = f"{len(bibs)} VĐV Tự túc"
        else:
            v['bibRange'] = f"BIB {min(bibs)} – {max(bibs)}"
    else:
        if v['num'] == 34:
            v['bibRange'] = 'Ekip Media, Quay phim & MC'
        else:
            v['bibRange'] = ''

# 4. Overview counts
c5 = [r for r in all_runners if r['distance'] == '5km']
c10 = [r for r in all_runners if r['distance'] == '10km']
c15 = [r for r in all_runners if r['distance'] == '15km']

summary_counts = {
    'total': len(all_runners),
    'c5k': len(c5),
    'c5k_m': sum(1 for r in c5 if r['gender'] == 'Nam'),
    'c5k_f': sum(1 for r in c5 if r['gender'] == 'Nữ'),
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

data['funrun']['runners'] = all_runners
data['funrun']['overview']['totalRunners'] = len(all_runners)
data['funrun']['overview']['totalVehicles'] = len(data['funrun']['vehicles'])
data['funrun']['overview']['summaryCounts'] = summary_counts

# Update categories list in data['funrun']['categories']
cat_counts = {}
for r in all_runners:
    cat_counts[r['category']] = cat_counts.get(r['category'], 0) + 1

for c in data['funrun'].get('categories', []):
    c['count'] = cat_counts.get(c['name'], 0)

# 5. Cross-reference athletes
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
