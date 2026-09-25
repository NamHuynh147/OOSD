using System.Drawing;
using System.Windows.Forms;

namespace Form_QLKS
{
    partial class FrmPhongTienNghi
    {
        private System.ComponentModel.IContainer components = null;

        private Label lblNav;
        private Label lblPhongTab;
        private Label lblTienNghiTab;
        private Label lblLapDatTab;

        private Label lblSoPhong;
        private TextBox txtSoPhong;

        private Label lblKhuVuc;
        private TextBox txtKhuVuc;

        private Label lblSoNguoiToiDa;
        private TextBox txtSoNguoiToiDa;

        private Label lblDonGiaNgay;
        private TextBox txtDonGiaNgay;

        private DataGridView dgvPhong;

        private DataGridViewTextBoxColumn colPhong;
        private DataGridViewTextBoxColumn colKhu;
        private DataGridViewTextBoxColumn colSucChua;
        private DataGridViewTextBoxColumn colDonGia;
        private DataGridViewTextBoxColumn colTrangThai;

        private Label lblPhieuLapDat;
        private TextBox txtPhieuLapDat;

        private Label lblTienNghi;
        private TextBox txtTienNghi;

        private Label lblPhongBottom;
        private TextBox txtPhongBottom;

        private Label lblTinhTrang;
        private TextBox txtTinhTrang;

        private Button btnLapPhieu;

        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }

            base.Dispose(disposing);
        }

        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();

            this.lblNav = new Label();
            this.lblPhongTab = new Label();
            this.lblTienNghiTab = new Label();
            this.lblLapDatTab = new Label();

            this.lblSoPhong = new Label();
            this.txtSoPhong = new TextBox();

            this.lblKhuVuc = new Label();
            this.txtKhuVuc = new TextBox();

            this.lblSoNguoiToiDa = new Label();
            this.txtSoNguoiToiDa = new TextBox();

            this.lblDonGiaNgay = new Label();
            this.txtDonGiaNgay = new TextBox();

            this.dgvPhong = new DataGridView();

            this.colPhong = new DataGridViewTextBoxColumn();
            this.colKhu = new DataGridViewTextBoxColumn();
            this.colSucChua = new DataGridViewTextBoxColumn();
            this.colDonGia = new DataGridViewTextBoxColumn();
            this.colTrangThai = new DataGridViewTextBoxColumn();

            this.lblPhieuLapDat = new Label();
            this.txtPhieuLapDat = new TextBox();

            this.lblTienNghi = new Label();
            this.txtTienNghi = new TextBox();

            this.lblPhongBottom = new Label();
            this.txtPhongBottom = new TextBox();

            this.lblTinhTrang = new Label();
            this.txtTinhTrang = new TextBox();

            this.btnLapPhieu = new Button();

            ((System.ComponentModel.ISupportInitialize)(this.dgvPhong)).BeginInit();

            this.SuspendLayout();

            // ==========================================
            // lblNav
            // ==========================================
            this.lblNav.AutoSize = true;
            this.lblNav.Font = new Font(
                "Microsoft Sans Serif",
                12F,
                FontStyle.Bold,
                GraphicsUnit.Point);

            this.lblNav.Location = new Point(18, 15);
            this.lblNav.Name = "lblNav";
            this.lblNav.Size = new Size(250, 20);
            this.lblNav.Text = "Phòng - Tiện nghi - Phiếu lắp đặt";

            // ==========================================
            // lblPhongTab
            // ==========================================
            this.lblPhongTab.AutoSize = true;
            this.lblPhongTab.Font = new Font(
                "Microsoft Sans Serif",
                9F,
                FontStyle.Bold,
                GraphicsUnit.Point);

            this.lblPhongTab.Location = new Point(20, 52);
            this.lblPhongTab.Name = "lblPhongTab";
            this.lblPhongTab.Size = new Size(52, 15);
            this.lblPhongTab.Text = "[Phòng]";

            // ==========================================
            // lblTienNghiTab
            // ==========================================
            this.lblTienNghiTab.AutoSize = true;
            this.lblTienNghiTab.Location = new Point(78, 52);
            this.lblTienNghiTab.Name = "lblTienNghiTab";
            this.lblTienNghiTab.Size = new Size(70, 15);
            this.lblTienNghiTab.Text = "[Tiện nghi]";

            // ==========================================
            // lblLapDatTab
            // ==========================================
            this.lblLapDatTab.AutoSize = true;
            this.lblLapDatTab.Location = new Point(152, 52);
            this.lblLapDatTab.Name = "lblLapDatTab";
            this.lblLapDatTab.Size = new Size(148, 15);
            this.lblLapDatTab.Text = "[Lắp đặt / luân chuyển]";

            // ==========================================
            // lblSoPhong
            // ==========================================
            this.lblSoPhong.AutoSize = true;
            this.lblSoPhong.Location = new Point(20, 88);
            this.lblSoPhong.Name = "lblSoPhong";
            this.lblSoPhong.Size = new Size(58, 15);
            this.lblSoPhong.Text = "Số phòng:";

            // ==========================================
            // txtSoPhong
            // ==========================================
            this.txtSoPhong.Location = new Point(91, 85);
            this.txtSoPhong.Name = "txtSoPhong";
            this.txtSoPhong.Size = new Size(105, 23);
            this.txtSoPhong.TabIndex = 0;
            this.txtSoPhong.Text = "A101";

            // ==========================================
            // lblKhuVuc
            // ==========================================
            this.lblKhuVuc.AutoSize = true;
            this.lblKhuVuc.Location = new Point(213, 88);
            this.lblKhuVuc.Name = "lblKhuVuc";
            this.lblKhuVuc.Size = new Size(55, 15);
            this.lblKhuVuc.Text = "Khu vực:";

            // ==========================================
            // txtKhuVuc
            // ==========================================
            this.txtKhuVuc.Location = new Point(276, 85);
            this.txtKhuVuc.Name = "txtKhuVuc";
            this.txtKhuVuc.Size = new Size(110, 23);
            this.txtKhuVuc.TabIndex = 1;
            this.txtKhuVuc.Text = "Khu A";

            // ==========================================
            // lblSoNguoiToiDa
            // ==========================================
            this.lblSoNguoiToiDa.AutoSize = true;
            this.lblSoNguoiToiDa.Location = new Point(402, 88);
            this.lblSoNguoiToiDa.Name = "lblSoNguoiToiDa";
            this.lblSoNguoiToiDa.Size = new Size(86, 15);
            this.lblSoNguoiToiDa.Text = "Số người tối đa:";

            // ==========================================
            // txtSoNguoiToiDa
            // ==========================================
            this.txtSoNguoiToiDa.Location = new Point(495, 85);
            this.txtSoNguoiToiDa.Name = "txtSoNguoiToiDa";
            this.txtSoNguoiToiDa.Size = new Size(65, 23);
            this.txtSoNguoiToiDa.TabIndex = 2;
            this.txtSoNguoiToiDa.Text = "2";

            // ==========================================
            // lblDonGiaNgay
            // ==========================================
            this.lblDonGiaNgay.AutoSize = true;
            this.lblDonGiaNgay.Location = new Point(580, 88);
            this.lblDonGiaNgay.Name = "lblDonGiaNgay";
            this.lblDonGiaNgay.Size = new Size(84, 15);
            this.lblDonGiaNgay.Text = "Đơn giá/ngày:";

            // ==========================================
            // txtDonGiaNgay
            // ==========================================
            this.txtDonGiaNgay.Location = new Point(670, 85);
            this.txtDonGiaNgay.Name = "txtDonGiaNgay";
            this.txtDonGiaNgay.Size = new Size(90, 23);
            this.txtDonGiaNgay.TabIndex = 3;
            this.txtDonGiaNgay.Text = "600000";

            // ==========================================
            // dgvPhong
            // ==========================================
            this.dgvPhong.AllowUserToAddRows = false;
            this.dgvPhong.AllowUserToDeleteRows = false;
            this.dgvPhong.AllowUserToResizeRows = false;

            this.dgvPhong.AutoGenerateColumns = false;
            this.dgvPhong.AutoSizeColumnsMode =
                DataGridViewAutoSizeColumnsMode.Fill;

            this.dgvPhong.BackgroundColor = Color.White;
            this.dgvPhong.BorderStyle = BorderStyle.Fixed3D;
            this.dgvPhong.ColumnHeadersHeightSizeMode =
                DataGridViewColumnHeadersHeightSizeMode.AutoSize;

            this.dgvPhong.Columns.AddRange(
                new DataGridViewColumn[]
                {
                    this.colPhong,
                    this.colKhu,
                    this.colSucChua,
                    this.colDonGia,
                    this.colTrangThai
                });

            this.dgvPhong.Location = new Point(20, 130);
            this.dgvPhong.MultiSelect = false;
            this.dgvPhong.Name = "dgvPhong";
            this.dgvPhong.ReadOnly = true;
            this.dgvPhong.RowHeadersVisible = false;
            this.dgvPhong.SelectionMode =
                DataGridViewSelectionMode.FullRowSelect;

            this.dgvPhong.Size = new Size(740, 195);
            this.dgvPhong.TabIndex = 4;

            this.dgvPhong.CellClick +=
                new DataGridViewCellEventHandler(
                    this.dgvPhong_CellClick);

            // ==========================================
            // colPhong
            // ==========================================
            this.colPhong.DataPropertyName = "Phòng";
            this.colPhong.HeaderText = "Phòng";
            this.colPhong.Name = "colPhong";
            this.colPhong.ReadOnly = true;

            // ==========================================
            // colKhu
            // ==========================================
            this.colKhu.DataPropertyName = "Khu";
            this.colKhu.HeaderText = "Khu";
            this.colKhu.Name = "colKhu";
            this.colKhu.ReadOnly = true;

            // ==========================================
            // colSucChua
            // ==========================================
            this.colSucChua.DataPropertyName = "Sức chứa";
            this.colSucChua.HeaderText = "Sức chứa";
            this.colSucChua.Name = "colSucChua";
            this.colSucChua.ReadOnly = true;

            // ==========================================
            // colDonGia
            // ==========================================
            this.colDonGia.DataPropertyName = "Đơn giá";
            this.colDonGia.HeaderText = "Đơn giá";
            this.colDonGia.Name = "colDonGia";
            this.colDonGia.ReadOnly = true;

            // ==========================================
            // colTrangThai
            // ==========================================
            this.colTrangThai.DataPropertyName = "Trạng thái";
            this.colTrangThai.HeaderText = "Trạng thái";
            this.colTrangThai.Name = "colTrangThai";
            this.colTrangThai.ReadOnly = true;

            // ==========================================
            // lblPhieuLapDat
            // ==========================================
            this.lblPhieuLapDat.AutoSize = true;
            this.lblPhieuLapDat.Location = new Point(20, 347);
            this.lblPhieuLapDat.Name = "lblPhieuLapDat";
            this.lblPhieuLapDat.Size = new Size(76, 15);
            this.lblPhieuLapDat.Text = "Phiếu lắp đặt:";

            // ==========================================
            // txtPhieuLapDat
            // ==========================================
            this.txtPhieuLapDat.Location = new Point(105, 344);
            this.txtPhieuLapDat.Name = "txtPhieuLapDat";
            this.txtPhieuLapDat.Size = new Size(95, 23);
            this.txtPhieuLapDat.TabIndex = 5;
            this.txtPhieuLapDat.Text = "LD001";

            // ==========================================
            // lblTienNghi
            // ==========================================
            this.lblTienNghi.AutoSize = true;
            this.lblTienNghi.Location = new Point(215, 347);
            this.lblTienNghi.Name = "lblTienNghi";
            this.lblTienNghi.Size = new Size(57, 15);
            this.lblTienNghi.Text = "Tiện nghi:";

            // ==========================================
            // txtTienNghi
            // ==========================================
            this.txtTienNghi.Location = new Point(280, 344);
            this.txtTienNghi.Name = "txtTienNghi";
            this.txtTienNghi.Size = new Size(85, 23);
            this.txtTienNghi.TabIndex = 6;
            this.txtTienNghi.Text = "TV01";

            // ==========================================
            // lblPhongBottom
            // ==========================================
            this.lblPhongBottom.AutoSize = true;
            this.lblPhongBottom.Location = new Point(385, 347);
            this.lblPhongBottom.Name = "lblPhongBottom";
            this.lblPhongBottom.Size = new Size(46, 15);
            this.lblPhongBottom.Text = "Phòng:";

            // ==========================================
            // txtPhongBottom
            // ==========================================
            this.txtPhongBottom.Location = new Point(440, 344);
            this.txtPhongBottom.Name = "txtPhongBottom";
            this.txtPhongBottom.Size = new Size(80, 23);
            this.txtPhongBottom.TabIndex = 7;
            this.txtPhongBottom.Text = "A101";

            // ==========================================
            // lblTinhTrang
            // ==========================================
            this.lblTinhTrang.AutoSize = true;
            this.lblTinhTrang.Location = new Point(535, 347);
            this.lblTinhTrang.Name = "lblTinhTrang";
            this.lblTinhTrang.Size = new Size(62, 15);
            this.lblTinhTrang.Text = "Tình trạng:";

            // ==========================================
            // txtTinhTrang
            // ==========================================
            this.txtTinhTrang.Location = new Point(605, 344);
            this.txtTinhTrang.Name = "txtTinhTrang";
            this.txtTinhTrang.Size = new Size(105, 23);
            this.txtTinhTrang.TabIndex = 8;
            this.txtTinhTrang.Text = "Tốt";

            // ==========================================
            // btnLapPhieu
            // ==========================================
            this.btnLapPhieu.Location = new Point(650, 380);
            this.btnLapPhieu.Name = "btnLapPhieu";
            this.btnLapPhieu.Size = new Size(110, 32);
            this.btnLapPhieu.TabIndex = 9;
            this.btnLapPhieu.Text = "Lập phiếu";
            this.btnLapPhieu.UseVisualStyleBackColor = true;

            this.btnLapPhieu.Click +=
                new System.EventHandler(
                    this.btnLapPhieu_Click);

            // ==========================================
            // FrmPhongTienNghi
            // ==========================================
            this.AutoScaleDimensions =
                new SizeF(7F, 15F);

            this.AutoScaleMode =
                AutoScaleMode.Font;

            this.ClientSize = new Size(790, 430);

            this.Controls.Add(this.btnLapPhieu);

            this.Controls.Add(this.txtTinhTrang);
            this.Controls.Add(this.lblTinhTrang);

            this.Controls.Add(this.txtPhongBottom);
            this.Controls.Add(this.lblPhongBottom);

            this.Controls.Add(this.txtTienNghi);
            this.Controls.Add(this.lblTienNghi);

            this.Controls.Add(this.txtPhieuLapDat);
            this.Controls.Add(this.lblPhieuLapDat);

            this.Controls.Add(this.dgvPhong);

            this.Controls.Add(this.txtDonGiaNgay);
            this.Controls.Add(this.lblDonGiaNgay);

            this.Controls.Add(this.txtSoNguoiToiDa);
            this.Controls.Add(this.lblSoNguoiToiDa);

            this.Controls.Add(this.txtKhuVuc);
            this.Controls.Add(this.lblKhuVuc);

            this.Controls.Add(this.txtSoPhong);
            this.Controls.Add(this.lblSoPhong);

            this.Controls.Add(this.lblLapDatTab);
            this.Controls.Add(this.lblTienNghiTab);
            this.Controls.Add(this.lblPhongTab);

            this.Controls.Add(this.lblNav);

            this.FormBorderStyle =
                FormBorderStyle.FixedSingle;

            this.MaximizeBox = false;
            this.Name = "FrmPhongTienNghi";
            this.StartPosition =
                FormStartPosition.CenterScreen;

            this.Text = "Phòng - Tiện nghi - Phiếu lắp đặt";

            this.Load +=
                new System.EventHandler(
                    this.FrmPhongTienNghi_Load);

            ((System.ComponentModel.ISupportInitialize)(this.dgvPhong)).EndInit();

            this.ResumeLayout(false);
            this.PerformLayout();
        }
    }
}