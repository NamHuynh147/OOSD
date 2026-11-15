---
id: ARC-001
category: architecture
title: Kiến trúc hệ thống thanh toán
publisher: Tài liệu kiến trúc SA-017
published: 2025-11-20
---
Hệ thống thanh toán gồm cổng thanh toán (payment gateway), dịch vụ sổ cái (ledger) và hàng đợi tin nhắn xử lý bất đồng bộ.
Dữ liệu giao dịch nằm trong cụm PostgreSQL ba nút, một nút chính và hai nút phụ, đặt ở hai vùng sẵn sàng.
Cổng thanh toán phụ thuộc dịch vụ đăng nhập SSO để xác thực lời gọi nội bộ, vì vậy lỗi SSO có thể làm chậm thanh toán.
Chứng chỉ TLS của cổng thanh toán được gia hạn tự động 30 ngày trước khi hết hạn và có cảnh báo khi còn dưới 14 ngày.
Mọi thay đổi cấu hình của cổng thanh toán chỉ thực hiện trong cửa sổ thay đổi quy định.
