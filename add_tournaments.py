import sys, json

sys.stdout.reconfigure(encoding='utf-8')

# Build the complete tournaments list
tournaments = [
    # ============================================================
    # 1. BÓNG ĐÁ NAM (8 ĐỘI) - KNOCKOUT 8
    # ============================================================
    {
        'id': 'bd_m',
        'name': 'Bóng đá Nam (8 đội)',
        'sport': 'Bóng đá',
        'code': 'BĐ.M',
        'color': '#15803d',
        'format': 'knockout8',
        'scoreLabel': 'Bàn thắng',
        'rules': 'Bốc thăm chia cặp 8 đội, thi đấu loại trực tiếp (2 hiệp 25p). Đội thắng Tứ kết vào Bán kết. Đội thắng Bán kết vào Chung kết tranh 1-2, đội thua Bán kết tranh 3-4.',
        'rounds': [
            {
                'id': 'tk',
                'name': 'TỨ KẾT',
                'matches': [
                    {
                        'id': 'BD.M.TK1',
                        'name': 'Tứ kết 1',
                        'team1': {'code': 'LQ.HLO', 'name': 'LQ.HLO', 'sub': 'SMO-HLC-HLR'},
                        'team2': {'code': 'LQ.NTR', 'name': 'LQ.NTR', 'sub': 'VTR-NTR-CCNTrang'},
                        'time': '15:00 27/10',
                        'venue': 'BĐ.Sân 02',
                        'nextWin': 'BD.M.BK1',
                        'nextWinSlot': 1
                    },
                    {
                        'id': 'BD.M.TK2',
                        'name': 'Tứ kết 2',
                        'team1': {'code': 'LQ.HNO', 'name': 'LQ.HNO', 'sub': 'XLA-HNC-HNO'},
                        'team2': {'code': 'LQ.Vinh', 'name': 'LQ.Vinh', 'sub': 'LQ.Vinh'},
                        'time': '15:00 27/10',
                        'venue': 'BĐ.Sân 03',
                        'nextWin': 'BD.M.BK1',
                        'nextWinSlot': 2
                    },
                    {
                        'id': 'BD.M.TK3',
                        'name': 'Tứ kết 3',
                        'team1': {'code': 'LQ.SLA', 'name': 'LQ.SLA', 'sub': 'SLA-MCH'},
                        'team2': {'code': 'Cienco5', 'name': 'Cienco5 và DHE', 'sub': 'Cienco5-DHE'},
                        'time': '15:00 27/10',
                        'venue': 'BĐ.Sân 02',
                        'nextWin': 'BD.M.BK2',
                        'nextWinSlot': 1
                    },
                    {
                        'id': 'BD.M.TK4',
                        'name': 'Tứ kết 4',
                        'team1': {'code': 'CTH', 'name': 'MT Cần Thơ', 'sub': 'CTH'},
                        'team2': {'code': 'ĐNA', 'name': 'MT Đà Nẵng', 'sub': 'DNA'},
                        'time': '15:00 27/10',
                        'venue': 'BĐ.Sân 03',
                        'nextWin': 'BD.M.BK2',
                        'nextWinSlot': 2
                    }
                ]
            },
            {
                'id': 'bk',
                'name': 'BÁN KẾT',
                'matches': [
                    {
                        'id': 'BD.M.BK1',
                        'name': 'Bán kết 1',
                        'time': '16:00 28/10',
                        'venue': 'BĐ.Sân 01',
                        'source1': 'Thắng TK1',
                        'source2': 'Thắng TK2',
                        'nextWin': 'BD.M.CK',
                        'nextWinSlot': 1,
                        'nextLose': 'BD.M.3-4',
                        'nextLoseSlot': 1
                    },
                    {
                        'id': 'BD.M.BK2',
                        'name': 'Bán kết 2',
                        'time': '16:00 28/10',
                        'venue': 'BĐ.Sân 03',
                        'source1': 'Thắng TK3',
                        'source2': 'Thắng TK4',
                        'nextWin': 'BD.M.CK',
                        'nextWinSlot': 2,
                        'nextLose': 'BD.M.3-4',
                        'nextLoseSlot': 2
                    }
                ]
            },
            {
                'id': 'fn',
                'name': 'CHUNG KẾT & TRANH 3-4',
                'matches': [
                    {
                        'id': 'BD.M.CK',
                        'name': 'Chung Kết (Tranh 1-2)',
                        'time': '08:00 29/10',
                        'venue': 'BĐ.Sân 01',
                        'isFinal': True,
                        'source1': 'Thắng BK1',
                        'source2': 'Thắng BK2'
                    },
                    {
                        'id': 'BD.M.3-4',
                        'name': 'Tranh Hạng 3 - 4',
                        'time': '07:00 29/10',
                        'venue': 'BĐ.Sân 01',
                        'isThirdPlace': True,
                        'source1': 'Thua BK1',
                        'source2': 'Thua BK2'
                    }
                ]
            }
        ]
    },

    # ============================================================
    # 2. CẦU LÔNG ĐÔI NAM (8 ĐÔI) - KNOCKOUT 8
    # ============================================================
    {
        'id': 'cl_2m',
        'name': 'Cầu lông Đôi Nam (8 cặp)',
        'sport': 'Cầu lông',
        'code': 'CL.2M',
        'color': '#dc2626',
        'format': 'knockout8',
        'scoreLabel': 'Tỉ số séc',
        'rules': 'Bốc thăm chia cặp 8 đôi, loại trực tiếp tranh 1-2-3-4 (3 hiệp thắng 2, chạm 15đ ăn điểm trực tiếp). Thắng TK vào BK; Thắng BK vào CK tranh 1-2, thua BK tranh 3-4.',
        'rounds': [
            {
                'id': 'tk',
                'name': 'TỨ KẾT',
                'matches': [
                    {
                        'id': 'CL.2M.TK1',
                        'name': 'Tứ kết 1',
                        'team1': {'code': 'QTR', 'name': 'Nguyễn Lực - Trần Đức Tâm', 'sub': 'MT Quảng Trị'},
                        'team2': {'code': 'HNC', 'name': 'Ngô Văn Thơi - Triệu Minh Hiếu', 'sub': 'MT Hà Nội Center'},
                        'time': '14:00 27/10',
                        'venue': 'CL.Sân 01',
                        'nextWin': 'CL.2M.BK1',
                        'nextWinSlot': 1
                    },
                    {
                        'id': 'CL.2M.TK2',
                        'name': 'Tứ kết 2',
                        'team1': {'code': 'CCHN', 'name': 'Bùi Gia Đức - Nguyễn Hồng Hiệp', 'sub': 'Cụm CC Hà Nội'},
                        'team2': {'code': 'SHA', 'name': 'Dương Thanh Tú - Huỳnh Tăng Vĩnh', 'sub': 'MT Sông Hàn'},
                        'time': '14:00 27/10',
                        'venue': 'CL.Sân 02',
                        'nextWin': 'CL.2M.BK1',
                        'nextWinSlot': 2
                    },
                    {
                        'id': 'CL.2M.TK3',
                        'name': 'Tứ kết 3',
                        'team1': {'code': 'NTC', 'name': 'Lê Đức Công - Nguyễn Thiện Cung', 'sub': 'MT Nha Trang Centre'},
                        'team2': {'code': 'CCHN', 'name': 'Phạm Ngọc Hanh - Nguyễn Văn Linh', 'sub': 'Cụm CC Hà Nội'},
                        'time': '14:00 27/10',
                        'venue': 'CL.Sân 03',
                        'nextWin': 'CL.2M.BK2',
                        'nextWinSlot': 1
                    },
                    {
                        'id': 'CL.2M.TK4',
                        'name': 'Tứ kết 4',
                        'team1': {'code': 'BMT', 'name': 'Nguyễn Trọng Vinh - Nguyễn Văn Chí', 'sub': 'MT Buôn Ma Thuột'},
                        'team2': {'code': 'ĐNA', 'name': 'Phan Tá Hùng - Nguyễn Lương Hoàng', 'sub': 'MT Đà Nẵng'},
                        'time': '14:00 27/10',
                        'venue': 'CL.Sân 04',
                        'nextWin': 'CL.2M.BK2',
                        'nextWinSlot': 2
                    }
                ]
            },
            {
                'id': 'bk',
                'name': 'BÁN KẾT',
                'matches': [
                    {
                        'id': 'CL.2M.BK1',
                        'name': 'Bán kết 1',
                        'time': '08:00 29/10',
                        'venue': 'CL.Sân 01',
                        'source1': 'Thắng TK1',
                        'source2': 'Thắng TK2',
                        'nextWin': 'CL.2M.CK',
                        'nextWinSlot': 1,
                        'nextLose': 'CL.2M.Ba-Tư',
                        'nextLoseSlot': 1
                    },
                    {
                        'id': 'CL.2M.BK2',
                        'name': 'Bán kết 2',
                        'time': '08:00 29/10',
                        'venue': 'CL.Sân 02',
                        'source1': 'Thắng TK3',
                        'source2': 'Thắng TK4',
                        'nextWin': 'CL.2M.CK',
                        'nextWinSlot': 2,
                        'nextLose': 'CL.2M.Ba-Tư',
                        'nextLoseSlot': 2
                    }
                ]
            },
            {
                'id': 'fn',
                'name': 'CHUNG KẾT & TRANH 3-4',
                'matches': [
                    {
                        'id': 'CL.2M.CK',
                        'name': 'Chung Kết (Tranh 1-2)',
                        'time': '09:00 29/10',
                        'venue': 'CL.Sân 02',
                        'isFinal': True,
                        'source1': 'Thắng BK1',
                        'source2': 'Thắng BK2'
                    },
                    {
                        'id': 'CL.2M.Ba-Tư',
                        'name': 'Tranh Hạng 3 - 4',
                        'time': '09:00 29/10',
                        'venue': 'CL.Sân 01',
                        'isThirdPlace': True,
                        'source1': 'Thua BK1',
                        'source2': 'Thua BK2'
                    }
                ]
            }
        ]
    },

    # ============================================================
    # 3. CẦU LÔNG ĐÔI NỮ (8 ĐÔI) - KNOCKOUT 8
    # ============================================================
    {
        'id': 'cl_2f',
        'name': 'Cầu lông Đôi Nữ (8 cặp)',
        'sport': 'Cầu lông',
        'code': 'CL.2F',
        'color': '#f43f5e',
        'format': 'knockout8',
        'scoreLabel': 'Tỉ số séc',
        'rules': 'Bốc thăm chia cặp 8 đôi, loại trực tiếp tranh 1-2-3-4 (3 hiệp thắng 2, chạm 15đ). Thắng TK vào BK; Thắng BK vào CK tranh 1-2, thua BK tranh 3-4.',
        'rounds': [
            {
                'id': 'tk',
                'name': 'TỨ KẾT',
                'matches': [
                    {
                        'id': 'CL.2F.TK1',
                        'name': 'Tứ kết 1',
                        'team1': {'code': 'Cienco5', 'name': 'Trương Thị Tuyết - Nguyễn Thị Thu Hằng', 'sub': 'Cienco5 và DHE'},
                        'team2': {'code': 'SGO', 'name': 'Trịnh Thị Lan Hương - Phan Ngọc Kiều', 'sub': 'MT Sài Gòn'},
                        'time': '14:00 27/10',
                        'venue': 'CL.Sân 01',
                        'nextWin': 'CL.2F.BK1',
                        'nextWinSlot': 1
                    },
                    {
                        'id': 'CL.2F.TK2',
                        'name': 'Tứ kết 2',
                        'team1': {'code': 'VRC', 'name': 'Lỗ Thị Thúy An - Phan Thảo Nam', 'sub': 'VRC'},
                        'team2': {'code': 'TQU', 'name': 'Vũ Linh Chi - Hoàng Kiều Trinh', 'sub': 'MT Tuyên Quang'},
                        'time': '14:00 27/10',
                        'venue': 'CL.Sân 02',
                        'nextWin': 'CL.2F.BK1',
                        'nextWinSlot': 2
                    },
                    {
                        'id': 'CL.2F.TK3',
                        'name': 'Tứ kết 3',
                        'team1': {'code': 'HLO', 'name': 'Vũ Thị Phượng - Lê Ngọc Mai', 'sub': 'MT Hạ Long'},
                        'team2': {'code': 'SHA', 'name': 'Lê Thị Mai - Tô Thị Trâm Anh', 'sub': 'MT Sông Hàn'},
                        'time': '14:00 27/10',
                        'venue': 'CL.Sân 03',
                        'nextWin': 'CL.2F.BK2',
                        'nextWinSlot': 1
                    },
                    {
                        'id': 'CL.2F.TK4',
                        'name': 'Tứ kết 4',
                        'team1': {'code': 'QTR', 'name': 'Lê Thị Kim Chi - Nguyễn Thị Thu Thuỷ', 'sub': 'MT Quảng Trị'},
                        'team2': {'code': 'TQU', 'name': 'Trần Thị Trang - Lê Thị Phương', 'sub': 'MT Tuyên Quang'},
                        'time': '14:00 27/10',
                        'venue': 'CL.Sân 04',
                        'nextWin': 'CL.2F.BK2',
                        'nextWinSlot': 2
                    }
                ]
            },
            {
                'id': 'bk',
                'name': 'BÁN KẾT',
                'matches': [
                    {
                        'id': 'CL.2F.BK1',
                        'name': 'Bán kết 1',
                        'time': '08:00 29/10',
                        'venue': 'CL.Sân 03',
                        'source1': 'Thắng TK1',
                        'source2': 'Thắng TK2',
                        'nextWin': 'CL.2F.CK',
                        'nextWinSlot': 1,
                        'nextLose': 'CL.2F.Ba-Tư',
                        'nextLoseSlot': 1
                    },
                    {
                        'id': 'CL.2F.BK2',
                        'name': 'Bán kết 2',
                        'time': '08:00 29/10',
                        'venue': 'CL.Sân 04',
                        'source1': 'Thắng TK3',
                        'source2': 'Thắng TK4',
                        'nextWin': 'CL.2F.CK',
                        'nextWinSlot': 2,
                        'nextLose': 'CL.2F.Ba-Tư',
                        'nextLoseSlot': 2
                    }
                ]
            },
            {
                'id': 'fn',
                'name': 'CHUNG KẾT & TRANH 3-4',
                'matches': [
                    {
                        'id': 'CL.2F.CK',
                        'name': 'Chung Kết (Tranh 1-2)',
                        'time': '09:00 29/10',
                        'venue': 'CL.Sân 04',
                        'isFinal': True,
                        'source1': 'Thắng BK1',
                        'source2': 'Thắng BK2'
                    },
                    {
                        'id': 'CL.2F.Ba-Tư',
                        'name': 'Tranh Hạng 3 - 4',
                        'time': '09:00 29/10',
                        'venue': 'CL.Sân 03',
                        'isThirdPlace': True,
                        'source1': 'Thua BK1',
                        'source2': 'Thua BK2'
                    }
                ]
            }
        ]
    },

    # ============================================================
    # 4. CẦU LÔNG ĐƠN NAM (8 VĐV) - KNOCKOUT 8
    # ============================================================
    {
        'id': 'cl_m',
        'name': 'Cầu lông Đơn Nam (8 VĐV)',
        'sport': 'Cầu lông',
        'code': 'CL.M',
        'color': '#ef4444',
        'format': 'knockout8',
        'scoreLabel': 'Tỉ số séc',
        'rules': 'Bốc thăm chia cặp 8 VĐV, loại trực tiếp tranh 1-2-3-4 (3 hiệp thắng 2, chạm 15đ).',
        'rounds': [
            {
                'id': 'tk',
                'name': 'TỨ KẾT',
                'matches': [
                    {
                        'id': 'CL.M.TK1',
                        'name': 'Tứ kết 1',
                        'team1': {'code': 'VRC', 'name': 'Nguyễn Quang Đạt', 'sub': 'VRC'},
                        'team2': {'code': 'CCHN', 'name': 'Nguyễn Mạnh Cường', 'sub': 'Cụm CC Hà Nội'},
                        'time': '15:00 27/10',
                        'venue': 'CL.Sân 01',
                        'nextWin': 'CL.M.BK1',
                        'nextWinSlot': 1
                    },
                    {
                        'id': 'CL.M.TK2',
                        'name': 'Tứ kết 2',
                        'team1': {'code': 'HNC', 'name': 'Ngô Văn Thơi', 'sub': 'MT Hà Nội Center'},
                        'team2': {'code': 'ĐLA', 'name': 'Nguyễn Hải Triều', 'sub': 'MT Đà Lạt'},
                        'time': '15:00 27/10',
                        'venue': 'CL.Sân 02',
                        'nextWin': 'CL.M.BK1',
                        'nextWinSlot': 2
                    },
                    {
                        'id': 'CL.M.TK3',
                        'name': 'Tứ kết 3',
                        'team1': {'code': 'HUE', 'name': 'Phạm Quang Huy', 'sub': 'MT Huế'},
                        'team2': {'code': 'CCHN', 'name': 'Nguyễn Hồng Hiệp', 'sub': 'Cụm CC Hà Nội'},
                        'time': '15:00 27/10',
                        'venue': 'CL.Sân 03',
                        'nextWin': 'CL.M.BK2',
                        'nextWinSlot': 1
                    },
                    {
                        'id': 'CL.M.TK4',
                        'name': 'Tứ kết 4',
                        'team1': {'code': 'HNC', 'name': 'Triệu Minh Hiếu', 'sub': 'MT Hà Nội Center'},
                        'team2': {'code': 'CTH', 'name': 'Nguyễn Thái Dương', 'sub': 'MT Cần Thơ'},
                        'time': '15:00 27/10',
                        'venue': 'CL.Sân 04',
                        'nextWin': 'CL.M.BK2',
                        'nextWinSlot': 2
                    }
                ]
            },
            {
                'id': 'bk',
                'name': 'BÁN KẾT',
                'matches': [
                    {
                        'id': 'CL.M.BK1',
                        'name': 'Bán kết 1',
                        'time': '07:30 29/10',
                        'venue': 'CL.Sân 01',
                        'source1': 'Thắng TK1',
                        'source2': 'Thắng TK2',
                        'nextWin': 'CL.M.CK',
                        'nextWinSlot': 1,
                        'nextLose': 'CL.M.Ba-Tư',
                        'nextLoseSlot': 1
                    },
                    {
                        'id': 'CL.M.BK2',
                        'name': 'Bán kết 2',
                        'time': '07:30 29/10',
                        'venue': 'CL.Sân 02',
                        'source1': 'Thắng TK3',
                        'source2': 'Thắng TK4',
                        'nextWin': 'CL.M.CK',
                        'nextWinSlot': 2,
                        'nextLose': 'CL.M.Ba-Tư',
                        'nextLoseSlot': 2
                    }
                ]
            },
            {
                'id': 'fn',
                'name': 'CHUNG KẾT & TRANH 3-4',
                'matches': [
                    {
                        'id': 'CL.M.CK',
                        'name': 'Chung Kết (Tranh 1-2)',
                        'time': '08:30 29/10',
                        'venue': 'CL.Sân 02',
                        'isFinal': True,
                        'source1': 'Thắng BK1',
                        'source2': 'Thắng BK2'
                    },
                    {
                        'id': 'CL.M.Ba-Tư',
                        'name': 'Tranh Hạng 3 - 4',
                        'time': '08:30 29/10',
                        'venue': 'CL.Sân 01',
                        'isThirdPlace': True,
                        'source1': 'Thua BK1',
                        'source2': 'Thua BK2'
                    }
                ]
            }
        ]
    },

    # ============================================================
    # 5. CẦU LÔNG ĐƠN NỮ (8 VĐV) - KNOCKOUT 8
    # ============================================================
    {
        'id': 'cl_f',
        'name': 'Cầu lông Đơn Nữ (8 VĐV)',
        'sport': 'Cầu lông',
        'code': 'CL.F',
        'color': '#fb7185',
        'format': 'knockout8',
        'scoreLabel': 'Tỉ số séc',
        'rules': 'Bốc thăm chia cặp 8 VĐV, loại trực tiếp tranh 1-2-3-4 (3 hiệp thắng 2, chạm 15đ).',
        'rounds': [
            {
                'id': 'tk',
                'name': 'TỨ KẾT',
                'matches': [
                    {
                        'id': 'CL.F.TK1',
                        'name': 'Tứ kết 1',
                        'team1': {'code': 'VPTĐ', 'name': 'Vũ Huyền Thu', 'sub': 'Văn phòng Tập đoàn'},
                        'team2': {'code': 'BMT', 'name': 'Nguyễn Ngọc Quỳnh Vy', 'sub': 'MT Buôn Ma Thuột'},
                        'time': '15:00 27/10',
                        'venue': 'CL.Sân 01',
                        'nextWin': 'CL.F.BK1',
                        'nextWinSlot': 1
                    },
                    {
                        'id': 'CL.F.TK2',
                        'name': 'Tứ kết 2',
                        'team1': {'code': 'LSG', 'name': 'Trần Tú Trân', 'sub': 'MT Luxury Sài Gòn'},
                        'team2': {'code': 'HLO', 'name': 'Vũ Thị Phượng', 'sub': 'MT Hạ Long'},
                        'time': '15:00 27/10',
                        'venue': 'CL.Sân 02',
                        'nextWin': 'CL.F.BK1',
                        'nextWinSlot': 2
                    },
                    {
                        'id': 'CL.F.TK3',
                        'name': 'Tứ kết 3',
                        'team1': {'code': 'ĐNA', 'name': 'Nguyễn Trần Vương Nhi', 'sub': 'MT Đà Nẵng'},
                        'team2': {'code': 'HNO', 'name': 'Lương Thanh Loan', 'sub': 'MT Hà Nội'},
                        'time': '15:00 27/10',
                        'venue': 'CL.Sân 03',
                        'nextWin': 'CL.F.BK2',
                        'nextWinSlot': 1
                    },
                    {
                        'id': 'CL.F.TK4',
                        'name': 'Tứ kết 4',
                        'team1': {'code': 'QTR', 'name': 'Nguyễn Thị Thu Thuỷ', 'sub': 'MT Quảng Trị'},
                        'team2': {'code': 'TQU', 'name': 'Vũ Linh Chi', 'sub': 'MT Tuyên Quang'},
                        'time': '15:00 27/10',
                        'venue': 'CL.Sân 04',
                        'nextWin': 'CL.F.BK2',
                        'nextWinSlot': 2
                    }
                ]
            },
            {
                'id': 'bk',
                'name': 'BÁN KẾT',
                'matches': [
                    {
                        'id': 'CL.F.BK1',
                        'name': 'Bán kết 1',
                        'time': '07:30 29/10',
                        'venue': 'CL.Sân 03',
                        'source1': 'Thắng TK1',
                        'source2': 'Thắng TK2',
                        'nextWin': 'CL.F.CK',
                        'nextWinSlot': 1,
                        'nextLose': 'CL.F.Ba-Tư',
                        'nextLoseSlot': 1
                    },
                    {
                        'id': 'CL.F.BK2',
                        'name': 'Bán kết 2',
                        'time': '07:30 29/10',
                        'venue': 'CL.Sân 04',
                        'source1': 'Thắng TK3',
                        'source2': 'Thắng TK4',
                        'nextWin': 'CL.F.CK',
                        'nextWinSlot': 2,
                        'nextLose': 'CL.F.Ba-Tư',
                        'nextLoseSlot': 2
                    }
                ]
            },
            {
                'id': 'fn',
                'name': 'CHUNG KẾT & TRANH 3-4',
                'matches': [
                    {
                        'id': 'CL.F.CK',
                        'name': 'Chung Kết (Tranh 1-2)',
                        'time': '08:30 29/10',
                        'venue': 'CL.Sân 04',
                        'isFinal': True,
                        'source1': 'Thắng BK1',
                        'source2': 'Thắng BK2'
                    },
                    {
                        'id': 'CL.F.Ba-Tư',
                        'name': 'Tranh Hạng 3 - 4',
                        'time': '08:30 29/10',
                        'venue': 'CL.Sân 03',
                        'isThirdPlace': True,
                        'source1': 'Thua BK1',
                        'source2': 'Thua BK2'
                    }
                ]
            }
        ]
    },

    # ============================================================
    # 6. PICKLEBALL ĐÔI NAM (8 ĐÔI) - KNOCKOUT 8
    # ============================================================
    {
        'id': 'pk_2m',
        'name': 'Pickleball Đôi Nam (8 cặp)',
        'sport': 'Pickleball',
        'code': 'PK.2M',
        'color': '#ea580c',
        'format': 'knockout8',
        'scoreLabel': 'Tỉ số séc',
        'rules': 'Bốc thăm chia cặp 8 đôi, loại trực tiếp tranh 1-2-3-4 (3 hiệp thắng 2, chạm 15đ ăn điểm trực tiếp).',
        'rounds': [
            {
                'id': 'tk',
                'name': 'TỨ KẾT',
                'matches': [
                    {
                        'id': 'PK.2M.TK1',
                        'name': 'Tứ kết 1',
                        'team1': {'code': 'CCHN', 'name': 'Nguyễn Văn Linh - Phạm Ngọc Hanh', 'sub': 'Cụm CC Hà Nội'},
                        'team2': {'code': 'HAN', 'name': 'Trần Quốc Việt - Lê Tạ Tấn', 'sub': 'MT Hà Nội'},
                        'time': '19:00 28/10',
                        'venue': 'PK.Sân 01',
                        'nextWin': 'PK.2M.BK1',
                        'nextWinSlot': 1
                    },
                    {
                        'id': 'PK.2M.TK2',
                        'name': 'Tứ kết 2',
                        'team1': {'code': 'PTH', 'name': 'Nguyễn Hạ Long - Nguyễn Văn Đồng', 'sub': 'MT Phan Thiết'},
                        'team2': {'code': 'SGO', 'name': 'Trần Mạnh Hùng - Trương Nhật Minh', 'sub': 'MT Sài Gòn'},
                        'time': '19:00 28/10',
                        'venue': 'PK.Sân 02',
                        'nextWin': 'PK.2M.BK1',
                        'nextWinSlot': 2
                    },
                    {
                        'id': 'PK.2M.TK3',
                        'name': 'Tứ kết 3',
                        'team1': {'code': 'BVPD', 'name': 'Hoàng Xuân Kỳ - Bùi Sỹ Tư', 'sub': 'Bệnh viện Phương Đông'},
                        'team2': {'code': 'CCHN', 'name': 'Nguyễn Công Toàn - Nguyễn Quốc Chính', 'sub': 'Cụm CC Hà Nội'},
                        'time': '19:30 28/10',
                        'venue': 'PK.Sân 01',
                        'nextWin': 'PK.2M.BK2',
                        'nextWinSlot': 1
                    },
                    {
                        'id': 'PK.2M.TK4',
                        'name': 'Tứ kết 4',
                        'team1': {'code': 'VPTĐ', 'name': 'Trần Đại Nghĩa - Nguyễn Duy Anh', 'sub': 'Văn phòng Tập đoàn'},
                        'team2': {'code': 'MCH', 'name': 'Lê Thanh Quý - Trương Văn Vững', 'sub': 'MT Mộc Châu'},
                        'time': '19:30 28/10',
                        'venue': 'PK.Sân 02',
                        'nextWin': 'PK.2M.BK2',
                        'nextWinSlot': 2
                    }
                ]
            },
            {
                'id': 'bk',
                'name': 'BÁN KẾT',
                'matches': [
                    {
                        'id': 'PK.2M.BK1',
                        'name': 'Bán kết 1',
                        'time': '08:00 29/10',
                        'venue': 'PK.Sân 01',
                        'source1': 'Thắng TK1',
                        'source2': 'Thắng TK2',
                        'nextWin': 'PK.2M.CK',
                        'nextWinSlot': 1,
                        'nextLose': 'PK.2M.Ba-Tư',
                        'nextLoseSlot': 1
                    },
                    {
                        'id': 'PK.2M.BK2',
                        'name': 'Bán kết 2',
                        'time': '08:00 29/10',
                        'venue': 'PK.Sân 02',
                        'source1': 'Thắng TK3',
                        'source2': 'Thắng TK4',
                        'nextWin': 'PK.2M.CK',
                        'nextWinSlot': 2,
                        'nextLose': 'PK.2M.Ba-Tư',
                        'nextLoseSlot': 2
                    }
                ]
            },
            {
                'id': 'fn',
                'name': 'CHUNG KẾT & TRANH 3-4',
                'matches': [
                    {
                        'id': 'PK.2M.CK',
                        'name': 'Chung Kết (Tranh 1-2)',
                        'time': '10:00 29/10',
                        'venue': 'PK.Sân 02',
                        'isFinal': True,
                        'source1': 'Thắng BK1',
                        'source2': 'Thắng BK2'
                    },
                    {
                        'id': 'PK.2M.Ba-Tư',
                        'name': 'Tranh Hạng 3 - 4',
                        'time': '10:00 29/10',
                        'venue': 'PK.Sân 01',
                        'isThirdPlace': True,
                        'source1': 'Thua BK1',
                        'source2': 'Thua BK2'
                    }
                ]
            }
        ]
    },

    # ============================================================
    # 7. PICKLEBALL ĐÔI NỮ (8 ĐÔI) - KNOCKOUT 8
    # ============================================================
    {
        'id': 'pk_2f',
        'name': 'Pickleball Đôi Nữ (8 cặp)',
        'sport': 'Pickleball',
        'code': 'PK.2F',
        'color': '#f97316',
        'format': 'knockout8',
        'scoreLabel': 'Tỉ số séc',
        'rules': 'Bốc thăm chia cặp 8 đôi, loại trực tiếp tranh 1-2-3-4 (3 hiệp thắng 2, chạm 15đ ăn điểm trực tiếp).',
        'rounds': [
            {
                'id': 'tk',
                'name': 'TỨ KẾT',
                'matches': [
                    {
                        'id': 'PK.2F.TK1',
                        'name': 'Tứ kết 1',
                        'team1': {'code': 'Cienco5', 'name': 'Trương Thị Tuyết - Vũ Thị Hoài', 'sub': 'Cienco5 và DHE'},
                        'team2': {'code': 'LCH', 'name': 'Trần Thị Lập - Lò Thị Bình', 'sub': 'MT Lai Châu'},
                        'time': '18:00 28/10',
                        'venue': 'PK.Sân 01',
                        'nextWin': 'PK.2F.BK1',
                        'nextWinSlot': 1
                    },
                    {
                        'id': 'PK.2F.TK2',
                        'name': 'Tứ kết 2',
                        'team1': {'code': 'Cienco5', 'name': 'Hồ Thị Hồng Nhung - Nguyễn Thị Cẩm Vân', 'sub': 'Cienco5 và DHE'},
                        'team2': {'code': 'BGI', 'name': 'Dương Thị Phương Thảo - Trương Thị Thu Hạnh', 'sub': 'MT Bắc Giang'},
                        'time': '18:00 28/10',
                        'venue': 'PK.Sân 02',
                        'nextWin': 'PK.2F.BK1',
                        'nextWinSlot': 2
                    },
                    {
                        'id': 'PK.2F.TK3',
                        'name': 'Tứ kết 3',
                        'team1': {'code': 'Cienco5', 'name': 'Phạm Thị Hương - Hoàng Thị Xuốt', 'sub': 'Cienco5 và DHE'},
                        'team2': {'code': 'PDO', 'name': 'Trương Thị Thu Nguyệt - Lê Thị Tình', 'sub': 'MT Phú Quốc'},
                        'time': '18:30 28/10',
                        'venue': 'PK.Sân 01',
                        'nextWin': 'PK.2F.BK2',
                        'nextWinSlot': 1
                    },
                    {
                        'id': 'PK.2F.TK4',
                        'name': 'Tứ kết 4',
                        'team1': {'code': 'VPTĐ', 'name': 'Lê Diệp Anh - Trần Thị Thu Nguyệt', 'sub': 'Văn phòng Tập đoàn'},
                        'team2': {'code': 'LDN', 'name': 'Thân Ngọc Thúy An - Nguyễn Thị Hòa', 'sub': 'MT Đà Lạt'},
                        'time': '18:30 28/10',
                        'venue': 'PK.Sân 02',
                        'nextWin': 'PK.2F.BK2',
                        'nextWinSlot': 2
                    }
                ]
            },
            {
                'id': 'bk',
                'name': 'BÁN KẾT',
                'matches': [
                    {
                        'id': 'PK.2F.BK1',
                        'name': 'Bán kết 1',
                        'time': '07:30 29/10',
                        'venue': 'PK.Sân 01',
                        'source1': 'Thắng TK1',
                        'source2': 'Thắng TK2',
                        'nextWin': 'PK.2F.CK',
                        'nextWinSlot': 1,
                        'nextLose': 'PK.2F.Ba-Tư',
                        'nextLoseSlot': 1
                    },
                    {
                        'id': 'PK.2F.BK2',
                        'name': 'Bán kết 2',
                        'time': '07:30 29/10',
                        'venue': 'PK.Sân 02',
                        'source1': 'Thắng TK3',
                        'source2': 'Thắng TK4',
                        'nextWin': 'PK.2F.CK',
                        'nextWinSlot': 2,
                        'nextLose': 'PK.2F.Ba-Tư',
                        'nextLoseSlot': 2
                    }
                ]
            },
            {
                'id': 'fn',
                'name': 'CHUNG KẾT & TRANH 3-4',
                'matches': [
                    {
                        'id': 'PK.2F.CK',
                        'name': 'Chung Kết (Tranh 1-2)',
                        'time': '09:30 29/10',
                        'venue': 'PK.Sân 02',
                        'isFinal': True,
                        'source1': 'Thắng BK1',
                        'source2': 'Thắng BK2'
                    },
                    {
                        'id': 'PK.2F.Ba-Tư',
                        'name': 'Tranh Hạng 3 - 4',
                        'time': '09:30 29/10',
                        'venue': 'PK.Sân 01',
                        'isThirdPlace': True,
                        'source1': 'Thua BK1',
                        'source2': 'Thua BK2'
                    }
                ]
            }
        ]
    },

    # ============================================================
    # 8. PICKLEBALL ĐÔI NAM - NỮ (8 ĐÔI) - KNOCKOUT 8
    # ============================================================
    {
        'id': 'pk_mf',
        'name': 'Pickleball Đôi Nam - Nữ (8 cặp)',
        'sport': 'Pickleball',
        'code': 'PK.MF',
        'color': '#c2410c',
        'format': 'knockout8',
        'scoreLabel': 'Tỉ số séc',
        'rules': 'Bốc thăm chia cặp 8 đôi, loại trực tiếp tranh 1-2-3-4 (3 hiệp thắng 2, chạm 15đ ăn điểm trực tiếp).',
        'rounds': [
            {
                'id': 'tk',
                'name': 'TỨ KẾT',
                'matches': [
                    {
                        'id': 'PK.MF.TK1',
                        'name': 'Tứ kết 1',
                        'team1': {'code': 'VPTĐ', 'name': 'Nguyễn Duy Anh - Lê Thị Thu Nguyệt', 'sub': 'Văn phòng Tập đoàn'},
                        'team2': {'code': 'SLA', 'name': 'Trần Đình Trí - Hà Mai Kiên', 'sub': 'MT Sơn La'},
                        'time': '20:00 28/10',
                        'venue': 'PK.Sân 01',
                        'nextWin': 'PK.MF.BK1',
                        'nextWinSlot': 1
                    },
                    {
                        'id': 'PK.MF.TK2',
                        'name': 'Tứ kết 2',
                        'team1': {'code': 'VTI', 'name': 'Thái Bá Niên - Ninh Thị Nguyên', 'sub': 'MT Vientiane'},
                        'team2': {'code': 'SHA', 'name': 'Phạm Thái Ly - Lê Thị Mai', 'sub': 'MT Sông Hàn'},
                        'time': '20:00 28/10',
                        'venue': 'PK.Sân 02',
                        'nextWin': 'PK.MF.BK1',
                        'nextWinSlot': 2
                    },
                    {
                        'id': 'PK.MF.TK3',
                        'name': 'Tứ kết 3',
                        'team1': {'code': 'Cienco5', 'name': 'Lê Văn Đức - Trương Thị Tuyết', 'sub': 'Cienco5 và DHE'},
                        'team2': {'code': 'NLE', 'name': 'Nguyễn Bá Lộc - Hà Thị Thuỳ Giang', 'sub': 'MT Nhật Lệ'},
                        'time': '20:30 28/10',
                        'venue': 'PK.Sân 01',
                        'nextWin': 'PK.MF.BK2',
                        'nextWinSlot': 1
                    },
                    {
                        'id': 'PK.MF.TK4',
                        'name': 'Tứ kết 4',
                        'team1': {'code': 'Cienco5', 'name': 'Đào Việt Hà - Hoàng Thị Thu Hương', 'sub': 'Cienco5 và DHE'},
                        'team2': {'code': 'PQU', 'name': 'Lương Văn Linh - Trần Thị Lê', 'sub': 'MT Phú Quốc'},
                        'time': '20:30 28/10',
                        'venue': 'PK.Sân 02',
                        'nextWin': 'PK.MF.BK2',
                        'nextWinSlot': 2
                    }
                ]
            },
            {
                'id': 'bk',
                'name': 'BÁN KẾT',
                'matches': [
                    {
                        'id': 'PK.MF.BK1',
                        'name': 'Bán kết 1',
                        'time': '08:30 29/10',
                        'venue': 'PK.Sân 01',
                        'source1': 'Thắng TK1',
                        'source2': 'Thắng TK2',
                        'nextWin': 'PK.MF.CK',
                        'nextWinSlot': 1,
                        'nextLose': 'PK.MF.Ba-Tư',
                        'nextLoseSlot': 1
                    },
                    {
                        'id': 'PK.MF.BK2',
                        'name': 'Bán kết 2',
                        'time': '08:30 29/10',
                        'venue': 'PK.Sân 02',
                        'source1': 'Thắng TK3',
                        'source2': 'Thắng TK4',
                        'nextWin': 'PK.MF.CK',
                        'nextWinSlot': 2,
                        'nextLose': 'PK.MF.Ba-Tư',
                        'nextLoseSlot': 2
                    }
                ]
            },
            {
                'id': 'fn',
                'name': 'CHUNG KẾT & TRANH 3-4',
                'matches': [
                    {
                        'id': 'PK.MF.CK',
                        'name': 'Chung Kết (Tranh 1-2)',
                        'time': '10:30 29/10',
                        'venue': 'PK.Sân 02',
                        'isFinal': True,
                        'source1': 'Thắng BK1',
                        'source2': 'Thắng BK2'
                    },
                    {
                        'id': 'PK.MF.Ba-Tư',
                        'name': 'Tranh Hạng 3 - 4',
                        'time': '10:30 29/10',
                        'venue': 'PK.Sân 01',
                        'isThirdPlace': True,
                        'source1': 'Thua BK1',
                        'source2': 'Thua BK2'
                    }
                ]
            }
        ]
    },

    # ============================================================
    # 9. BÓNG ĐÁ NỮ (6 ĐỘI) - 2 BẢNG -> CHUNG KẾT & TRANH 3-4
    # ============================================================
    {
        'id': 'bd_f',
        'name': 'Bóng đá Nữ (6 đội - 2 Bảng)',
        'sport': 'Bóng đá',
        'code': 'BĐ.F',
        'color': '#16a34a',
        'format': 'group2_final',
        'scoreLabel': 'Bàn thắng',
        'rules': 'Bốc thăm chia 2 bảng đấu vòng tròn (20p/hiệp, Thắng 3đ, Hòa 1đ, Thua 0đ). Nhất bảng vào Chung kết tranh 1-2, Nhì bảng vào tranh 3-4.',
        'groups': [
            {
                'id': 'A',
                'name': 'Bảng A',
                'teams': [
                    {'id': 'A1', 'code': 'LQ.XTH', 'name': 'LQ.XTH (GXT - XTH)'},
                    {'id': 'A2', 'code': 'LQ.DLR', 'name': 'LQ.DLR (DLR - DLG - DLS)'},
                    {'id': 'A3', 'code': 'LQ.QNA', 'name': 'LQ.QNA (QNA - HAN)'}
                ],
                'matches': [
                    {'id': 'BĐ.F.A1-A2', 'name': 'LQ.XTH vs LQ.DLR', 'team1': 'A1', 'team2': 'A2', 'time': '15:00 27/10', 'venue': 'BĐ.Sân 01'},
                    {'id': 'BĐ.F.A2-A3', 'name': 'LQ.DLR vs LQ.QNA', 'team1': 'A2', 'team2': 'A3', 'time': '15:00 28/10', 'venue': 'BĐ.Sân 01'},
                    {'id': 'BĐ.F.A3-A1', 'name': 'LQ.QNA vs LQ.XTH', 'team1': 'A3', 'team2': 'A1', 'time': '17:00 28/10', 'venue': 'BĐ.Sân 01'}
                ]
            },
            {
                'id': 'B',
                'name': 'Bảng B',
                'teams': [
                    {'id': 'B1', 'code': 'LQ.SGO', 'name': 'LQ.SGO (LSG - PQU)'},
                    {'id': 'B2', 'code': 'LQ.SLA', 'name': 'LQ.SLA (SLA - MCH)'},
                    {'id': 'B3', 'code': 'LQ.MT Mart', 'name': 'LQ.MT Mart (Siêu thị MT)'}
                ],
                'matches': [
                    {'id': 'BĐ.F.B1-B2', 'name': 'LQ.SGO vs LQ.SLA', 'team1': 'B1', 'team2': 'B2', 'time': '15:00 27/10', 'venue': 'BĐ.Sân 01'},
                    {'id': 'BĐ.F.B2-B3', 'name': 'LQ.SLA vs LQ.MT Mart', 'team1': 'B2', 'team2': 'B3', 'time': '15:00 28/10', 'venue': 'BĐ.Sân 03'},
                    {'id': 'BĐ.F.B3-B1', 'name': 'LQ.MT Mart vs LQ.SGO', 'team1': 'B3', 'team2': 'B1', 'time': '17:00 28/10', 'venue': 'BĐ.Sân 03'}
                ]
            }
        ],
        'finals': [
            {
                'id': 'BĐ.F.CK',
                'name': 'Chung Kết (Tranh 1-2)',
                'time': '08:00 29/10',
                'venue': 'BĐ.Sân 03',
                'isFinal': True,
                'source1': 'Nhất Bảng A',
                'source2': 'Nhất Bảng B',
                'srcGroup1': 'A',
                'srcRank1': 1,
                'srcGroup2': 'B',
                'srcRank2': 1
            },
            {
                'id': 'BĐ.F.3-4',
                'name': 'Tranh Hạng 3 - 4',
                'time': '07:00 29/10',
                'venue': 'BĐ.Sân 03',
                'isThirdPlace': True,
                'source1': 'Nhì Bảng A',
                'source2': 'Nhì Bảng B',
                'srcGroup1': 'A',
                'srcRank1': 2,
                'srcGroup2': 'B',
                'srcRank2': 2
            }
        ]
    },

    # ============================================================
    # 10. KÉO CO PHỐI HỢP (8 ĐỘI) - 2 BẢNG -> BÁN KẾT CHÉO -> CK
    # ============================================================
    {
        'id': 'kc',
        'name': 'Kéo co Phối hợp Nam - Nữ (8 đội)',
        'sport': 'Kéo co',
        'code': 'KC',
        'color': '#b45309',
        'format': 'group2_cross',
        'scoreLabel': 'Tỉ số hiệp',
        'rules': 'Bốc thăm chia 2 bảng đấu vòng tròn (3 hiệp thắng 2). Nhất-Nhì mỗi bảng vào Bán kết đấu chéo (Nhất A - Nhì B, Nhất B - Nhì A). Chung kết loại trực tiếp tranh 1-2-3-4.',
        'groups': [
            {
                'id': 'A',
                'name': 'Bảng A',
                'teams': [
                    {'id': 'A1', 'code': 'CMA', 'name': 'MT Luxury Cà Mau'},
                    {'id': 'A2', 'code': 'LQ.DLR', 'name': 'LQ.DLR (DLR - DLG - DLS)'},
                    {'id': 'A3', 'code': 'VTI', 'name': 'MT Luxury Vientiane'},
                    {'id': 'A4', 'code': 'LQ.ĐBP', 'name': 'LQ.ĐBP (LDB - DBP)'}
                ],
                'matches': [
                    {'id': 'KC.A1-A2', 'name': 'CMA vs LQ.DLR', 'team1': 'A1', 'team2': 'A2', 'time': '13:00 27/10', 'venue': 'KC.Làn 01'},
                    {'id': 'KC.A3-A4', 'name': 'VTI vs LQ.ĐBP', 'team1': 'A3', 'team2': 'A4', 'time': '13:00 27/10', 'venue': 'KC.Làn 01'},
                    {'id': 'KC.A1-A3', 'name': 'CMA vs VTI', 'team1': 'A1', 'team2': 'A3', 'time': '13:00 27/10', 'venue': 'KC.Làn 01'},
                    {'id': 'KC.A2-A4', 'name': 'LQ.DLR vs LQ.ĐBP', 'team1': 'A2', 'team2': 'A4', 'time': '13:00 27/10', 'venue': 'KC.Làn 01'},
                    {'id': 'KC.A1-A4', 'name': 'CMA vs LQ.ĐBP', 'team1': 'A1', 'team2': 'A4', 'time': '13:00 27/10', 'venue': 'KC.Làn 01'},
                    {'id': 'KC.A2-A3', 'name': 'LQ.DLR vs VTI', 'team1': 'A2', 'team2': 'A3', 'time': '13:00 27/10', 'venue': 'KC.Làn 01'}
                ]
            },
            {
                'id': 'B',
                'name': 'Bảng B',
                'teams': [
                    {'id': 'B1', 'code': 'LQ.HLO', 'name': 'LQ.HLO (HLC1 - HLC2 - SMO)'},
                    {'id': 'B2', 'code': 'LQ.NTR', 'name': 'LQ.NTR (VTR - NTR - CC Nha Trang)'},
                    {'id': 'B3', 'code': 'VPTĐ', 'name': 'Văn phòng Tập đoàn'},
                    {'id': 'B4', 'code': 'LYS', 'name': 'MT Lý Sơn'}
                ],
                'matches': [
                    {'id': 'KC.B1-B2', 'name': 'LQ.HLO vs LQ.NTR', 'team1': 'B1', 'team2': 'B2', 'time': '13:00 27/10', 'venue': 'KC.Làn 02'},
                    {'id': 'KC.B3-B4', 'name': 'VPTĐ vs LYS', 'team1': 'B3', 'team2': 'B4', 'time': '13:00 27/10', 'venue': 'KC.Làn 02'},
                    {'id': 'KC.B1-B3', 'name': 'LQ.HLO vs VPTĐ', 'team1': 'B1', 'team2': 'B3', 'time': '13:00 27/10', 'venue': 'KC.Làn 02'},
                    {'id': 'KC.B2-B4', 'name': 'LQ.NTR vs LYS', 'team1': 'B2', 'team2': 'B4', 'time': '13:00 27/10', 'venue': 'KC.Làn 02'},
                    {'id': 'KC.B1-B4', 'name': 'LQ.HLO vs LYS', 'team1': 'B1', 'team2': 'B4', 'time': '13:00 27/10', 'venue': 'KC.Làn 02'},
                    {'id': 'KC.B2-B3', 'name': 'LQ.NTR vs VPTĐ', 'team1': 'B2', 'team2': 'B3', 'time': '13:00 27/10', 'venue': 'KC.Làn 02'}
                ]
            }
        ],
        'knockout': [
            {
                'id': 'bk',
                'name': 'BÁN KẾT (ĐẤU CHÉO)',
                'matches': [
                    {
                        'id': 'KC.BK1',
                        'name': 'Bán kết 1',
                        'time': '11:00 29/10',
                        'venue': 'KC.Làn 01',
                        'source1': 'Nhất Bảng A',
                        'source2': 'Nhì Bảng B',
                        'srcGroup1': 'A',
                        'srcRank1': 1,
                        'srcGroup2': 'B',
                        'srcRank2': 2,
                        'nextWin': 'KC.CK',
                        'nextWinSlot': 1,
                        'nextLose': 'KC.3-4',
                        'nextLoseSlot': 1
                    },
                    {
                        'id': 'KC.BK2',
                        'name': 'Bán kết 2',
                        'time': '11:00 29/10',
                        'venue': 'KC.Làn 02',
                        'source1': 'Nhất Bảng B',
                        'source2': 'Nhì Bảng A',
                        'srcGroup1': 'B',
                        'srcRank1': 1,
                        'srcGroup2': 'A',
                        'srcRank2': 2,
                        'nextWin': 'KC.CK',
                        'nextWinSlot': 2,
                        'nextLose': 'KC.3-4',
                        'nextLoseSlot': 2
                    }
                ]
            },
            {
                'id': 'fn',
                'name': 'CHUNG KẾT & TRANH 3-4',
                'matches': [
                    {
                        'id': 'KC.CK',
                        'name': 'Chung Kết (Tranh 1-2)',
                        'time': '11:00 29/10',
                        'venue': 'KC.Làn 01',
                        'isFinal': True,
                        'source1': 'Thắng BK1',
                        'source2': 'Thắng BK2'
                    },
                    {
                        'id': 'KC.3-4',
                        'name': 'Tranh Hạng 3 - 4',
                        'time': '11:00 29/10',
                        'venue': 'KC.Làn 01',
                        'isThirdPlace': True,
                        'source1': 'Thua BK1',
                        'source2': 'Thua BK2'
                    }
                ]
            }
        ]
    },

    # ============================================================
    # 11. CẦU LÔNG ĐÔI NAM - NỮ (9 ĐÔI) - 3 BẢNG -> VÒNG CHUNG KẾT
    # ============================================================
    {
        'id': 'cl_mf',
        'name': 'Cầu lông Đôi Nam - Nữ (9 cặp)',
        'sport': 'Cầu lông',
        'code': 'CL.MF',
        'color': '#b91c1c',
        'format': 'group3_roundrobin',
        'scoreLabel': 'Tỉ số séc',
        'rules': 'Bốc thăm chia 3 bảng đấu vòng tròn (1 hiệp chạm 21đ). Chọn 3 đội Nhất mỗi bảng vào Vòng Chung Kết đấu vòng tròn tính điểm tranh 1-2-3.',
        'groups': [
            {
                'id': 'A',
                'name': 'Bảng A',
                'teams': [
                    {'id': 'A1', 'code': 'HUE', 'name': 'Phạm Quang Huy - Đặng Thị Hoài Anh', 'sub': 'MT Huế'},
                    {'id': 'A2', 'code': 'TQU', 'name': 'Lê Thị Phương - Hà Xuân Giang', 'sub': 'MT Tuyên Quang'},
                    {'id': 'A3', 'code': 'NTC', 'name': 'Nguyễn Thị Vân Kiều - Nguyễn Thiện Cung', 'sub': 'MT Nha Trang Centre'}
                ],
                'matches': [
                    {'id': 'CL.MF.A1-A2', 'name': 'HUE vs TQU', 'team1': 'A1', 'team2': 'A2', 'time': '15:00 27/10', 'venue': 'CL.Sân 01'},
                    {'id': 'CL.MF.A2-A3', 'name': 'TQU vs NTC', 'team1': 'A2', 'team2': 'A3', 'time': '15:00 27/10', 'venue': 'CL.Sân 01'},
                    {'id': 'CL.MF.A3-A1', 'name': 'NTC vs HUE', 'team1': 'A3', 'team2': 'A1', 'time': '17:00 27/10', 'venue': 'CL.Sân 01'}
                ]
            },
            {
                'id': 'B',
                'name': 'Bảng B',
                'teams': [
                    {'id': 'B1', 'code': 'VRC', 'name': 'Lỗ Thị Thúy An - Nguyễn Quang Đạt', 'sub': 'VRC'},
                    {'id': 'B2', 'code': 'DBP', 'name': 'Nguyễn Thị Thảo - Đinh Ngọc Dương', 'sub': 'MT Điện Biên Phủ'},
                    {'id': 'B3', 'code': 'HNO', 'name': 'Nguyễn Nam Khánh - Lương Thanh Loan', 'sub': 'MT Hà Nội'}
                ],
                'matches': [
                    {'id': 'CL.MF.B1-B2', 'name': 'VRC vs DBP', 'team1': 'B1', 'team2': 'B2', 'time': '15:00 27/10', 'venue': 'CL.Sân 02'},
                    {'id': 'CL.MF.B2-B3', 'name': 'DBP vs HNO', 'team1': 'B2', 'team2': 'B3', 'time': '15:00 27/10', 'venue': 'CL.Sân 02'},
                    {'id': 'CL.MF.B3-B1', 'name': 'HNO vs VRC', 'team1': 'B3', 'team2': 'B1', 'time': '17:00 27/10', 'venue': 'CL.Sân 02'}
                ]
            },
            {
                'id': 'C',
                'name': 'Bảng C',
                'teams': [
                    {'id': 'C1', 'code': 'QTR', 'name': 'Nguyễn Lực - Lê Thị Kim Chi', 'sub': 'MT Quảng Trị'},
                    {'id': 'C2', 'code': 'CCHN', 'name': 'Lê Thị Phúc - Nguyễn Mạnh Cường', 'sub': 'Cụm CC Hà Nội'},
                    {'id': 'C3', 'code': 'ĐLA', 'name': 'Trần Thị Cẩm Ly - Nguyễn Hải Triều', 'sub': 'MT Đà Lạt'}
                ],
                'matches': [
                    {'id': 'CL.MF.C1-C2', 'name': 'QTR vs CCHN', 'team1': 'C1', 'team2': 'C2', 'time': '15:00 27/10', 'venue': 'CL.Sân 03'},
                    {'id': 'CL.MF.C2-C3', 'name': 'CCHN vs ĐLA', 'team1': 'C2', 'team2': 'C3', 'time': '15:00 27/10', 'venue': 'CL.Sân 03'},
                    {'id': 'CL.MF.C3-C1', 'name': 'ĐLA vs QTR', 'team1': 'C3', 'team2': 'C1', 'time': '17:00 27/10', 'venue': 'CL.Sân 03'}
                ]
            }
        ],
        'finalRound': {
            'name': 'VÒNG CHUNG KẾT (3 ĐỘI NHẤT BẢNG)',
            'matches': [
                {
                    'id': 'CL.MF.F1',
                    'name': 'Nhất A vs Nhất B',
                    'time': '09:30 29/10',
                    'venue': 'CL.Sân 01',
                    'srcTeam1': {'group': 'A', 'rank': 1, 'label': 'Nhất Bảng A'},
                    'srcTeam2': {'group': 'B', 'rank': 1, 'label': 'Nhất Bảng B'}
                },
                {
                    'id': 'CL.MF.F2',
                    'name': 'Nhất B vs Nhất C',
                    'time': '10:00 29/10',
                    'venue': 'CL.Sân 01',
                    'srcTeam1': {'group': 'B', 'rank': 1, 'label': 'Nhất Bảng B'},
                    'srcTeam2': {'group': 'C', 'rank': 1, 'label': 'Nhất Bảng C'}
                },
                {
                    'id': 'CL.MF.F3',
                    'name': 'Nhất C vs Nhất A',
                    'time': '10:30 29/10',
                    'venue': 'CL.Sân 01',
                    'srcTeam1': {'group': 'C', 'rank': 1, 'label': 'Nhất Bảng C'},
                    'srcTeam2': {'group': 'A', 'rank': 1, 'label': 'Nhất Bảng A'}
                }
            ]
        }
    },

    # ============================================================
    # 12. BÓNG BÀN ĐƠN NAM (8 VĐV) - 2 PLAY-OFF -> 2 BẢNG -> BK CHÉO -> CK
    # ============================================================
    {
        'id': 'bb_m',
        'name': 'Bóng bàn Đơn Nam (8 VĐV)',
        'sport': 'Bóng bàn',
        'code': 'BB.M',
        'color': '#1d4ed8',
        'format': 'tabletennis_men',
        'scoreLabel': 'Tỉ số séc',
        'rules': '2 trận Play-off (5 hiệp thắng 3, 11đ/séc cách biệt 2đ). Thắng PO vào Bảng (PO2 vào A1, PO1 vào B1). Bốc thăm 2 bảng đấu vòng tròn. Nhất-nhì mỗi bảng vào Bán kết chéo (Nhất A-Nhì B, Nhất B-Nhì A), Chung kết tranh 1-2-3-4.',
        'playoffs': [
            {
                'id': 'BB.M.PO1',
                'name': 'Play-off 1 (Vào B1)',
                'team1': {'code': 'DCH', 'name': 'Vy Văn Hùng', 'sub': 'MT Diễn Châu'},
                'team2': {'code': 'HUE', 'name': 'Lê Trọng Phú', 'sub': 'MT Huế'},
                'time': '14:00 27/10',
                'venue': 'BB.Bàn 01',
                'targetSlot': {'group': 'B', 'pos': 'B1'}
            },
            {
                'id': 'BB.M.PO2',
                'name': 'Play-off 2 (Vào A1)',
                'team1': {'code': 'HNO', 'name': 'Nguyễn Văn Tuấn', 'sub': 'MT Hà Nội'},
                'team2': {'code': 'NTR', 'name': 'Nguyễn Thành Trạng', 'sub': 'MT Nha Trang'},
                'time': '14:00 27/10',
                'venue': 'BB.Bàn 02',
                'targetSlot': {'group': 'A', 'pos': 'A1'}
            }
        ],
        'groups': [
            {
                'id': 'A',
                'name': 'Bảng A',
                'teams': [
                    {'id': 'A1', 'code': 'PO2', 'name': 'Thắng PO2 (Tuấn / Trạng)', 'isFromPO': True, 'poId': 'BB.M.PO2'},
                    {'id': 'A2', 'code': 'CCHN', 'name': 'Lê Xuân', 'sub': 'LQ Chung cư Hà Nội'},
                    {'id': 'A3', 'code': 'NTC', 'name': 'Nguyễn Thiện Cung', 'sub': 'MT Nha Trang Centre'},
                    {'id': 'A4', 'code': 'DCH', 'name': 'Nguyễn Văn Qúy', 'sub': 'MT Diễn Châu'}
                ],
                'matches': [
                    {'id': 'BB.M.A1-A2', 'name': 'PO2 vs CCHN (Xuân)', 'team1': 'A1', 'team2': 'A2', 'time': '15:00 27/10', 'venue': 'BB.Bàn 01'},
                    {'id': 'BB.M.A3-A4', 'name': 'NTC (Cung) vs DCH (Quý)', 'team1': 'A3', 'team2': 'A4', 'time': '15:00 27/10', 'venue': 'BB.Bàn 02'},
                    {'id': 'BB.M.A1-A3', 'name': 'PO2 vs NTC (Cung)', 'team1': 'A1', 'team2': 'A3', 'time': '15:00 27/10', 'venue': 'BB.Bàn 01'},
                    {'id': 'BB.M.A2-A4', 'name': 'CCHN (Xuân) vs DCH (Quý)', 'team1': 'A2', 'team2': 'A4', 'time': '15:00 27/10', 'venue': 'BB.Bàn 02'},
                    {'id': 'BB.M.A1-A4', 'name': 'PO2 vs DCH (Quý)', 'team1': 'A1', 'team2': 'A4', 'time': '17:00 27/10', 'venue': 'BB.Bàn 01'},
                    {'id': 'BB.M.A2-A3', 'name': 'CCHN (Xuân) vs NTC (Cung)', 'team1': 'A2', 'team2': 'A3', 'time': '17:00 27/10', 'venue': 'BB.Bàn 02'}
                ]
            },
            {
                'id': 'B',
                'name': 'Bảng B',
                'teams': [
                    {'id': 'B1', 'code': 'PO1', 'name': 'Thắng PO1 (Hùng / Phú)', 'isFromPO': True, 'poId': 'BB.M.PO1'},
                    {'id': 'B2', 'code': 'PDI', 'name': 'Ngô Tuấn Anh', 'sub': 'ST MT Phủ Diễn'},
                    {'id': 'B3', 'code': 'BNI', 'name': 'Trịnh Quang Toàn', 'sub': 'MT Bắc Ninh'},
                    {'id': 'B4', 'code': 'ĐNA', 'name': 'Nguyễn Lương Hoàng', 'sub': 'MT Đà Nẵng'}
                ],
                'matches': [
                    {'id': 'BB.M.B1-B2', 'name': 'PO1 vs PDI (Tuấn Anh)', 'team1': 'B1', 'team2': 'B2', 'time': '14:00 27/10', 'venue': 'BB.Bàn 01'},
                    {'id': 'BB.M.B3-B4', 'name': 'BNI (Toàn) vs ĐNA (Hoàng)', 'team1': 'B3', 'team2': 'B4', 'time': '14:00 27/10', 'venue': 'BB.Bàn 02'},
                    {'id': 'BB.M.B1-B3', 'name': 'PO1 vs BNI (Toàn)', 'team1': 'B1', 'team2': 'B3', 'time': '15:00 27/10', 'venue': 'BB.Bàn 01'},
                    {'id': 'BB.M.B2-B4', 'name': 'PDI (Tuấn Anh) vs ĐNA (Hoàng)', 'team1': 'B2', 'team2': 'B4', 'time': '15:00 27/10', 'venue': 'BB.Bàn 02'},
                    {'id': 'BB.M.B1-B4', 'name': 'PO1 vs ĐNA (Hoàng)', 'team1': 'B1', 'team2': 'B4', 'time': '15:00 27/10', 'venue': 'BB.Bàn 01'},
                    {'id': 'BB.M.B2-B3', 'name': 'PDI (Tuấn Anh) vs BNI (Toàn)', 'team1': 'B2', 'team2': 'B3', 'time': '15:00 27/10', 'venue': 'BB.Bàn 02'}
                ]
            }
        ],
        'knockout': [
            {
                'id': 'bk',
                'name': 'BÁN KẾT (ĐẤU CHÉO)',
                'matches': [
                    {
                        'id': 'BB.M.BK1',
                        'name': 'Bán kết 1',
                        'time': '07:30 29/10',
                        'venue': 'BB.Bàn 01',
                        'source1': 'Nhất Bảng A',
                        'source2': 'Nhì Bảng B',
                        'srcGroup1': 'A',
                        'srcRank1': 1,
                        'srcGroup2': 'B',
                        'srcRank2': 2,
                        'nextWin': 'BB.M.CK',
                        'nextWinSlot': 1,
                        'nextLose': 'BB.M.Ba-Tư',
                        'nextLoseSlot': 1
                    },
                    {
                        'id': 'BB.M.BK2',
                        'name': 'Bán kết 2',
                        'time': '07:30 29/10',
                        'venue': 'BB.Bàn 02',
                        'source1': 'Nhất Bảng B',
                        'source2': 'Nhì Bảng A',
                        'srcGroup1': 'B',
                        'srcRank1': 1,
                        'srcGroup2': 'A',
                        'srcRank2': 2,
                        'nextWin': 'BB.M.CK',
                        'nextWinSlot': 2,
                        'nextLose': 'BB.M.Ba-Tư',
                        'nextLoseSlot': 2
                    }
                ]
            },
            {
                'id': 'fn',
                'name': 'CHUNG KẾT & TRANH 3-4',
                'matches': [
                    {
                        'id': 'BB.M.CK',
                        'name': 'Chung Kết (Tranh 1-2)',
                        'time': '08:30 29/10',
                        'venue': 'BB.Bàn 02',
                        'isFinal': True,
                        'source1': 'Thắng BK1',
                        'source2': 'Thắng BK2'
                    },
                    {
                        'id': 'BB.M.Ba-Tư',
                        'name': 'Tranh Hạng 3 - 4',
                        'time': '08:30 29/10',
                        'venue': 'BB.Bàn 01',
                        'isThirdPlace': True,
                        'source1': 'Thua BK1',
                        'source2': 'Thua BK2'
                    }
                ]
            }
        ]
    },

    # ============================================================
    # 13. BÓNG BÀN ĐƠN NỮ (11 VĐV) - 3 BẢNG -> VÒNG CHUNG KẾT
    # ============================================================
    {
        'id': 'bb_f',
        'name': 'Bóng bàn Đơn Nữ (11 VĐV)',
        'sport': 'Bóng bàn',
        'code': 'BB.F',
        'color': '#2563eb',
        'format': 'group3_roundrobin',
        'scoreLabel': 'Tỉ số séc',
        'rules': 'Bốc thăm chia 3 bảng (Bảng A 4 VĐV, Bảng B 4 VĐV, Bảng C 3 VĐV), đấu vòng tròn (3 hiệp thắng 2, 11đ/séc cách biệt 2đ). Chọn Nhất mỗi bảng vào Vòng Chung Kết đấu vòng tròn tranh 1-2-3.',
        'groups': [
            {
                'id': 'A',
                'name': 'Bảng A (4 VĐV)',
                'teams': [
                    {'id': 'A1', 'code': 'SGO', 'name': 'Lê Thị Lụa', 'sub': 'MT Sài Gòn'},
                    {'id': 'A2', 'code': 'VPTĐ', 'name': 'Trần Mai Phương', 'sub': 'Văn phòng Tập đoàn'},
                    {'id': 'A3', 'code': 'VPTĐ', 'name': 'Trần Hồng Hạnh', 'sub': 'Văn phòng Tập đoàn'},
                    {'id': 'A4', 'code': 'Cienco5', 'name': 'Trần Khánh Vân', 'sub': 'Cienco5 và DHE'}
                ],
                'matches': [
                    {'id': 'BB.F.A1-A2', 'name': 'SGO (Lụa) vs VPTĐ (Phương)', 'team1': 'A1', 'team2': 'A2', 'time': '17:00 27/10', 'venue': 'BB.Bàn 01'},
                    {'id': 'BB.F.A3-A4', 'name': 'VPTĐ (Hạnh) vs Cienco5 (Vân)', 'team1': 'A3', 'team2': 'A4', 'time': '17:00 27/10', 'venue': 'BB.Bàn 02'},
                    {'id': 'BB.F.A1-A3', 'name': 'SGO (Lụa) vs VPTĐ (Hạnh)', 'team1': 'A1', 'team2': 'A3', 'time': '17:00 27/10', 'venue': 'BB.Bàn 02'},
                    {'id': 'BB.F.A2-A4', 'name': 'VPTĐ (Phương) vs Cienco5 (Vân)', 'team1': 'A2', 'team2': 'A4', 'time': '17:00 27/10', 'venue': 'BB.Bàn 01'},
                    {'id': 'BB.F.A1-A4', 'name': 'SGO (Lụa) vs Cienco5 (Vân)', 'team1': 'A1', 'team2': 'A4', 'time': '17:00 27/10', 'venue': 'BB.Bàn 01'},
                    {'id': 'BB.F.A2-A3', 'name': 'VPTĐ (Phương) vs VPTĐ (Hạnh)', 'team1': 'A2', 'team2': 'A3', 'time': '17:00 27/10', 'venue': 'BB.Bàn 02'}
                ]
            },
            {
                'id': 'B',
                'name': 'Bảng B (4 VĐV)',
                'teams': [
                    {'id': 'B1', 'code': 'THO', 'name': 'Phùng Thị Hiền', 'sub': 'MT Thanh Hóa'},
                    {'id': 'B2', 'code': 'VPTĐ', 'name': 'Phạm Thị Thảo Nhi', 'sub': 'Văn phòng Tập đoàn'},
                    {'id': 'B3', 'code': 'Cienco5', 'name': 'Hoàng Thị Thu Hương', 'sub': 'Cienco5 và DHE'},
                    {'id': 'B4', 'code': 'CLO', 'name': 'Cao Thị Thủy', 'sub': 'MT Cửa Lò'}
                ],
                'matches': [
                    {'id': 'BB.F.B1-B2', 'name': 'THO (Hiền) vs VPTĐ (Nhi)', 'team1': 'B1', 'team2': 'B2', 'time': '17:00 27/10', 'venue': 'BB.Bàn 01'},
                    {'id': 'BB.F.B3-B4', 'name': 'Cienco5 (Hương) vs CLO (Thủy)', 'team1': 'B3', 'team2': 'B4', 'time': '17:00 27/10', 'venue': 'BB.Bàn 02'},
                    {'id': 'BB.F.B1-B3', 'name': 'THO (Hiền) vs Cienco5 (Hương)', 'team1': 'B1', 'team2': 'B3', 'time': '17:00 27/10', 'venue': 'BB.Bàn 02'},
                    {'id': 'BB.F.B2-B4', 'name': 'VPTĐ (Nhi) vs CLO (Thủy)', 'team1': 'B2', 'team2': 'B4', 'time': '17:00 27/10', 'venue': 'BB.Bàn 01'},
                    {'id': 'BB.F.B1-B4', 'name': 'THO (Hiền) vs CLO (Thủy)', 'team1': 'B1', 'team2': 'B4', 'time': '17:00 27/10', 'venue': 'BB.Bàn 01'},
                    {'id': 'BB.F.B2-B3', 'name': 'VPTĐ (Nhi) vs Cienco5 (Hương)', 'team1': 'B2', 'team2': 'B3', 'time': '17:00 27/10', 'venue': 'BB.Bàn 02'}
                ]
            },
            {
                'id': 'C',
                'name': 'Bảng C (3 VĐV)',
                'teams': [
                    {'id': 'C1', 'code': 'DBP', 'name': 'Lò Thị Xuân', 'sub': 'MT Điện Biên Phủ'},
                    {'id': 'C2', 'code': 'Cienco5', 'name': 'Nguyễn Thị Thơ', 'sub': 'Cienco5 và DHE'},
                    {'id': 'C3', 'code': 'VPTĐ', 'name': 'Võ Thị Mai Trang', 'sub': 'Văn phòng Tập đoàn'}
                ],
                'matches': [
                    {'id': 'BB.F.C1-C2', 'name': 'DBP (Xuân) vs Cienco5 (Thơ)', 'team1': 'C1', 'team2': 'C2', 'time': '17:00 27/10', 'venue': 'BB.Bàn 01'},
                    {'id': 'BB.F.C2-C3', 'name': 'Cienco5 (Thơ) vs VPTĐ (Trang)', 'team1': 'C2', 'team2': 'C3', 'time': '17:00 27/10', 'venue': 'BB.Bàn 02'},
                    {'id': 'BB.F.C3-C1', 'name': 'VPTĐ (Trang) vs DBP (Xuân)', 'team1': 'C3', 'team2': 'C1', 'time': '17:00 27/10', 'venue': 'BB.Bàn 01'}
                ]
            }
        ],
        'finalRound': {
            'name': 'VÒNG CHUNG KẾT (3 VĐV NHẤT BẢNG)',
            'matches': [
                {
                    'id': 'BB.F.F1',
                    'name': 'Nhất A vs Nhất B',
                    'time': '08:00 29/10',
                    'venue': 'BB.Bàn 01',
                    'srcTeam1': {'group': 'A', 'rank': 1, 'label': 'Nhất Bảng A'},
                    'srcTeam2': {'group': 'B', 'rank': 1, 'label': 'Nhất Bảng B'}
                },
                {
                    'id': 'BB.F.F2',
                    'name': 'Nhất B vs Nhất C',
                    'time': '09:00 29/10',
                    'venue': 'BB.Bàn 01',
                    'srcTeam1': {'group': 'B', 'rank': 1, 'label': 'Nhất Bảng B'},
                    'srcTeam2': {'group': 'C', 'rank': 1, 'label': 'Nhất Bảng C'}
                },
                {
                    'id': 'BB.F.F3',
                    'name': 'Nhất C vs Nhất A',
                    'time': '09:30 29/10',
                    'venue': 'BB.Bàn 01',
                    'srcTeam1': {'group': 'C', 'rank': 1, 'label': 'Nhất Bảng C'},
                    'srcTeam2': {'group': 'A', 'rank': 1, 'label': 'Nhất Bảng A'}
                }
            ]
        }
    },

    # ============================================================
    # 14. BƠI LỘI (6 NỘI DUNG) - VÒNG LOẠI -> CHUNG KẾT 6 LÀN
    # ============================================================
    {
        'id': 'swimming',
        'name': 'Bơi lội (Toàn bộ 6 nội dung)',
        'sport': 'Bơi',
        'code': 'BƠI',
        'color': '#0284c7',
        'format': 'swimming',
        'scoreLabel': 'Thời gian (giây hoặc phút:giây)',
        'rules': 'Chia 2 vòng: Vòng loại (chiều 27/10, 14:00 - 14:30) gồm 12 lượt; VCK (sáng 29/10, 10:00 - 10:30) gồm 6 lượt. TOP 6 mỗi nội dung thi cùng 1 lượt Chung kết tranh 1-2-3-4.',
        'subEvents': [
            {'id': 'swim_m_td40', 'name': 'Bơi Tự Do Nam 40m', 'gender': 'Nam', 'style': 'Tự do', 'dist': '40m', 'qlHeats': [1, 2], 'fnHeat': 1},
            {'id': 'swim_m_td80', 'name': 'Bơi Tự Do Nam 80m', 'gender': 'Nam', 'style': 'Tự do', 'dist': '80m', 'qlHeats': [3, 4], 'fnHeat': 2},
            {'id': 'swim_m_e40',  'name': 'Bơi Ếch Nam 40m',   'gender': 'Nam', 'style': 'Ếch',   'dist': '40m', 'qlHeats': [5, 6], 'fnHeat': 3},
            {'id': 'swim_m_e80',  'name': 'Bơi Ếch Nam 80m',   'gender': 'Nam', 'style': 'Ếch',   'dist': '80m', 'qlHeats': [7, 8], 'fnHeat': 4},
            {'id': 'swim_f_td40', 'name': 'Bơi Tự Do Nữ 40m', 'gender': 'Nữ',  'style': 'Tự do', 'dist': '40m', 'qlHeats': [9, 10], 'fnHeat': 5},
            {'id': 'swim_f_e40',  'name': 'Bơi Ếch Nữ 40m',   'gender': 'Nữ',  'style': 'Ếch',   'dist': '40m', 'qlHeats': [11, 12], 'fnHeat': 6}
        ]
    }
]

if __name__ == '__main__':
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    data['tournaments'] = tournaments
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'Done! Successfully updated data.json with {len(tournaments)} tournaments.')
