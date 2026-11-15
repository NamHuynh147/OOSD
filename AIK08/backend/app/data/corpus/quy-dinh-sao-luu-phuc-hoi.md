---
id: BCP-001
category: continuity
title: Quy định sao lưu và phục hồi dữ liệu
publisher: Quy định BCP/DR v1.8
published: 2026-02-10
---
Dữ liệu thanh toán phải đạt RPO 15 phút và RTO 2 giờ.
Sao lưu đầy đủ chạy mỗi ngày lúc 01:00, kết hợp lưu liên tục nhật ký ghi trước (WAL) để phục hồi theo thời điểm.
Bản sao lưu được mã hóa AES-256, lưu ở vùng khác với vùng sản xuất và giữ tối thiểu 35 ngày.
Việc phục hồi thử phải được thực hiện mỗi quý và có biên bản; sao lưu chưa từng phục hồi thử không được coi là hợp lệ.
Người phụ trách dữ liệu báo cáo kết quả diễn tập phục hồi cho đội An toàn thông tin trong 5 ngày làm việc.
