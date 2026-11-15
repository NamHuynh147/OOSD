"""Bộ đánh giá tìm kiếm: câu hỏi -> các doc_id chấp nhận được (chỉ cần một trong số đó nằm trong top-3).
Viết theo cách người dùng thật hỏi (có và không có dấu, câu hỏi dài, từ thông dụng), KHÔNG chép nguyên câu từ tài liệu."""

RELEVANT = [
    ("Sự cố P1 phải được phản hồi trong bao lâu?", {"PRC-001"}),
    ("quy trinh ung pho su co ra sao", {"PRC-001"}),
    ("Ai là người điều phối khi có sự cố nghiêm trọng?", {"PRC-001"}),
    ("postmortem phải nộp trong thời hạn nào", {"PRC-001", "RPT-001"}),
    ("Mật khẩu tối thiểu bao nhiêu ký tự?", {"POL-001"}),
    ("Tài khoản bị khóa khi đăng nhập sai mấy lần", {"POL-001"}),
    ("tai khoan quan tri co bat buoc MFA khong", {"POL-001"}),
    ("mật khẩu được lưu như thế nào", {"POL-001"}),
    ("Ai được truy cập môi trường sản xuất và trong bao lâu?", {"POL-002"}),
    ("nhật ký truy cập dữ liệu khách hàng lưu bao lâu", {"POL-002"}),
    ("Quyền của tài khoản được rà soát khi nào", {"POL-002"}),
    ("Cam kết SLA của dịch vụ thanh toán là bao nhiêu phần trăm", {"SLA-001"}),
    ("dich vu SSO cam ket san sang bao nhieu", {"SLA-001"}),
    ("Điều gì xảy ra khi dịch vụ vi phạm SLA hai tháng liên tiếp", {"SLA-001"}),
    ("RPO và RTO của dữ liệu thanh toán", {"BCP-001"}),
    ("Bản sao lưu được giữ bao nhiêu ngày", {"BCP-001"}),
    ("sao lưu có được mã hóa không", {"BCP-001"}),
    ("Bao lâu phải diễn tập phục hồi một lần?", {"BCP-001"}),
    ("CAB họp vào ngày nào", {"PRC-002"}),
    ("thay đổi khẩn cấp xử lý ra sao", {"PRC-002"}),
    ("Cấu hình SSO có được thay đổi không qua CAB không", {"PRC-002", "RPT-001"}),
    ("Triển khai canary gồm những nấc nào", {"PRC-003"}),
    ("Khi nào hệ thống tự động rollback", {"PRC-003"}),
    ("Cổng thanh toán phụ thuộc dịch vụ nào", {"ARC-001"}),
    ("Chứng chỉ TLS được gia hạn khi nào", {"ARC-001", "RPT-001"}),
    ("dữ liệu giao dịch nằm ở đâu", {"ARC-001"}),
    ("Tháng 9 có bao nhiêu sự cố", {"RPT-001"}),
    ("báo cáo sự cố tháng 09/2026", {"RPT-001"}),
    ("Sự cố INC-0911 do nguyên nhân gì", {"RPT-001"}),
    ("Cửa sổ bảo trì cơ sở dữ liệu thanh toán là lúc nào", {"NOTE-001", "PRC-002"}),
]

# Câu hỏi ngoài phạm vi kho tài liệu: kỳ vọng không có kết quả nào (không nhồi nguồn không liên quan).
OUT_OF_SCOPE = [
    "Thời tiết Hà Nội hôm nay thế nào?",
    "Giá vàng hôm nay là bao nhiêu",
    "Công thức nấu phở bò",
    "Ai vô địch World Cup 2022",
    "Hướng dẫn cài đặt Photoshop",
    "Lịch thi đấu bóng đá cuối tuần này",
]
