using System.Drawing;
using System.Windows.Forms;

namespace Form_QLKS
{
    partial class FrmDichVu
    {
        private System.ComponentModel.IContainer components = null;

        private Label lblPhieuLuuTru;
        private TextBox txtPhieuLuuTru;

        private Label lblPhong;
        private TextBox txtPhong;

        private Label lblDichVu;
        private TextBox txtDichVu;

        private Label lblNgaySuDung;
        private TextBox txtNgaySuDung;

        private Label lblSoLuong;
        private TextBox txtSoLuong;

        private Button btnGhiNhan;

        private DataGridView dgvDichVu;

        private DataGridViewTextBoxColumn colSoPhieu;
        private DataGridViewTextBoxColumn colPhong;
        private DataGridViewTextBoxColumn colNgay;
        private DataGridViewTextBoxColumn colDichVu;
        private DataGridViewTextBoxColumn colSoLuong;
        private DataGridViewTextBoxColumn colDonGia;
        private DataGridViewTextBoxColumn colThanhTien;

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
            this.components =
                new System.ComponentModel.Container();

            this.lblPhieuLuuTru =
                new Label();

            this.txtPhieuLuuTru =
                new TextBox();

            this.lblPhong =
                new Label();

            this.txtPhong =
                new TextBox();

            this.lblDichVu =
                new Label();

            this.txtDichVu =
                new TextBox();

            this.lblNgaySuDung =
                new Label();

            this.txtNgaySuDung =
                new TextBox();

            this.lblSoLuong =
                new Label();

            this.txtSoLuong =
                new TextBox();

            this.btnGhiNhan =
                new Button();

            this.dgvDichVu =
                new DataGridView();

            this.colSoPhieu =
                new DataGridViewTextBoxColumn();

            this.colPhong =
                new DataGridViewTextBoxColumn();

            this.colNgay =
                new DataGridViewTextBoxColumn();

            this.colDichVu =
                new DataGridViewTextBoxColumn();

            this.colSoLuong =
                new DataGridViewTextBoxColumn();

            this.colDonGia =
                new DataGridViewTextBoxColumn();

            this.colThanhTien =
                new DataGridViewTextBoxColumn();

            ((System.ComponentModel.ISupportInitialize)
                (this.dgvDichVu)).BeginInit();

            this.SuspendLayout();

            // ==========================================
            // lblPhieuLuuTru
            // ==========================================
            this.lblPhieuLuuTru.AutoSize = true;

            this.lblPhieuLuuTru.Location =
                new Point(20, 25);

            this.lblPhieuLuuTru.Name =
                "lblPhieuLuuTru";

            this.lblPhieuLuuTru.Text =
                "Phiếu lưu trú:";

            // ==========================================
            // txtPhieuLuuTru
            // ==========================================
            this.txtPhieuLuuTru.Location =
                new Point(115, 22);

            this.txtPhieuLuuTru.Name =
                "txtPhieuLuuTru";

            this.txtPhieuLuuTru.Size =
                new Size(140, 23);

            this.txtPhieuLuuTru.TabIndex = 0;

            this.txtPhieuLuuTru.Text =
                "DP001";

            // ==========================================
            // lblPhong
            // ==========================================
            this.lblPhong.AutoSize = true;

            this.lblPhong.Location =
                new Point(285, 25);

            this.lblPhong.Name =
                "lblPhong";

            this.lblPhong.Text =
                "Phòng:";

            // ==========================================
            // txtPhong
            // ==========================================
            this.txtPhong.Location =
                new Point(335, 22);

            this.txtPhong.Name =
                "txtPhong";

            this.txtPhong.Size =
                new Size(100, 23);

            this.txtPhong.TabIndex = 1;

            this.txtPhong.Text =
                "A101";

            // ==========================================
            // lblDichVu
            // ==========================================
            this.lblDichVu.AutoSize = true;

            this.lblDichVu.Location =
                new Point(455, 25);

            this.lblDichVu.Name =
                "lblDichVu";

            this.lblDichVu.Text =
                "Dịch vụ:";

            // ==========================================
            // txtDichVu
            // ==========================================
            this.txtDichVu.Location =
                new Point(515, 22);

            this.txtDichVu.Name =
                "txtDichVu";

            this.txtDichVu.Size =
                new Size(175, 23);

            this.txtDichVu.TabIndex = 2;

            this.txtDichVu.Text =
                "Ăn sáng";

            // ==========================================
            // lblNgaySuDung
            // ==========================================
            this.lblNgaySuDung.AutoSize = true;

            this.lblNgaySuDung.Location =
                new Point(20, 67);

            this.lblNgaySuDung.Name =
                "lblNgaySuDung";

            this.lblNgaySuDung.Text =
                "Ngày sử dụng:";

            // ==========================================
            // txtNgaySuDung
            // ==========================================
            this.txtNgaySuDung.Location =
                new Point(115, 64);

            this.txtNgaySuDung.Name =
                "txtNgaySuDung";

            this.txtNgaySuDung.Size =
                new Size(140, 23);

            this.txtNgaySuDung.TabIndex = 3;

            this.txtNgaySuDung.Text =
                "12/09/2026";

            // ==========================================
            // lblSoLuong
            // ==========================================
            this.lblSoLuong.AutoSize = true;

            this.lblSoLuong.Location =
                new Point(285, 67);

            this.lblSoLuong.Name =
                "lblSoLuong";

            this.lblSoLuong.Text =
                "Số lượng:";

            // ==========================================
            // txtSoLuong
            // ==========================================
            this.txtSoLuong.Location =
                new Point(335, 64);

            this.txtSoLuong.Name =
                "txtSoLuong";

            this.txtSoLuong.Size =
                new Size(100, 23);

            this.txtSoLuong.TabIndex = 4;

            this.txtSoLuong.Text =
                "2";

            // ==========================================
            // btnGhiNhan
            // ==========================================
            this.btnGhiNhan.Location =
                new Point(515, 58);

            this.btnGhiNhan.Name =
                "btnGhiNhan";

            this.btnGhiNhan.Size =
                new Size(140, 35);

            this.btnGhiNhan.TabIndex = 5;

            this.btnGhiNhan.Text =
                "Ghi nhận";

            this.btnGhiNhan.UseVisualStyleBackColor =
                true;

            this.btnGhiNhan.Click +=
                new System.EventHandler(
                    this.btnGhiNhan_Click);

            // ==========================================
            // dgvDichVu
            // ==========================================
            this.dgvDichVu.AllowUserToAddRows = false;

            this.dgvDichVu.AllowUserToDeleteRows =
                false;

            this.dgvDichVu.AllowUserToResizeRows =
                false;

            this.dgvDichVu.AutoGenerateColumns =
                false;

            this.dgvDichVu.AutoSizeColumnsMode =
                DataGridViewAutoSizeColumnsMode.Fill;

            this.dgvDichVu.BackgroundColor =
                Color.White;

            this.dgvDichVu.ColumnHeadersHeightSizeMode =
                DataGridViewColumnHeadersHeightSizeMode.AutoSize;

            this.dgvDichVu.Columns.AddRange(
                new DataGridViewColumn[]
                {
                    this.colSoPhieu,
                    this.colPhong,
                    this.colNgay,
                    this.colDichVu,
                    this.colSoLuong,
                    this.colDonGia,
                    this.colThanhTien
                });

            this.dgvDichVu.Location =
                new Point(20, 125);

            this.dgvDichVu.MultiSelect = false;

            this.dgvDichVu.Name =
                "dgvDichVu";

            this.dgvDichVu.ReadOnly = true;

            this.dgvDichVu.RowHeadersVisible = false;

            this.dgvDichVu.SelectionMode =
                DataGridViewSelectionMode.FullRowSelect;

            this.dgvDichVu.Size =
                new Size(735, 315);

            this.dgvDichVu.TabIndex = 6;

            this.dgvDichVu.CellClick +=
                new DataGridViewCellEventHandler(
                    this.dgvDichVu_CellClick);

            // ==========================================
            // colSoPhieu
            // ==========================================
            this.colSoPhieu.DataPropertyName =
                "Số phiếu";

            this.colSoPhieu.HeaderText =
                "Số phiếu";

            this.colSoPhieu.Name =
                "colSoPhieu";

            this.colSoPhieu.ReadOnly = true;

            // ==========================================
            // colPhong
            // ==========================================
            this.colPhong.DataPropertyName =
                "Phòng";

            this.colPhong.HeaderText =
                "Phòng";

            this.colPhong.Name =
                "colPhong";

            this.colPhong.ReadOnly = true;

            // ==========================================
            // colNgay
            // ==========================================
            this.colNgay.DataPropertyName =
                "Ngày";

            this.colNgay.HeaderText =
                "Ngày";

            this.colNgay.Name =
                "colNgay";

            this.colNgay.ReadOnly = true;

            // ==========================================
            // colDichVu
            // ==========================================
            this.colDichVu.DataPropertyName =
                "Dịch vụ";

            this.colDichVu.HeaderText =
                "Dịch vụ";

            this.colDichVu.Name =
                "colDichVu";

            this.colDichVu.ReadOnly = true;

            // ==========================================
            // colSoLuong
            // ==========================================
            this.colSoLuong.DataPropertyName =
                "Số lượng";

            this.colSoLuong.HeaderText =
                "Số lượng";

            this.colSoLuong.Name =
                "colSoLuong";

            this.colSoLuong.ReadOnly = true;

            // ==========================================
            // colDonGia
            // ==========================================
            this.colDonGia.DataPropertyName =
                "Đơn giá";

            this.colDonGia.HeaderText =
                "Đơn giá";

            this.colDonGia.Name =
                "colDonGia";

            this.colDonGia.ReadOnly = true;

            // ==========================================
            // colThanhTien
            // ==========================================
            this.colThanhTien.DataPropertyName =
                "Thành tiền";

            this.colThanhTien.HeaderText =
                "Thành tiền";

            this.colThanhTien.Name =
                "colThanhTien";

            this.colThanhTien.ReadOnly = true;

            // ==========================================
            // FORM
            // ==========================================
            this.AutoScaleDimensions =
                new SizeF(7F, 15F);

            this.AutoScaleMode =
                AutoScaleMode.Font;

            this.ClientSize =
                new Size(780, 465);

            this.Controls.Add(
                this.dgvDichVu);

            this.Controls.Add(
                this.btnGhiNhan);

            this.Controls.Add(
                this.txtSoLuong);

            this.Controls.Add(
                this.lblSoLuong);

            this.Controls.Add(
                this.txtNgaySuDung);

            this.Controls.Add(
                this.lblNgaySuDung);

            this.Controls.Add(
                this.txtDichVu);

            this.Controls.Add(
                this.lblDichVu);

            this.Controls.Add(
                this.txtPhong);

            this.Controls.Add(
                this.lblPhong);

            this.Controls.Add(
                this.txtPhieuLuuTru);

            this.Controls.Add(
                this.lblPhieuLuuTru);

            this.FormBorderStyle =
                FormBorderStyle.FixedSingle;

            this.MaximizeBox = false;

            this.Name =
                "FrmDichVu";

            this.StartPosition =
                FormStartPosition.CenterScreen;

            this.Text =
                "Sử dụng dịch vụ";

            this.Load +=
                new System.EventHandler(
                    this.FrmDichVu_Load);

            ((System.ComponentModel.ISupportInitialize)
                (this.dgvDichVu)).EndInit();

            this.ResumeLayout(false);
            this.PerformLayout();
        }
    }
}