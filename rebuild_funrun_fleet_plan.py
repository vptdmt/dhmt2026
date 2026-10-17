import openpyxl
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def rebuild_funrun():
    wb = openpyxl.load_workbook('DS VĐV & BTC CHẠY_FINAL 16.10.xlsx', data_only=True)
    s_runners = wb['Dang ky chay']
    s_btc = wb['BTC Chạy']
    s_time = wb['Timline']

    # 1. Load all runners
    runners_dict = {}
    for r in s_runners.iter_rows(min_row=4, values_only=True):
        if r[1] is None:
            continue
        bib = int(r[1])
        runners_dict[bib] = {
            'stt': r[0],
            'bib': bib,
            'name': str(r[2] or '').strip(),
            'title': str(r[3] or '').strip(),
            'unit': str(r[4] or '').strip(),
            'phone': str(r[5] or '').strip(),
            'gender': str(r[6] or '').strip(),
            'size': str(r[7] or '').strip(),
            'dist': str(r[8] or '').strip(),
            'category': str(r[9] or '').strip(),
            'btc': str(r[10] or '').strip(),
            'note': str(r[12] or '').strip()
        }

    print(f"Total raw runners: {len(runners_dict)}")

    # 2. Categorize special groups
    # Self-transport: Cienco5 (11), DHE (4), Siêu thị (13, except 15004 Ms. Thơ)
    self_cienco_dhe_bibs = [
        5034, 5193, 5195, 5196, 5197, 5198, 5199, 5208, 5231, 5289, 5340, 5341, 10017, 15003, 15008
    ]
    self_sieuthi_bibs = [
        5040, 5049, 5060, 5074, 5100, 5131, 5136, 5311, 5336, 5374, 10005, 10018, 10032
    ]
    # Ms. Thơ 15004 runs 15km and rides BTC bus!

    tgd_bib = [5001]
    pho_tgd_runner_bibs = [5002, 5003, 5306, 5010, 15005] # 3 Phó Tổng + Thu Nguyệt + Thanh Trà
    coord_team_bibs = [5004, 5005, 10001] # Thanh Huyền, Huyền Trang, Quốc Việt

    special_bibs = set(self_cienco_dhe_bibs + self_sieuthi_bibs + tgd_bib + pho_tgd_runner_bibs + coord_team_bibs)

    # Regular runners by distance
    regular_5k = [runners_dict[b] for b in sorted(runners_dict.keys()) if b < 10000 and b not in special_bibs]
    regular_10k = [runners_dict[b] for b in sorted(runners_dict.keys()) if 10000 <= b < 15000 and b not in special_bibs]
    regular_15k = [runners_dict[b] for b in sorted(runners_dict.keys()) if b >= 15000 and b not in special_bibs]

    print(f"Regular 5k: {len(regular_5k)}, 10k: {len(regular_10k)}, 15k: {len(regular_15k)}")

    vehicles = []

    # =========================================================================
    # 1. XE VIP 01 - TỔNG GIÁM ĐỐC (XE RIÊNG)
    # =========================================================================
    r_tgd = [runners_dict[5001]]
    v_tgd = {
        'id': 'XE-VIP-01',
        'code': 'VIP-TGD',
        'label': 'Xe VIP 01 - Tổng Giám Đốc',
        'type': 'Xe riêng TGĐ',
        'capacity': 4,
        'paxCount': len(r_tgd),
        'departTime': '05:00',
        'pickupLoc': 'Sảnh Khách sạn Mường Thanh Luxury Ninh Bình',
        'destLoc': 'Sân Golf Tràng An & Resort',
        'returnTime': '11:00',
        'captain': {
            'name': 'Lê Thị Hoàng Yến',
            'title': 'Tổng Giám đốc Tập đoàn (Trưởng BTC)',
            'unit': 'Văn phòng Tập đoàn Mường Thanh',
            'phone': 'Nội bộ Lãnh đạo'
        },
        'bibRange': 'BIB 5001',
        'distance': '5km (Ban Lãnh đạo)',
        'note': 'Xe riêng phục vụ Tổng Giám đốc Tập đoàn Mường Thanh',
        'isVIP': True,
        'runners': r_tgd,
        'btcStaff': []
    }
    vehicles.append(v_tgd)
    for r in r_tgd:
        r['vehicleId'] = v_tgd['id']
        r['vehicleLabel'] = v_tgd['label']
        r['captainName'] = v_tgd['captain']['name']
        r['captainPhone'] = v_tgd['captain']['phone']

    # =========================================================================
    # 2. XE VIP 02 - BAN PHÓ TỔNG & LÃNH ĐẠO CẤP CAO (XE 7 CHỖ)
    # Ghép: 3 Phó Tổng + Lê Thị Thu Nguyệt, Lê Thị Thanh Trà, Tạ Diệp Anh
    # =========================================================================
    r_pho_tgd = [runners_dict[b] for b in pho_tgd_runner_bibs]
    v_pho_tgd = {
        'id': 'XE-VIP-02',
        'code': 'VIP-PHO-TGD',
        'label': 'Xe VIP 02 - Ban Phó Tổng & Lãnh Đạo Cấp Cao (7 chỗ)',
        'type': 'Xe 7 chỗ',
        'capacity': 7,
        'paxCount': 6, # 5 runners + 1 BTC non-runner
        'departTime': '05:00',
        'pickupLoc': 'Sảnh Khách sạn Mường Thanh Luxury Ninh Bình',
        'destLoc': 'Sân Golf Tràng An & Resort',
        'returnTime': '11:00',
        'captain': {
            'name': 'Nguyễn Thanh Tuấn',
            'title': 'Phó Tổng Giám đốc thường trực',
            'unit': 'Văn phòng Tập đoàn Mường Thanh',
            'phone': '0913 029 376'
        },
        'bibRange': '5002, 5003, 5306, 5010, 15005',
        'distance': 'Lãnh đạo cấp cao (5km & 15km)',
        'note': 'Xe 7 chỗ bố trí riêng cho 3 Phó Tổng Giám đốc ghép cùng Ms. Thu Nguyệt (MKT), Ms. Thanh Trà (KD), Ms. Tạ Diệp Anh (TC)',
        'isVIP': True,
        'runners': r_pho_tgd,
        'btcStaff': [
            {
                'name': 'Tạ Diệp Anh',
                'title': 'Giám đốc Tài chính',
                'dept': 'Tài chính - VPTD',
                'duty': 'Điều phối chung & Trao giải (BTC)',
                'phone': 'Ban Lãnh đạo'
            }
        ]
    }
    vehicles.append(v_pho_tgd)
    for r in r_pho_tgd:
        r['vehicleId'] = v_pho_tgd['id']
        r['vehicleLabel'] = v_pho_tgd['label']
        r['captainName'] = v_pho_tgd['captain']['name']
        r['captainPhone'] = v_pho_tgd['captain']['phone']

    # =========================================================================
    # 3. XE #00 - BAN TỔ CHỨC ĐI SỚM (04H30) (XE 16 CHỖ)
    # =========================================================================
    v_early = {
        'id': 'XE-00-BTC',
        'code': 'BTC-EARLY',
        'label': 'Xe #00 - Ban Tổ Chức Đi Sớm (04h30)',
        'type': 'Xe 16 chỗ',
        'capacity': 16,
        'paxCount': 6,
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
        'bibRange': 'BTC Đi Sớm',
        'distance': 'Điều hành & Setup hiện trường',
        'note': 'Xuất phát sớm 04h30 chở cán bộ kỹ thuật, cổng hơi, âm thanh, bộ đàm và chốt trạm sớm',
        'isEarly': True,
        'runners': [],
        'btcStaff': [
            {'name': 'Vũ Minh Tuấn', 'title': 'GĐ Đào tạo & KSCL', 'duty': 'Điều phối chung & Trao giải', 'dept': 'Đào tạo'},
            {'name': 'Nguyễn Tuấn Long', 'title': 'TP Đào tạo & KSCL', 'duty': 'Điều phối xuất phát & về đích', 'dept': 'Đào tạo'},
            {'name': 'Phạm Văn Nhất', 'title': 'TP Phần mềm', 'duty': 'Kiểm soát/đóng dấu vòng chạy km 1.1', 'dept': 'CNTT'},
            {'name': 'Lê Hoàng', 'title': 'PP Hạ tầng CNTT', 'duty': 'Chốt điều hướng 1 - Bus Stop A', 'dept': 'CNTT'},
            {'name': 'Nguyễn Huy Nhân', 'title': 'Giảng viên Đào tạo', 'duty': 'Kiểm soát đích 5km Nữ', 'dept': 'Đào tạo'},
            {'name': 'Vũ Chiến Thắng', 'title': 'GS Lập trình', 'duty': 'Kiểm soát đích 10km & 15km', 'dept': 'CNTT'}
        ]
    }
    vehicles.append(v_early)

    # =========================================================================
    # 4. XE CHỐT ĐOÀN - TEAM ĐIỀU PHỐI XE (XE 7 CHỖ)
    # Lưu Quốc Việt, Đỗ Thị Thanh Huyền, Hoàng Thị Huyền Trang (di chuyển cuối cùng)
    # =========================================================================
    r_coord = [runners_dict[b] for b in coord_team_bibs]
    v_coord = {
        'id': 'XE-CHOT-DOAN',
        'code': 'XE-CHOT',
        'label': 'Xe Chốt Đoàn - Team Điều Phối Xe Di Chuyển (7 chỗ)',
        'type': 'Xe 7 chỗ',
        'capacity': 7,
        'paxCount': len(r_coord),
        'departTime': '05:15 (Xuất phát cuối cùng)',
        'pickupLoc': 'Sảnh Khách sạn Mường Thanh Luxury Ninh Bình',
        'destLoc': 'Sân Golf Tràng An & Resort',
        'returnTime': '11:00',
        'captain': {
            'name': 'Lưu Quốc Việt',
            'title': 'Giám đốc CNTT (Trưởng Team Điều phối xe)',
            'unit': 'Văn phòng Tập đoàn Mường Thanh',
            'phone': '0948 154 816'
        },
        'bibRange': 'BIB 5004, 5005, 10001',
        'distance': 'Điều phối xe & Chốt đoàn',
        'note': 'Team điều phối xe ở lại sảnh KS điều phối đoàn lên xe, soát quân số và di chuyển khóa đuôi cuối cùng lúc 05:15',
        'isCoordination': True,
        'runners': r_coord,
        'btcStaff': []
    }
    vehicles.append(v_coord)
    for r in r_coord:
        r['vehicleId'] = v_coord['id']
        r['vehicleLabel'] = v_coord['label']
        r['captainName'] = v_coord['captain']['name']
        r['captainPhone'] = v_coord['captain']['phone']

    # =========================================================================
    # 5. ĐOÀN TỰ DI CHUYỂN: KHỐI SIÊU THỊ MƯỜNG THANH (13 VĐV)
    # =========================================================================
    r_sieuthi = [runners_dict[b] for b in self_sieuthi_bibs]
    v_sieuthi = {
        'id': 'XE-TU-DI-01',
        'code': 'TUDI-SIEUTHI',
        'label': 'Xe Đơn Vị - Khối Siêu Thị Mường Thanh (Tự di chuyển)',
        'type': 'Xe riêng đơn vị',
        'capacity': len(r_sieuthi),
        'paxCount': len(r_sieuthi),
        'departTime': 'Tự túc phương tiện',
        'pickupLoc': 'Theo kế hoạch của Khối Siêu Thị',
        'destLoc': 'Sân Golf Tràng An & Resort',
        'returnTime': 'Tự túc phương tiện',
        'captain': {
            'name': 'Vũ Trọng Hà / Nguyễn Văn Tùng',
            'title': 'Giám đốc Siêu thị HH1 & Giám đốc Siêu thị Hoàng Mai',
            'unit': 'Hệ thống Siêu thị Mường Thanh',
            'phone': 'Nội bộ Siêu thị'
        },
        'bibRange': '13 VĐV Khối Siêu Thị',
        'distance': 'Khối Siêu thị (5km & 10km)',
        'note': 'Đoàn Siêu thị chủ động phương tiện tự di chuyển (Trừ Ms. Lê Thị Thơ 15004 chạy 15km đi xe BTC theo yêu cầu)',
        'isSelfTransport': True,
        'runners': r_sieuthi,
        'btcStaff': []
    }
    vehicles.append(v_sieuthi)
    for r in r_sieuthi:
        r['vehicleId'] = v_sieuthi['id']
        r['vehicleLabel'] = v_sieuthi['label']
        r['captainName'] = v_sieuthi['captain']['name']
        r['captainPhone'] = v_sieuthi['captain']['phone']

    # =========================================================================
    # 6. ĐOÀN TỰ DI CHUYỂN: CIENCO5 & THANG MÁY DHE (15 VĐV)
    # =========================================================================
    r_cienco_dhe = [runners_dict[b] for b in self_cienco_dhe_bibs]
    v_cienco_dhe = {
        'id': 'XE-TU-DI-02',
        'code': 'TUDI-CIENCO-DHE',
        'label': 'Xe Đơn Vị - Công ty Cienco5 & Thang máy DHE (Tự di chuyển)',
        'type': 'Xe riêng đơn vị',
        'capacity': len(r_cienco_dhe),
        'paxCount': len(r_cienco_dhe),
        'departTime': 'Tự túc phương tiện',
        'pickupLoc': 'Theo kế hoạch của Công ty Cienco5 & DHE',
        'destLoc': 'Sân Golf Tràng An & Resort',
        'returnTime': 'Tự túc phương tiện',
        'captain': {
            'name': 'Phạm Thị Hương (Cienco5) & Trần Xuân Dương (DHE)',
            'title': 'Lãnh đạo đoàn Cienco5 & DHE',
            'unit': 'Cienco5 & Thang máy DHE',
            'phone': 'Nội bộ đơn vị'
        },
        'bibRange': '15 VĐV Cienco5 & DHE',
        'distance': 'Khối Cienco5 & DHE (5km, 10km, 15km)',
        'note': 'Đoàn Cienco5 (11 VĐV) và Thang máy DHE (4 VĐV) chủ động bố trí xe riêng tự di chuyển đến giải chạy',
        'isSelfTransport': True,
        'runners': r_cienco_dhe,
        'btcStaff': []
    }
    vehicles.append(v_cienco_dhe)
    for r in r_cienco_dhe:
        r['vehicleId'] = v_cienco_dhe['id']
        r['vehicleLabel'] = v_cienco_dhe['label']
        r['captainName'] = v_cienco_dhe['captain']['name']
        r['captainPhone'] = v_cienco_dhe['captain']['phone']

    # =========================================================================
    # 7. 8 XE 45 CHỖ (XE #01 ĐẾN XE #08) - CỰ LY 5KM (351 VĐV)
    # Trưởng xe: Lấy đúng 8 người đầu tiên từ danh sách ưu tiên BTC của User!
    # =========================================================================
    priority_btc_captains = [
        {'name': 'Hoàng Thanh Hải', 'title': 'Chuyên viên Hành chính (BTC Tiếp nước)', 'dept': 'Hành chính - VPTD', 'phone': '0977 760 567', 'duty': 'Trạm tiếp nước số 1 (Km 2.3)'},
        {'name': 'Dương Thị Hải Anh', 'title': 'Giám đốc Pháp chế (BTC Tiếp nước)', 'dept': 'Pháp chế - VPTD', 'phone': '0989 376 751', 'duty': 'Trạm tiếp nước số 2 (Km 4.1)'},
        {'name': 'Nguyễn Thu Mai', 'title': 'Giám sát Chế độ chính sách (BTC Kiểm soát)', 'dept': 'Nhân sự - VPTD', 'phone': '0986 950 890', 'duty': 'Trạm kiểm soát vòng chạy (Km 1.1)'},
        {'name': 'Nguyễn Thái Mỹ', 'title': 'Chuyên viên Thiết kế báo cáo (BTC Kiểm soát)', 'dept': 'CNTT - VPTD', 'phone': '0973 666 015', 'duty': 'Trạm kiểm soát vòng chạy (Km 1.1)'},
        {'name': 'Nguyễn Duy Hoạt', 'title': 'Giám sát CNTT (BTC Điều hướng)', 'dept': 'CNTT - VPTD', 'phone': '0913 009 091', 'duty': 'Điều hướng 2 (Trả khách C)'},
        {'name': 'Phạm Minh Hiếu', 'title': 'Giám sát Lập trình CSDL (BTC Điều hướng)', 'dept': 'CNTT - VPTD', 'phone': '0983 011 084', 'duty': 'Điều hướng 3 (Ngã ba rộng)'},
        {'name': 'Trần Đình Thông', 'title': 'Chuyên viên Quản trị CSDL (BTC Điều hướng)', 'dept': 'CNTT - VPTD', 'phone': '0904 598 678', 'duty': 'Điều hướng 4 (Lối hố tập H)'},
        {'name': 'Võ Thị Mai Trang', 'title': 'Giám sát Điều phối (BTC Kiểm soát đích)', 'dept': 'Đào tạo & KSCL - VPTD', 'phone': '0978 359 749', 'duty': 'Kiểm soát về đích 5km Nam'}
    ]

    # Chia 351 VĐV 5km vào 8 xe: 44, 44, 44, 44, 44, 44, 44, 43
    sizes_5k = [44, 44, 44, 44, 44, 44, 44, 43]
    ptr_5k = 0

    for i, sz in enumerate(sizes_5k):
        car_num = i + 1
        car_id = f'XE-{car_num:02d}'
        group = regular_5k[ptr_5k:ptr_5k + sz]
        ptr_5k += sz

        cpt = priority_btc_captains[i]

        v_obj = {
            'id': car_id,
            'code': f'XE-{car_num:02d}',
            'label': f'Xe #{car_num:02d} (45 chỗ)',
            'type': 'Xe 45 chỗ',
            'capacity': 45,
            'paxCount': len(group) + 1, # group runners + 1 BTC captain on board
            'departTime': '05:00',
            'pickupLoc': 'Sảnh Khách sạn Mường Thanh Luxury Ninh Bình',
            'destLoc': 'Sân Golf Tràng An & Resort',
            'returnTime': '11:00',
            'captain': {
                'name': cpt['name'],
                'title': cpt['title'],
                'unit': cpt['dept'],
                'phone': cpt['phone']
            },
            'bibRange': f"BIB {group[0]['bib']} – {group[-1]['bib']}",
            'distance': '5km',
            'note': f"Khối VĐV 5km ({len(group)} VĐV + Trưởng xe BTC {cpt['name']} đi cùng xe). Nhiệm vụ BTC: {cpt['duty']}",
            'runners': group,
            'btcStaff': [
                {
                    'name': cpt['name'],
                    'title': cpt['title'],
                    'dept': cpt['dept'],
                    'duty': f"Trưởng xe #{car_num:02d} & {cpt['duty']}",
                    'phone': cpt['phone'],
                    'isCaptain': True
                }
            ]
        }
        vehicles.append(v_obj)
        for r in group:
            r['vehicleId'] = v_obj['id']
            r['vehicleLabel'] = v_obj['label']
            r['captainName'] = cpt['name']
            r['captainPhone'] = cpt['phone']

    print(f"Allocated 8 xe 45 cho. Total runners in 8 buses: {ptr_5k}")

    # =========================================================================
    # 8. CỰ LY 10KM (27 VĐV) -> XE #09 (16 CHỖ) + XE #10 (7 CHỖ) + XE #11 (7 CHỖ)
    # Người thứ 9 & 10 trong DS ưu tiên BTC: Phạm Hà An, Đoàn Thế Cương!
    # Xe #11: Lấy VĐV Văn phòng Tập đoàn trên xe: Nguyễn Bá Lãm (BIB 10026)!
    # =========================================================================
    # Xe #09: 15 VĐV 10km (10002 -> 10016) + Trưởng xe Phạm Hà An
    group_10k_15 = regular_10k[:15]
    cpt_09 = {
        'name': 'Phạm Hà An',
        'title': 'Giám sát Chế độ chính sách (BTC Thư ký kết quả)',
        'dept': 'Nhân sự - VPTD',
        'phone': '0986 950 890',
        'duty': 'Thư ký tổng hợp kết quả & xác nhận Finisher'
    }
    v_09 = {
        'id': 'XE-09',
        'code': 'XE-09',
        'label': 'Xe #09 (16 chỗ)',
        'type': 'Xe 16 chỗ',
        'capacity': 16,
        'paxCount': len(group_10k_15) + 1,
        'departTime': '05:00',
        'pickupLoc': 'Sảnh Khách sạn Mường Thanh Luxury Ninh Bình',
        'destLoc': 'Sân Golf Tràng An & Resort',
        'returnTime': '11:00',
        'captain': {
            'name': cpt_09['name'],
            'title': cpt_09['title'],
            'unit': cpt_09['dept'],
            'phone': cpt_09['phone']
        },
        'bibRange': f"BIB {group_10k_15[0]['bib']} – {group_10k_15[-1]['bib']}",
        'distance': '10km',
        'note': f"Đội VĐV 10km ({len(group_10k_15)} VĐV + Trưởng xe BTC Phạm Hà An đi cùng xe).",
        'runners': group_10k_15,
        'btcStaff': [
            {
                'name': cpt_09['name'],
                'title': cpt_09['title'],
                'dept': cpt_09['dept'],
                'duty': 'Trưởng xe #09 & Thư ký tổng hợp kết quả Finisher',
                'phone': cpt_09['phone'],
                'isCaptain': True
            }
        ]
    }
    vehicles.append(v_09)
    for r in group_10k_15:
        r['vehicleId'] = v_09['id']
        r['vehicleLabel'] = v_09['label']
        r['captainName'] = cpt_09['name']
        r['captainPhone'] = cpt_09['phone']

    # Xe #10: 6 VĐV 10km (10019 -> 10025) + Trưởng xe Đoàn Thế Cương
    group_10k_6a = regular_10k[15:21]
    cpt_10 = {
        'name': 'Đoàn Thế Cương',
        'title': 'Quản lý Nghiệp vụ An ninh (BTC An ninh)',
        'dept': 'Operation - VPTD',
        'phone': '0913 009 091',
        'duty': 'Quản lý an ninh chung & hỗ trợ thu gom VĐV'
    }
    v_10 = {
        'id': 'XE-10',
        'code': 'XE-10',
        'label': 'Xe #10 (7 chỗ)',
        'type': 'Xe 7 chỗ',
        'capacity': 7,
        'paxCount': len(group_10k_6a) + 1,
        'departTime': '05:00',
        'pickupLoc': 'Sảnh Khách sạn Mường Thanh Luxury Ninh Bình',
        'destLoc': 'Sân Golf Tràng An & Resort',
        'returnTime': '11:00',
        'captain': {
            'name': cpt_10['name'],
            'title': cpt_10['title'],
            'unit': cpt_10['dept'],
            'phone': cpt_10['phone']
        },
        'bibRange': f"BIB {group_10k_6a[0]['bib']} – {group_10k_6a[-1]['bib']}",
        'distance': '10km',
        'note': f"Đội VĐV 10km ({len(group_10k_6a)} VĐV + Trưởng xe BTC Đoàn Thế Cương đi cùng xe).",
        'runners': group_10k_6a,
        'btcStaff': [
            {
                'name': cpt_10['name'],
                'title': cpt_10['title'],
                'dept': cpt_10['dept'],
                'duty': 'Trưởng xe #10 & Quản lý an ninh chung',
                'phone': cpt_10['phone'],
                'isCaptain': True
            }
        ]
    }
    vehicles.append(v_10)
    for r in group_10k_6a:
        r['vehicleId'] = v_10['id']
        r['vehicleLabel'] = v_10['label']
        r['captainName'] = cpt_10['name']
        r['captainPhone'] = cpt_10['phone']

    # Xe #11: 6 VĐV 10km còn lại (10026 -> 10031).
    # Trưởng xe: Lấy VĐV Văn phòng Tập đoàn trên xe: Nguyễn Bá Lãm (BIB 10026)!
    group_10k_6b = regular_10k[21:]
    cpt_11 = {
        'name': 'Nguyễn Bá Lãm',
        'title': 'Giám sát Thuế và Tài sản (VĐV BIB 10026)',
        'dept': 'Văn phòng Tập đoàn Mường Thanh',
        'phone': '0986 670 418'
    }
    v_11 = {
        'id': 'XE-11',
        'code': 'XE-11',
        'label': 'Xe #11 (7 chỗ)',
        'type': 'Xe 7 chỗ',
        'capacity': 7,
        'paxCount': len(group_10k_6b),
        'departTime': '05:00',
        'pickupLoc': 'Sảnh Khách sạn Mường Thanh Luxury Ninh Bình',
        'destLoc': 'Sân Golf Tràng An & Resort',
        'returnTime': '11:00',
        'captain': {
            'name': cpt_11['name'],
            'title': cpt_11['title'],
            'unit': cpt_11['dept'],
            'phone': cpt_11['phone']
        },
        'bibRange': f"BIB {group_10k_6b[0]['bib']} – {group_10k_6b[-1]['bib']}",
        'distance': '10km',
        'note': f"Đội VĐV 10km ({len(group_10k_6b)} VĐV). Trưởng xe là VĐV Văn phòng Tập đoàn đi trên xe: Nguyễn Bá Lãm.",
        'runners': group_10k_6b,
        'btcStaff': []
    }
    vehicles.append(v_11)
    for r in group_10k_6b:
        r['vehicleId'] = v_11['id']
        r['vehicleLabel'] = v_11['label']
        r['captainName'] = cpt_11['name']
        r['captainPhone'] = cpt_11['phone']

    # =========================================================================
    # 9. CỰ LY 15KM (19 VĐV) -> XE #12, #13, #14 (XE 7 CHỖ)
    # Xe #12 chở Ms. Lê Thị Thơ (15004) theo đúng yêu cầu user!
    # Trưởng xe: VĐV uy tín ngồi trên xe!
    # =========================================================================
    # Xe #12: 6 VĐV (15001, 15002, 15004 - Lê Thị Thơ, 15006, 15007, 15009)
    group_15k_a = regular_15k[:6]
    cpt_12 = {
        'name': 'Trần Hồng Phong',
        'title': 'Trưởng bộ phận Buồng (VĐV BIB 15009)',
        'dept': 'Mường Thanh Luxury Phú Thọ',
        'phone': '0978 460 442'
    }
    v_12 = {
        'id': 'XE-12',
        'code': 'XE-12',
        'label': 'Xe #12 (7 chỗ)',
        'type': 'Xe 7 chỗ',
        'capacity': 7,
        'paxCount': len(group_15k_a),
        'departTime': '05:00',
        'pickupLoc': 'Sảnh Khách sạn Mường Thanh Luxury Ninh Bình',
        'destLoc': 'Sân Golf Tràng An & Resort',
        'returnTime': '11:00',
        'captain': {
            'name': cpt_12['name'],
            'title': cpt_12['title'],
            'unit': cpt_12['dept'],
            'phone': cpt_12['phone']
        },
        'bibRange': f"BIB {group_15k_a[0]['bib']} – {group_15k_a[-1]['bib']}",
        'distance': '15km',
        'note': 'Đội VĐV 15km (có Ms. Lê Thị Thơ 15004 - Ban Điều hành Siêu thị đi cùng xe). Trưởng xe: Trần Hồng Phong.',
        'runners': group_15k_a,
        'btcStaff': []
    }
    vehicles.append(v_12)
    for r in group_15k_a:
        r['vehicleId'] = v_12['id']
        r['vehicleLabel'] = v_12['label']
        r['captainName'] = cpt_12['name']
        r['captainPhone'] = cpt_12['phone']

    # Xe #13: 6 VĐV (15010, 15011, 15012, 15013, 15014, 15015)
    group_15k_b = regular_15k[6:12]
    cpt_13 = {
        'name': 'Trần Hải Đăng',
        'title': 'Quản lý CNTT (VĐV BIB 15015)',
        'dept': 'Mường Thanh Grand Tuyên Quang',
        'phone': '0988 312 188'
    }
    v_13 = {
        'id': 'XE-13',
        'code': 'XE-13',
        'label': 'Xe #13 (7 chỗ)',
        'type': 'Xe 7 chỗ',
        'capacity': 7,
        'paxCount': len(group_15k_b),
        'departTime': '05:00',
        'pickupLoc': 'Sảnh Khách sạn Mường Thanh Luxury Ninh Bình',
        'destLoc': 'Sân Golf Tràng An & Resort',
        'returnTime': '11:00',
        'captain': {
            'name': cpt_13['name'],
            'title': cpt_13['title'],
            'unit': cpt_13['dept'],
            'phone': cpt_13['phone']
        },
        'bibRange': f"BIB {group_15k_b[0]['bib']} – {group_15k_b[-1]['bib']}",
        'distance': '15km',
        'note': 'Đội VĐV 15km. Trưởng xe là VĐV ngồi trên xe: Trần Hải Đăng.',
        'runners': group_15k_b,
        'btcStaff': []
    }
    vehicles.append(v_13)
    for r in group_15k_b:
        r['vehicleId'] = v_13['id']
        r['vehicleLabel'] = v_13['label']
        r['captainName'] = cpt_13['name']
        r['captainPhone'] = cpt_13['phone']

    # Xe #14: 7 VĐV (15016, 15017, 15018, 15019, 15020, 15021, 15022)
    group_15k_c = regular_15k[12:]
    cpt_14 = {
        'name': 'Trần Văn Nhựt',
        'title': 'Giám sát dịch vụ ẩm thực (VĐV BIB 15021)',
        'dept': 'Mường Thanh Quy Nhơn',
        'phone': '0388 170 130'
    }
    v_14 = {
        'id': 'XE-14',
        'code': 'XE-14',
        'label': 'Xe #14 (7 chỗ)',
        'type': 'Xe 7 chỗ',
        'capacity': 7,
        'paxCount': len(group_15k_c),
        'departTime': '05:00',
        'pickupLoc': 'Sảnh Khách sạn Mường Thanh Luxury Ninh Bình',
        'destLoc': 'Sân Golf Tràng An & Resort',
        'returnTime': '11:00',
        'captain': {
            'name': cpt_14['name'],
            'title': cpt_14['title'],
            'unit': cpt_14['dept'],
            'phone': cpt_14['phone']
        },
        'bibRange': f"BIB {group_15k_c[0]['bib']} – {group_15k_c[-1]['bib']}",
        'distance': '15km',
        'note': 'Đội VĐV 15km. Trưởng xe là VĐV ngồi trên xe: Trần Văn Nhựt.',
        'runners': group_15k_c,
        'btcStaff': []
    }
    vehicles.append(v_14)
    for r in group_15k_c:
        r['vehicleId'] = v_14['id']
        r['vehicleLabel'] = v_14['label']
        r['captainName'] = cpt_14['name']
        r['captainPhone'] = cpt_14['phone']

    # =========================================================================
    # 10. XE #15 (7 CHỖ) - TỔ Y TẾ BỆNH VIỆN PHỦ DIỄN (4 NGƯỜI)
    # =========================================================================
    v_15 = {
        'id': 'XE-15-YTE',
        'code': 'XE-15',
        'label': 'Xe #15 - Tổ Y Tế BV Phủ Diễn (7 chỗ)',
        'type': 'Xe 7 chỗ',
        'capacity': 7,
        'paxCount': 3,
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
        'bibRange': 'Tổ Y Tế & Cứu Thương',
        'distance': 'Y tế & Cấp cứu',
        'note': 'Chở 3 Bác sĩ (BS Lê Kim Vũ, BS Võ Thị Mai Anh, BS Quang Tuấn Anh) cùng trang thiết bị y tế, cáng và túi thuốc',
        'runners': [],
        'btcStaff': [
            {'name': 'BS Lê Kim Vũ', 'title': 'Bác sỹ BV Phủ Diễn', 'dept': 'Y tế', 'duty': 'Trạm Y tế 0 (Start/Finish)'},
            {'name': 'BS Võ Thị Mai Anh', 'title': 'Bác sỹ BV Phủ Diễn', 'dept': 'Y tế', 'duty': 'Trạm Y tế 1 (Km 2.3)'},
            {'name': 'BS Quang Tuấn Anh', 'title': 'Bác sỹ BV Phủ Diễn', 'dept': 'Y tế', 'duty': 'Trạm Y tế 2 (Km 4.1)'}
        ]
    }
    vehicles.append(v_15)

    # =========================================================================
    # 11. XE #16 (7 CHỖ) - TỔ MEDIA & MARKETING TRUYỀN THÔNG (6 NGƯỜI)
    # =========================================================================
    v_16 = {
        'id': 'XE-16-MEDIA',
        'code': 'XE-16',
        'label': 'Xe #16 - Tổ Media & Truyền Thông Marketing (7 chỗ)',
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
            'unit': 'Marketing - VPTD',
            'phone': '0983 011 084'
        },
        'bibRange': 'Tổ Media Sự Kiện',
        'distance': 'Truyền thông & Ghi hình',
        'note': 'Chở ekip Media 6 chuyên viên (quay phim, flycam, máy ảnh chốt tại Cửa sổ tình yêu & vạch Finish)',
        'runners': [],
        'btcStaff': [
            {'name': 'Nguyễn Huy Quỳnh', 'title': 'Trưởng nhóm Marketing', 'dept': 'Marketing - VPTD', 'duty': 'Chỉ đạo Media & Truyền thông'},
            {'name': 'Phạm Hoàng Hiệp', 'title': 'GS Quay dựng video', 'dept': 'Marketing - VPTD', 'duty': 'Flycam & Video'},
            {'name': 'Trần Hồng Hạnh', 'title': 'CV Truyền thông nội bộ', 'dept': 'Marketing - VPTD', 'duty': 'Nhiếp ảnh gia'},
            {'name': 'Nguyễn Thị Vân Anh', 'title': 'CV Truyền thông nội bộ', 'dept': 'Marketing - VPTD', 'duty': 'Nhiếp ảnh gia'},
            {'name': 'Võ Tuấn Dương', 'title': 'CV Sáng tạo nội dung', 'dept': 'Marketing - VPTD', 'duty': 'Truyền thông'},
            {'name': 'Vũ Thị Hoàng Nhung', 'title': 'CV Nội dung Marketing', 'dept': 'Marketing - VPTD', 'duty': 'Truyền thông'}
        ]
    }
    vehicles.append(v_16)

    # =========================================================================
    # VALIDATION
    # =========================================================================
    all_assigned_runners = []
    for v in vehicles:
        all_assigned_runners.extend(v['runners'])

    print(f"Total vehicles created: {len(vehicles)}")
    print(f"Total assigned runners across all vehicles: {len(all_assigned_runners)}")

    # Verify every runner in runners_dict has an assignment
    missing_bibs = [b for b in runners_dict.keys() if 'vehicleId' not in runners_dict[b]]
    print(f"Missing runners without vehicleId: {len(missing_bibs)}")
    if missing_bibs:
        print("Missing BIBs:", missing_bibs)

    # Verify each vehicle captain is physically present on that vehicle!
    print("\n--- CHECKING TRƯỞNG XE COMPLIANCE ---")
    for v in vehicles:
        c_name = v['captain']['name']
        # Check if captain is in runners or btcStaff of this vehicle
        in_runners = any(c_name in r['name'] for r in v['runners'])
        in_btc = any(c_name in b['name'] for b in v['btcStaff'])
        is_composite_name = '/' in c_name or '&' in c_name
        valid = in_runners or in_btc or is_composite_name
        status = "OK (Trưởng xe có mặt trên xe)" if valid else "ERROR: Trưởng xe không có trên xe!"
        print(f"  {v['label']}: Trưởng xe '{c_name}' -> {status}")

    # Load existing data.json and update funrun
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    data['funrun']['vehicles'] = vehicles
    data['funrun']['runners'] = list(runners_dict.values())

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("\nSuccessfully updated data.json with new vehicle plan!")

if __name__ == '__main__':
    rebuild_funrun()
