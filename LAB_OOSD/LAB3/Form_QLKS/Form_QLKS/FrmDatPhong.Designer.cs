using System.Drawing;
using System.Windows.Forms;

namespace Form_QLKS
{
    partial class FrmDatPhong
    {
        private System.ComponentModel.IContainer components = null;

        private Label lblNav;

        private Label lblKhachTab;
        private Label lblDatPhongTab;
        private Label lblNhanPhongTab;

        private Label lblSoPhieuDat;
        private TextBox txtSoPhieuDat;

        private Label lblKhach;
        private TextBox txtKhach;

        private Label lblKenhDat;
        private TextBox txtKenhDat;

        private Label lblTienCoc;
        private TextBox txtTienCoc;

        private DataGridView dgvPhong;

        private DataGridViewTextBoxColumn colPhong;
        private DataGridViewTextBoxColumn colKhu;
        private DataGridViewTextBoxColumn colSucChua;
        private DataGridViewTextBoxColumn colDonGia;

        private DataGridView dgvPhongChon;

        private DataGridViewTextBoxColumn colPhongChon;
        private DataGridViewTextBoxColumn colSoNguoi;
        private DataGridViewTextBoxColumn colDonGiaNgay;

        private Button btnLapPhieuDat;

        private Label lblPhieuDat;

        private DataGridView dgvPhieuDat;

        private DataGridViewTextBoxColumn colSoPhieu;
        private DataGridViewTextBoxColumn colKhach;
        private DataGridViewTextBoxColumn colNgayNhan;
        private DataGridViewTextBoxColumn colNgayTraDuKien;
        private DataGridViewTextBoxColumn colCoc;
        private DataGridViewTextBoxColumn colKenh;
        private DataGridViewTextBoxColumn colTrangThai;

        protected override void Dispose(bool disposing)
        {
            if (disposing && components != null)
            {
                components.Dispose();
            }

            base.Dispose(disposing);
        }

        private void InitializeComponent()
        {
            this.lblNav = new Label();

            this.lblKhachTab = new Label();
            this.lblDatPhongTab = new Label();
            this.lblNhanPhongTab = new Label();

            this.lblSoPhieuDat = new Label();
            this.txtSoPhieuDat = new TextBox();

            this.lblKhach = new Label();
            this.txtKhach = new TextBox();

            this.lblKenhDat = new Label();
            this.txtKenhDat = new TextBox();

            this.lblTienCoc = new Label();
            this.txtTienCoc = new TextBox();

            this.dgvPhong = new DataGridView();

            this.colPhong = new DataGridViewTextBoxColumn();
            this.colKhu = new DataGridViewTextBoxColumn();
            this.colSucChua = new DataGridViewTextBoxColumn();
            this.colDonGia = new DataGridViewTextBoxColumn();

            this.dgvPhongChon = new DataGridView();

            this.colPhongChon = new DataGridViewTextBoxColumn();
            this.colSoNguoi = new DataGridViewTextBoxColumn();
            this.colDonGiaNgay = new DataGridViewTextBoxColumn();

            this.btnLapPhieuDat = new Button();

            this.lblPhieuDat = new Label();

            this.dgvPhieuDat = new DataGridView();

            this.colSoPhieu = new DataGridViewTextBoxColumn();
            this.colKhach = new DataGridViewTextBoxColumn();
            this.colNgayNhan = new DataGridViewTextBoxColumn();
            this.colNgayTraDuKien = new DataGridViewTextBoxColumn();
            this.colCoc = new DataGridViewTextBoxColumn();
            this.colKenh = new DataGridViewTextBoxColumn();
            this.colTrangThai = new DataGridViewTextBoxColumn();

            ((System.ComponentModel.ISupportInitialize)(this.dgvPhong)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.dgvPhongChon)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.dgvPhieuDat)).BeginInit();

            this.SuspendLayout();

            // =====================================================
            // lblNav
            // =====================================================

            this.lblNav.AutoSize = true;
            this.lblNav.Font = new Font(
                "Microsoft Sans Serif",
                12F,
                FontStyle.Bold);

            this.lblNav.Location = new Point(21, 20);
            this.lblNav.Name = "lblNav";
            this.lblNav.Size = new Size(247, 25);
            this.lblNav.TabIndex = 0;
            this.lblNav.Text = "Khách hàng - Đặt phòng";

            // =====================================================
            // lblKhachTab
            // =====================================================

            this.lblKhachTab.AutoSize = true;
            this.lblKhachTab.Font = new Font(
                "Microsoft Sans Serif",
                9F,
                FontStyle.Bold);

            this.lblKhachTab.Location = new Point(23, 69);
            this.lblKhachTab.Name = "lblKhachTab";
            this.lblKhachTab.Size = new Size(106, 18);
            this.lblKhachTab.TabIndex = 1;
            this.lblKhachTab.Text = "[Khách hàng]";

            // =====================================================
            // lblDatPhongTab
            // =====================================================

            this.lblDatPhongTab.AutoSize = true;
            this.lblDatPhongTab.Location = new Point(123, 69);
            this.lblDatPhongTab.Name = "lblDatPhongTab";
            this.lblDatPhongTab.Size = new Size(90, 20);
            this.lblDatPhongTab.TabIndex = 2;
            this.lblDatPhongTab.Text = "[Đặt phòng]";

            // =====================================================
            // lblNhanPhongTab
            // =====================================================

            this.lblNhanPhongTab.AutoSize = true;
            this.lblNhanPhongTab.Location = new Point(211, 69);
            this.lblNhanPhongTab.Name = "lblNhanPhongTab";
            this.lblNhanPhongTab.Size = new Size(204, 20);
            this.lblNhanPhongTab.TabIndex = 3;
            this.lblNhanPhongTab.Text =
                "[Nhận phòng / Người lưu trú]";

            // =====================================================
            // lblSoPhieuDat
            // =====================================================

            this.lblSoPhieuDat.AutoSize = true;
            this.lblSoPhieuDat.Location = new Point(23, 116);
            this.lblSoPhieuDat.Name = "lblSoPhieuDat";
            this.lblSoPhieuDat.Size = new Size(96, 20);
            this.lblSoPhieuDat.TabIndex = 4;
            this.lblSoPhieuDat.Text = "Số phiếu đặt:";

            // =====================================================
            // txtSoPhieuDat
            // =====================================================

            this.txtSoPhieuDat.Location = new Point(120, 112);
            this.txtSoPhieuDat.Name = "txtSoPhieuDat";
            this.txtSoPhieuDat.Size = new Size(119, 27);
            this.txtSoPhieuDat.TabIndex = 0;
            this.txtSoPhieuDat.Text = "DP001";
            this.txtSoPhieuDat.TextChanged +=
                new System.EventHandler(this.txtSoPhieuDat_TextChanged);

            // =====================================================
            // lblKhach
            // =====================================================

            this.lblKhach.AutoSize = true;
            this.lblKhach.Location = new Point(257, 116);
            this.lblKhach.Name = "lblKhach";
            this.lblKhach.Size = new Size(52, 20);
            this.lblKhach.TabIndex = 5;
            this.lblKhach.Text = "Khách:";

            // =====================================================
            // txtKhach
            // =====================================================

            this.txtKhach.Location = new Point(314, 112);
            this.txtKhach.Name = "txtKhach";
            this.txtKhach.Size = new Size(171, 27);
            this.txtKhach.TabIndex = 1;
            this.txtKhach.Text = "Nguyễn Văn A";

            // =====================================================
            // lblKenhDat
            // =====================================================

            this.lblKenhDat.AutoSize = true;
            this.lblKenhDat.Location = new Point(509, 116);
            this.lblKenhDat.Name = "lblKenhDat";
            this.lblKenhDat.Size = new Size(71, 20);
            this.lblKenhDat.TabIndex = 6;
            this.lblKenhDat.Text = "Kênh đặt:";

            // =====================================================
            // txtKenhDat
            // =====================================================

            this.txtKenhDat.Location = new Point(577, 112);
            this.txtKenhDat.Name = "txtKenhDat";
            this.txtKenhDat.Size = new Size(114, 27);
            this.txtKenhDat.TabIndex = 2;
            this.txtKenhDat.Text = "Website";

            // =====================================================
            // lblTienCoc
            // =====================================================

            this.lblTienCoc.AutoSize = true;
            this.lblTienCoc.Location = new Point(709, 116);
            this.lblTienCoc.Name = "lblTienCoc";
            this.lblTienCoc.Size = new Size(67, 20);
            this.lblTienCoc.TabIndex = 7;
            this.lblTienCoc.Text = "Tiền cọc:";

            // =====================================================
            // txtTienCoc
            // =====================================================

            this.txtTienCoc.Location = new Point(771, 112);
            this.txtTienCoc.Name = "txtTienCoc";
            this.txtTienCoc.Size = new Size(114, 27);
            this.txtTienCoc.TabIndex = 3;
            this.txtTienCoc.Text = "500000";

            // =====================================================
            // dgvPhong
            // =====================================================

            this.dgvPhong.AllowUserToAddRows = false;
            this.dgvPhong.AllowUserToDeleteRows = false;
            this.dgvPhong.AllowUserToResizeRows = false;
            this.dgvPhong.AutoSizeColumnsMode =
                DataGridViewAutoSizeColumnsMode.Fill;

            this.dgvPhong.BackgroundColor = Color.White;

            this.dgvPhong.ColumnHeadersHeightSizeMode =
                DataGridViewColumnHeadersHeightSizeMode.AutoSize;

            this.dgvPhong.Columns.AddRange(
                new DataGridViewColumn[]
                {
                    this.colPhong,
                    this.colKhu,
                    this.colSucChua,
                    this.colDonGia
                });

            this.dgvPhong.Location = new Point(23, 160);
            this.dgvPhong.MultiSelect = false;
            this.dgvPhong.Name = "dgvPhong";
            this.dgvPhong.ReadOnly = true;
            this.dgvPhong.RowHeadersVisible = false;
            this.dgvPhong.SelectionMode =
                DataGridViewSelectionMode.FullRowSelect;

            this.dgvPhong.Size = new Size(383, 193);
            this.dgvPhong.TabIndex = 4;

            this.dgvPhong.CellClick +=
                new DataGridViewCellEventHandler(
                    this.dgvPhong_CellClick);

            // =====================================================
            // colPhong
            // =====================================================

            this.colPhong.HeaderText = "Phòng";
            this.colPhong.Name = "colPhong";
            this.colPhong.ReadOnly = true;

            // =====================================================
            // colKhu
            // =====================================================

            this.colKhu.HeaderText = "Khu";
            this.colKhu.Name = "colKhu";
            this.colKhu.ReadOnly = true;

            // =====================================================
            // colSucChua
            // =====================================================

            this.colSucChua.HeaderText = "Sức chứa";
            this.colSucChua.Name = "colSucChua";
            this.colSucChua.ReadOnly = true;

            // =====================================================
            // colDonGia
            // =====================================================

            this.colDonGia.HeaderText = "Đơn giá/ngày";
            this.colDonGia.Name = "colDonGia";
            this.colDonGia.ReadOnly = true;

            // =====================================================
            // dgvPhongChon
            // =====================================================

            this.dgvPhongChon.AllowUserToAddRows = false;
            this.dgvPhongChon.AllowUserToDeleteRows = false;
            this.dgvPhongChon.AllowUserToResizeRows = false;
            this.dgvPhongChon.AutoSizeColumnsMode =
                DataGridViewAutoSizeColumnsMode.Fill;

            this.dgvPhongChon.BackgroundColor = Color.White;

            this.dgvPhongChon.ColumnHeadersHeightSizeMode =
                DataGridViewColumnHeadersHeightSizeMode.AutoSize;

            this.dgvPhongChon.Columns.AddRange(
                new DataGridViewColumn[]
                {
                    this.colPhongChon,
                    this.colSoNguoi,
                    this.colDonGiaNgay
                });

            this.dgvPhongChon.Location = new Point(423, 160);
            this.dgvPhongChon.MultiSelect = false;
            this.dgvPhongChon.Name = "dgvPhongChon";
            this.dgvPhongChon.ReadOnly = true;
            this.dgvPhongChon.RowHeadersVisible = false;
            this.dgvPhongChon.SelectionMode =
                DataGridViewSelectionMode.FullRowSelect;

            this.dgvPhongChon.Size = new Size(383, 193);
            this.dgvPhongChon.TabIndex = 5;

            // =====================================================
            // colPhongChon
            // =====================================================

            this.colPhongChon.HeaderText = "Phòng chọn";
            this.colPhongChon.Name = "colPhongChon";
            this.colPhongChon.ReadOnly = true;

            // =====================================================
            // colSoNguoi
            // =====================================================

            this.colSoNguoi.HeaderText = "Số người";
            this.colSoNguoi.Name = "colSoNguoi";
            this.colSoNguoi.ReadOnly = true;

            // =====================================================
            // colDonGiaNgay
            // =====================================================

            this.colDonGiaNgay.HeaderText = "Đơn giá/ngày";
            this.colDonGiaNgay.Name = "colDonGiaNgay";
            this.colDonGiaNgay.ReadOnly = true;

            // =====================================================
            // btnLapPhieuDat
            // =====================================================

            this.btnLapPhieuDat.Location = new Point(680, 371);
            this.btnLapPhieuDat.Name = "btnLapPhieuDat";
            this.btnLapPhieuDat.Size = new Size(126, 43);
            this.btnLapPhieuDat.TabIndex = 6;
            this.btnLapPhieuDat.Text = "Lập phiếu đặt";
            this.btnLapPhieuDat.UseVisualStyleBackColor = true;

            this.btnLapPhieuDat.Click +=
                new System.EventHandler(
                    this.btnLapPhieuDat_Click);

            // =====================================================
            // lblPhieuDat
            // =====================================================

            this.lblPhieuDat.AutoSize = true;
            this.lblPhieuDat.Location = new Point(23, 433);
            this.lblPhieuDat.Name = "lblPhieuDat";
            this.lblPhieuDat.Size = new Size(121, 20);
            this.lblPhieuDat.TabIndex = 8;
            this.lblPhieuDat.Text = "Phiếu đặt phòng:";

            // =====================================================
            // dgvPhieuDat
            // =====================================================

            this.dgvPhieuDat.AllowUserToAddRows = false;
            this.dgvPhieuDat.AllowUserToDeleteRows = false;
            this.dgvPhieuDat.AllowUserToResizeRows = false;
            this.dgvPhieuDat.AutoSizeColumnsMode =
                DataGridViewAutoSizeColumnsMode.Fill;

            this.dgvPhieuDat.BackgroundColor = Color.White;

            this.dgvPhieuDat.ColumnHeadersHeightSizeMode =
                DataGridViewColumnHeadersHeightSizeMode.AutoSize;

            this.dgvPhieuDat.Columns.AddRange(
                new DataGridViewColumn[]
                {
                    this.colSoPhieu,
                    this.colKhach,
                    this.colNgayNhan,
                    this.colNgayTraDuKien,
                    this.colCoc,
                    this.colKenh,
                    this.colTrangThai
                });

            this.dgvPhieuDat.Location = new Point(23, 467);
            this.dgvPhieuDat.MultiSelect = false;
            this.dgvPhieuDat.Name = "dgvPhieuDat";
            this.dgvPhieuDat.ReadOnly = true;
            this.dgvPhieuDat.RowHeadersVisible = false;
            this.dgvPhieuDat.SelectionMode =
                DataGridViewSelectionMode.FullRowSelect;

            this.dgvPhieuDat.Size = new Size(783, 167);
            this.dgvPhieuDat.TabIndex = 7;

            this.dgvPhieuDat.CellClick +=
                new DataGridViewCellEventHandler(
                    this.dgvPhieuDat_CellClick);

            this.dgvPhieuDat.CellContentClick +=
                new DataGridViewCellEventHandler(
                    this.dgvPhieuDat_CellContentClick);

            // =====================================================
            // Các cột dgvPhieuDat
            // =====================================================

            this.colSoPhieu.HeaderText = "Số phiếu";
            this.colSoPhieu.Name = "colSoPhieu";
            this.colSoPhieu.ReadOnly = true;

            this.colKhach.HeaderText = "Khách";
            this.colKhach.Name = "colKhach";
            this.colKhach.ReadOnly = true;

            this.colNgayNhan.HeaderText = "Ngày nhận";
            this.colNgayNhan.Name = "colNgayNhan";
            this.colNgayNhan.ReadOnly = true;

            this.colNgayTraDuKien.HeaderText = "Ngày trả dự kiến";
            this.colNgayTraDuKien.Name = "colNgayTraDuKien";
            this.colNgayTraDuKien.ReadOnly = true;

            this.colCoc.HeaderText = "Tiền cọc";
            this.colCoc.Name = "colCoc";
            this.colCoc.ReadOnly = true;

            this.colKenh.HeaderText = "Kênh đặt";
            this.colKenh.Name = "colKenh";
            this.colKenh.ReadOnly = true;

            this.colTrangThai.HeaderText = "Trạng thái";
            this.colTrangThai.Name = "colTrangThai";
            this.colTrangThai.ReadOnly = true;

            // =====================================================
            // FrmDatPhong
            // =====================================================

            this.AutoScaleDimensions = new SizeF(8F, 20F);
            this.AutoScaleMode = AutoScaleMode.Font;

            this.ClientSize = new Size(930, 667);

            this.Controls.Add(this.dgvPhieuDat);
            this.Controls.Add(this.lblPhieuDat);
            this.Controls.Add(this.btnLapPhieuDat);
            this.Controls.Add(this.dgvPhongChon);
            this.Controls.Add(this.dgvPhong);

            this.Controls.Add(this.txtTienCoc);
            this.Controls.Add(this.lblTienCoc);

            this.Controls.Add(this.txtKenhDat);
            this.Controls.Add(this.lblKenhDat);

            this.Controls.Add(this.txtKhach);
            this.Controls.Add(this.lblKhach);

            this.Controls.Add(this.txtSoPhieuDat);
            this.Controls.Add(this.lblSoPhieuDat);

            this.Controls.Add(this.lblNhanPhongTab);
            this.Controls.Add(this.lblDatPhongTab);
            this.Controls.Add(this.lblKhachTab);
            this.Controls.Add(this.lblNav);

            this.FormBorderStyle = FormBorderStyle.FixedSingle;
            this.MaximizeBox = false;
            this.Name = "FrmDatPhong";
            this.StartPosition =
                FormStartPosition.CenterScreen;

            this.Text =
                "Khách hàng - Đặt phòng - Nhận phòng";

            this.Load +=
                new System.EventHandler(
                    this.FrmDatPhong_Load);

            ((System.ComponentModel.ISupportInitialize)
                (this.dgvPhong)).EndInit();

            ((System.ComponentModel.ISupportInitialize)
                (this.dgvPhongChon)).EndInit();

            ((System.ComponentModel.ISupportInitialize)
                (this.dgvPhieuDat)).EndInit();

            this.ResumeLayout(false);
            this.PerformLayout();
        }
    }
}