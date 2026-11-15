---
id: POL-001
category: policy
title: Chính sách mật khẩu và xác thực
publisher: Quy chế An toàn thông tin v3.2
published: 2026-01-15
---
Chính sách này áp dụng cho mọi dịch vụ nội bộ có tài khoản người dùng hoặc tài khoản quản trị.
Mật khẩu phải dài tối thiểu 12 ký tự và không được trùng 10 mật khẩu gần nhất của cùng tài khoản.
Mật khẩu của tài khoản thường phải được đổi định kỳ mỗi 180 ngày hoặc ngay khi nghi ngờ bị lộ.
Mọi tài khoản quản trị bắt buộc bật xác thực đa yếu tố (MFA) bằng ứng dụng OTP hoặc khóa phần cứng.
Tài khoản bị khóa 15 phút sau 5 lần đăng nhập sai liên tiếp để hạn chế dò mật khẩu.
Mật khẩu chỉ được lưu dưới dạng băm Argon2id có muối; nghiêm cấm lưu hoặc ghi log mật khẩu rõ.
Đội dịch vụ chịu trách nhiệm cấu hình đúng chính sách; đội An toàn thông tin rà soát tuân thủ mỗi quý.
