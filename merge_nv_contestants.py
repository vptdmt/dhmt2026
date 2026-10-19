import openpyxl
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def norm_cat(cat):
    c = str(cat or '').strip()
    if 'An ninh' in c or 'Kỹ thuật' in c or 'Công nghệ Thông tin' in c or 'AN-KT' in c:
        return 'AN-KT-IT'
    elif 'Bếp' in c:
        return 'Bếp'
    elif 'Buồng' in c:
        return 'Buồng'
    elif 'Dịch vụ Ẩm thực' in c:
        return 'Dịch vụ Ẩm thực'
    elif 'Kế toán' in c or 'Nhân sự' in c:
        return 'Kế toán - Nhân sự'
    elif 'Kinh doanh' in c or 'Lễ tân' in c or 'Marketing' in c:
        return 'Kinh doanh – Lễ tân – Marketing'
    return c

def merge_nv():
    # 1. Load data.json
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Backup original athletes if not already backed up
    athletes = data.get('athletes', [])
    print(f"Current athletes count in data.json: {len(athletes)}")

    # 2. Load DS thi sinh thi Nghiep vu.xlsx
    wb = openpyxl.load_workbook('DS thi sinh thi Nghiep vu.xlsx', data_only=True)
    ws = wb['DS thi sinh']

    nv_rows = []
    for r in list(ws.iter_rows(values_only=True))[4:]:
        if r[0] is None:
            continue
        stt = r[0]
        ma_dv = str(r[1] or '').strip()
        don_vi = str(r[2] or '').strip()
        ho_ten = str(r[3] or '').strip()
        gioi_tinh = str(r[4] or '').strip()
        ma_nv = str(r[5] or '').strip()
        chuc_danh = str(r[6] or '').strip()
        noi_dung = norm_cat(r[7])
        sdt = str(r[8] or '').strip()
        if sdt and sdt.isdigit() and len(sdt) == 9:
            sdt = '0' + sdt
        nv_rows.append({
            'stt': stt,
            'maDv': ma_dv,
            'donVi': don_vi,
            'hoVaTen': ho_ten,
            'gioiTinh': gioi_tinh,
            'maNv': ma_nv,
            'chucDanh': chuc_danh,
            'noiDung': noi_dung,
            'sdt': sdt
        })

    print(f"Loaded {len(nv_rows)} contestants from DS thi sinh thi Nghiep vu.xlsx")

    # 3. Index existing athletes by normalized (name, unit)
    ath_map = {}
    for a in athletes:
        key = (a['hoVaTen'].strip().lower(), a['donVi'].strip().lower())
        ath_map[key] = a

    matched_count = 0
    added_count = 0

    # Also keep track of teams list for team code display
    teams = data.get('teams', [])

    for nv in nv_rows:
        key = (nv['hoVaTen'].strip().lower(), nv['donVi'].strip().lower())
        
        # Team code for professional competition
        nv_team_code = f"NV.{nv['maDv']} ({nv['noiDung']})"

        if key in ath_map:
            # Exists as sports athlete -> update
            a = ath_map[key]
            if nv['noiDung'] not in a['monThi']:
                a['monThi'].append(nv['noiDung'])
                a['soMon'] = len(a['monThi'])
            a['chucDanh'] = nv['chucDanh']
            a['maNv'] = nv['maNv']
            a['sdt'] = nv['sdt']
            matched_count += 1
            print(f"  [MATCHED] {a['hoVaTen']} ({a['donVi']}) -> Mon: {a['monThi']}")
        else:
            # New contestant -> append
            new_ath = {
                'stt': len(athletes) + 1,
                'donVi': nv['donVi'],
                'hoVaTen': nv['hoVaTen'],
                'gioiTinh': nv['gioiTinh'],
                'chucDanh': nv['chucDanh'],
                'maNv': nv['maNv'],
                'sdt': nv['sdt'],
                'monThi': [nv['noiDung']],
                'soMon': 1
            }
            athletes.append(new_ath)
            ath_map[key] = new_ath
            added_count += 1

        # Add team entry if not present
        if not any(t.get('hoVaTen', '').strip().lower() == nv['hoVaTen'].strip().lower() and t.get('maDoi') == nv_team_code for t in teams):
            teams.append({
                'mon': 'Thi nghiệp vụ',
                'maMon': 'NV',
                'hoVaTen': nv['hoVaTen'],
                'donVi': nv['donVi'],
                'chucDanh': nv['chucDanh'],
                'maDoi': nv_team_code
            })

    print(f"\nSummary:")
    print(f"- Matched & merged into existing athletes: {matched_count} người")
    print(f"- Added as new contestants: {added_count} người")
    print(f"- Total athletes & contestants: {len(athletes)} người")

    # 4. Save back to data.json
    data['athletes'] = athletes
    data['teams'] = teams

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Successfully updated data.json!")

if __name__ == '__main__':
    merge_nv()
