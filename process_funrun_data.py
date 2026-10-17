import openpyxl
import json
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

def build_funrun_data():
    wb = openpyxl.load_workbook('DS VĐV & BTC CHẠY_FINAL 16.10.xlsx', data_only=True)
    s_runners = wb['Dang ky chay']
    s_btc = wb['BTC Chạy']
    s_time = wb['Timline']

    # 1. Parse all 434 runners
    raw_runners = []
    for r in s_runners.iter_rows(min_row=4, values_only=True):
        if r[1] is None:
            continue
        raw_runners.append({
            'stt': r[0],
            'bib': int(r[1]),
            'name': str(r[2] or '').strip(),
            'title': str(r[3] or '').strip(),
            'unit': str(r[4] or '').strip(),
            'phone': str(r[5] or '').strip(),
            'gender': str(r[6] or '').strip(),
            'size': str(r[7] or '').strip(),
            'distance': str(r[8] or '').strip(),
            'category': str(r[9] or '').strip(),
            'btc': str(r[10] or '').strip(),
            'note': str(r[12] or '').strip()
        })

    print(f"Total raw runners loaded: {len(raw_runners)}")

    # 2. Parse BTC Staff (39 people)
    btc_staff = []
    for r in s_btc.iter_rows(min_row=6, values_only=True):
        if r[2] is None:
            continue
        btc_staff.append({
            'stt': r[0],
            'dept': str(r[1] or '').strip(),
            'name': str(r[2] or '').strip(),
            'title': str(r[3] or '').strip(),
            'reg': str(r[4] or '').strip(),
            'duty': str(r[5] or '').strip(),
            'note': str(r[6] or '').strip(),
            'early': (r[7] == 'x'),
            'radio': str(r[8] or '').strip() if r[8] is not None else ''
        })

    print(f"Total BTC staff loaded: {len(btc_staff)}")

    # 3. Parse Timeline (17 items)
    timeline = []
    for r in s_time.iter_rows(min_row=6, values_only=True):
        if r[1] is None:
            continue
        timeline.append({
            'stt': r[0],
            'time': str(r[1] or '').strip(),
            'title': str(r[2] or '').strip(),
            'desc': str(r[3] or '').strip(),
            'dept': str(r[4] or '').strip(),
            'pax': r[5] if r[5] is not None else '',
            'location': str(r[6] or '').strip(),
            'note': str(r[7] or '').strip()
        })

    print(f"Total Timeline items: {len(timeline)}")

    # 4. Checkpoints & Stations on the Course
    stations = [
        {
            'id': 'station_0',
            'code': 'Trạm 0',
            'name': 'Khu vực Xuất phát / Về đích (Start / Finish)',
            'location': 'Quảng trường khu nhà điều hành Tràng An Golf & Resort',
            'km': 'Km 0 (Start) & Km 5 (Finish)',
            'staff': 'Vũ Minh Tuấn, Nguyễn Tuấn Long, Nguyễn Huy Nhân, Võ Thị Mai Trang, Vũ Chiến Thắng, Phạm Hà An, BS Lê Kim Vũ, Đoàn Thế Cương',
            'desc': 'Khu vực cổng hơi Start/Finish, sân khấu khai mạc & trao giải, trạm tiếp nhận VĐV về đích, trạm y tế trung tâm, bàn thư ký đối soát kết quả'
        },
        {
            'id': 'station_1',
            'code': 'Trạm 1',
            'name': 'Trạm Kiểm soát vòng chạy (Check-point)',
            'location': 'Khu nhà Homestay 5 - hồ Đồng Chương',
            'km': 'Km 1,1',
            'staff': 'Phạm Văn Nhất, Đào Minh Anh, Nguyễn Thu Mai, Nguyễn Thái Mỹ',
            'desc': 'Đóng dấu / phát vòng đeo tay kiểm soát vòng chạy: Cự ly 10km (1 vòng đeo tay - vòng 2); Cự ly 15km (2 vòng đeo tay - vòng 2, 3) trước khi về đích. Thiếu dấu không công nhận kết quả.'
        },
        {
            'id': 'station_2',
            'code': 'Trạm 2',
            'name': 'Điểm Điều hướng & Giám sát 1',
            'location': 'Khu vực Bus Stop A',
            'km': 'Km 1,8',
            'staff': 'Lê Hoàng (Phó phòng Hạ tầng CNTT)',
            'desc': 'Chốt mềm hướng dẫn runner chạy đúng tuyến rẽ, phối hợp giữ làn giao thông nội bộ'
        },
        {
            'id': 'station_3',
            'code': 'Trạm 3',
            'name': 'Điểm Điều hướng & Giám sát 2',
            'location': 'Khu vực trả khách C (đầu cung đường rừng thông)',
            'km': 'Km 2,1',
            'staff': 'Nguyễn Duy Hoạt (Giám sát CNTT)',
            'desc': 'Điều tiết giao thông, cảnh báo khúc cua khu vực hồ và đồi thông'
        },
        {
            'id': 'station_4',
            'code': 'Trạm 4',
            'name': 'Trạm Tiếp nước & Y tế số 1',
            'location': 'Trạm nghỉ ven hồ Đồng Chương (Bus stop 8)',
            'km': 'Km 2,3',
            'staff': 'Hoàng Thanh Hải (Hành chính - tiếp nước), BS Võ Thị Mai Anh (BV Phủ Diễn - Y tế)',
            'desc': 'Cung cấp nước khoáng, nước điện giải, muối khoáng; sơ cấp cứu tại chỗ, xử lý chuột rút, hạ đường huyết'
        },
        {
            'id': 'station_5',
            'code': 'Trạm 5',
            'name': 'Điểm Check-in & Chụp ảnh Media',
            'location': 'Khu vực Cửa sổ tình yêu - ven hồ',
            'km': 'Km 3,2',
            'staff': 'Tổ Media Marketing Tập đoàn (Nhiếp ảnh gia & Quay phim)',
            'desc': 'Điểm ngắm cảnh đẹp nhất cung đường hồ, ghi lại khoảnh khắc thi đấu đẹp mắt của các runner'
        },
        {
            'id': 'station_6',
            'code': 'Trạm 6',
            'name': 'Điểm Điều hướng & Giám sát 3',
            'location': 'Ngã ba rộng giữa điểm chụp ảnh D và khu V',
            'km': 'Km 3,7',
            'staff': 'Phạm Minh Hiếu (Giám sát Lập trình CSDL)',
            'desc': 'Phân luồng VĐV chạy vào đường gom tránh các xe điện nội bộ của sân golf'
        },
        {
            'id': 'station_7',
            'code': 'Trạm 7',
            'name': 'Trạm Tiếp nước & Y tế số 2',
            'location': 'Trạm nghỉ khu trượt cỏ (Bus stop VII)',
            'km': 'Km 4,1',
            'staff': 'Dương Thị Hải Anh (Giám đốc Pháp chế - tiếp nước), BS Quang Tuấn Anh (BV Phủ Diễn - Y tế)',
            'desc': 'Tiếp nước và sơ cứu khẩn cấp cho đoạn dốc trượt cỏ trước khi vào chặng nước rút về đích'
        },
        {
            'id': 'station_8',
            'code': 'Trạm 8',
            'name': 'Điểm Điều hướng & Giám sát 4',
            'location': 'Khu vực lối xuống hố tập H',
            'km': 'Km 4,6',
            'staff': 'Trần Đình Thông (Chuyên viên Quản trị CSDL)',
            'desc': 'Chốt chặn đường sang khu vực thi đấu golf chuyên nghiệp, dẫn luồng runner tiến thẳng về vạch Finish'
        }
    ]

    # 5. Vehicle Allocation Algorithm
    # Special 1: VIP Ban TGD (4 people)
    vip_bibs = [5001, 5002, 5003, 5306]

    # Special 2: Early BTC (04:30)
    early_btc_names = [
        'Vũ Minh Tuấn', 'Nguyễn Tuấn Long', 'Phạm Văn Nhất', 
        'Lê Hoàng', 'Nguyễn Huy Nhân', 'Vũ Chiến Thắng'
    ]

    # Separate runners
    runners_5k = [r for r in raw_runners if r['bib'] < 10000 and r['bib'] not in vip_bibs]
    runners_10k = [r for r in raw_runners if 10000 <= r['bib'] < 15000]
    runners_15k = [r for r in raw_runners if r['bib'] >= 15000]

    # Containers for vehicles
    vehicles = []

    # --- VEHICLE 01: XE VIP BAN TỔNG GIÁM ĐỐC ---
    vip_runners = [r for r in raw_runners if r['bib'] in vip_bibs]
    v_vip = {
        'id': 'XE-VIP',
        'code': 'VIP-TGD',
        'label': 'Xe VIP Ban Tổng Giám Đốc',
        'type': 'Xe 7 chỗ riêng',
        'capacity': 7,
        'paxCount': len(vip_runners),
        'departTime': '05:00',
        'pickupLoc': 'Sảnh Khách sạn Mường Thanh Luxury Ninh Bình',
        'destLoc': 'Sân Golf Tràng An & Resort',
        'returnTime': '11:00',
        'captain': {
            'name': 'Ban Tổng Giám đốc',
            'title': 'Lãnh đạo Tập đoàn',
            'unit': 'Văn phòng Tập đoàn Mường Thanh',
            'phone': 'Nội bộ Lãnh đạo'
        },
        'bibRange': '5001, 5002, 5003, 5306',
        'distance': '5km (Ban Lãnh đạo)',
        'note': 'Xe riêng Ban TGĐ và Phó TGĐ Tập đoàn',
        'isVIP': True,
        'runners': vip_runners
    }
    vehicles.append(v_vip)
    for r in vip_runners:
        r['vehicleId'] = v_vip['id']
        r['vehicleLabel'] = v_vip['label']
        r['captainName'] = v_vip['captain']['name']
        r['captainPhone'] = v_vip['captain']['phone']

    # --- VEHICLE 02: XE BTC ĐI SỚM (04H30) ---
    v_early = {
        'id': 'XE-00-BTC',
        'code': 'BTC-EARLY',
        'label': 'Xe #00 - Ban Tổ Chức Đi Sớm (04h30)',
        'type': 'Xe 16 chỗ',
        'capacity': 16,
        'paxCount': len(early_btc_names),
        'departTime': '04:30',
        'pickupLoc': 'Sảnh Khách sạn Mường Thanh Luxury Ninh Bình',
        'destLoc': 'Sân Golf Tràng An & Resort (Khu vực Start/Finish)',
        'returnTime': '11:00',
        'captain': {
            'name': 'Vũ Minh Tuấn',
            'title': 'Giám đốc Đào tạo & KSCL (Trưởng ban Thể thao)',
            'unit': 'Văn phòng Tập đoàn Mường Thanh',
            'phone': '0988 888 666'
        },
        'bibRange': 'Ban Tổ Chức Đi Sớm',
        'distance': 'Điều hành & Setup hiện trường',
        'note': 'Xe xuất phát sớm lúc 04h30 chở 06 cán bộ kỹ thuật, cổng hơi, âm thanh, bộ đàm và chốt trạm sớm',
        'isEarly': True,
        'members': [
            '1. Vũ Minh Tuấn - GĐ Đào tạo & KSCL (Điều phối chung & Trao giải)',
            '2. Nguyễn Tuấn Long - TP Đào tạo & KSCL (Điều phối xuất phát & về đích)',
            '3. Phạm Văn Nhất - TP Phần mềm (Kiểm soát/đóng dấu vòng chạy km 1.1)',
            '4. Lê Hoàng - PP Hạ tầng (Chốt điều hướng 1 - Bus Stop A)',
            '5. Nguyễn Huy Nhân - Giảng viên Đào tạo (Kiểm soát đích 5km Nữ)',
            '6. Vũ Chiến Thắng - GS Lập trình (Kiểm soát đích 10km & 15km)'
        ],
        'runners': []
    }
    vehicles.append(v_early)

    # --- 8 XE 45 CHỖ (XE #01 ĐẾN XE #08) - CỰ LY 5KM (342 VĐV) ---
    # Phân bổ: 43, 43, 43, 43, 43, 43, 42, 42
    bus45_sizes = [43, 43, 43, 43, 43, 43, 42, 42]
    bus45_captains = [
        {'name': 'Đỗ Thị Thanh Huyền', 'title': 'Chánh Văn phòng Tập đoàn', 'unit': 'Văn phòng Tập đoàn Mường Thanh', 'phone': '0904 478 949'},
        {'name': 'Hoàng Thị Huyền Trang', 'title': 'Giám sát Hành chính', 'unit': 'Văn phòng Tập đoàn Mường Thanh', 'phone': '0977 752 089'},
        {'name': 'Lê Thị Thu Nguyệt', 'title': 'Giám đốc Marketing & Truyền thông', 'unit': 'Văn phòng Tập đoàn Mường Thanh', 'phone': '0983 671 281'},
        {'name': 'Hoàng Văn Lâm', 'title': 'Giám đốc Nhân sự', 'unit': 'Văn phòng Tập đoàn Mường Thanh', 'phone': '0349 602 913'},
        {'name': 'Trần Đại Nghĩa', 'title': 'Trưởng phòng Kiểm toán nội bộ', 'unit': 'Văn phòng Tập đoàn Mường Thanh', 'phone': '0987 379 398'},
        {'name': 'Hoàng Thị Thanh Nhàn', 'title': 'Trưởng phòng Kế toán Ngân hàng', 'unit': 'Văn phòng Tập đoàn Mường Thanh', 'phone': '0912 974 875'},
        {'name': 'Bùi Thị Nhung', 'title': 'Phó phòng Kế toán nội bộ', 'unit': 'Văn phòng Tập đoàn Mường Thanh', 'phone': '0978 359 749'},
        {'name': 'Lê Thị Ngọc', 'title': 'Giám sát Kinh doanh', 'unit': 'Văn phòng Tập đoàn Mường Thanh', 'phone': '0898 600 222'}
    ]

    r5k_ptr = 0
    for b_idx, sz in enumerate(bus45_sizes):
        car_num = b_idx + 1
        car_id = f'XE-{car_num:02d}'
        group = runners_5k[r5k_ptr:r5k_ptr + sz]
        r5k_ptr += sz
        
        cpt = bus45_captains[b_idx]
        v_obj = {
            'id': car_id,
            'code': f'XE-{car_num:02d}',
            'label': f'Xe #{car_num:02d} (45 chỗ)',
            'type': 'Xe 45 chỗ',
            'capacity': 45,
            'paxCount': len(group),
            'departTime': '05:00',
            'pickupLoc': 'Sảnh Khách sạn Mường Thanh Luxury Ninh Bình',
            'destLoc': 'Sân Golf Tràng An & Resort',
            'returnTime': '11:00',
            'captain': cpt,
            'bibRange': f"BIB {group[0]['bib']} – {group[-1]['bib']}",
            'distance': '5km',
            'note': f"Khối VĐV 5km ({len(group)} người). Trưởng xe: {cpt['name']} ({cpt['title']})",
            'runners': group
        }
        vehicles.append(v_obj)
        for r in group:
            r['vehicleId'] = v_obj['id']
            r['vehicleLabel'] = v_obj['label']
            r['captainName'] = cpt['name']
            r['captainPhone'] = cpt['phone']

    # --- NHÓM 5KM CÒN LẠI (34 VĐV) -> 6 XE 7 CHỖ (XE #09 ĐẾN XE #14) ---
    rem_5k = runners_5k[r5k_ptr:]
    print(f"Remaining 5k runners for 7-seat cars: {len(rem_5k)}")
    sizes_7seat_5k = [6, 6, 6, 6, 5, 5]
    captains_7seat_5k = [
        {'name': 'Hoàng Roãn Cường', 'title': 'Chuyên viên Kiểm soát chi phí', 'unit': 'Văn phòng Tập đoàn Mường Thanh', 'phone': '0904 340 911'},
        {'name': 'Nguyễn Phương Hà', 'title': 'Chuyên viên Thương mại điện tử', 'unit': 'Văn phòng Tập đoàn Mường Thanh', 'phone': '0868 356 133'},
        {'name': 'Đào Minh Anh', 'title': 'Chuyên viên Dữ liệu nhân sự (BTC)', 'unit': 'Văn phòng Tập đoàn Mường Thanh', 'phone': '0366 700 935'},
        {'name': 'Nguyễn Thu Mai', 'title': 'Giám sát Chế độ chính sách (BTC)', 'unit': 'Văn phòng Tập đoàn Mường Thanh', 'phone': '0986 950 890'},
        {'name': 'Nguyễn Thái Mỹ', 'title': 'Chuyên viên Thiết kế báo cáo (BTC)', 'unit': 'Văn phòng Tập đoàn Mường Thanh', 'phone': '0973 666 015'},
        {'name': 'Đoàn Thế Cương', 'title': 'Quản lý Nghiệp vụ An ninh (BTC)', 'unit': 'Văn phòng Tập đoàn Mường Thanh', 'phone': '0913 009 091'}
    ]

    rem_ptr = 0
    for idx_7, sz in enumerate(sizes_7seat_5k):
        car_num = 9 + idx_7
        car_id = f'XE-{car_num:02d}'
        group = rem_5k[rem_ptr:rem_ptr + sz]
        rem_ptr += sz
        cpt = captains_7seat_5k[idx_7]

        v_obj = {
            'id': car_id,
            'code': f'XE-{car_num:02d}',
            'label': f'Xe #{car_num:02d} (7 chỗ)',
            'type': 'Xe 7 chỗ',
            'capacity': 7,
            'paxCount': len(group),
            'departTime': '05:00',
            'pickupLoc': 'Sảnh Khách sạn Mường Thanh Luxury Ninh Bình',
            'destLoc': 'Sân Golf Tràng An & Resort',
            'returnTime': '11:00',
            'captain': cpt,
            'bibRange': f"BIB {group[0]['bib']} – {group[-1]['bib']}",
            'distance': '5km',
            'note': f"Khối VĐV 5km ({len(group)} người). Trưởng xe: {cpt['name']} ({cpt['title']})",
            'runners': group
        }
        vehicles.append(v_obj)
        for r in group:
            r['vehicleId'] = v_obj['id']
            r['vehicleLabel'] = v_obj['label']
            r['captainName'] = cpt['name']
            r['captainPhone'] = cpt['phone']

    # --- NHÓM 10KM (32 VĐV) -> 01 XE 16 CHỖ (XE #15) + 3 XE 7 CHỖ (XE #16 - XE #18) ---
    # Xe #15: 14 VĐV 10km (BIB 10001 - 10014)
    group_10k_16 = runners_10k[:14]
    cpt_15 = {'name': 'Lưu Quốc Việt', 'title': 'Giám đốc Công nghệ thông tin', 'unit': 'Văn phòng Tập đoàn Mường Thanh', 'phone': '0948 154 816'}
    v_15 = {
        'id': 'XE-15',
        'code': 'XE-15',
        'label': 'Xe #15 (16 chỗ)',
        'type': 'Xe 16 chỗ',
        'capacity': 16,
        'paxCount': len(group_10k_16),
        'departTime': '05:00',
        'pickupLoc': 'Sảnh Khách sạn Mường Thanh Luxury Ninh Bình',
        'destLoc': 'Sân Golf Tràng An & Resort',
        'returnTime': '11:00',
        'captain': cpt_15,
        'bibRange': f"BIB {group_10k_16[0]['bib']} – {group_10k_16[-1]['bib']}",
        'distance': '10km',
        'note': f"Đội VĐV 10km ({len(group_10k_16)} người). Trưởng xe: Lưu Quốc Việt (GĐ CNTT)",
        'runners': group_10k_16
    }
    vehicles.append(v_15)
    for r in group_10k_16:
        r['vehicleId'] = v_15['id']
        r['vehicleLabel'] = v_15['label']
        r['captainName'] = cpt_15['name']
        r['captainPhone'] = cpt_15['phone']

    # Xe #16, 17, 18: mỗi xe 6 VĐV 10km
    rem_10k = runners_10k[14:]
    captains_10k_7 = [
        {'name': 'Nguyễn Quốc Anh', 'title': 'Chuyên viên Pháp chế', 'unit': 'Văn phòng Tập đoàn Mường Thanh', 'phone': '0367 390 558'},
        {'name': 'Dương Đức Giang', 'title': 'Phó phòng Kiểm toán Nội bộ', 'unit': 'Văn phòng Tập đoàn Mường Thanh', 'phone': '0966 831 976'},
        {'name': 'Nguyễn Bá Lãm', 'title': 'Giám sát Thuế và Tài sản', 'unit': 'Văn phòng Tập đoàn Mường Thanh', 'phone': '0986 670 418'}
    ]
    sizes_10k_7 = [6, 6, 6]
    ptr_10k_7 = 0
    for idx_10, sz in enumerate(sizes_10k_7):
        car_num = 16 + idx_10
        car_id = f'XE-{car_num:02d}'
        group = rem_10k[ptr_10k_7:ptr_10k_7 + sz]
        ptr_10k_7 += sz
        cpt = captains_10k_7[idx_10]
        v_obj = {
            'id': car_id,
            'code': f'XE-{car_num:02d}',
            'label': f'Xe #{car_num:02d} (7 chỗ)',
            'type': 'Xe 7 chỗ',
            'capacity': 7,
            'paxCount': len(group),
            'departTime': '05:00',
            'pickupLoc': 'Sảnh Khách sạn Mường Thanh Luxury Ninh Bình',
            'destLoc': 'Sân Golf Tràng An & Resort',
            'returnTime': '11:00',
            'captain': cpt,
            'bibRange': f"BIB {group[0]['bib']} – {group[-1]['bib']}",
            'distance': '10km',
            'note': f"Đội VĐV 10km ({len(group)} người). Trưởng xe: {cpt['name']} ({cpt['title']})",
            'runners': group
        }
        vehicles.append(v_obj)
        for r in group:
            r['vehicleId'] = v_obj['id']
            r['vehicleLabel'] = v_obj['label']
            r['captainName'] = cpt['name']
            r['captainPhone'] = cpt['phone']

    # --- NHÓM 15KM (22 VĐV) -> 4 XE 7 CHỖ (XE #19 - XE #22) ---
    sizes_15k = [6, 5, 5, 6]
    captains_15k = [
        {'name': 'Lê Thị Thanh Trà', 'title': 'Giám đốc Kinh doanh', 'unit': 'Văn phòng Tập đoàn Mường Thanh', 'phone': '0948 198 743'},
        {'name': 'Dương Thị Hải Anh', 'title': 'Giám đốc Pháp chế (BTC)', 'unit': 'Văn phòng Tập đoàn Mường Thanh', 'phone': '0989 376 751'},
        {'name': 'Hoàng Thanh Hải', 'title': 'Chuyên viên Hành chính (BTC)', 'unit': 'Văn phòng Tập đoàn Mường Thanh', 'phone': '0977 760 567'},
        {'name': 'Võ Thị Mai Trang', 'title': 'Giám sát Điều phối (BTC)', 'unit': 'Văn phòng Tập đoàn Mường Thanh', 'phone': '0986 950 890'}
    ]
    ptr_15k = 0
    for idx_15, sz in enumerate(sizes_15k):
        car_num = 19 + idx_15
        car_id = f'XE-{car_num:02d}'
        group = runners_15k[ptr_15k:ptr_15k + sz]
        ptr_15k += sz
        cpt = captains_15k[idx_15]
        v_obj = {
            'id': car_id,
            'code': f'XE-{car_num:02d}',
            'label': f'Xe #{car_num:02d} (7 chỗ)',
            'type': 'Xe 7 chỗ',
            'capacity': 7,
            'paxCount': len(group),
            'departTime': '05:00',
            'pickupLoc': 'Sảnh Khách sạn Mường Thanh Luxury Ninh Bình',
            'destLoc': 'Sân Golf Tràng An & Resort',
            'returnTime': '11:00',
            'captain': cpt,
            'bibRange': f"BIB {group[0]['bib']} – {group[-1]['bib']}",
            'distance': '15km',
            'note': f"Đội VĐV 15km ({len(group)} người). Trưởng xe: {cpt['name']} ({cpt['title']})",
            'runners': group
        }
        vehicles.append(v_obj)
        for r in group:
            r['vehicleId'] = v_obj['id']
            r['vehicleLabel'] = v_obj['label']
            r['captainName'] = cpt['name']
            r['captainPhone'] = cpt['phone']

    # --- XE #23 (7 CHỖ): TỔ Y TẾ BÁC SĨ BỆNH VIỆN PHỦ DIỄN ---
    v_23 = {
        'id': 'XE-23-YTE',
        'code': 'XE-23',
        'label': 'Xe #23 - Tổ Y Tế BV Phủ Diễn (7 chỗ)',
        'type': 'Xe 7 chỗ',
        'capacity': 7,
        'paxCount': 4,
        'departTime': '05:00',
        'pickupLoc': 'Sảnh Khách sạn Mường Thanh Luxury Ninh Bình',
        'destLoc': 'Sân Golf Tràng An & Resort',
        'returnTime': '11:00',
        'captain': {
            'name': 'BS Lê Kim Vũ',
            'title': 'Bác sỹ Bệnh viện Phủ Diễn (Trực trạm Y tế 0)',
            'unit': 'Bệnh viện Phủ Diễn',
            'phone': '0912 345 678'
        },
        'bibRange': 'Tổ Y Tế Cứu Thương',
        'distance': 'Chăm sóc y tế & Cứu thương',
        'note': 'Chở đoàn 3 Bác sĩ (BS Lê Kim Vũ, BS Võ Thị Mai Anh, BS Quang Tuấn Anh) cùng trang thiết bị sơ cứu, cáng cứu thương, túi thuốc',
        'members': [
            '1. BS Lê Kim Vũ - Trực Trạm Y tế 0 (Start / Finish)',
            '2. BS Võ Thị Mai Anh - Trực Trạm Y tế 1 (Km 2.3)',
            '3. BS Quang Tuấn Anh - Trực Trạm Y tế 2 (Km 4.1 khu trượt cỏ)'
        ],
        'runners': []
    }
    vehicles.append(v_23)

    # --- XE #24 (7 CHỖ): TỔ MEDIA, QUAY PHIM & TRUYỀN THÔNG ---
    v_24 = {
        'id': 'XE-24-MEDIA',
        'code': 'XE-24',
        'label': 'Xe #24 - Tổ Media & Truyền Thông (7 chỗ)',
        'type': 'Xe 7 chỗ',
        'capacity': 7,
        'paxCount': 6,
        'departTime': '05:00',
        'pickupLoc': 'Sảnh Khách sạn Mường Thanh Luxury Ninh Bình',
        'destLoc': 'Sân Golf Tràng An & Resort',
        'returnTime': '11:00',
        'captain': {
            'name': 'Nguyễn Huy Quỳnh',
            'title': 'Trưởng nhóm Marketing',
            'unit': 'Văn phòng Tập đoàn Mường Thanh',
            'phone': '0983 011 084'
        },
        'bibRange': 'Tổ Media & Sự Kiện',
        'distance': 'Truyền thông & Ghi hình',
        'note': 'Chở ekip truyền thông gồm 6 chuyên viên (quay phim, flycam, nhiếp ảnh gia chốt tại Cửa sổ tình yêu & vạch Finish)',
        'members': [
            '1. Nguyễn Huy Quỳnh - Trưởng nhóm Marketing',
            '2. Phạm Hoàng Hiệp - GS Quay dựng video',
            '3. Trần Hồng Hạnh - CV Truyền thông nội bộ',
            '4. Nguyễn Thị Vân Anh - CV Truyền thông nội bộ',
            '5. Võ Tuấn Dương - CV Sáng tạo nội dung',
            '6. Vũ Thị Hoàng Nhung - CV Nội dung Marketing'
        ],
        'runners': []
    }
    vehicles.append(v_24)

    # Verify all 434 runners have vehicle assigned
    unassigned = [r for r in raw_runners if 'vehicleId' not in r]
    print(f"Total vehicles generated: {len(vehicles)}")
    print(f"Unassigned runners: {len(unassigned)}")

    # 6. Assemble complete funrun data object
    funrun_data = {
        'overview': {
            'title': 'Giải chạy Mường Thanh Fun Run - Đại hội 2026',
            'date': '2026-10-28',
            'dateDisplay': 'Thứ Tư, 28/10/2026',
            'timeDisplay': '04:30 – 11:45',
            'location': 'Tràng An Golf & Resort (Quanh hồ Đồng Chương)',
            'distanceKm': 32,
            'lapDistance': '5 km / vòng',
            'totalRunners': len(raw_runners),
            'categoriesCount': 8,
            'summaryCounts': {
                'total': len(raw_runners),
                'c5k': len([r for r in raw_runners if r['bib'] < 10000]),
                'c5k_m_lt35': len([r for r in raw_runners if r['category'] == '5km Nam dưới 35 tuổi']),
                'c5k_m_gte35': len([r for r in raw_runners if r['category'] == '5km Nam trên 35 tuổi']),
                'c5k_f_lt35': len([r for r in raw_runners if r['category'] == '5km Nữ dưới 35 tuổi']),
                'c5k_f_gte35': len([r for r in raw_runners if r['category'] == '5km Nữ trên 35 tuổi']),
                'c10k': len(runners_10k),
                'c10k_m': len([r for r in runners_10k if r['gender'] == 'Nam']),
                'c10k_f': len([r for r in runners_10k if r['gender'] == 'Nữ']),
                'c15k': len(runners_15k),
                'c15k_m': len([r for r in runners_15k if r['gender'] == 'Nam']),
                'c15k_f': len([r for r in runners_15k if r['gender'] == 'Nữ'])
            }
        },
        'categories': [
            {'name': '5km Nam dưới 35 tuổi', 'distance': '5km', 'gender': 'Nam', 'age': 'Dưới 35', 'count': 82, 'bibColor': '#16a34a', 'badgeBg': '#dcfce7', 'badgeText': '#15803d', 'bibSample': '5186 (Xanh lá)'},
            {'name': '5km Nam trên 35 tuổi', 'distance': '5km', 'gender': 'Nam', 'age': 'Từ 35 trở lên', 'count': 92, 'bibColor': '#ca8a04', 'badgeBg': '#fef9c3', 'badgeText': '#854d0e', 'bibSample': '5008 (Vàng chanh)'},
            {'name': '5km Nữ dưới 35 tuổi', 'distance': '5km', 'gender': 'Nữ', 'age': 'Dưới 35', 'count': 102, 'bibColor': '#0284c7', 'badgeBg': '#e0f2fe', 'badgeText': '#0369a1', 'bibSample': '5050 (Xanh dương)'},
            {'name': '5km Nữ trên 35 tuổi', 'distance': '5km', 'gender': 'Nữ', 'age': 'Từ 35 trở lên', 'count': 104, 'bibColor': '#db2777', 'badgeBg': '#fce7f3', 'badgeText': '#9d174d', 'bibSample': '5005 (Hồng cánh sen)'},
            {'name': '10km Nam', 'distance': '10km', 'gender': 'Nam', 'age': 'Chung', 'count': 24, 'bibColor': '#ea580c', 'badgeBg': '#ffedd5', 'badgeText': '#9a3412', 'bibSample': '10001 (Cam đậm)'},
            {'name': '10km Nữ', 'distance': '10km', 'gender': 'Nữ', 'age': 'Chung', 'count': 8, 'bibColor': '#d97706', 'badgeBg': '#fef3c7', 'badgeText': '#92400e', 'bibSample': '10003 (Vàng cam)'},
            {'name': '15km Nam', 'distance': '15km', 'gender': 'Nam', 'age': 'Chung', 'count': 15, 'bibColor': '#1e3a8a', 'badgeBg': '#dbeafe', 'badgeText': '#1e40af', 'bibSample': '15001 (Xanh navy)'},
            {'name': '15km Nữ', 'distance': '15km', 'gender': 'Nữ', 'age': 'Chung', 'count': 7, 'bibColor': '#4338ca', 'badgeBg': '#e0e7ff', 'badgeText': '#3730a3', 'bibSample': '15002 (Tím chàm)'}
        ],
        'distances': [
            {'distance': '5km', 'laps': 1, 'cutoffMinutes': 75, 'startTime': '06:40 (Nam) / 06:45 (Nữ)', 'checkpoints': '0 (Chạy 1 vòng về đích)', 'desc': '1 vòng hồ Đồng Chương - thời gian tối đa 75 phút'},
            {'distance': '10km', 'laps': 2, 'cutoffMinutes': 120, 'startTime': '06:35', 'checkpoints': '1 vòng đeo tay xác nhận (Trạm homestay 5 km 1.1)', 'desc': '2 vòng hồ Đồng Chương - thời gian tối đa 120 phút'},
            {'distance': '15km', 'laps': 3, 'cutoffMinutes': 150, 'startTime': '06:30', 'checkpoints': '2 vòng đeo tay xác nhận (Trạm homestay 5 km 1.1)', 'desc': '3 vòng hồ Đồng Chương - thời gian tối đa 150 phút'}
        ],
        'timeline': timeline,
        'stations': stations,
        'btcStaff': btc_staff,
        'vehicles': vehicles,
        'runners': raw_runners
    }

    # Load existing data.json and embed funrun
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    data['funrun'] = funrun_data

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Successfully saved funrun data into data.json! File size: {len(json.dumps(data)):,} bytes")

if __name__ == '__main__':
    build_funrun_data()
