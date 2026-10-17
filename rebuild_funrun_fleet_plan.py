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

    # Xe #00 đi sớm 04h30 (7 chỗ):
    # - Nguyễn Tuấn Long (BIB 5380 - Trưởng phòng Đào tạo & KSCL)
    # - Hoàng Roãn Cường (BIB 5357 - Chuyên viên KSCP VPTĐ - LÁI XE KIÊM VĐV)
    early_btc_runner_bibs = [5380, 5357]

    # Ban Sự Kiện riêng (có VĐV Lê Đức Tuấn Định 5011)
    event_team_bibs = [5011]

    # 6 Lái xe kiêm VĐV chạy 5km (tách riêng sang các xe 7 chỗ)
    driver_runner_bibs = [5194, 5284, 5302, 5315, 5322, 5349]

    special_bibs = set(self_cienco_dhe_bibs + self_sieuthi_bibs + tgd_bib + pho_tgd_runner_bibs + coord_team_bibs + early_btc_runner_bibs + event_team_bibs + driver_runner_bibs)

    # Regular runners by distance
    regular_5k = [runners_dict[b] for b in sorted(runners_dict.keys()) if b < 10000 and b not in special_bibs]
    regular_10k = [runners_dict[b] for b in sorted(runners_dict.keys()) if 10000 <= b < 15000 and b not in special_bibs]
    regular_15k = [runners_dict[b] for b in sorted(runners_dict.keys()) if b >= 15000 and b not in special_bibs]

    print(f"Regular 5k (đã bớt Mr. Cường 5357 và Mr. Long 5380): {len(regular_5k)} (8 buses x 43/42), 10k: {len(regular_10k)}, 15k: {len(regular_15k)}")

    vehicles = []

    # =========================================================================
    # 1. XE VIP 01 - TỔNG GIÁM ĐỐC & THƯ KÝ TGĐ (XE RIÊNG 4 CHỖ)
    # Không có VĐV kiêm lái xe -> chừa 1 ghế cho lái xe riêng (2 khách / 4 chỗ)
    # =========================================================================
    r_tgd = [runners_dict[5001]]
    v_tgd = {
        'id': 'XE-VIP-01',
        'code': 'VIP-TGD',
        'label': 'Xe VIP 01 - Tổng Giám Đốc & Thư Ký TGĐ',
        'type': 'Xe riêng TGĐ (4 chỗ)',
        'capacity': 4,
        'paxCount': 2, # TGĐ + Thư ký TGĐ (chừa 1 ghế cho lái xe riêng)
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
        'note': 'Xe riêng phục vụ Tổng Giám đốc Tập đoàn Lê Thị Hoàng Yến và Thư ký TGĐ Phạm Thị Thu Thủy. Có lái xe riêng phục vụ.',
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
    # Không có VĐV kiêm lái xe -> chừa 1 ghế cho lái xe hợp đồng (6 khách / 7 chỗ)
    # 3 Phó Tổng + Thu Nguyệt, Thanh Trà, Tạ Diệp Anh
    # =========================================================================
    r_pho_tgd = [runners_dict[b] for b in pho_tgd_runner_bibs]
    v_pho_tgd = {
        'id': 'XE-VIP-02',
        'code': 'VIP-PHO-TGD',
        'label': 'Xe VIP 02 - Ban Phó Tổng & Lãnh Đạo Cấp Cao (7 chỗ)',
        'type': 'Xe 7 chỗ',
        'capacity': 7,
        'paxCount': 6, # 6 cán bộ nội bộ + 1 lái xe thuê ngoài = 7/7
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
        'note': 'Xe 7 chỗ bố trí riêng cho 3 Phó Tổng Giám đốc ghép cùng Ms. Thu Nguyệt (MKT), Ms. Thanh Trà (KD), Ms. Tạ Diệp Anh (TC). Chở 6 người nội bộ (chừa 1 ghế cho lái xe thuê ngoài).',
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
    # 3. XE #00 - BAN TỔ CHỨC ĐI SỚM (04H30) (XE 7 CHỖ)
    # YÊU CẦU:
    # + BTC đi sớm có 6 người sao lại xếp xe 16 chỗ cho phí? Chỉ cần xe 7 chỗ.
    # + Và xe này do VĐV Hoàng Roãn Cường lái nhé (bớt Mr. Cường ở xe khác).
    # -> CÓ VĐV KIÊM LÁI XE: Hoàng Roãn Cường (BIB 5357) ngồi ghế lái!
    # -> 6 cán bộ BTC ngồi 6 ghế còn lại = ĐỦ 7/7 CHỖ!
    # =========================================================================
    r_driver_00 = runners_dict[5357] # Hoàng Roãn Cường - Chuyên viên KSCP VPTĐ
    r_long = runners_dict[5380] # Nguyễn Tuấn Long - TP Đào tạo & KSCL
    r_early = [r_driver_00, r_long]

    cpt_00 = {
        'name': 'Vũ Minh Tuấn',
        'title': 'Giám đốc Đào tạo & KSCL (Trưởng ban Thể thao)',
        'dept': 'Văn phòng Tập đoàn Mường Thanh',
        'phone': get_phone('Vũ Minh Tuấn', '0934 269 369')
    }

    v_early = {
        'id': 'XE-00-BTC',
        'code': 'BTC-EARLY',
        'label': 'Xe #00 - Ban Tổ Chức Đi Sớm (04h30) (7 chỗ)',
        'type': 'Xe 7 chỗ',
        'capacity': 7,
        'paxCount': 7, # 1 Lái xe kiêm VĐV 5357 + 1 VĐV 5380 + 5 cán bộ BTC = 7 người (đầy 7/7 ghế vì chính VĐV tự lái!)
        'departTime': '04:30',
        'pickupLoc': 'Sảnh Khách sạn Mường Thanh Luxury Ninh Bình',
        'destLoc': 'Sân Golf Tràng An & Resort (Khu vực Start/Finish)',
        'returnTime': '11:00',
        'captain': {
            'name': cpt_00['name'],
            'title': cpt_00['title'],
            'unit': cpt_00['dept'],
            'phone': cpt_00['phone']
        },
        'driver': {
            'name': r_driver_00['name'],
            'bib': r_driver_00['bib'],
            'unit': r_driver_00['unit'],
            'phone': r_driver_00['phone'],
            'role': 'Lái xe kiêm VĐV chạy 5km (Chuyên viên KSCP - VPTĐ)'
        },
        'bibRange': 'BIB 5357, 5380 & BTC Đi Sớm',
        'distance': 'Điều hành, Setup & Chạy 5km',
        'note': 'Xe 7 chỗ xuất phát sớm 04h30 do VĐV Hoàng Roãn Cường (BIB 5357 - Chuyên viên Kiểm soát chi phí VPTĐ) tự lái. Chở Giám đốc Đào tạo & KSCL Vũ Minh Tuấn (Trưởng xe), Trưởng phòng Đào tạo & KSCL Nguyễn Tuấn Long (BIB 5380) cùng 4 cán bộ kỹ thuật và chốt trạm sớm setup âm thanh, cổng hơi, bộ đàm.',
        'isEarly': True,
        'runners': r_early,
        'btcStaff': [
            {'name': 'Vũ Minh Tuấn', 'title': 'GĐ Đào tạo & KSCL', 'duty': 'Điều phối chung & Trao giải', 'dept': 'Đào tạo - VPTD', 'phone': get_phone('Vũ Minh Tuấn'), 'isCaptain': True},
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
    # 4. XE CHỐT ĐOÀN - TEAM ĐIỀU PHỐI XE DI CHUYỂN (XE 7 CHỖ) (05H15)
    # Lưu Quốc Việt, Đỗ Thị Thanh Huyền, Hoàng Thị Huyền Trang
    # Không có VĐV kiêm lái xe -> chừa 1 ghế cho lái xe thuê ngoài (3 khách / 7 chỗ)
    # =========================================================================
    r_coord = [runners_dict[b] for b in coord_team_bibs]
    v_coord = {
        'id': 'XE-CHOT-DOAN',
        'code': 'XE-CHOT',
        'label': 'Xe Chốt Đoàn - Team Điều Phối Xe Di Chuyển (7 chỗ)',
        'type': 'Xe 7 chỗ',
        'capacity': 7,
        'paxCount': len(r_coord) + 1, # 3 cán bộ điều phối kiêm VĐV + 1 cán bộ BTC Lương Tú Anh = 4 người (chừa 1 ghế cho lái xe thuê ngoài: 4/7)
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
        'bibRange': 'BIB 5004, 5005, 10001 & BTC Khóa Đuôi',
        'distance': 'Điều phối xe & Chốt đoàn (5km & 10km)',
        'note': 'Xe 7 chỗ phục vụ Team điều phối xe ở lại sảnh KS điều phối đoàn lên xe, soát quân số và di chuyển khóa đuôi lúc 05:15. Thành viên gồm: Lưu Quốc Việt (GĐ CNTT), Đỗ Thị Thanh Huyền (Chánh VP), Hoàng Thị Huyền Trang (GS Hành chính) và Lương Tú Anh (GS KSCP cấp cao - phụ trách giám sát hợp đồng và nghiệm thu). Có lái xe thuê ngoài phục vụ.',
        'isCoordination': True,
        'runners': r_coord,
        'btcStaff': [
            {'name': 'Đỗ Thị Thanh Huyền', 'title': 'Chánh Văn phòng', 'duty': 'Điều phối xe & Quân số sảnh KS', 'dept': 'Hành chính - VPTD', 'phone': get_phone('Đỗ Thị Thanh Huyền', '0982 999 158')},
            {'name': 'Hoàng Thị Huyền Trang', 'title': 'GS Hành chính', 'duty': 'Điều phối xe & Khóa đuôi', 'dept': 'Hành chính - VPTD', 'phone': get_phone('Hoàng Thị Huyền Trang', '0974 669 283')},
            {'name': 'Lương Tú Anh', 'title': 'GS Kiểm soát chi phí cấp cao', 'duty': 'Giám sát hợp đồng, chốt số lượng vào cửa, nghiệm thu hợp đồng', 'dept': 'Tài chính - VPTD', 'phone': get_phone('Lương Tú Anh', '0974 951 992')}
        ]
    }
    vehicles.append(v_coord)
    for r in r_coord:
        r['vehicleId'] = v_coord['id']
        r['vehicleLabel'] = v_coord['label']
        r['captainName'] = v_coord['captain']['name']
        r['captainPhone'] = v_coord['captain']['phone']

    # =========================================================================
    # 5. XE RIÊNG TEAM BAN SỰ KIỆN BTC (XE 16 CHỖ RIÊNG)
    # Ban Sự Kiện gồm 7 người: Lê Đức Tuấn Định (5011) + 6 cán bộ Marketing
    # Bố trí Xe 16 chỗ rộng rãi để chở 7 cán bộ cùng trang thiết bị flycam, máy quay, máy ảnh, backdrop sự kiện!
    # Không có VĐV kiêm lái xe -> có lái xe hợp đồng phục vụ riêng (7 khách / 16 chỗ)
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
        'label': 'Xe Ban Sự Kiện - Team Sự Kiện & Media BTC (16 chỗ)',
        'type': 'Xe 16 chỗ riêng',
        'capacity': 16,
        'paxCount': 7, # 7 cán bộ Ban Sự Kiện (chở thêm máy quay, flycam, thiết bị media)
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
        'note': 'Xe 16 chỗ riêng phục vụ Ban Sự kiện và Ekip Media gồm 7 người: Lê Đức Tuấn Định (Trưởng phòng Thiết kế - kiêm VĐV 5km), Nguyễn Huy Quỳnh, Phạm Hoàng Hiệp, Trần Hồng Hạnh, Nguyễn Thị Vân Anh, Võ Tuấn Dương, Vũ Thị Hoàng Nhung. Xe chở toàn bộ máy quay, flycam và đạo cụ sự kiện.',
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
        'pickupLoc': 'Theo kế hoạch của Cienco5 & DHE',
        'destLoc': 'Sân Golf Tràng An & Resort',
        'returnTime': 'Tự túc phương tiện',
        'captain': {
            'name': 'Phạm Thị Hương (Cienco5) & Trần Xuân Dương (DHE)',
            'title': 'Đại diện Lãnh đạo Đơn vị',
            'unit': 'Cienco5 & Thang máy DHE',
            'phone': 'Nội bộ đơn vị'
        },
        'bibRange': '15 VĐV Cienco5 & DHE',
        'distance': 'Đơn vị tự di chuyển (5km, 10km & 15km)',
        'note': 'Toàn bộ VĐV thuộc Công ty Cổ phần Xây dựng Cienco 5 và Công ty Thang máy DHE tự túc phương tiện di chuyển đến giải chạy Fun Run.',
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
    # 8. CÁC XE 45 CHỖ (XE #01 ĐẾN XE #08) - CỰ LY 5KM (342 VĐV)
    # 6 xe chở 43 VĐV + 2 xe chở 42 VĐV = 342 VĐV (Mỗi xe có 1 Trưởng xe BTC)
    # =========================================================================
    captains_45 = [
        {'name': 'Hoàng Thanh Hải', 'title': 'Giám đốc Vận hành', 'dept': 'Operation - VPTD', 'phone': get_phone('Hoàng Thanh Hải', '0982 054 788')},
        {'name': 'Dương Thị Hải Anh', 'title': 'Trưởng phòng Nhân sự', 'dept': 'Nhân sự - VPTD', 'phone': get_phone('Dương Thị Hải Anh', '0982 821 654')},
        {'name': 'Nguyễn Thu Mai', 'title': 'Trưởng phòng Hành chính', 'dept': 'Hành chính - VPTD', 'phone': get_phone('Nguyễn Thu Mai', '0918 816 891')},
        {'name': 'Nguyễn Thái Mỹ', 'title': 'Phó Giám đốc Kỹ thuật', 'dept': 'Kỹ thuật - VPTD', 'phone': get_phone('Nguyễn Thái Mỹ', '0362 109 907')},
        {'name': 'Nguyễn Duy Hoạt', 'title': 'Trưởng phòng Kế toán', 'dept': 'Tài chính Kế toán - VPTD', 'phone': get_phone('Nguyễn Duy Hoạt', '0916 464 029')},
        {'name': 'Phạm Minh Hiếu', 'title': 'Trưởng nhóm Kiểm soát nội bộ', 'dept': 'Ban KSCL - VPTD', 'phone': get_phone('Phạm Minh Hiếu', '0979 140 391')},
        {'name': 'Trần Đình Thông', 'title': 'Trưởng phòng Pháp chế', 'dept': 'Pháp chế - VPTD', 'phone': get_phone('Trần Đình Thông', '0912 177 998')},
        {'name': 'Võ Thị Mai Trang', 'title': 'Phó Ban Quản lý Nhà hàng', 'dept': 'Ẩm thực - VPTD', 'phone': get_phone('Võ Thị Mai Trang', '0974 899 868')},
    ]

    # Phân bổ 342 VĐV cho 8 xe:
    # Xe 1-6: 43 VĐV
    # Xe 7-8: 42 VĐV
    bus_slices = [
        (0, 43),
        (43, 86),
        (86, 129),
        (129, 172),
        (172, 215),
        (215, 258),
        (258, 300),
        (300, 342)
    ]

    for idx, (st, en) in enumerate(bus_slices, start=1):
        bus_runners = regular_5k[st:en]
        cpt = captains_45[idx - 1]
        v_bus = {
            'id': f'XE-{idx:02d}',
            'code': f'XE-{idx:02d}',
            'label': f'Xe #{idx:02d} (45 chỗ)',
            'type': 'Xe 45 chỗ',
            'capacity': 45,
            'paxCount': len(bus_runners) + 1, # VĐV + Trưởng xe BTC (chừa ghế cho lái xe)
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
            'bibRange': f"BIB {bus_runners[0]['bib']} – {bus_runners[-1]['bib']}",
            'distance': '5km',
            'note': f"Khối VĐV 5km ({len(bus_runners)} VĐV + Trưởng xe BTC {cpt['name']} đi cùng xe). Lái xe hợp đồng phục vụ.",
            'runners': bus_runners,
            'btcStaff': [
                {
                    'name': cpt['name'],
                    'title': cpt['title'],
                    'dept': cpt['dept'],
                    'duty': f"Trưởng xe #{idx:02d} phụ trách điểm danh và hướng dẫn đoàn VĐV",
                    'phone': cpt['phone'],
                    'isCaptain': True
                }
            ]
        }
        vehicles.append(v_bus)
        for r in bus_runners:
            r['vehicleId'] = v_bus['id']
            r['vehicleLabel'] = v_bus['label']
            r['captainName'] = cpt['name']
            r['captainPhone'] = cpt['phone']

    # =========================================================================
    # 9. XE #09 (XE 16 CHỖ) - CỰ LY 10KM
    # YÊU CẦU: Không có VĐV là lái xe kiêm thì phải chừa 1 ghế cho lái xe!
    # Không thể xếp tối đa 16/16 được -> Chỉ xếp 14 VĐV + 1 Trưởng xe = 15/16 chỗ!
    # =========================================================================
    group_10k_14 = regular_10k[:14] # 14 VĐV 10km (từ 10002 đến 10016)
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
        'paxCount': len(group_10k_14) + 1, # 14 VĐV + 1 Trưởng xe = 15 người (chừa 1 ghế cho lái xe hợp đồng)
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
        'bibRange': f"BIB {group_10k_14[0]['bib']} – {group_10k_14[-1]['bib']}",
        'distance': '10km',
        'note': f"Đội VĐV 10km gồm 14 VĐV và Trưởng xe BTC Phạm Hà An (Tổng 15 người, chừa 1 ghế cho lái xe hợp đồng phục vụ).",
        'runners': group_10k_14,
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
    for r in group_10k_14:
        r['vehicleId'] = v_09['id']
        r['vehicleLabel'] = v_09['label']
        r['captainName'] = cpt_09['name']
        r['captainPhone'] = cpt_09['phone']

    # =========================================================================
    # 10. CÁC XE 7 CHỖ CÓ VĐV KIÊM LÁI XE (XE #10 ĐẾN XE #15)
    # Vì chính VĐV kiêm lái xe ngồi ở ghế lái nên được xếp đủ 7/7 chỗ!
    # =========================================================================

    # --- XE #10 (7 CHỖ): Lái xe Trần Văn Tuân (5194 - MT Cửa Lò) ---
    r_driver_10 = runners_dict[5194]
    group_10k_10 = regular_10k[14:19] # 5 VĐV 10km (10019 đến 10023)
    cpt_10 = {
        'name': 'Đoàn Thế Cương',
        'title': 'Phó phòng Quản trị & Đầu tư',
        'dept': 'Quản trị - VPTD',
        'phone': get_phone('Đoàn Thế Cương', '0912 211 929'),
        'duty': 'Trưởng xe #10 & Điều phối VĐV 10km'
    }
    v_10 = {
        'id': 'XE-10',
        'code': 'XE-10',
        'label': 'Xe #10 (7 chỗ)',
        'type': 'Xe 7 chỗ',
        'capacity': 7,
        'paxCount': len(group_10k_10) + 2, # 5 VĐV 10k + 1 Trưởng xe + 1 Lái xe kiêm VĐV = 7 (VĐV tự lái đủ 7/7)
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
        'bibRange': f"BIB 5194, {group_10k_10[0]['bib']} – {group_10k_10[-1]['bib']}",
        'distance': '10km (kèm Lái xe kiêm VĐV 5km)',
        'note': f"Xe 7 chỗ. Trưởng xe: Đoàn Thế Cương (VPTĐ). Lái xe kiêm VĐV tự lái: Trần Văn Tuân (BIB 5194 - MT Cửa Lò). Chở 5 VĐV cự ly 10km.",
        'runners': [r_driver_10] + group_10k_10,
        'btcStaff': [
            {
                'name': cpt_10['name'],
                'title': cpt_10['title'],
                'dept': cpt_10['dept'],
                'duty': cpt_10['duty'],
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

    # --- XE #11 (7 CHỖ): Lái xe Lương Trung Thành (5284 - MT Diễn Châu) ---
    r_driver_11 = runners_dict[5284]
    group_10k_11 = regular_10k[19:25] # 6 VĐV 10km (10024 đến 10029, trong đó 10026 là Trưởng xe Nguyễn Bá Lãm)
    cpt_11 = {
        'name': 'Nguyễn Bá Lãm',
        'title': 'Trưởng phòng Kiểm soát Doanh thu (kiêm VĐV 10km)',
        'dept': 'Văn phòng Tập đoàn Mường Thanh',
        'phone': get_phone('Nguyễn Bá Lãm', '0986 670 418'),
        'duty': 'Trưởng xe #11 phụ trách đoàn VĐV 10km'
    }
    v_11 = {
        'id': 'XE-11',
        'code': 'XE-11',
        'label': 'Xe #11 (7 chỗ)',
        'type': 'Xe 7 chỗ',
        'capacity': 7,
        'paxCount': len(group_10k_11) + 1, # 1 Lái xe kiêm VĐV (Thành 5284) + 6 VĐV (gồm Trưởng xe Lãm 10026) = 7/7
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
        'bibRange': f"BIB 5284, {group_10k_11[0]['bib']} – {group_10k_11[-1]['bib']}",
        'distance': '10km (kèm Lái xe kiêm VĐV 5km)',
        'note': f"Xe 7 chỗ. Trưởng xe: Nguyễn Bá Lãm (Trưởng phòng Kiểm soát Doanh thu - VPTĐ, kiêm VĐV 10km BIB 10026). Lái xe kiêm VĐV tự lái: Lương Trung Thành (BIB 5284 - MT Diễn Châu). Chở 6 VĐV 10km.",
        'runners': [r_driver_11] + group_10k_11,
        'btcStaff': [
            {
                'name': cpt_11['name'],
                'title': cpt_11['title'],
                'dept': cpt_11['dept'],
                'duty': cpt_11['duty'],
                'phone': cpt_11['phone'],
                'isCaptain': True
            }
        ]
    }
    vehicles.append(v_11)
    for r in v_11['runners']:
        r['vehicleId'] = v_11['id']
        r['vehicleLabel'] = v_11['label']
        r['captainName'] = cpt_11['name']
        r['captainPhone'] = cpt_11['phone']

    # --- XE #12 (7 CHỖ): Lái xe Lê Văn Chiến (5302 - MT Luxury Sông Hàn) ---
    r_driver_12 = runners_dict[5302]
    group_15k_a = regular_15k[:5] # 5 VĐV 15k (15001, 15002, 15004 Ms. Thơ, 15006, 15007)
    cpt_12 = {
        'name': 'Đào Minh Anh',
        'title': 'Trưởng phòng Marketing',
        'dept': 'Marketing - VPTD',
        'phone': get_phone('Đào Minh Anh', '0366 700 935'),
        'duty': 'Trưởng xe #12 phụ trách đoàn 15km'
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
        'distance': '15km (kèm Lái xe kiêm VĐV 5km)',
        'note': f"Xe 7 chỗ. Trưởng xe: Đào Minh Anh (Trưởng phòng Marketing - VPTĐ). Lái xe kiêm VĐV tự lái: Lê Văn Chiến (BIB 5302 - MT Luxury Sông Hàn). Chở 5 VĐV 15km (bao gồm Ms. Lê Thị Thơ - Siêu thị Mường Thanh).",
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

    # --- XE #13 (7 CHỖ): Lái xe Đoàn Công Anh Tú (5315 - MT Grand Quảng Nam) ---
    r_driver_13 = runners_dict[5315]
    group_15k_b = regular_15k[5:10] # 5 runners 15k (15009 đến 15013)
    cpt_13 = {
        'name': 'Hoàng Kim Chính',
        'title': 'Trưởng phòng Quản lý dự án',
        'dept': 'Ban QLDA - VPTD',
        'phone': get_phone('Hoàng Kim Chính', '0985 434 292'),
        'duty': 'Trưởng xe #13 phụ trách đoàn 15km'
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
        'note': f"Xe 7 chỗ. Trưởng xe: Hoàng Kim Chính (Trưởng phòng QLDA - VPTĐ). Lái xe kiêm VĐV tự lái: Đoàn Công Anh Tú (BIB 5315 - MT Grand Quảng Nam). Chở 5 VĐV 15km.",
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

    # --- XE #14 (7 CHỖ): Lái xe Trần Quang Lợi (5322 - MT Luxury Vientiane) ---
    r_driver_14 = runners_dict[5322]
    group_15k_c = regular_15k[10:15] # 5 runners 15k (15014 đến 15018)
    cpt_14 = {
        'name': 'Trần Đại Nghĩa',
        'title': 'Trưởng phòng Kiểm toán nội bộ',
        'dept': 'Văn phòng Tập đoàn Mường Thanh',
        'phone': get_phone('Trần Đại Nghĩa', '0987 379 398'),
        'duty': 'Trưởng xe #14 phụ trách đoàn 15km'
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

    # --- XE #15 (7 CHỖ): Lái xe Nguyễn Minh Khoa (5349 - MT Grand Lào Cai) ---
    # Chở 2 VĐV 10km còn lại (10030, 10031) + 4 VĐV 15km còn lại (15019, 15020, 15021, 15022)
    # Lái xe kiêm VĐV 5349 tự lái kiêm Trưởng xe phụ trách nhóm = đúng 7/7 VĐV!
    r_driver_15 = runners_dict[5349]
    group_10k_rem = regular_10k[25:] # 2 VĐV 10k (10030, 10031)
    group_15k_rem = regular_15k[15:] # 4 VĐV 15k (15019, 15020, 15021, 15022)
    all_runners_15 = [r_driver_15] + group_10k_rem + group_15k_rem

    cpt_15 = {
        'name': 'Nguyễn Minh Hiếu',
        'title': 'Huấn luyện viên Thể hình (BTC Khởi động)',
        'dept': 'Văn phòng Tập đoàn Mường Thanh',
        'phone': get_phone('Phạm Minh Hiếu', '0979 140 391'),
        'duty': 'Trưởng xe #15 phụ trách đoàn VĐV'
    }
    v_15 = {
        'id': 'XE-15',
        'code': 'XE-15',
        'label': 'Xe #15 (7 chỗ)',
        'type': 'Xe 7 chỗ',
        'capacity': 7,
        'paxCount': len(all_runners_15), # 1 Lái xe kiêm VĐV 5349 + 2 VĐV 10k + 4 VĐV 15k = 7/7 VĐV tự lái
        'departTime': '05:00',
        'pickupLoc': 'Sảnh Khách sạn Mường Thanh Luxury Ninh Bình',
        'destLoc': 'Sân Golf Tràng An & Resort',
        'returnTime': '11:00',
        'captain': {
            'name': cpt_15['name'],
            'title': cpt_15['title'],
            'unit': cpt_15['dept'],
            'phone': cpt_15['phone']
        },
        'driver': {
            'name': r_driver_15['name'],
            'bib': r_driver_15['bib'],
            'unit': r_driver_15['unit'],
            'phone': r_driver_15['phone'],
            'role': 'Lái xe kiêm VĐV chạy 5km'
        },
        'bibRange': f"BIB 5349, 10030, 10031, {group_15k_rem[0]['bib']} – {group_15k_rem[-1]['bib']}",
        'distance': '10km & 15km (kèm Lái xe kiêm VĐV 5km)',
        'note': f"Xe 7 chỗ. Trưởng đoàn phụ trách: Nguyễn Minh Hiếu (HLV Thể hình VPTĐ). Lái xe kiêm VĐV tự lái: Nguyễn Minh Khoa (BIB 5349 - MT Grand Lào Cai). Chở 2 VĐV 10km và 4 VĐV 15km.",
        'runners': all_runners_15,
        'btcStaff': [
            {
                'name': cpt_15['name'],
                'title': cpt_15['title'],
                'dept': cpt_15['dept'],
                'duty': cpt_15['duty'],
                'phone': cpt_15['phone'],
                'isCaptain': True
            }
        ]
    }
    vehicles.append(v_15)
    for r in all_runners_15:
        r['vehicleId'] = v_15['id']
        r['vehicleLabel'] = v_15['label']
        r['captainName'] = cpt_15['name']
        r['captainPhone'] = cpt_15['phone']

    # =========================================================================
    # 11. XE #16-YTE (7 CHỖ) - TỔ Y TẾ BỆNH VIỆN PHỦ DIỄN
    # Không có VĐV kiêm lái xe -> chừa 1 ghế cho lái xe thuê ngoài (4 khách / 7 chỗ)
    # Trưởng xe: Nguyễn Thị Lan (Trưởng nhóm Nhân sự - VPTD: 0977 760 567)
    # Chở: 3 Bác sĩ (BS Lê Kim Vũ, BS Võ Thị Mai Anh, BS Quang Tuấn Anh)
    # Trống 2 ghế sau để cáng thương, túi thuốc cấp cứu và bình oxy
    # =========================================================================
    cpt_yte = {
        'name': 'Nguyễn Thị Lan',
        'title': 'Trưởng nhóm Nhân sự (BTC Hậu cần Y tế)',
        'dept': 'Nhân sự - VPTD',
        'phone': get_phone('Nguyễn Thị Lan', '0977 760 567'),
        'duty': 'Trưởng xe Y tế & Phụ trách điều phối cứu thương'
    }
    v_yte = {
        'id': 'XE-16-YTE',
        'code': 'XE-16-YTE',
        'label': 'Xe #16 - Tổ Y Tế BV Phủ Diễn (7 chỗ)',
        'type': 'Xe 7 chỗ',
        'capacity': 7,
        'paxCount': 4, # 1 Trưởng xe BTC + 3 Bác sĩ (chừa 1 ghế cho lái xe thuê ngoài và khoang y tế)
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
        'bibRange': 'Tổ Y Tế & Cứu Thương',
        'distance': 'Y tế & Cấp cứu đường chạy',
        'note': f"Xe 7 chỗ chuyên dụng y tế. Trưởng xe phụ trách: Nguyễn Thị Lan (Trưởng nhóm Nhân sự Văn phòng Tập đoàn). Chở 3 Bác sĩ Bệnh viện Phủ Diễn (BS Lê Kim Vũ, BS Võ Thị Mai Anh, BS Quang Tuấn Anh) cùng cáng thương và thiết bị sơ cấp cứu. Lái xe hợp đồng phục vụ.",
        'runners': [],
        'btcStaff': [
            {'name': cpt_yte['name'], 'title': cpt_yte['title'], 'dept': cpt_yte['dept'], 'duty': cpt_yte['duty'], 'phone': cpt_yte['phone'], 'isCaptain': True},
            {'name': 'BS Lê Kim Vũ', 'title': 'Bác sỹ BV Phủ Diễn', 'dept': 'Y tế', 'duty': 'Trạm Y tế 0 (Start/Finish)', 'phone': '0912 345 678'},
            {'name': 'BS Võ Thị Mai Anh', 'title': 'Bác sỹ BV Phủ Diễn', 'dept': 'Y tế', 'duty': 'Trạm Y tế 1 (Km 2.3)'},
            {'name': 'BS Quang Tuấn Anh', 'title': 'Bác sỹ BV Phủ Diễn', 'dept': 'Y tế', 'duty': 'Trạm Y tế 2 (Km 4.1)'}
        ]
    }
    vehicles.append(v_yte)

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

    # 5. Parse and update BTC Staff (including Lương Tú Anh)
    s_btc = wb['BTC Chạy']
    btc_staff_list = []
    for r in s_btc.iter_rows(min_row=6, values_only=True):
        if r[2] is None:
            continue
        name = str(r[2] or '').strip()
        stt = r[0]
        dept = str(r[1] or '').strip()
        title = str(r[3] or '').strip()
        reg = str(r[4] or '').strip()
        duty = str(r[5] or '').strip()
        note = str(r[6] or '').strip()
        
        # If duty is empty (like row 41), use note
        if not duty and note:
            duty = note

        early = (len(r) > 7 and r[7] == 'x')
        radio = str(r[8] or '').strip() if len(r) > 8 and r[8] is not None else ''

        phone = get_phone(name, '')
        if name == 'Lê Thị Hoàng Yến':
            phone = ''

        btc_staff_list.append({
            'stt': stt,
            'dept': dept,
            'name': name,
            'title': title,
            'reg': reg,
            'duty': duty,
            'note': note,
            'phone': phone,
            'early': early,
            'radio': radio
        })
    print(f"Total BTC staff loaded (gồm Lương Tú Anh): {len(btc_staff_list)}")

    # 6. Save to data.json
    with open('data.json', 'r', encoding='utf-8') as f:
        full_data = json.load(f)

    full_data['funrun']['vehicles'] = vehicles
    full_data['funrun']['runners'] = list(runners_dict.values())
    full_data['funrun']['btcStaff'] = btc_staff_list

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(full_data, f, ensure_ascii=False, indent=2)

    print("Successfully updated data.json with 23 vehicles and 40 BTC staff!")

if __name__ == '__main__':
    rebuild_funrun()
