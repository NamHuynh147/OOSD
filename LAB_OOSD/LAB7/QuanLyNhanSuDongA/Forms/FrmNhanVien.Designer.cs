namespace QuanLyNhanSuDongA.Forms
{
    partial class FrmNhanVien
    {
        private System.ComponentModel.IContainer components = null;

        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null)) components.Dispose();
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        private void InitializeComponent()
        {
            this.lblTieuDe = new System.Windows.Forms.Label();
            this.grpNhanVien = new System.Windows.Forms.GroupBox();
            this.lblMaNV = new System.Windows.Forms.Label();
            this.txtMaNV = new System.Windows.Forms.TextBox();
            this.lblHoTen = new System.Windows.Forms.Label();
            this.txtHoTen = new System.Windows.Forms.TextBox();
            this.lblNgaySinh = new System.Windows.Forms.Label();
            this.dtpNgaySinh = new System.Windows.Forms.DateTimePicker();
            this.lblGioiTinh = new System.Windows.Forms.Label();
            this.cboGioiTinh = new System.Windows.Forms.ComboBox();
            this.lblSDT = new System.Windows.Forms.Label();
            this.txtSDT = new System.Windows.Forms.TextBox();
            this.lblEmail = new System.Windows.Forms.Label();
            this.txtEmail = new System.Windows.Forms.TextBox();
            this.lblPhongBan = new System.Windows.Forms.Label();
            this.cboPhongBan = new System.Windows.Forms.ComboBox();
            this.lblTrangThai = new System.Windows.Forms.Label();
            this.cboTrangThai = new System.Windows.Forms.ComboBox();
            this.lblDiaChi = new System.Windows.Forms.Label();
            this.txtDiaChi = new System.Windows.Forms.TextBox();
            this.grpThuViec = new System.Windows.Forms.GroupBox();
            this.chkThuViec = new System.Windows.Forms.CheckBox();
            this.lblSoQD = new System.Windows.Forms.Label();
            this.txtSoQD = new System.Windows.Forms.TextBox();
            this.lblNgayKy = new System.Windows.Forms.Label();
            this.dtpNgayKy = new System.Windows.Forms.DateTimePicker();
            this.lblThang = new System.Windows.Forms.Label();
            this.numThang = new System.Windows.Forms.NumericUpDown();
            this.lblLuong = new System.Windows.Forms.Label();
            this.numLuong = new System.Windows.Forms.NumericUpDown();
            this.lblDieuKhoan = new System.Windows.Forms.Label();
            this.txtDieuKhoan = new System.Windows.Forms.TextBox();
            this.btnThem = new System.Windows.Forms.Button();
            this.btnSua = new System.Windows.Forms.Button();
            this.btnXoa = new System.Windows.Forms.Button();
            this.btnLamMoi = new System.Windows.Forms.Button();
            this.btnThoat = new System.Windows.Forms.Button();
            this.lblTim = new System.Windows.Forms.Label();
            this.txtTim = new System.Windows.Forms.TextBox();
            this.cboLocPB = new System.Windows.Forms.ComboBox();
            this.btnTim = new System.Windows.Forms.Button();
            this.dgvNhanVien = new System.Windows.Forms.DataGridView();
            this.lblTong = new System.Windows.Forms.Label();
            this.grpNhanVien.SuspendLayout();
            this.grpThuViec.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.numThang)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.numLuong)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.dgvNhanVien)).BeginInit();
            this.SuspendLayout();
            // 
            // lblTieuDe
            // 
            this.lblTieuDe.Font = new System.Drawing.Font("Segoe UI", 14F, System.Drawing.FontStyle.Bold);
            this.lblTieuDe.ForeColor = System.Drawing.Color.DarkBlue;
            this.lblTieuDe.Location = new System.Drawing.Point(0, 9);
            this.lblTieuDe.Name = "lblTieuDe";
            this.lblTieuDe.Size = new System.Drawing.Size(1257, 34);
            this.lblTieuDe.TabIndex = 0;
            this.lblTieuDe.Text = "QUẢN LÝ NHÂN VIÊN & QUYẾT ĐỊNH THỬ VIỆC - CÔNG TY SƠN ĐÔNG Á";
            this.lblTieuDe.TextAlign = System.Drawing.ContentAlignment.MiddleCenter;
            // 
            // grpNhanVien
            // 
            this.grpNhanVien.Controls.Add(this.lblMaNV);
            this.grpNhanVien.Controls.Add(this.txtMaNV);
            this.grpNhanVien.Controls.Add(this.lblHoTen);
            this.grpNhanVien.Controls.Add(this.txtHoTen);
            this.grpNhanVien.Controls.Add(this.lblNgaySinh);
            this.grpNhanVien.Controls.Add(this.dtpNgaySinh);
            this.grpNhanVien.Controls.Add(this.lblGioiTinh);
            this.grpNhanVien.Controls.Add(this.cboGioiTinh);
            this.grpNhanVien.Controls.Add(this.lblSDT);
            this.grpNhanVien.Controls.Add(this.txtSDT);
            this.grpNhanVien.Controls.Add(this.lblEmail);
            this.grpNhanVien.Controls.Add(this.txtEmail);
            this.grpNhanVien.Controls.Add(this.lblPhongBan);
            this.grpNhanVien.Controls.Add(this.cboPhongBan);
            this.grpNhanVien.Controls.Add(this.lblTrangThai);
            this.grpNhanVien.Controls.Add(this.cboTrangThai);
            this.grpNhanVien.Controls.Add(this.lblDiaChi);
            this.grpNhanVien.Controls.Add(this.txtDiaChi);
            this.grpNhanVien.Location = new System.Drawing.Point(14, 51);
            this.grpNhanVien.Name = "grpNhanVien";
            this.grpNhanVien.Size = new System.Drawing.Size(617, 245);
            this.grpNhanVien.TabIndex = 1;
            this.grpNhanVien.TabStop = false;
            this.grpNhanVien.Text = "Thông tin nhân viên";
            // 
            // lblMaNV
            // 
            this.lblMaNV.AutoSize = true;
            this.lblMaNV.Location = new System.Drawing.Point(17, 35);
            this.lblMaNV.Name = "lblMaNV";
            this.lblMaNV.Size = new System.Drawing.Size(48, 16);
            this.lblMaNV.TabIndex = 0;
            this.lblMaNV.Text = "Mã NV";
            // 
            // txtMaNV
            // 
            this.txtMaNV.Location = new System.Drawing.Point(114, 32);
            this.txtMaNV.Name = "txtMaNV";
            this.txtMaNV.Size = new System.Drawing.Size(188, 22);
            this.txtMaNV.TabIndex = 1;
            // 
            // lblHoTen
            // 
            this.lblHoTen.AutoSize = true;
            this.lblHoTen.Location = new System.Drawing.Point(320, 35);
            this.lblHoTen.Name = "lblHoTen";
            this.lblHoTen.Size = new System.Drawing.Size(46, 16);
            this.lblHoTen.TabIndex = 2;
            this.lblHoTen.Text = "Họ tên";
            // 
            // txtHoTen
            // 
            this.txtHoTen.Location = new System.Drawing.Point(411, 32);
            this.txtHoTen.Name = "txtHoTen";
            this.txtHoTen.Size = new System.Drawing.Size(188, 22);
            this.txtHoTen.TabIndex = 3;
            // 
            // lblNgaySinh
            // 
            this.lblNgaySinh.AutoSize = true;
            this.lblNgaySinh.Location = new System.Drawing.Point(17, 73);
            this.lblNgaySinh.Name = "lblNgaySinh";
            this.lblNgaySinh.Size = new System.Drawing.Size(67, 16);
            this.lblNgaySinh.TabIndex = 4;
            this.lblNgaySinh.Text = "Ngày sinh";
            // 
            // dtpNgaySinh
            // 
            this.dtpNgaySinh.Format = System.Windows.Forms.DateTimePickerFormat.Short;
            this.dtpNgaySinh.Location = new System.Drawing.Point(114, 69);
            this.dtpNgaySinh.Name = "dtpNgaySinh";
            this.dtpNgaySinh.Size = new System.Drawing.Size(188, 22);
            this.dtpNgaySinh.TabIndex = 5;
            // 
            // lblGioiTinh
            // 
            this.lblGioiTinh.AutoSize = true;
            this.lblGioiTinh.Location = new System.Drawing.Point(320, 73);
            this.lblGioiTinh.Name = "lblGioiTinh";
            this.lblGioiTinh.Size = new System.Drawing.Size(54, 16);
            this.lblGioiTinh.TabIndex = 6;
            this.lblGioiTinh.Text = "Giới tính";
            // 
            // cboGioiTinh
            // 
            this.cboGioiTinh.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.cboGioiTinh.Location = new System.Drawing.Point(411, 69);
            this.cboGioiTinh.Name = "cboGioiTinh";
            this.cboGioiTinh.Size = new System.Drawing.Size(188, 24);
            this.cboGioiTinh.TabIndex = 7;
            // 
            // lblSDT
            // 
            this.lblSDT.AutoSize = true;
            this.lblSDT.Location = new System.Drawing.Point(17, 110);
            this.lblSDT.Name = "lblSDT";
            this.lblSDT.Size = new System.Drawing.Size(66, 16);
            this.lblSDT.TabIndex = 8;
            this.lblSDT.Text = "Điện thoại";
            // 
            // txtSDT
            // 
            this.txtSDT.Location = new System.Drawing.Point(114, 107);
            this.txtSDT.Name = "txtSDT";
            this.txtSDT.Size = new System.Drawing.Size(188, 22);
            this.txtSDT.TabIndex = 9;
            // 
            // lblEmail
            // 
            this.lblEmail.AutoSize = true;
            this.lblEmail.Location = new System.Drawing.Point(320, 110);
            this.lblEmail.Name = "lblEmail";
            this.lblEmail.Size = new System.Drawing.Size(41, 16);
            this.lblEmail.TabIndex = 10;
            this.lblEmail.Text = "Email";
            // 
            // txtEmail
            // 
            this.txtEmail.Location = new System.Drawing.Point(411, 107);
            this.txtEmail.Name = "txtEmail";
            this.txtEmail.Size = new System.Drawing.Size(188, 22);
            this.txtEmail.TabIndex = 11;
            // 
            // lblPhongBan
            // 
            this.lblPhongBan.AutoSize = true;
            this.lblPhongBan.Location = new System.Drawing.Point(17, 147);
            this.lblPhongBan.Name = "lblPhongBan";
            this.lblPhongBan.Size = new System.Drawing.Size(72, 16);
            this.lblPhongBan.TabIndex = 12;
            this.lblPhongBan.Text = "Phòng ban";
            // 
            // cboPhongBan
            // 
            this.cboPhongBan.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.cboPhongBan.Location = new System.Drawing.Point(114, 144);
            this.cboPhongBan.Name = "cboPhongBan";
            this.cboPhongBan.Size = new System.Drawing.Size(188, 24);
            this.cboPhongBan.TabIndex = 13;
            // 
            // lblTrangThai
            // 
            this.lblTrangThai.AutoSize = true;
            this.lblTrangThai.Location = new System.Drawing.Point(320, 147);
            this.lblTrangThai.Name = "lblTrangThai";
            this.lblTrangThai.Size = new System.Drawing.Size(67, 16);
            this.lblTrangThai.TabIndex = 14;
            this.lblTrangThai.Text = "Trạng thái";
            // 
            // cboTrangThai
            // 
            this.cboTrangThai.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.cboTrangThai.Location = new System.Drawing.Point(411, 144);
            this.cboTrangThai.Name = "cboTrangThai";
            this.cboTrangThai.Size = new System.Drawing.Size(188, 24);
            this.cboTrangThai.TabIndex = 15;
            // 
            // lblDiaChi
            // 
            this.lblDiaChi.AutoSize = true;
            this.lblDiaChi.Location = new System.Drawing.Point(17, 185);
            this.lblDiaChi.Name = "lblDiaChi";
            this.lblDiaChi.Size = new System.Drawing.Size(47, 16);
            this.lblDiaChi.TabIndex = 16;
            this.lblDiaChi.Text = "Địa chỉ";
            // 
            // txtDiaChi
            // 
            this.txtDiaChi.Location = new System.Drawing.Point(114, 181);
            this.txtDiaChi.Name = "txtDiaChi";
            this.txtDiaChi.Size = new System.Drawing.Size(485, 22);
            this.txtDiaChi.TabIndex = 17;
            // 
            // grpThuViec
            // 
            this.grpThuViec.Controls.Add(this.chkThuViec);
            this.grpThuViec.Controls.Add(this.lblSoQD);
            this.grpThuViec.Controls.Add(this.txtSoQD);
            this.grpThuViec.Controls.Add(this.lblNgayKy);
            this.grpThuViec.Controls.Add(this.dtpNgayKy);
            this.grpThuViec.Controls.Add(this.lblThang);
            this.grpThuViec.Controls.Add(this.numThang);
            this.grpThuViec.Controls.Add(this.lblLuong);
            this.grpThuViec.Controls.Add(this.numLuong);
            this.grpThuViec.Controls.Add(this.lblDieuKhoan);
            this.grpThuViec.Controls.Add(this.txtDieuKhoan);
            this.grpThuViec.Location = new System.Drawing.Point(642, 51);
            this.grpThuViec.Name = "grpThuViec";
            this.grpThuViec.Size = new System.Drawing.Size(594, 245);
            this.grpThuViec.TabIndex = 2;
            this.grpThuViec.TabStop = false;
            this.grpThuViec.Text = "Quyết định tuyển dụng / thử việc";
            // 
            // chkThuViec
            // 
            this.chkThuViec.AutoSize = true;
            this.chkThuViec.Checked = true;
            this.chkThuViec.CheckState = System.Windows.Forms.CheckState.Checked;
            this.chkThuViec.Location = new System.Drawing.Point(17, 27);
            this.chkThuViec.Name = "chkThuViec";
            this.chkThuViec.Size = new System.Drawing.Size(354, 20);
            this.chkThuViec.TabIndex = 0;
            this.chkThuViec.Text = "Lập quyết định thử việc kèm theo (thao tác Transaction)";
            this.chkThuViec.CheckedChanged += new System.EventHandler(this.chkThuViec_CheckedChanged);
            // 
            // lblSoQD
            // 
            this.lblSoQD.AutoSize = true;
            this.lblSoQD.Location = new System.Drawing.Point(17, 62);
            this.lblSoQD.Name = "lblSoQD";
            this.lblSoQD.Size = new System.Drawing.Size(88, 16);
            this.lblSoQD.TabIndex = 1;
            this.lblSoQD.Text = "Số quyết định";
            // 
            // txtSoQD
            // 
            this.txtSoQD.Location = new System.Drawing.Point(126, 59);
            this.txtSoQD.Name = "txtSoQD";
            this.txtSoQD.Size = new System.Drawing.Size(171, 22);
            this.txtSoQD.TabIndex = 2;
            // 
            // lblNgayKy
            // 
            this.lblNgayKy.AutoSize = true;
            this.lblNgayKy.Location = new System.Drawing.Point(320, 62);
            this.lblNgayKy.Name = "lblNgayKy";
            this.lblNgayKy.Size = new System.Drawing.Size(57, 16);
            this.lblNgayKy.TabIndex = 3;
            this.lblNgayKy.Text = "Ngày ký";
            // 
            // dtpNgayKy
            // 
            this.dtpNgayKy.Format = System.Windows.Forms.DateTimePickerFormat.Short;
            this.dtpNgayKy.Location = new System.Drawing.Point(406, 59);
            this.dtpNgayKy.Name = "dtpNgayKy";
            this.dtpNgayKy.Size = new System.Drawing.Size(171, 22);
            this.dtpNgayKy.TabIndex = 4;
            // 
            // lblThang
            // 
            this.lblThang.AutoSize = true;
            this.lblThang.Location = new System.Drawing.Point(17, 99);
            this.lblThang.Name = "lblThang";
            this.lblThang.Size = new System.Drawing.Size(102, 16);
            this.lblThang.TabIndex = 5;
            this.lblThang.Text = "Thử việc (tháng)";
            // 
            // numThang
            // 
            this.numThang.Location = new System.Drawing.Point(126, 96);
            this.numThang.Maximum = new decimal(new int[] {
            1000000000,
            0,
            0,
            0});
            this.numThang.Name = "numThang";
            this.numThang.Size = new System.Drawing.Size(171, 22);
            this.numThang.TabIndex = 6;
            // 
            // lblLuong
            // 
            this.lblLuong.AutoSize = true;
            this.lblLuong.Location = new System.Drawing.Point(320, 99);
            this.lblLuong.Name = "lblLuong";
            this.lblLuong.Size = new System.Drawing.Size(92, 16);
            this.lblLuong.TabIndex = 7;
            this.lblLuong.Text = "Lương thử việc";
            // 
            // numLuong
            // 
            this.numLuong.Increment = new decimal(new int[] {
            100000,
            0,
            0,
            0});
            this.numLuong.Location = new System.Drawing.Point(429, 96);
            this.numLuong.Maximum = new decimal(new int[] {
            1000000000,
            0,
            0,
            0});
            this.numLuong.Name = "numLuong";
            this.numLuong.Size = new System.Drawing.Size(149, 22);
            this.numLuong.TabIndex = 8;
            this.numLuong.ThousandsSeparator = true;
            // 
            // lblDieuKhoan
            // 
            this.lblDieuKhoan.AutoSize = true;
            this.lblDieuKhoan.Location = new System.Drawing.Point(17, 137);
            this.lblDieuKhoan.Name = "lblDieuKhoan";
            this.lblDieuKhoan.Size = new System.Drawing.Size(74, 16);
            this.lblDieuKhoan.TabIndex = 9;
            this.lblDieuKhoan.Text = "Điều khoản";
            // 
            // txtDieuKhoan
            // 
            this.txtDieuKhoan.Location = new System.Drawing.Point(126, 133);
            this.txtDieuKhoan.Multiline = true;
            this.txtDieuKhoan.Name = "txtDieuKhoan";
            this.txtDieuKhoan.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this.txtDieuKhoan.Size = new System.Drawing.Size(451, 96);
            this.txtDieuKhoan.TabIndex = 10;
            // 
            // btnThem
            // 
            this.btnThem.Location = new System.Drawing.Point(14, 307);
            this.btnThem.Name = "btnThem";
            this.btnThem.Size = new System.Drawing.Size(114, 36);
            this.btnThem.TabIndex = 3;
            this.btnThem.Text = "Thêm";
            this.btnThem.UseVisualStyleBackColor = true;
            this.btnThem.Click += new System.EventHandler(this.btnThem_Click);
            // 
            // btnSua
            // 
            this.btnSua.Location = new System.Drawing.Point(139, 307);
            this.btnSua.Name = "btnSua";
            this.btnSua.Size = new System.Drawing.Size(114, 36);
            this.btnSua.TabIndex = 4;
            this.btnSua.Text = "Sửa";
            this.btnSua.UseVisualStyleBackColor = true;
            this.btnSua.Click += new System.EventHandler(this.btnSua_Click);
            // 
            // btnXoa
            // 
            this.btnXoa.Location = new System.Drawing.Point(265, 307);
            this.btnXoa.Name = "btnXoa";
            this.btnXoa.Size = new System.Drawing.Size(114, 36);
            this.btnXoa.TabIndex = 5;
            this.btnXoa.Text = "Xóa";
            this.btnXoa.UseVisualStyleBackColor = true;
            this.btnXoa.Click += new System.EventHandler(this.btnXoa_Click);
            // 
            // btnLamMoi
            // 
            this.btnLamMoi.Location = new System.Drawing.Point(391, 307);
            this.btnLamMoi.Name = "btnLamMoi";
            this.btnLamMoi.Size = new System.Drawing.Size(114, 36);
            this.btnLamMoi.TabIndex = 6;
            this.btnLamMoi.Text = "Làm mới";
            this.btnLamMoi.UseVisualStyleBackColor = true;
            this.btnLamMoi.Click += new System.EventHandler(this.btnLamMoi_Click);
            // 
            // btnThoat
            // 
            this.btnThoat.Location = new System.Drawing.Point(517, 307);
            this.btnThoat.Name = "btnThoat";
            this.btnThoat.Size = new System.Drawing.Size(114, 36);
            this.btnThoat.TabIndex = 7;
            this.btnThoat.Text = "Thoát";
            this.btnThoat.UseVisualStyleBackColor = true;
            this.btnThoat.Click += new System.EventHandler(this.btnThoat_Click);
            // 
            // lblTim
            // 
            this.lblTim.AutoSize = true;
            this.lblTim.Location = new System.Drawing.Point(686, 316);
            this.lblTim.Name = "lblTim";
            this.lblTim.Size = new System.Drawing.Size(91, 16);
            this.lblTim.TabIndex = 8;
            this.lblTim.Text = "Tìm (Mã/Tên):";
            // 
            // txtTim
            // 
            this.txtTim.Location = new System.Drawing.Point(794, 313);
            this.txtTim.Name = "txtTim";
            this.txtTim.Size = new System.Drawing.Size(194, 22);
            this.txtTim.TabIndex = 9;
            this.txtTim.KeyDown += new System.Windows.Forms.KeyEventHandler(this.txtTim_KeyDown);
            // 
            // cboLocPB
            // 
            this.cboLocPB.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.cboLocPB.Location = new System.Drawing.Point(1000, 313);
            this.cboLocPB.Name = "cboLocPB";
            this.cboLocPB.Size = new System.Drawing.Size(159, 24);
            this.cboLocPB.TabIndex = 10;
            // 
            // btnTim
            // 
            this.btnTim.Location = new System.Drawing.Point(1168, 310);
            this.btnTim.Name = "btnTim";
            this.btnTim.Size = new System.Drawing.Size(69, 30);
            this.btnTim.TabIndex = 11;
            this.btnTim.Text = "Tìm";
            this.btnTim.UseVisualStyleBackColor = true;
            this.btnTim.Click += new System.EventHandler(this.btnTim_Click);
            // 
            // dgvNhanVien
            // 
            this.dgvNhanVien.AllowUserToAddRows = false;
            this.dgvNhanVien.AllowUserToDeleteRows = false;
            this.dgvNhanVien.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.dgvNhanVien.AutoSizeColumnsMode = System.Windows.Forms.DataGridViewAutoSizeColumnsMode.Fill;
            this.dgvNhanVien.ColumnHeadersHeight = 29;
            this.dgvNhanVien.Location = new System.Drawing.Point(12, 349);
            this.dgvNhanVien.MultiSelect = false;
            this.dgvNhanVien.Name = "dgvNhanVien";
            this.dgvNhanVien.ReadOnly = true;
            this.dgvNhanVien.RowHeadersWidth = 51;
            this.dgvNhanVien.SelectionMode = System.Windows.Forms.DataGridViewSelectionMode.FullRowSelect;
            this.dgvNhanVien.Size = new System.Drawing.Size(1223, 320);
            this.dgvNhanVien.TabIndex = 12;
            this.dgvNhanVien.CellClick += new System.Windows.Forms.DataGridViewCellEventHandler(this.dgvNhanVien_CellClick);
            // 
            // lblTong
            // 
            this.lblTong.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)));
            this.lblTong.AutoSize = true;
            this.lblTong.Location = new System.Drawing.Point(14, 685);
            this.lblTong.Name = "lblTong";
            this.lblTong.Size = new System.Drawing.Size(112, 16);
            this.lblTong.TabIndex = 13;
            this.lblTong.Text = "Tổng: 0 nhân viên";
            // 
            // FrmNhanVien
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1250, 717);
            this.Controls.Add(this.lblTieuDe);
            this.Controls.Add(this.grpNhanVien);
            this.Controls.Add(this.grpThuViec);
            this.Controls.Add(this.btnThem);
            this.Controls.Add(this.btnSua);
            this.Controls.Add(this.btnXoa);
            this.Controls.Add(this.btnLamMoi);
            this.Controls.Add(this.btnThoat);
            this.Controls.Add(this.lblTim);
            this.Controls.Add(this.txtTim);
            this.Controls.Add(this.cboLocPB);
            this.Controls.Add(this.btnTim);
            this.Controls.Add(this.dgvNhanVien);
            this.Controls.Add(this.lblTong);
            this.MinimumSize = new System.Drawing.Size(1266, 754);
            this.Name = "FrmNhanVien";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "Quản lý nhân sự - Công ty sơn Đông Á";
            this.Load += new System.EventHandler(this.FrmNhanVien_Load);
            this.grpNhanVien.ResumeLayout(false);
            this.grpNhanVien.PerformLayout();
            this.grpThuViec.ResumeLayout(false);
            this.grpThuViec.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.numThang)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.numLuong)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.dgvNhanVien)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label lblTieuDe;
        private System.Windows.Forms.GroupBox grpNhanVien;
        private System.Windows.Forms.GroupBox grpThuViec;
        private System.Windows.Forms.Label lblMaNV;
        private System.Windows.Forms.TextBox txtMaNV;
        private System.Windows.Forms.Label lblHoTen;
        private System.Windows.Forms.TextBox txtHoTen;
        private System.Windows.Forms.Label lblNgaySinh;
        private System.Windows.Forms.DateTimePicker dtpNgaySinh;
        private System.Windows.Forms.Label lblGioiTinh;
        private System.Windows.Forms.ComboBox cboGioiTinh;
        private System.Windows.Forms.Label lblSDT;
        private System.Windows.Forms.TextBox txtSDT;
        private System.Windows.Forms.Label lblEmail;
        private System.Windows.Forms.TextBox txtEmail;
        private System.Windows.Forms.Label lblPhongBan;
        private System.Windows.Forms.ComboBox cboPhongBan;
        private System.Windows.Forms.Label lblTrangThai;
        private System.Windows.Forms.ComboBox cboTrangThai;
        private System.Windows.Forms.Label lblDiaChi;
        private System.Windows.Forms.TextBox txtDiaChi;
        private System.Windows.Forms.CheckBox chkThuViec;
        private System.Windows.Forms.Label lblSoQD;
        private System.Windows.Forms.TextBox txtSoQD;
        private System.Windows.Forms.Label lblNgayKy;
        private System.Windows.Forms.DateTimePicker dtpNgayKy;
        private System.Windows.Forms.Label lblThang;
        private System.Windows.Forms.NumericUpDown numThang;
        private System.Windows.Forms.Label lblLuong;
        private System.Windows.Forms.NumericUpDown numLuong;
        private System.Windows.Forms.Label lblDieuKhoan;
        private System.Windows.Forms.TextBox txtDieuKhoan;
        private System.Windows.Forms.Button btnThem;
        private System.Windows.Forms.Button btnSua;
        private System.Windows.Forms.Button btnXoa;
        private System.Windows.Forms.Button btnLamMoi;
        private System.Windows.Forms.Button btnThoat;
        private System.Windows.Forms.Label lblTim;
        private System.Windows.Forms.TextBox txtTim;
        private System.Windows.Forms.ComboBox cboLocPB;
        private System.Windows.Forms.Button btnTim;
        private System.Windows.Forms.DataGridView dgvNhanVien;
        private System.Windows.Forms.Label lblTong;
    }
}
