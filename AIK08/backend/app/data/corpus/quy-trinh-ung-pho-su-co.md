---
id: PRC-001
category: process
title: Quy trình ứng phó sự cố vận hành
publisher: Sổ tay vận hành SRE v2.4
published: 2026-01-20
---
Sự cố được phân loại theo mức độ ảnh hưởng: P1 là ngừng dịch vụ thanh toán hoặc đăng nhập, P2 là suy giảm nghiêm trọng, P3 là ảnh hưởng một phần người dùng, P4 là lỗi nhỏ.
Với P1 phải phản hồi trong 15 phút và đặt mục tiêu khắc phục trong 4 giờ; với P2 phản hồi trong 30 phút và khắc phục trong 8 giờ.
P3 phản hồi trong 4 giờ, khắc phục trong 3 ngày làm việc; P4 xử lý trong ngày làm việc kế tiếp.
Mỗi sự cố P1 và P2 có một người chỉ huy sự cố (incident commander) điều phối và cập nhật tiến độ mỗi 30 phút.
Báo cáo sau sự cố (postmortem) là bắt buộc cho P1 và P2 và phải nộp trong vòng 5 ngày làm việc kể từ khi khắc phục.
Postmortem nêu nguyên nhân gốc, tác động, dòng thời gian và hành động phòng ngừa có người chịu trách nhiệm.
