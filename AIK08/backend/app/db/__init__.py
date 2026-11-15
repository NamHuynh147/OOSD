"""Tầng CSDL: PostgreSQL + pgvector, SQL thuần qua psycopg 3 (KHÔNG dùng ORM).

Ràng buộc nằm trong CSDL (xem migrations/*.sql); mã Python chỉ thực thi câu lệnh và
dịch lỗi ràng buộc sang lỗi miền (errors.py).
"""
