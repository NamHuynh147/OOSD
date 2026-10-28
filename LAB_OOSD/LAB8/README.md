# Quản lý Bán nước Giải khát – QuanLyNGK

Bài thực hành **Lab 8** – Phân tích thiết kế hệ thống và xây dựng giao diện WinForms cho hệ thống quản lý mua bán và phân phối Nước giải khát (NGK).

|               |                                                           |
| ------------- | --------------------------------------------------------- |
| **Sinh viên** | Huỳnh Đại Lục                                             |
| **MSSV**      | 1250080109                                                |
| **Công nghệ** | C# WinForms, .NET Framework 4.7.2  , SQL Server       |
| **Công cụ**   | Visual Studio 2022, SQL Server Management Studio, draw.io |

---

## 1. Giới thiệu

Hệ thống tin học hóa quy trình quản lý bán và phân phối nước giải khát (NGK) cho đại lý/cửa hàng, bao gồm:

- Quản lý danh mục Nước giải khát, Nhãn hiệu và Nhà cung ứng.
- Lập Đơn đặt hàng (ĐĐH) gửi cho Nhà cung ứng và ghi nhận Phiếu giao hàng (tối đa 3 đợt/đơn).
- Quản lý Khách hàng (Khách quen và Khách vãng lai).
- Quản lý Hóa đơn bán hàng, Phiếu hẹn (khi kho thiếu hàng cho Khách quen) và Phiếu ghi nợ (trả chậm).
- Tra cứu, thống kê doanh thu, tồn kho và công nợ.

---

## 2. Nội dung báo cáo (file `Lab8.docx`)

| Phần             | Nội dung                                                                                                                                                               |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Yêu cầu hệ thống | Đầu vào – xử lý – xuất kết quả; bảng Actor – Công việc – Quy định; quy tắc nghiệp vụ (BR01–BR08); quyết định triển khai (QD01–QD09); yêu cầu chức năng & phi chức năng |
| Câu 1            | Xác định 14 class chính, thuộc tính, phương thức và định danh                                                                                                          |
| Câu 2            | Mối liên kết, bản số giữa các class và Class Diagram                                                                                                                   |
| Câu 3            | Actor và Use Case tổng quát (UC01–UC08)                                                                                                                                |
| Câu 4            | Use Case phân rã: Lập đơn đặt hàng, Ghi nhận phiếu giao, Bán hàng & Ghi nợ                                                                                             |
| Câu 5            | Activity Diagram cho các luồng nghiệp vụ giao hàng và ghi nợ                                                                                                           |
| Câu 6            | Sequence Diagram xử lý Transaction bán hàng và trừ tồn kho                                                                                                             |
| Phần cuối        | Giao diện các Form WinForms phân lớp theo mô hình UI - Services - Models - Data                                                                                        |

### 2.1. Các class chính

`NhanHieu`, `NhaCungUng`, `NuocGiaiKhat`, `KhachHang`, `NhanVien`, `DonDatHang`, `ChiTietDDH`, `PhieuGiao`, `ChiTietPhieuGiao`, `HoaDon`, `ChiTietHoaDon`, `PhieuHen`, `ChiTietPhieuHen`, `PhieuGhiNo`.

### 2.2. Quan hệ tiêu biểu

- `NhaCungUng` 1 – N `NhanHieu`; `NhanHieu` 1 – N `NuocGiaiKhat`.
- `NhaCungUng` 1 – N `DonDatHang`; `DonDatHang` 1 – N `ChiTietDDH` (Composition).
- `DonDatHang` 1 – 0..3 `PhieuGiao` (Mỗi ĐĐH giao tối đa 3 đợt); `PhieuGiao` 1 – N `ChiTietPhieuGiao`.
- `KhachHang` 1 – N `HoaDon`; `HoaDon` 1 – N `ChiTietHoaDon` (Composition).
- `HoaDon` 1 – 0..N `PhieuHen` (Hóa đơn khách quen "Chờ giao hẹn" có thể lập nhiều phiếu hẹn giao từng đợt).
- `HoaDon` 1 – 0..1 `PhieuGhiNo` (Chỉ dành cho khách quen trả chậm).

### 2.3. Actor

- **Nhân viên cửa hàng**: Người trực tiếp sử dụng phần mềm (quản lý danh mục, lập ĐĐH, ghi nhận phiếu giao, lập hóa đơn, phiếu hẹn, lập phiếu ghi nợ, tra cứu, thống kê).
- **Nhà cung ứng**: Actor bên ngoài (nhận ĐĐH, giao hàng tối đa 3 đợt kèm phiếu giao).
- **Khách hàng**: Actor bên ngoài (đặt mua NGK, nhận hàng và hóa đơn; bao gồm Khách quen và Khách vãng lai).
- **Khách quen**: Được hẹn giao nhiều đợt khi kho thiếu và được trả chậm (phiếu ghi nợ).
- **Khách vãng lai**: Thanh toán và nhận hàng ngay tại cửa hàng; không hẹn giao, không ghi nợ.

---

## 3. Chức năng hệ thống WinForms (`QuanLyNGK`)

- **Quản lý Danh mục**: Thêm/Sửa/Xóa Nước giải khát, Nhãn hiệu, Nhà cung ứng, Khách hàng.
- **Quản lý Đơn đặt hàng & Nhập kho**: Lập ĐĐH gửi nhà cung ứng, ghi nhận Phiếu giao (tự tăng số đợt 1..3, tự cập nhật cộng số lượng tồn kho `SoLuongTon`).
- **Quản lý Bán hàng & Hóa đơn**: Lập hóa đơn bán hàng cho khách vãng lai/khách quen. Tự động kiểm tra tồn kho bằng khóa `UPDLOCK`, trừ tồn kho trong Transaction.
- **Quản lý Giao hẹn & Công nợ**: Lập Phiếu hẹn giao đợt tiếp theo khi kho đủ hàng; lập Phiếu ghi nợ cho khách quen trả chậm với hạn trả dự kiến.
- **Tra cứu & Thống kê**: Tìm kiếm chứng từ theo từ khóa/khoảng ngày, xuất bảng chỉ số tổng hợp nhập/bán/hẹn/nợ.

### Đáp ứng yêu cầu chức năng hệ thống

| STT | Yêu cầu              | Cách thực hiện                                                                                                      |
| --- | -------------------- | ------------------------------------------------------------------------------------------------------------------- |
| 1   | Kiểm tra dữ liệu     | Bắt buộc Mã, Tên; kiểm tra Số lượng > 0, Đơn giá > 0, Ngày hẹn/Ngày nợ hợp lệ                                       |
| 2   | Transaction          | Thao tác ghi nhiều bảng (ĐĐH + CT_DDH, Hóa đơn + CT_HoaDon + Trừ kho) chạy trong `SqlTransaction`, lỗi thì Rollback |
| 3   | Thông báo trạng thái | `MessageBox` hiển thị nguyên nhân chi tiết từ tầng Service/CSDL                                                     |
| 4   | Tra cứu quan hệ      | `ComboBox` chứa danh mục khóa ngoại (NhaCungUng, NhanHieu, KhachHang); `DataGridView` hiển thị danh sách            |
| 5   | Ngăn thao tác rủi ro | Khóa mã chính khi sửa; ràng buộc Foreign Key chặn xóa dữ liệu đã phát sinh nghiệp vụ                                |

---

## 4. Cấu trúc thư mục dự án

Dựa trên cấu trúc tổ chức dự án thực tế trong thư mục `D:\LAB_OOSD\LAB8\`:

`

---

## 5. Cơ sở dữ liệu

Database `QL_NGK` được thiết kế theo đúng quy tắc nghiệp vụ (BR01–BR08) và các quyết định triển khai (QD01–QD09):

| Bảng               | Khóa chính             | Khóa ngoại & Ràng buộc                                         |
| ------------------ | ---------------------- | -------------------------------------------------------------- |
| `NhaCungUng`       | `MaNCC`                | Lưu thông tin Tên, Địa chỉ, SĐT                                |
| `NhanHieu`         | `MaLoai`               | `MaNCC` → `NhaCungUng` (QD01)                                  |
| `NuocGiaiKhat`     | `MaNGK`                | `MaLoai` → `NhanHieu`, `SoLuongTon` $\ge 0$                    |
| `KhachHang`        | `MaKH`                 | Phân loại Khách quen / Khách vãng lai                          |
| `DonDatHang`       | `MaDDH`                | `MaNCC` → `NhaCungUng`, Ngày đặt, Ngày nhận                    |
| `ChiTietDDH`       | `MaDDH`, `MaNGK`       | Số lượng đặt                                                   |
| `PhieuGiao`        | `MaPhieuGiao`          | `MaDDH` → `DonDatHang`, `DotGiao` (1..3)                       |
| `ChiTietPhieuGiao` | `MaPhieuGiao`, `MaNGK` | Số lượng giao, DonGiaNhap                                      |
| `HoaDon`           | `MaHD`                 | `MaKH` → `KhachHang`, TrangThai ("Đã giao đủ", "Chờ giao hẹn") |
| `ChiTietHoaDon`    | `MaHD`, `MaNGK`        | Số lượng bán, DonGiaBan                                        |
| `PhieuHen`         | `MaPhieuHen`           | `MaHD` → `HoaDon`                                              |
| `ChiTietPhieuHen`  | `MaPhieuHen`, `MaNGK`  | Số lượng hẹn giao                                              |
| `PhieuGhiNo`       | `MaPhieuNo`            | `MaHD` → `HoaDon`, SoTienNo $\le$ TongTien                     |

---

## 6. Hướng dẫn cài đặt và chạy ứng dụng

1. Mở **SQL Server Management Studio (SSMS)**, mở file `Database/QL_NGK.sql` và nhấn **Execute** để khởi tạo CSDL và dữ liệu mẫu.
2. Mở file giải pháp `QuanLyNGK.csproj` hoặc `QuanLyNGK.sln` bằng **Visual Studio 2022**.
3. Mở file `App.config`, kiểm tra và chỉnh sửa chuỗi kết nối `connectionString` khớp với tên Server SQL của bạn:
   ```xml
   <connectionStrings>
     <add name="QL_NGK_Conn" connectionString="Data Source=.;Initial Catalog=QL_NGK;Integrated Security=True" providerName="System.Data.SqlClient"/>
   </connectionStrings>
   ```
4. Nhấn **F5** (hoặc bấm nút **Start**) để chạy ứng dụng.

---

## 7. Đánh giá và Hướng phát triển

- **Đạt được**: Cài đặt hoàn chỉnh kiến trúc phân lớp (UI - Services - Models - Data) chuẩn OOP/OOSD, xử lý Transaction an toàn dữ liệu khi mua/bán, giao diện tiếng Việt thân thiện chuẩn `vi-VN`.
- **Hướng phát triển**: Bổ sung phân quyền nhân viên, in báo cáo hóa đơn qua Crystal Reports/DevExpress, kết nối thêm mã vạch cho sản phẩm.
