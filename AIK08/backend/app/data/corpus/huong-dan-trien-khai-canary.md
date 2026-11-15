---
id: PRC-003
category: process
title: Hướng dẫn triển khai canary và hoàn tác
publisher: Sổ tay vận hành SRE v2.4
published: 2026-03-12
---
Phiên bản mới được triển khai theo ba nấc: 5% lưu lượng, rồi 25%, rồi 100%, mỗi nấc quan sát ít nhất 15 phút.
Chỉ chuyển nấc khi tỷ lệ lỗi dưới 0,5% và độ trễ p95 không tăng quá 20% so với phiên bản đang chạy.
Hệ thống tự động hoàn tác (rollback) nếu tỷ lệ lỗi vượt 2% liên tục trong 5 phút.
Mọi lần hoàn tác phải được ghi lại trong phiếu thay đổi cùng nguyên nhân và hành động tiếp theo.
