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
            lblNav = new Label();
            lblKhachTab = new Label();
            lblDatPhongTab = new Label();
            lblNhanPhongTab = new Label();
            lblSoPhieuDat = new Label();
            txtSoPhieuDat = new TextBox();
            lblKhach = new Label();
            txtKhach = new TextBox();
            lblKenhDat = new Label();
            txtKenhDat = new TextBox();
            lblTienCoc = new Label();
            txtTienCoc = new TextBox();
            dgvPhong = new DataGridView();
            dgvPhongChon = new DataGridView();
            colPhongChon = new DataGridViewTextBoxColumn();
            colSoNguoi = new DataGridViewTextBoxColumn();
            colDonGiaNgay = new DataGridViewTextBoxColumn();
            btnLapPhieuDat = new Button();
            lblPhieuDat = new Label();
            dgvPhieuDat = new DataGridView();
            ((System.ComponentModel.ISupportInitialize)dgvPhong).BeginInit();
            ((System.ComponentModel.ISupportInitialize)dgvPhongChon).BeginInit();
            ((System.ComponentModel.ISupportInitialize)dgvPhieuDat).BeginInit();
            SuspendLayout();
            // 
            // lblNav
            // 
            lblNav.AutoSize = true;
            lblNav.Font = new Font("Microsoft Sans Serif", 12F, FontStyle.Bold);
            lblNav.Location = new Point(21, 20);
            lblNav.Name = "lblNav";
            lblNav.Size = new Size(247, 25);
            lblNav.TabIndex = 16;
            lblNav.Text = "Khách hàng - Đặt phòng";
            // 
            // lblKhachTab
            // 
            lblKhachTab.AutoSize = true;
            lblKhachTab.Font = new Font("Microsoft Sans Serif", 9F, FontStyle.Bold);
            lblKhachTab.Location = new Point(23, 69);
            lblKhachTab.Name = "lblKhachTab";
            lblKhachTab.Size = new Size(106, 18);
            lblKhachTab.TabIndex = 15;
            lblKhachTab.Text = "[Khách hàng]";
            // 
            // lblDatPhongTab
            // 
            lblDatPhongTab.AutoSize = true;
            lblDatPhongTab.Location = new Point(123, 69);
            lblDatPhongTab.Name = "lblDatPhongTab";
            lblDatPhongTab.Size = new Size(90, 20);
            lblDatPhongTab.TabIndex = 14;
            lblDatPhongTab.Text = "[Đặt phòng]";
            // 
            // lblNhanPhongTab
            // 
            lblNhanPhongTab.AutoSize = true;
            lblNhanPhongTab.Location = new Point(211, 69);
            lblNhanPhongTab.Name = "lblNhanPhongTab";
            lblNhanPhongTab.Size = new Size(204, 20);
            lblNhanPhongTab.TabIndex = 13;
            lblNhanPhongTab.Text = "[Nhận phòng / Người lưu trú]";
            // 
            // lblSoPhieuDat
            // 
            lblSoPhieuDat.AutoSize = true;
            lblSoPhieuDat.Location = new Point(23, 116);
            lblSoPhieuDat.Name = "lblSoPhieuDat";
            lblSoPhieuDat.Size = new Size(96, 20);
            lblSoPhieuDat.TabIndex = 12;
            lblSoPhieuDat.Text = "Số phiếu đặt:";
            // 
            // txtSoPhieuDat
            // 
            txtSoPhieuDat.Location = new Point(120, 112);
            txtSoPhieuDat.Margin = new Padding(3, 4, 3, 4);
            txtSoPhieuDat.Name = "txtSoPhieuDat";
            txtSoPhieuDat.Size = new Size(119, 27);
            txtSoPhieuDat.TabIndex = 0;
            txtSoPhieuDat.Text = "DP001";
            txtSoPhieuDat.TextChanged += txtSoPhieuDat_TextChanged;
            // 
            // lblKhach
            // 
            lblKhach.AutoSize = true;
            lblKhach.Location = new Point(257, 116);
            lblKhach.Name = "lblKhach";
            lblKhach.Size = new Size(52, 20);
            lblKhach.TabIndex = 11;
            lblKhach.Text = "Khách:";
            // 
            // txtKhach
            // 
            txtKhach.Location = new Point(314, 112);
            txtKhach.Margin = new Padding(3, 4, 3, 4);
            txtKhach.Name = "txtKhach";
            txtKhach.Size = new Size(171, 27);
            txtKhach.TabIndex = 1;
            txtKhach.Text = "Nguyễn Văn A";
            // 
            // lblKenhDat
            // 
            lblKenhDat.AutoSize = true;
            lblKenhDat.Location = new Point(509, 116);
            lblKenhDat.Name = "lblKenhDat";
            lblKenhDat.Size = new Size(71, 20);
            lblKenhDat.TabIndex = 10;
            lblKenhDat.Text = "Kênh đặt:";
            // 
            // txtKenhDat
            // 
            txtKenhDat.Location = new Point(577, 112);
            txtKenhDat.Margin = new Padding(3, 4, 3, 4);
            txtKenhDat.Name = "txtKenhDat";
            txtKenhDat.Size = new Size(114, 27);
            txtKenhDat.TabIndex = 2;
            txtKenhDat.Text = "Website";
            // 
            // lblTienCoc
            // 
            lblTienCoc.AutoSize = true;
            lblTienCoc.Location = new Point(709, 116);
            lblTienCoc.Name = "lblTienCoc";
            lblTienCoc.Size = new Size(67, 20);
            lblTienCoc.TabIndex = 9;
            lblTienCoc.Text = "Tiền cọc:";
            // 
            // txtTienCoc
            // 
            txtTienCoc.Location = new Point(771, 112);
            txtTienCoc.Margin = new Padding(3, 4, 3, 4);
            txtTienCoc.Name = "txtTienCoc";
            txtTienCoc.Size = new Size(114, 27);
            txtTienCoc.TabIndex = 3;
            txtTienCoc.Text = "500000";
            // 
            // dgvPhong
            // 
            dgvPhong.AllowUserToAddRows = false;
            dgvPhong.AllowUserToDeleteRows = false;
            dgvPhong.AllowUserToResizeRows = false;
            dgvPhong.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
            dgvPhong.BackgroundColor = Color.White;
            dgvPhong.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            dgvPhong.Location = new Point(23, 160);
            dgvPhong.Margin = new Padding(3, 4, 3, 4);
            dgvPhong.MultiSelect = false;
            dgvPhong.Name = "dgvPhong";
            dgvPhong.ReadOnly = true;
            dgvPhong.RowHeadersVisible = false;
            dgvPhong.RowHeadersWidth = 51;
            dgvPhong.SelectionMode = DataGridViewSelectionMode.FullRowSelect;
            dgvPhong.Size = new Size(383, 193);
            dgvPhong.TabIndex = 4;
            dgvPhong.CellClick += dgvPhong_CellClick;
            // 
            // dgvPhongChon
            // 
            dgvPhongChon.AllowUserToAddRows = false;
            dgvPhongChon.AllowUserToDeleteRows = false;
            dgvPhongChon.AllowUserToResizeRows = false;
            dgvPhongChon.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
            dgvPhongChon.BackgroundColor = Color.White;
            dgvPhongChon.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            dgvPhongChon.Columns.AddRange(new DataGridViewColumn[] { colPhongChon, colSoNguoi, colDonGiaNgay });
            dgvPhongChon.Location = new Point(423, 160);
            dgvPhongChon.Margin = new Padding(3, 4, 3, 4);
            dgvPhongChon.MultiSelect = false;
            dgvPhongChon.Name = "dgvPhongChon";
            dgvPhongChon.ReadOnly = true;
            dgvPhongChon.RowHeadersVisible = false;
            dgvPhongChon.RowHeadersWidth = 51;
            dgvPhongChon.SelectionMode = DataGridViewSelectionMode.FullRowSelect;
            dgvPhongChon.Size = new Size(383, 193);
            dgvPhongChon.TabIndex = 5;
            // 
            // colPhongChon
            // 
            colPhongChon.HeaderText = "Phòng chọn";
            colPhongChon.MinimumWidth = 6;
            colPhongChon.Name = "colPhongChon";
            colPhongChon.ReadOnly = true;
            // 
            // colSoNguoi
            // 
            colSoNguoi.HeaderText = "Số người";
            colSoNguoi.MinimumWidth = 6;
            colSoNguoi.Name = "colSoNguoi";
            colSoNguoi.ReadOnly = true;
            // 
            // colDonGiaNgay
            // 
            colDonGiaNgay.HeaderText = "Đơn giá/ngày";
            colDonGiaNgay.MinimumWidth = 6;
            colDonGiaNgay.Name = "colDonGiaNgay";
            colDonGiaNgay.ReadOnly = true;
            // 
            // btnLapPhieuDat
            // 
            btnLapPhieuDat.Location = new Point(680, 371);
            btnLapPhieuDat.Margin = new Padding(3, 4, 3, 4);
            btnLapPhieuDat.Name = "btnLapPhieuDat";
            btnLapPhieuDat.Size = new Size(126, 43);
            btnLapPhieuDat.TabIndex = 6;
            btnLapPhieuDat.Text = "Lập phiếu đặt";
            btnLapPhieuDat.UseVisualStyleBackColor = true;
            btnLapPhieuDat.Click += btnLapPhieuDat_Click;
            // 
            // lblPhieuDat
            // 
            lblPhieuDat.AutoSize = true;
            lblPhieuDat.Location = new Point(23, 433);
            lblPhieuDat.Name = "lblPhieuDat";
            lblPhieuDat.Size = new Size(121, 20);
            lblPhieuDat.TabIndex = 8;
            lblPhieuDat.Text = "Phiếu đặt phòng:";
            // 
            // dgvPhieuDat
            // 
            dgvPhieuDat.AllowUserToAddRows = false;
            dgvPhieuDat.AllowUserToDeleteRows = false;
            dgvPhieuDat.AllowUserToResizeRows = false;
            dgvPhieuDat.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
            dgvPhieuDat.BackgroundColor = Color.White;
            dgvPhieuDat.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            dgvPhieuDat.Location = new Point(23, 467);
            dgvPhieuDat.Margin = new Padding(3, 4, 3, 4);
            dgvPhieuDat.MultiSelect = false;
            dgvPhieuDat.Name = "dgvPhieuDat";
            dgvPhieuDat.ReadOnly = true;
            dgvPhieuDat.RowHeadersVisible = false;
            dgvPhieuDat.RowHeadersWidth = 51;
            dgvPhieuDat.SelectionMode = DataGridViewSelectionMode.FullRowSelect;
            dgvPhieuDat.Size = new Size(783, 167);
            dgvPhieuDat.TabIndex = 7;
            dgvPhieuDat.CellClick += dgvPhieuDat_CellClick;
            dgvPhieuDat.CellContentClick += dgvPhieuDat_CellContentClick;
            // 
            // FrmDatPhong
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(834, 667);
            Controls.Add(dgvPhieuDat);
            Controls.Add(lblPhieuDat);
            Controls.Add(btnLapPhieuDat);
            Controls.Add(dgvPhongChon);
            Controls.Add(dgvPhong);
            Controls.Add(txtTienCoc);
            Controls.Add(lblTienCoc);
            Controls.Add(txtKenhDat);
            Controls.Add(lblKenhDat);
            Controls.Add(txtKhach);
            Controls.Add(lblKhach);
            Controls.Add(txtSoPhieuDat);
            Controls.Add(lblSoPhieuDat);
            Controls.Add(lblNhanPhongTab);
            Controls.Add(lblDatPhongTab);
            Controls.Add(lblKhachTab);
            Controls.Add(lblNav);
            FormBorderStyle = FormBorderStyle.FixedSingle;
            Margin = new Padding(3, 4, 3, 4);
            MaximizeBox = false;
            Name = "FrmDatPhong";
            StartPosition = FormStartPosition.CenterScreen;
            Text = "Khách hàng - Đặt phòng - Nhận phòng";
            Load += FrmDatPhong_Load;
            ((System.ComponentModel.ISupportInitialize)dgvPhong).EndInit();
            ((System.ComponentModel.ISupportInitialize)dgvPhongChon).EndInit();
            ((System.ComponentModel.ISupportInitialize)dgvPhieuDat).EndInit();
            ResumeLayout(false);
            PerformLayout();
        }
    }
}