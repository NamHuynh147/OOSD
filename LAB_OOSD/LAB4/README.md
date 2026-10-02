# BÁO CÁO KẾT QUẢ LAB 4

## 1. Thông tin sinh viên

- **Họ và tên:** Huỳnh Đại Lục
- **Mã số sinh viên (MSSV):** 1250080109
- **Lớp:** 12_ĐH_CNPM2

## 2. Thông tin bài Lab

- **Tên bài Lab:** LAB 4 - Hệ thống phần mềm Cửa hàng online “e-SHOPPING”
- **Ngày hoàn thành:** 02/10/2026

## 3. Môi trường & Phiên bản (Environment)

- **Hệ điều hành:** Windows 11
- **Ngôn ngữ lập trình:** C#
- **Framework / Thư viện:** .NET 9
- **Công cụ / IDE:** Visual Studio Code 2022

## 4.** Nội dung đã thực hiện

### 4.1 Mục tiêu hệ thống

Hệ thống **e-SHOPPING** là hệ thống mua hàng trực tuyến dành cho khách hàng. Hệ thống không trực tiếp quản lý sản phẩm, thanh toán trực tuyến mà kết nối với các hệ thống/dịch vụ bên ngoài khi cần.

Các chức năng chính của hệ thống:

* Tìm kiếm sản phẩm.
* Xem danh sách nhóm sản phẩm.
* Xem danh sách sản phẩm trong một nhóm.
* Xem chi tiết sản phẩm.
* Quản lý giỏ hàng.
* Quản lý tài khoản khách hàng.
* Quản lý đặt và nhận hàng.
* Quản lý đơn hàng.
* Tính tổng giá tiền cần thanh toán, bao gồm tiền sản phẩm và phí vận chuyển.
* Gửi email thông báo.

### 4.2. Tác nhân (Actors) & Hệ thống bên ngoài

Hệ thống gồm các actor:

1. **Khách hàng:** Người sử dụng hệ thống để tìm kiếm sản phẩm, quản lý giỏ hàng và đặt hàng.
2. **Hệ thống quản lý sản phẩm:** Cung cấp thông tin sản phẩm cho e-SHOPPING.
3. **Hệ thống thanh toán trực tuyến:** Thực hiện xác thực khách hàng và xác thực thanh toán.
4. **Hệ thống Email:** Gửi email xác nhận đơn hàng.

Trong đó, có **3 hệ thống/dịch vụ bên ngoài** được e-SHOPPING tích hợp:

* Hệ thống quản lý sản phẩm.
* Hệ thống thanh toán trực tuyến.
* Hệ thống Email.

---

## 4.3. Danh sách Use Case & Đặc tả chi tiết

### 4.3.1. Danh sách Use Case

| STT | Mã Use Case | Use Case | Tác nhân liên quan |
| :---: | :---: | :--- | :--- |
| 1 | UC01 | Đăng ký tài khoản | Khách hàng |
| 2 | UC02 | Đăng nhập | Khách hàng |
| 3 | UC03 | Xem nhóm sản phẩm | Khách hàng |
| 4 | UC04 | Xem danh sách sản phẩm | Khách hàng |
| 5 | UC05 | Xem chi tiết sản phẩm | Khách hàng |
| 6 | UC06 | Thêm sản phẩm vào giỏ hàng | Khách hàng |
| 7 | UC07 | Xem giỏ hàng | Khách hàng |
| 8 | UC08 | Cập nhật giỏ hàng | Khách hàng |
| 9 | UC09 | Xóa sản phẩm khỏi giỏ | Khách hàng |
| 10 | UC10 | Đặt mua hàng | Khách hàng |
| 11 | UC11 | Gửi email xác nhận đơn hàng | Khách hàng, Hệ thống email |
| 12 | UC12 | Xác thực khách hàng | Hệ thống dịch vụ thanh toán trực tuyến, Khách hàng |
| 13 | UC13 | Lấy thông tin sản phẩm | Hệ thống quản lý sản phẩm |
| 14 | UC14 | Chọn loại giao hàng | Khách hàng |
| 15 | UC15 | Xác thực thanh toán | Hệ thống dịch vụ thanh toán trực tuyến |
| 16 | UC16 | Tính phí giao hàng | Không có |
| 17 | UC17 | Nhập thông tin người nhận | Khách hàng |
| 18 | UC18 | Nhập thông tin thanh toán | Khách hàng |
| 19 | UC19 | Ghi nhận đơn hàng | Không có |

---

### 4.3.2. Đặc tả Use Case chi tiết

#### 📌 UC01 - Đăng ký tài khoản

| Mục | Nội dung |
| :--- | :--- |
| **Mã Use Case** | UC01 |
| **Tên Use Case** | Đăng ký tài khoản |
| **Tác nhân** | Khách hàng (chưa có tài khoản) |
| **Mô tả ngắn** | Tạo tài khoản khách hàng mới trên hệ thống e-SHOPPING. |
| **Quan hệ** | `«include»` Xác thực khách hàng |
| **Điều kiện tiên quyết** | Người dùng chọn chức năng "Đăng ký". |
| **Điều kiện sau** | Thông tin khách hàng mới được lưu vào CSDL. |
| **Luồng sự kiện chính** | 1. Người dùng nhấn "Đăng ký".<br>2. Hệ thống hiển thị biểu mẫu đăng ký.<br>3. Người dùng nhập: họ tên, ngày sinh, CMND/Passport, địa chỉ, điện thoại, tên đăng nhập, mật khẩu, email.<br>4. Người dùng nhấn "Xác nhận đăng ký".<br>5. Hệ thống thực hiện Xác thực khách hàng (kiểm tra dữ liệu hợp lệ, không trùng).<br>6. Hệ thống lưu thông tin vào CSDL.<br>7. Hệ thống báo "Đăng ký thành công". |
| **Luồng ngoại lệ** | **5a. Thiếu thông tin bắt buộc:** yêu cầu điền đủ, quay lại bước 3.<br>**5b. Tên đăng nhập hoặc email đã tồn tại:** báo lỗi, yêu cầu nhập lại. |

---

#### 📌 UC10 - Đặt mua hàng

| Mục | Nội dung |
| :--- | :--- |
| **Mã Use Case** | UC10 |
| **Tên Use Case** | Đặt mua hàng |
| **Tác nhân** | Chính: Khách hàng. Phụ: Hệ thống dịch vụ thanh toán trực tuyến, Hệ thống email. |
| **Mô tả ngắn** | Khách hàng đặt mua các sản phẩm trong giỏ hàng, chọn giao hàng, thanh toán thẻ tín dụng; hệ thống ghi nhận đơn hàng. |
| **Quan hệ** | `«include»`: Xác thực khách hàng, Chọn loại giao hàng, Nhập thông tin người nhận, Tính phí giao hàng, Nhập thông tin thanh toán, Xác thực thanh toán, Ghi nhận đơn hàng.<br>`«extend»` (qua Ghi nhận đơn hàng): Gửi email xác nhận đơn hàng. |
| **Điều kiện tiên quyết** | Giỏ hàng có ít nhất 1 sản phẩm. |
| **Điều kiện sau** | Đơn hàng được ghi nhận vào CSDL; email xác nhận được gửi nếu khách có email. |
| **Luồng sự kiện chính** | 1. Khách hàng nhấn "Tính tiền".<br>2. Xác thực khách hàng: đăng nhập, hoặc đăng ký (UC01) nếu chưa có tài khoản.<br>3. Khách hàng chọn loại giao hàng (thường, nhanh, nhanh trong ngày).<br>4. Khách hàng nhập thông tin người nhận (họ tên, địa chỉ, điện thoại).<br>5. Hệ thống tính phí giao hàng theo khu vực và loại giao hàng (miễn phí nhanh từ 1.000.000đ, nhanh trong ngày từ 5.000.000đ).<br>6. Khách hàng nhập thông tin thanh toán (loại thẻ, số thẻ, ngày hết hạn, tên chủ thẻ, CSV).<br>7. Hệ thống xác thực thanh toán qua Hệ thống dịch vụ thanh toán trực tuyến.<br>8. Hệ thống ghi nhận đơn hàng và báo đặt hàng thành công.<br>9. Nếu khách có email, hệ thống gửi email xác nhận (không kèm thông tin thẻ). |
| **Luồng ngoại lệ** | **2a. Chưa có tài khoản:** chuyển sang UC01.<br>**4a. Thiếu thông tin người nhận:** yêu cầu bổ sung.<br>**6a. Thông tin thẻ sai định dạng:** yêu cầu nhập lại.<br>**7a. Thẻ không hợp lệ hoặc không đủ khả năng thanh toán:** báo lỗi, không ghi nhận đơn.<br>**9a. Khách không có email:** bỏ qua bước gửi email. |

---

## 4.4. Quy định nghiệp vụ (Business Rules)

1. Mỗi sản phẩm phải có **mã sản phẩm duy nhất**.
2. Mỗi sản phẩm thuộc **một nhóm sản phẩm**.
3. Thông tin sản phẩm gồm:
   * Tên sản phẩm.
   * Mã sản phẩm.
   * Nhà sản xuất.
   * Hình ảnh.
   * Mô tả.
   * Thông số kỹ thuật.
   * Giá bán hiện hành.
   * Tình trạng còn/hết hàng.
4. Thông tin sản phẩm được lấy từ **Hệ thống quản lý sản phẩm bên ngoài**.
5. e-SHOPPING **không tự quản lý dữ liệu sản phẩm gốc**.
6. Giá bán phải sử dụng **giá hiện hành tại thời điểm đặt hàng**.
7. Chỉ sản phẩm đang **còn hàng** mới được phép đưa vào đơn mua hàng.
8. Khi đặt hàng, khách hàng có thể chọn:
   * Giao hàng thường.
   * Giao hàng nhanh.
   * Giao hàng nhanh trong ngày.
9. Miễn phí giao hàng nhanh khi đơn hàng từ **1.000.000 VNĐ**.
10. Miễn phí giao hàng nhanh trong ngày khi đơn hàng từ **5.000.000 VNĐ**.
11. Đơn hàng chỉ được ghi nhận khi **thanh toán thành công**.
12. Email xác nhận đơn hàng **không được chứa thông tin thẻ thanh toán**.
13. Nếu khách hàng không có email thì bỏ qua bước gửi email xác nhận.



---

## 4.5. Yêu cầu phi chức năng

### 4.5.1. Bảo mật

* Thông tin thanh toán của khách hàng phải được bảo vệ.
* Không gửi thông tin thẻ thanh toán trong email xác nhận đơn hàng.

### 4.5.2. Toàn vẹn dữ liệu

* Mã sản phẩm phải duy nhất.
* Mỗi sản phẩm thuộc một nhóm sản phẩm.
* Chỉ sản phẩm còn hàng mới được đưa vào đơn hàng.
* Giá sản phẩm phải là giá hiện hành tại thời điểm đặt hàng.
* Đơn hàng không được ghi nhận nếu thanh toán không thành công.

### 4.5.3. Khả năng tích hợp

* Hệ thống phải có khả năng kết nối với Hệ thống quản lý sản phẩm.
* Hệ thống phải kết nối được với Hệ thống thanh toán trực tuyến.
* Hệ thống phải kết nối với Hệ thống Email để gửi email xác nhận đơn hàng.


## 5. Kết quả đạt được

- **Mô tả ngắn:** 
- **Hình ảnh minh họa:**

## 6. Lỗi gặp phải & Cách khắc phục

| STT | Lỗi gặp phải           | Nguyên nhân                                 | Cách khắc phục                       |
| :-: | :--------------------- | :------------------------------------------ | :----------------------------------- |
|  1  | `'` |  |  |**
|  2  | `...`                  | ...                                         | ...                                  |
