import openpyxl
import json
import sys
from vptd_directory import DIRECTORY

sys.stdout.reconfigure(encoding='utf-8')

def get_phone(name, fallback=''):
    if name in DIRECTORY and DIRECTORY[name].get('phone'):
        return DIRECTORY[name]['phone']
    return fallback

def rebuild_funrun():
    wb = openpyxl.load_workbook('DS VĐV & BTC CHẠY_FINAL 16.10.xlsx', data_only=True)
    s_runners = wb['Dang ky chay']

    # 1. Load all runners
    runners_dict = {}
    for r in s_runners.iter_rows(min_row=4, values_only=True):
        if r[1] is None:
            continue
        bib = int(r[1])
        name = str(r[2] or '').strip()
        phone = str(r[5] or '').strip()
        unit = str(r[4] or '').strip()
        
        # If in VPTD official directory, use official phone number!
        if name in DIRECTORY:
            phone = DIRECTORY[name]['phone']

        # Ẩn số điện thoại của TGĐ Lê Thị Hoàng Yến
        if name == 'Lê Thị Hoàng Yến':
            phone = ''

        runners_dict[bib] = {
            'stt': r[0],
            'bib': bib,
            'name': name,
            'title': str(r[3] or '').strip(),
            'unit': unit,
            'phone': phone,
            'gender': str(r[6] or '').strip(),
            'size': str(r[7] or '').strip(),
            'dist': str(r[8] or '').strip(),
            'category': str(r[9] or '').strip(),
            'btc': str(r[10] or '').strip(),
            'note': str(r[12] or '').strip()
        }

    print(f"Total raw runners: {len(runners_dict)}")

    # 2. Categorize special groups
    self_cienco_dhe_bibs = [
        5034, 5193, 5195, 5196, 5197, 5198, 5199, 5208, 5231, 5289, 5340, 5341, 10017, 15003, 15008
    ]
    self_sieuthi_bibs = [
        5040, 5049, 5060, 5074, 5100, 5131, 5136, 5311, 5336, 5374, 10005, 10018, 10032
    ]
    # Ms. Thơ 15004 rides BTC bus!

    tgd_bib = [5001]
    pho_tgd_runner_bibs = [5002, 5003, 5306, 5010, 15005] # 3 Phó Tổng + Thu Nguyệt + Thanh Trà
    coord_team_bibs = [5004, 5005, 10001] # Thanh Huyền, Huyền Trang, Quốc Việt

    # Nguyễn Tuấn Long (BIB 5380) đi xe sớm của BTC (Xe #00), không đi Xe #08!
    early_btc_runner_bibs = [5380]

    # Ban Sự Kiện riêng (có VĐV Lê Đức Tuấn Định 5011)
    event_team_bibs = [5011]

    # 6 Lái xe kiêm VĐV chạy 5km (tách riêng sang các xe 7 chỗ)
    driver_runner_bibs = [5194, 5284, 5302, 5315, 5322, 5349]

    special_bibs = set(self_cienco_dhe_bibs + self_sieuthi_bibs + tgd_bib + pho_tgd_runner_bibs + coord_team_bibs + early_btc_runner_bibs + event_team_bibs + driver_runner_bibs)

    # Regular runners by distance
    regular_5k = [runners_dict[b] for b in sorted(runners_dict.keys()) if b < 10000 and b not in special_bibs]
    regular_10k = [runners_dict[b] for b in sorted(runners_dict.keys()) if 10000 <= b < 15000 and b not in special_bibs]
    regular_15k = [runners_dict[b] for b in sorted(runners_dict.keys()) if b >= 15000 and b not in special_bibs]

    print(f"Regular 5k (đã bỏ 5380): {len(regular_5k)} (8 buses x 43/42), 10k: {len(regular_10k)}, 15k: {len(regular_15k)}")

    vehicles = []

    # =========================================================================
    # 1. XE VIP 01 - TỔNG GIÁM ĐỐC & THƯ KÝ TGĐ (XE RIÊNG)
    # =========================================================================
    r_tgd = [runners_dict[5001]]
    v_tgd = {
        'id': 'XE-VIP-01',
        'code': 'VIP-TGD',
        'label': 'Xe VIP 01 - Tổng Giám Đốc & Thư Ký TGĐ',
        'type': 'Xe riêng TGĐ',
        'capacity': 4,
        'paxCount': 2, # TGĐ + Thư ký TGĐ
        'departTime': '05:00',
        'pickupLoc': 'Sảnh Khách sạn Mường Thanh Luxury Ninh Bình',
        'destLoc': 'Sân Golf Tràng An & Resort',
        'returnTime': '11:00',
        'captain': {
            'name': 'Lê Thị Hoàng Yến',
            'title': 'Tổng Giám đốc Tập đoàn (Trưởng BTC)',
            'unit': 'Văn phòng Tập đoàn Mường Thanh',
            'phone': ''
        },
        'bibRange': 'BIB 5001',
        'distance': '5km (Ban Lãnh đạo)',
        'note': 'Xe riêng phục vụ Tổng Giám đốc Tập đoàn Lê Thị Hoàng Yến và Thư ký TGĐ Phạm Thị Thu Thủy. (Liên hệ qua Thư ký: 0968 449 690)',
        'isVIP': True,
        'runners': r_tgd,
        'btcStaff': [
            {
                'name': 'Phạm Thị Thu Thủy',
                'title': 'Trợ lý Tổng Giám Đốc',
                'dept': 'Văn phòng Tập đoàn Mường Thanh',
                'duty': 'Thư ký TGĐ & Hỗ trợ Ban Tổ Chức',
                'phone': get_phone('Phạm Thị Thu Thủy', '0968 449 690')
            }
        ]
    }
    vehicles.append(v_tgd)
    for r in r_tgd:
        r['vehicleId'] = v_tgd['id']
        r['vehicleLabel'] = v_tgd['label']
        r['captainName'] = v_tgd['captain']['name']
        r['captainPhone'] = ''

    # =========================================================================
    # 2. XE VIP 02 - BAN PHÓ TỔNG & LÃNH ĐẠO CẤP CAO (XE 7 CHỖ)
    # 3 Phó Tổng + Thu Nguyệt, Thanh Trà, Tạ Diệp Anh
    # =========================================================================
    r_pho_tgd = [runners_dict[b] for b in pho_tgd_runner_bibs]
    v_pho_tgd = {
        'id': 'XE-VIP-02',
        'code': 'VIP-PHO-TGD',
        'label': 'Xe VIP 02 - Ban Phó Tổng & Lãnh Đạo Cấp Cao (7 chỗ)',
        'type': 'Xe 7 chỗ',
        'capacity': 7,
        'paxCount': 6,
        'departTime': '05:00',
        'pickupLoc': 'Sảnh Khách sạn Mường Thanh Luxury Ninh Bình',
        'destLoc': 'Sân Golf Tràng An & Resort',
        'returnTime': '11:00',
        'captain': {
            'name': 'Nguyễn Thanh Tuấn',
            'title': 'Phó Tổng Giám đốc thường trực',
            'unit': 'Văn phòng Tập đoàn Mường Thanh',
            'phone': get_phone('Nguyễn Thanh Tuấn', '0913 029 376')
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
                'phone': get_phone('Tạ Diệp Anh', '0983 263 668')
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
    # Bao gồm Nguyễn Tuấn Long (BIB 5380 - Trưởng phòng Đào tạo & KSCL) đi sớm!
    # =========================================================================
    r_early = [runners_dict[5380]] # Nguyễn Tuấn Long
    v_early = {
        'id': 'XE-00-BTC',
        'code': 'BTC-EARLY',
        'label': 'Xe #00 - Ban Tổ Chức Đi Sớm (04h30)',
        'type': 'Xe 16 chỗ',
        'capacity': 16,
        'paxCount': 6, # 5 cán bộ BTC + 1 cán bộ BTC kiêm VĐV 5380
        'departTime': '04:30',
        'pickupLoc': 'Sảnh Khách sạn Mường Thanh Luxury Ninh Bình',
        'destLoc': 'Sân Golf Tràng An & Resort (Khu vực Start/Finish)',
        'returnTime': '11:00',
        'captain': {
            'name': 'Vũ Minh Tuấn',
            'title': 'Giám đốc Đào tạo & KSCL (Trưởng ban Thể thao)',
            'unit': 'Văn phòng Tập đoàn Mường Thanh',
            'phone': get_phone('Vũ Minh Tuấn', '0934 269 369')
        },
        'bibRange': 'BIB 5380 & BTC Đi Sớm',
        'distance': 'Điều hành, Setup & Chạy 5km',
        'note': 'Xuất phát sớm 04h30 chở các cán bộ kỹ thuật, cổng hơi, âm thanh, bộ đàm và chốt trạm sớm (bao gồm Nguyễn Tuấn Long - TP Đào tạo & KSCL, kiêm VĐV 5km BIB 5380).',
        'isEarly': True,
        'runners': r_early,
        'btcStaff': [
            {'name': 'Vũ Minh Tuấn', 'title': 'GĐ Đào tạo & KSCL', 'duty': 'Điều phối chung & Trao giải', 'dept': 'Đào tạo - VPTD', 'phone': get_phone('Vũ Minh Tuấn')},
            {'name': 'Nguyễn Tuấn Long', 'title': 'TP Đào tạo & KSCL', 'duty': 'Điều phối xuất phát, về đích & Chạy 5km', 'dept': 'Đào tạo - VPTD', 'phone': get_phone('Nguyễn Tuấn Long')},
            {'name': 'Phạm Văn Nhất', 'title': 'TP Phần mềm', 'duty': 'Kiểm soát/đóng dấu vòng chạy km 1.1', 'dept': 'CNTT - VPTD', 'phone': get_phone('Phạm Văn Nhất')},
            {'name': 'Lê Hoàng', 'title': 'PP Hạ tầng CNTT', 'duty': 'Chốt điều hướng 1 - Bus Stop A', 'dept': 'CNTT - VPTD', 'phone': get_phone('Lê Hoàng')},
            {'name': 'Nguyễn Huy Nhân', 'title': 'Giảng viên Đào tạo', 'duty': 'Kiểm soát đích 5km Nữ', 'dept': 'Đào tạo - VPTD', 'phone': get_phone('Nguyễn Huy Nhân')},
            {'name': 'Vũ Chiến Thắng', 'title': 'GS Lập trình', 'duty': 'Kiểm soát đích 10km & 15km', 'dept': 'CNTT - VPTD', 'phone': get_phone('Vũ Chiến Thắng')}
        ]
    }
    vehicles.append(v_early)
    for r in r_early:
        r['vehicleId'] = v_early['id']
        r['vehicleLabel'] = v_early['label']
        r['captainName'] = v_early['captain']['name']
        r['captainPhone'] = v_early['captain']['phone']

    # =========================================================================
    # 4. XE CHỐT ĐOÀN - TEAM ĐIỀU PHỐI XE & DỒN VĐV (XE 7 CHỖ) (05H15)
    # Lưu Quốc Việt, Đỗ Thị Thanh Huyền, Hoàng Thị Huyền Trang + 3 VĐV dồn xe!
    # =========================================================================
    r_coord = [runners_dict[b] for b in coord_team_bibs]
    # Dồn 3 VĐV vào xe chốt đoàn (2 VĐV 10k: 10030, 10031 + 1 VĐV 15k: 15019)
    r_dồn_chot = [runners_dict[10030], runners_dict[10031], runners_dict[15019]]
    all_chot = r_coord + r_dồn_chot

    v_coord = {
        'id': 'XE-CHOT-DOAN',
        'code': 'XE-CHOT',
        'label': 'Xe Chốt Đoàn - Team Điều Phối Xe Di Chuyển (7 chỗ)',
        'type': 'Xe 7 chỗ',
        'capacity': 7,
        'paxCount': len(all_chot), # 3 cán bộ điều phối + 3 VĐV dồn xe = 6/7
        'departTime': '05:15 (Xuất phát cuối cùng)',
        'pickupLoc': 'Sảnh Khách sạn Mường Thanh Luxury Ninh Bình',
        'destLoc': 'Sân Golf Tràng An & Resort',
        'returnTime': '11:00',
        'captain': {
            'name': 'Lưu Quốc Việt',
            'title': 'Giám đốc CNTT (Trưởng Team Điều phối xe)',
            'unit': 'Văn phòng Tập đoàn Mường Thanh',
            'phone': get_phone('Lưu Quốc Việt', '0948 154 816')
        },
        'bibRange': 'BIB 5004, 5005, 10001, 10030, 10031, 15019',
        'distance': 'Điều phối xe & Chốt đoàn (ghép 3 VĐV 10km, 15km)',
        'note': 'Team điều phối xe ở lại sảnh KS điều phối đoàn lên xe, soát quân số và di chuyển khóa đuôi lúc 05:15. Ghép thêm 3 VĐV (10030, 10031, 15019) để dồn tiết kiệm xe.',
        'isCoordination': True,
        'runners': all_chot,
        'btcStaff': [
            {'name': 'Đỗ Thị Thanh Huyền', 'title': 'Chánh Văn phòng', 'duty': 'Điều phối xe & Quân số sảnh KS', 'dept': 'Hành chính - VPTD', 'phone': get_phone('Đỗ Thị Thanh Huyền')},
            {'name': 'Hoàng Thị Huyền Trang', 'title': 'GS Hành chính', 'duty': 'Điều phối xe & Khóa đuôi', 'dept': 'Hành chính - VPTD', 'phone': get_phone('Hoàng Thị Huyền Trang')}
        ]
    }
    vehicles.append(v_coord)
    for r in all_chot:
        r['vehicleId'] = v_coord['id']
        r['vehicleLabel'] = v_coord['label']
        r['captainName'] = v_coord['captain']['name']
        r['captainPhone'] = v_coord['captain']['phone']

    # =========================================================================
    # 5. XE RIÊNG TEAM BAN SỰ KIỆN BTC (XE 7 CHỖ)
    # =========================================================================
    r_event = [runners_dict[5011]]
    cpt_event = {
        'name': 'Lê Đức Tuấn Định',
        'title': 'Trưởng phòng Thiết kế (Trưởng đoàn Ban Sự kiện)',
        'dept': 'Marketing - VPTD',
        'phone': get_phone('Lê Đức Tuấn Định', '0989 414 580'),
        'duty': 'Điều hành Ban Sự kiện & tham gia chạy 5km'
    }
    v_event = {
        'id': 'XE-BAN-SU-KIEN',
        'code': 'XE-SK',
        'label': 'Xe Ban Sự Kiện - Team Sự Kiện & Media BTC (7 chỗ)',
        'type': 'Xe 7 chỗ riêng',
        'capacity': 7,
        'paxCount': 7,
        'departTime': '04:45',
        'pickupLoc': 'Sảnh Khách sạn Mường Thanh Luxury Ninh Bình',
        'destLoc': 'Sân Golf Tràng An & Resort',
        'returnTime': '11:00',
        'captain': {
            'name': cpt_event['name'],
            'title': cpt_event['title'],
            'unit': cpt_event['dept'],
            'phone': cpt_event['phone']
        },
        'bibRange': 'BIB 5011 & Ban Sự Kiện',
        'distance': 'Tác nghiệp Sự kiện, Truyền thông & Chạy 5km',
        'note': 'Xe riêng phục vụ Ban Sự kiện và Ekip Media gồm 7 người: Lê Đức Tuấn Định (Trưởng phòng Thiết kế - kiêm VĐV 5km), Nguyễn Huy Quỳnh, Phạm Hoàng Hiệp, Trần Hồng Hạnh, Nguyễn Thị Vân Anh, Võ Tuấn Dương, Vũ Thị Hoàng Nhung.',
        'runners': r_event,
        'btcStaff': [
            {'name': 'Lê Đức Tuấn Định', 'title': 'TP Thiết kế', 'duty': 'Trưởng đoàn Ban Sự kiện & Chạy 5km', 'dept': 'Marketing - VPTD', 'phone': get_phone('Lê Đức Tuấn Định'), 'isCaptain': True},
            {'name': 'Nguyễn Huy Quỳnh', 'title': 'Trưởng nhóm Marketing', 'duty': 'Điều phối nội dung & tác nghiệp sự kiện', 'dept': 'Marketing - VPTD', 'phone': get_phone('Nguyễn Huy Quỳnh')},
            {'name': 'Phạm Hoàng Hiệp', 'title': 'Giám sát Quay dựng video', 'duty': 'Quay phim, flycam tác nghiệp', 'dept': 'Marketing - VPTD', 'phone': get_phone('Phạm Hoàng Hiệp')},
            {'name': 'Trần Hồng Hạnh', 'title': 'Chuyên viên TTNB', 'duty': 'Chụp ảnh, đưa tin bài sự kiện', 'dept': 'Marketing - VPTD', 'phone': get_phone('Trần Hồng Hạnh')},
            {'name': 'Nguyễn Thị Vân Anh', 'title': 'Chuyên viên TTNB', 'duty': 'Chụp ảnh, đưa tin bài sự kiện', 'dept': 'Marketing - VPTD', 'phone': get_phone('Nguyễn Thị Vân Anh')},
            {'name': 'Võ Tuấn Dương', 'title': 'Chuyên viên STND', 'duty': 'Sáng tạo nội dung truyền thông', 'dept': 'Marketing - VPTD', 'phone': get_phone('Võ Tuấn Dương')},
            {'name': 'Vũ Thị Hoàng Nhung', 'title': 'Chuyên viên Nội dung Marketing', 'duty': 'Nội dung truyền thông', 'dept': 'Marketing - VPTD', 'phone': get_phone('Vũ Thị Hoàng Nhung')}
        ]
    }
    vehicles.append(v_event)
    for r in r_event:
        r['vehicleId'] = v_event['id']
        r['vehicleLabel'] = v_event['label']
        r['captainName'] = cpt_event['name']
        r['captainPhone'] = cpt_event['phone']

    # =========================================================================
    # 6. ĐOÀN TỰ DI CHUYỂN: KHỐI SIÊU THỊ MƯỜNG THANH (13 VĐV)
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
    # 7. ĐOÀN TỰ DI CHUYỂN: CIENCO5 & THANG MÁY DHE (15 VĐV)
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
    # 8. 8 XE 45 CHỖ (XE #01 ĐẾN XE #08) - CỰ LY 5KM (343 VĐV)
    # Xe #08 đã bỏ Nguyễn Tuấn Long (5380), chỉ chở 42 VĐV + 1 Trưởng xe = 43/45 chỗ!
    # =========================================================================
    priority_btc_captains = [
        {'name': 'Hoàng Thanh Hải', 'title': 'Chuyên viên Hành chính (BTC Tiếp nước)', 'dept': 'Hành chính - VPTD', 'phone': get_phone('Hoàng Thanh Hải', '0982 054 788'), 'duty': 'Trạm tiếp nước số 1 (Km 2.3)'},
        {'name': 'Dương Thị Hải Anh', 'title': 'Giám đốc Pháp chế (BTC Tiếp nước)', 'dept': 'Pháp chế - VPTD', 'phone': get_phone('Dương Thị Hải Anh', '0982 821 654'), 'duty': 'Trạm tiếp nước số 2 (Km 4.1)'},
        {'name': 'Nguyễn Thu Mai', 'title': 'Giám sát Chế độ chính sách (BTC Kiểm soát)', 'dept': 'Nhân sự - VPTD', 'phone': get_phone('Nguyễn Thu Mai', '0918 816 891'), 'duty': 'Trạm kiểm soát vòng chạy (Km 1.1)'},
        {'name': 'Nguyễn Thái Mỹ', 'title': 'Chuyên viên Thiết kế báo cáo (BTC Kiểm soát)', 'dept': 'CNTT - VPTD', 'phone': get_phone('Nguyễn Thái Mỹ', '0362 109 907'), 'duty': 'Trạm kiểm soát vòng chạy (Km 1.1)'},
        {'name': 'Nguyễn Duy Hoạt', 'title': 'Giám sát CNTT (BTC Điều hướng)', 'dept': 'CNTT - VPTD', 'phone': get_phone('Nguyễn Duy Hoạt', '0916 464 029'), 'duty': 'Điều hướng 2 (Trả khách C)'},
        {'name': 'Phạm Minh Hiếu', 'title': 'Giám sát Lập trình CSDL cấp cao (BTC Điều hướng)', 'dept': 'CNTT - VPTD', 'phone': get_phone('Phạm Minh Hiếu', '0979 140 391'), 'duty': 'Điều hướng 3 (Ngã ba rộng)'},
        {'name': 'Trần Đình Thông', 'title': 'Chuyên viên Quản trị CSDL (BTC Điều hướng)', 'dept': 'CNTT - VPTD', 'phone': get_phone('Trần Đình Thông', '0912 177 998'), 'duty': 'Điều hướng 4 (Lối hố tập H)'},
        {'name': 'Võ Thị Mai Trang', 'title': 'Giám sát Điều phối (BTC Kiểm soát đích)', 'dept': 'Đào tạo & KSCL - VPTD', 'phone': get_phone('Võ Thị Mai Trang', '0974 899 868'), 'duty': 'Kiểm soát về đích 5km Nam'}
    ]

    # 343 runners = 7 x 43 + 1 x 42
    sizes_5k = [43, 43, 43, 43, 43, 43, 43, 42]
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
            'paxCount': len(group) + 1,
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
    # 9. CỰ LY 10KM (27 VĐV) & LÁI XE KIÊM VĐV
    # Xe #09: 15 VĐV 10km (10002 -> 10016) + Trưởng xe Phạm Hà An = 16/16
    # Xe #10: 5 VĐV 10km (10019 -> 10023) + Trưởng xe Đoàn Thế Cương + Lái xe kiêm VĐV Trần Văn Tuân (5194) = 7/7
    # Xe #11: 5 VĐV 10km (10024 -> 10029) + 1 Lái xe kiêm VĐV Lương Trung Thành (5284) + 1 VĐV 15km (15020) dồn sang = 7/7
    # =========================================================================
    # Xe #09 (16 chỗ)
    group_10k_15 = regular_10k[:15]
    cpt_09 = {
        'name': 'Phạm Hà An',
        'title': 'Giám sát Chế độ chính sách (BTC Thư ký kết quả)',
        'dept': 'Nhân sự - VPTD',
        'phone': get_phone('Phạm Hà An', '0973 554 996'),
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

    # Xe #10: Lái xe kiêm VĐV 5km: Trần Văn Tuân (5194 - MT Luxury Quảng Ninh)
    r_driver_10 = runners_dict[5194]
    group_10k_5a = regular_10k[15:20]
    cpt_10 = {
        'name': 'Đoàn Thế Cương',
        'title': 'Quản lý Nghiệp vụ An ninh (BTC An ninh)',
        'dept': 'Operation - VPTD',
        'phone': get_phone('Đoàn Thế Cương', '0912 211 929'),
        'duty': 'Quản lý an ninh chung & hỗ trợ thu gom VĐV'
    }
    v_10 = {
        'id': 'XE-10',
        'code': 'XE-10',
        'label': 'Xe #10 (7 chỗ)',
        'type': 'Xe 7 chỗ',
        'capacity': 7,
        'paxCount': len(group_10k_5a) + 2, # 5 VĐV 10k + 1 Trưởng xe + 1 Lái xe kiêm VĐV = 7
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
        'driver': {
            'name': r_driver_10['name'],
            'bib': r_driver_10['bib'],
            'unit': r_driver_10['unit'],
            'role': 'Lái xe kiêm VĐV chạy 5km'
        },
        'bibRange': f"BIB 5194, {group_10k_5a[0]['bib']} – {group_10k_5a[-1]['bib']}",
        'distance': '10km (kèm Lái xe kiêm VĐV 5km)',
        'note': f"Xe 7 chỗ. Trưởng xe BTC: Đoàn Thế Cương. Lái xe kiêm VĐV tự lái: Trần Văn Tuân (BIB 5194 - MT Luxury Quảng Ninh). Chở 5 VĐV 10km.",
        'runners': [r_driver_10] + group_10k_5a,
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
    for r in v_10['runners']:
        r['vehicleId'] = v_10['id']
        r['vehicleLabel'] = v_10['label']
        r['captainName'] = cpt_10['name']
        r['captainPhone'] = cpt_10['phone']

    # Xe #11: Lái xe kiêm VĐV 5km: Lương Trung Thành (5284 - MT Luxury Cao Bằng)
    # 5 VĐV 10k (10024 -> 10029, gồm Trưởng xe Nguyễn Bá Lãm 10026) + 1 VĐV 15k (15020) dồn xe
    r_driver_11 = runners_dict[5284]
    group_10k_5b = regular_10k[20:25] # 5 runners 10k (10024, 10025, 10026, 10027, 10028, 10029 -> lấy 5 runners)
    r_dồn_11 = [runners_dict[15020]] # Dồn thêm 15020 sang đây cho tròn 7 chỗ!

    cpt_11 = {
        'name': 'Nguyễn Bá Lãm',
        'title': 'Giám sát Thuế và Tài sản (VĐV BIB 10026)',
        'dept': 'Văn phòng Tập đoàn Mường Thanh',
        'phone': get_phone('Nguyễn Bá Lãm', '0986 670 418')
    }
    runners_11 = [r_driver_11] + group_10k_5b + r_dồn_11
    v_11 = {
        'id': 'XE-11',
        'code': 'XE-11',
        'label': 'Xe #11 (7 chỗ)',
        'type': 'Xe 7 chỗ',
        'capacity': 7,
        'paxCount': len(runners_11), # 7 người
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
        'driver': {
            'name': r_driver_11['name'],
            'bib': r_driver_11['bib'],
            'unit': r_driver_11['unit'],
            'role': 'Lái xe kiêm VĐV chạy 5km'
        },
        'bibRange': f"BIB 5284, 15020, {group_10k_5b[0]['bib']} – {group_10k_5b[-1]['bib']}",
        'distance': '10km & 15km (kèm Lái xe kiêm VĐV 5km)',
        'note': f"Xe 7 chỗ. Trưởng xe là VĐV Văn phòng Tập đoàn: Nguyễn Bá Lãm (BIB 10026). Lái xe kiêm VĐV tự lái: Lương Trung Thành (BIB 5284 - MT Luxury Cao Bằng). Ghép thêm VĐV 15020 để dồn xe.",
        'runners': runners_11,
        'btcStaff': []
    }
    vehicles.append(v_11)
    for r in runners_11:
        r['vehicleId'] = v_11['id']
        r['vehicleLabel'] = v_11['label']
        r['captainName'] = cpt_11['name']
        r['captainPhone'] = cpt_11['phone']

    # =========================================================================
    # 10. CỰ LY 15KM & LÁI XE KIÊM VĐV (XE #12, #13, #14)
    # Xe #12: Trưởng xe Đào Minh Anh (VPTD) + Lái xe kiêm VĐV Lê Văn Chiến (5302)
    # Xe #13: Trưởng xe Hoàng Kim Chính (VPTD) + Lái xe kiêm VĐV Đoàn Công Anh Tú (5315)
    # Xe #14: Trưởng xe Trần Đại Nghĩa (VPTD) + Lái xe kiêm VĐV Trần Quang Lợi (5322)
    # =========================================================================
    # Xe #12: Lái xe kiêm VĐV Lê Văn Chiến (5302 - MT Vinh)
    r_driver_12 = runners_dict[5302]
    group_15k_a = regular_15k[:5] # 5 runners 15k (including 15004 Ms. Lê Thị Thơ)
    cpt_12 = {
        'name': 'Đào Minh Anh',
        'title': 'Chuyên viên Dữ liệu nhân sự (BTC Kiểm soát vòng chạy)',
        'dept': 'Nhân sự - VPTD',
        'phone': get_phone('Đào Minh Anh', '0366 700 935'),
        'duty': 'Trưởng xe #12 & Kiểm soát đóng dấu vòng chạy Km 1.1'
    }
    v_12 = {
        'id': 'XE-12',
        'code': 'XE-12',
        'label': 'Xe #12 (7 chỗ)',
        'type': 'Xe 7 chỗ',
        'capacity': 7,
        'paxCount': len(group_15k_a) + 2, # 5 VĐV 15k + 1 Trưởng xe BTC + 1 Lái xe kiêm VĐV = 7
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
        'driver': {
            'name': r_driver_12['name'],
            'bib': r_driver_12['bib'],
            'unit': r_driver_12['unit'],
            'role': 'Lái xe kiêm VĐV chạy 5km'
        },
        'bibRange': f"BIB 5302, {group_15k_a[0]['bib']} – {group_15k_a[-1]['bib']}",
        'distance': '15km (gồm Ms. Thơ Siêu thị & Lái xe kiêm VĐV 5km)',
        'note': f"Xe 7 chỗ. Trưởng xe BTC: Đào Minh Anh (VPTĐ). Lái xe kiêm VĐV tự lái: Lê Văn Chiến (BIB 5302 - MT Vinh). Đón Ms. Lê Thị Thơ (BIB 15004 - Ban Điều hành Siêu thị) và 4 VĐV 15km.",
        'runners': [r_driver_12] + group_15k_a,
        'btcStaff': [
            {
                'name': cpt_12['name'],
                'title': cpt_12['title'],
                'dept': cpt_12['dept'],
                'duty': cpt_12['duty'],
                'phone': cpt_12['phone'],
                'isCaptain': True
            }
        ]
    }
    vehicles.append(v_12)
    for r in v_12['runners']:
        r['vehicleId'] = v_12['id']
        r['vehicleLabel'] = v_12['label']
        r['captainName'] = cpt_12['name']
        r['captainPhone'] = cpt_12['phone']

    # Xe #13: Lái xe kiêm VĐV Đoàn Công Anh Tú (5315 - MT Holiday Quảng Bình)
    r_driver_13 = runners_dict[5315]
    group_15k_b = regular_15k[5:10] # 5 runners 15k
    cpt_13 = {
        'name': 'Hoàng Kim Chính',
        'title': 'Phó phòng Kiểm soát chi phí (BTC Trao giải Finisher)',
        'dept': 'Tài chính - VPTD',
        'phone': get_phone('Hoàng Kim Chính', '0985 434 292'),
        'duty': 'Trưởng xe #13 & Hỗ trợ trao giải Finisher'
    }
    v_13 = {
        'id': 'XE-13',
        'code': 'XE-13',
        'label': 'Xe #13 (7 chỗ)',
        'type': 'Xe 7 chỗ',
        'capacity': 7,
        'paxCount': len(group_15k_b) + 2, # 5 VĐV 15k + 1 Trưởng xe BTC + 1 Lái xe kiêm VĐV = 7
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
        'driver': {
            'name': r_driver_13['name'],
            'bib': r_driver_13['bib'],
            'unit': r_driver_13['unit'],
            'role': 'Lái xe kiêm VĐV chạy 5km'
        },
        'bibRange': f"BIB 5315, {group_15k_b[0]['bib']} – {group_15k_b[-1]['bib']}",
        'distance': '15km (kèm Lái xe kiêm VĐV 5km)',
        'note': f"Xe 7 chỗ. Trưởng xe BTC: Hoàng Kim Chính (VPTĐ). Lái xe kiêm VĐV tự lái: Đoàn Công Anh Tú (BIB 5315 - MT Holiday Quảng Bình). Chở 5 VĐV 15km.",
        'runners': [r_driver_13] + group_15k_b,
        'btcStaff': [
            {
                'name': cpt_13['name'],
                'title': cpt_13['title'],
                'dept': cpt_13['dept'],
                'duty': cpt_13['duty'],
                'phone': cpt_13['phone'],
                'isCaptain': True
            }
        ]
    }
    vehicles.append(v_13)
    for r in v_13['runners']:
        r['vehicleId'] = v_13['id']
        r['vehicleLabel'] = v_13['label']
        r['captainName'] = cpt_13['name']
        r['captainPhone'] = cpt_13['phone']

    # Xe #14: Lái xe kiêm VĐV Trần Quang Lợi (5322 - MT Luxury Vientiane)
    # Trưởng xe: Trần Đại Nghĩa (Trưởng phòng Kiểm toán nội bộ - VPTD)
    r_driver_14 = runners_dict[5322]
    group_15k_c = regular_15k[10:15] # 5 runners 15k
    cpt_14 = {
        'name': 'Trần Đại Nghĩa',
        'title': 'Trưởng phòng Kiểm toán nội bộ',
        'dept': 'Văn phòng Tập đoàn Mường Thanh',
        'phone': get_phone('Trần Đại Nghĩa', '0987 379 398'),
        'duty': 'Trưởng xe #14 phụ trách đoàn'
    }
    v_14 = {
        'id': 'XE-14',
        'code': 'XE-14',
        'label': 'Xe #14 (7 chỗ)',
        'type': 'Xe 7 chỗ',
        'capacity': 7,
        'paxCount': len(group_15k_c) + 2, # 5 VĐV 15k + 1 Trưởng xe BTC + 1 Lái xe kiêm VĐV = 7
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
        'driver': {
            'name': r_driver_14['name'],
            'bib': r_driver_14['bib'],
            'unit': r_driver_14['unit'],
            'role': 'Lái xe kiêm VĐV chạy 5km'
        },
        'bibRange': f"BIB 5322, {group_15k_c[0]['bib']} – {group_15k_c[-1]['bib']}",
        'distance': '15km (kèm Lái xe kiêm VĐV 5km)',
        'note': f"Xe 7 chỗ. Trưởng xe: Trần Đại Nghĩa (Trưởng phòng Kiểm toán nội bộ - VPTĐ). Lái xe kiêm VĐV tự lái: Trần Quang Lợi (BIB 5322 - MT Luxury Vientiane). Chở 5 VĐV 15km.",
        'runners': [r_driver_14] + group_15k_c,
        'btcStaff': [
            {
                'name': cpt_14['name'],
                'title': cpt_14['title'],
                'dept': cpt_14['dept'],
                'duty': cpt_14['duty'],
                'phone': cpt_14['phone'],
                'isCaptain': True
            }
        ]
    }
    vehicles.append(v_14)
    for r in v_14['runners']:
        r['vehicleId'] = v_14['id']
        r['vehicleLabel'] = v_14['label']
        r['captainName'] = cpt_14['name']
        r['captainPhone'] = cpt_14['phone']

    # =========================================================================
    # 11. XE #15-YTE (7 CHỖ) - TỔ Y TẾ BỆNH VIỆN PHỦ DIỄN & DỒN VĐV TIẾT KIỆM XE
    # Lái xe kiêm VĐV 5km: Nguyễn Minh Khoa (5349 - MT Grand Lào Cai) tự lái!
    # Trưởng xe: Nguyễn Thị Lan (Trưởng nhóm Nhân sự VPTĐ)
    # Chở: 3 Bác sĩ (BS Lê Kim Vũ, BS Võ Thị Mai Anh, BS Quang Tuấn Anh) + 2 VĐV 15km (15021, 15022)
    # =========================================================================
    r_driver_yte = runners_dict[5349]
    r_dồn_yte = [runners_dict[15021], runners_dict[15022]]
    runners_yte = [r_driver_yte] + r_dồn_yte

    cpt_yte = {
        'name': 'Nguyễn Thị Lan',
        'title': 'Trưởng nhóm Nhân sự (BTC Hậu cần Y tế)',
        'dept': 'Nhân sự - VPTD',
        'phone': get_phone('Nguyễn Thị Lan', '0977 760 567'),
        'duty': 'Trưởng xe Y tế & Phụ trách điều phối cứu thương'
    }
    v_yte = {
        'id': 'XE-15-YTE',
        'code': 'XE-15-YTE',
        'label': 'Xe #15 - Tổ Y Tế BV Phủ Diễn (7 chỗ)',
        'type': 'Xe 7 chỗ',
        'capacity': 7,
        'paxCount': len(runners_yte) + 4, # 3 VĐV (gồm lái xe) + 1 Trưởng xe + 3 Bác sĩ = 7 người
        'departTime': '05:00',
        'pickupLoc': 'Sảnh Khách sạn Mường Thanh Luxury Ninh Bình',
        'destLoc': 'Sân Golf Tràng An & Resort',
        'returnTime': '11:00',
        'captain': {
            'name': cpt_yte['name'],
            'title': cpt_yte['title'],
            'unit': cpt_yte['dept'],
            'phone': cpt_yte['phone']
        },
        'driver': {
            'name': r_driver_yte['name'],
            'bib': r_driver_yte['bib'],
            'unit': r_driver_yte['unit'],
            'role': 'Lái xe kiêm VĐV chạy 5km'
        },
        'bibRange': 'BIB 5349, 15021, 15022 & Tổ Y Tế',
        'distance': 'Y tế, Cấp cứu & Chạy 5km/15km',
        'note': f"Trưởng xe phụ trách là cán bộ Ban Nhân sự Văn phòng Tập đoàn: Nguyễn Thị Lan. Lái xe kiêm VĐV tự lái: Nguyễn Minh Khoa (BIB 5349 - MT Grand Lào Cai). Chở 3 Bác sĩ Bệnh viện Phủ Diễn (BS Lê Kim Vũ, BS Võ Thị Mai Anh, BS Quang Tuấn Anh), cáng thương và ghép thêm 2 VĐV 15km để dồn tiết kiệm xe.",
        'runners': runners_yte,
        'btcStaff': [
            {'name': cpt_yte['name'], 'title': cpt_yte['title'], 'dept': cpt_yte['dept'], 'duty': cpt_yte['duty'], 'phone': cpt_yte['phone'], 'isCaptain': True},
            {'name': 'BS Lê Kim Vũ', 'title': 'Bác sỹ BV Phủ Diễn', 'dept': 'Y tế', 'duty': 'Trạm Y tế 0 (Start/Finish)', 'phone': '0912 345 678'},
            {'name': 'BS Võ Thị Mai Anh', 'title': 'Bác sỹ BV Phủ Diễn', 'dept': 'Y tế', 'duty': 'Trạm Y tế 1 (Km 2.3)'},
            {'name': 'BS Quang Tuấn Anh', 'title': 'Bác sỹ BV Phủ Diễn', 'dept': 'Y tế', 'duty': 'Trạm Y tế 2 (Km 4.1)'}
        ]
    }
    vehicles.append(v_yte)
    for r in runners_yte:
        r['vehicleId'] = v_yte['id']
        r['vehicleLabel'] = v_yte['label']
        r['captainName'] = cpt_yte['name']
        r['captainPhone'] = cpt_yte['phone']

    print(f"\nTotal vehicles configured: {len(vehicles)}")

    # 4. Count total runners assigned
    assigned_runners = set()
    for v in vehicles:
        for r in v.get('runners', []):
            assigned_runners.add(r['bib'])

    print(f"Total unique runners assigned across all vehicles: {len(assigned_runners)} / {len(runners_dict)}")
    if len(assigned_runners) != len(runners_dict):
        missing = set(runners_dict.keys()) - assigned_runners
        print(f"WARNING: Missing BIBs: {missing}")

    # 5. Save to data.json
    with open('data.json', 'r', encoding='utf-8') as f:
        full_data = json.load(f)

    full_data['funrun']['vehicles'] = vehicles
    full_data['funrun']['runners'] = list(runners_dict.values())

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(full_data, f, ensure_ascii=False, indent=2)

    print("Successfully updated data.json with new consolidated vehicle plan!")

if __name__ == '__main__':
    rebuild_funrun()
