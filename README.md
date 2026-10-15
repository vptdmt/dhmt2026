# Đại Hội Mường Thanh 2026 - Quản Lý Lịch Thi Đấu & Lịch Trình

Ứng dụng web quản lý lịch trình, lịch thi đấu, danh sách vận động viên, lịch di chuyển và cập nhật kết quả thi đấu thời gian thực (Realtime Cloud Sync) phục vụ Đại hội Mường Thanh 2026 tại Ninh Bình (27 - 29/10/2026).

## 🚀 Tính năng chính
- 📅 **Agenda**: Lịch trình tổng thể 3 ngày hội tụ theo khung giờ và loại hoạt động.
- 🏆 **Lịch thi đấu**: Ma trận lịch chi tiết theo sân/bàn/khung giờ, tự động đồng bộ kết quả.
- 👤 **Vận động viên**: Tra cứu 358 VĐV theo đơn vị, môn thi và in phiếu lịch thi đấu cá nhân.
- 📍 **Địa điểm**: Thông tin các cụm thi đấu và sơ đồ sân bãi.
- 🚌 **Lịch di chuyển**: Điều phối xe đưa đón giữa Khách sạn Mường Thanh, Nhà thi đấu Ninh Bình và Sân bóng Teddy; tự động tính định mức VĐV vòng Bán kết/Chung kết; in phiếu điều xe và xuất CSV.
- 🥇 **Kết quả & Sơ đồ thi đấu (Realtime)**: Cập nhật tỷ số trực tiếp qua Google Firebase Realtime Database; phân quyền Admin BTC và Tổ Trọng tài theo từng môn.

## 🛠️ Công nghệ
- HTML5, CSS3 (Tailwind CSS CDN), Vanilla JavaScript.
- Google Firebase Realtime Database (Đồng bộ tức thì không cần tải lại trang).
- Hoàn toàn độc lập, chạy trực tiếp trên GitHub Pages.
