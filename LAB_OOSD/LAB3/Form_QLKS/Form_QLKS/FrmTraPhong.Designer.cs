using System.Drawing;
using System.Windows.Forms;

namespace Form_QLKS

{
    partial class FrmTraPhong
    {
        private System.ComponentModel.IContainer components = null;

        private Label lblPhieuDangO;
        private TextBox txtPhieuDangO;

        private DataGridView dgvPhong;
        private DataGridViewTextBoxColumn colPhong;
        private DataGridViewTextBoxColumn colDonGiaNgay;

        private DataGridView dgvTienNghi;
        private DataGridViewTextBoxColumn colTienNghi;
        private DataGridViewTextBoxColumn colLoai;
        private DataGridViewTextBoxColumn colTinhTrang;

        private DataGridView dgvDenBu;
        private DataGridViewTextBoxColumn colTienNghiDenBu;
        private DataGridViewTextBoxColumn colMucDo;
        private DataGridViewTextBoxColumn colSoTien;

        private Label lblSoPhieuDenBu;
        private TextBox txtPhieuDenBu;

        private Label lblMucDo;
        private TextBox txtMucDo;

        private Label lblSoTienDenBu;
        private TextBox txtSoTienDenBu;

        private Button btnLapPhieuDenBu;

        private Label lblSoHoaDon;
        private TextBox txtSoHoaDon;

        private Label lblSoNgayTinhTien;
        private TextBox txtSoNgayTinhTien;

        private Button btnLapHoaDon;

        private DataGridView dgvHoaDon;

        private DataGridViewTextBoxColumn colHoaDon;
        private DataGridViewTextBoxColumn colPhieuDat;
        private DataGridViewTextBoxColumn colTienPhong;
        private DataGridViewTextBoxColumn colTienDichVu;
        private DataGridViewTextBoxColumn colTongTien;
        private DataGridViewTextBoxColumn colTrangThai;

        private Label lblHinhThuc;
        private TextBox txtHinhThuc;

        private Label lblSoTienThanhToan;
        private TextBox txtSoTienThanhToan;

        private Button btnThanhToan;
        private Button btnHoanTatTraPhong;

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

            this.lblPhieuDangO = new Label();
            this.txtPhieuDangO = new TextBox();

            this.dgvPhong = new DataGridView();
            this.colPhong = new DataGridViewTextBoxColumn();
            this.colDonGiaNgay = new DataGridViewTextBoxColumn();

            this.dgvTienNghi = new DataGridView();
            this.colTienNghi = new DataGridViewTextBoxColumn();
            this.colLoai = new DataGridViewTextBoxColumn();
            this.colTinhTrang = new DataGridViewTextBoxColumn();

            this.dgvDenBu = new DataGridView();
            this.colTienNghiDenBu =
                new DataGridViewTextBoxColumn();
            this.colMucDo =
                new DataGridViewTextBoxColumn();
            this.colSoTien =
                new DataGridViewTextBoxColumn();

            this.lblSoPhieuDenBu = new Label();
            this.txtPhieuDenBu = new TextBox();

            this.lblMucDo = new Label();
            this.txtMucDo = new TextBox();

            this.lblSoTienDenBu = new Label();
            this.txtSoTienDenBu = new TextBox();

            this.btnLapPhieuDenBu = new Button();

            this.lblSoHoaDon = new Label();
            this.txtSoHoaDon = new TextBox();

            this.lblSoNgayTinhTien = new Label();
            this.txtSoNgayTinhTien = new TextBox();

            this.btnLapHoaDon = new Button();

            this.dgvHoaDon = new DataGridView();

            this.colHoaDon =
                new DataGridViewTextBoxColumn();

            this.colPhieuDat =
                new DataGridViewTextBoxColumn();

            this.colTienPhong =
                new DataGridViewTextBoxColumn();

            this.colTienDichVu =
                new DataGridViewTextBoxColumn();

            this.colTongTien =
                new DataGridViewTextBoxColumn();

            this.colTrangThai =
                new DataGridViewTextBoxColumn();

            this.lblHinhThuc = new Label();
            this.txtHinhThuc = new TextBox();

            this.lblSoTienThanhToan = new Label();
            this.txtSoTienThanhToan = new TextBox();

            this.btnThanhToan = new Button();
            this.btnHoanTatTraPhong = new Button();

            ((System.ComponentModel.ISupportInitialize)
                (this.dgvPhong)).BeginInit();

            ((System.ComponentModel.ISupportInitialize)
                (this.dgvTienNghi)).BeginInit();

            ((System.ComponentModel.ISupportInitialize)
                (this.dgvDenBu)).BeginInit();

            ((System.ComponentModel.ISupportInitialize)
                (this.dgvHoaDon)).BeginInit();

            this.SuspendLayout();

            // =================================================
            // Phiếu đang ở
            // =================================================
            this.lblPhieuDangO.AutoSize = true;
            this.lblPhieuDangO.Location =
                new Point(20, 25);
            this.lblPhieuDangO.Name =
                "lblPhieuDangO";
            this.lblPhieuDangO.Text =
                "Phiếu đang ở:";

            this.txtPhieuDangO.Location =
                new Point(110, 22);
            this.txtPhieuDangO.Name =
                "txtPhieuDangO";
            this.txtPhieuDangO.Size =
                new Size(120, 23);
            this.txtPhieuDangO.TabIndex = 0;
            this.txtPhieuDangO.Text =
                "DP001";

            // =================================================
            // dgvPhong
            // =================================================
            this.dgvPhong.AllowUserToAddRows = false;
            this.dgvPhong.AllowUserToDeleteRows = false;
            this.dgvPhong.AutoGenerateColumns = false;
            this.dgvPhong.AutoSizeColumnsMode =
                DataGridViewAutoSizeColumnsMode.Fill;
            this.dgvPhong.BackgroundColor = Color.White;

            this.dgvPhong.Columns.AddRange(
                new DataGridViewColumn[]
                {
                    this.colPhong,
                    this.colDonGiaNgay
                });

            this.dgvPhong.Location =
                new Point(20, 62);
            this.dgvPhong.Name =
                "dgvPhong";
            this.dgvPhong.ReadOnly = true;
            this.dgvPhong.RowHeadersVisible = false;
            this.dgvPhong.SelectionMode =
                DataGridViewSelectionMode.FullRowSelect;
            this.dgvPhong.Size =
                new Size(215, 130);

            
            this.colPhong.DataPropertyName =
                "Phòng";
            this.colPhong.HeaderText =
                "Phòng";
            this.colPhong.Name =
                "colPhong";

            this.colDonGiaNgay.DataPropertyName =
                "Đơn giá/ngày";
            this.colDonGiaNgay.HeaderText =
                "Đơn giá/ngày";
            this.colDonGiaNgay.Name =
                "colDonGiaNgay";

            // =================================================
            // dgvTienNghi
            // =================================================
            this.dgvTienNghi.AllowUserToAddRows = false;
            this.dgvTienNghi.AllowUserToDeleteRows = false;
            this.dgvTienNghi.AutoGenerateColumns = false;
            this.dgvTienNghi.AutoSizeColumnsMode =
                DataGridViewAutoSizeColumnsMode.Fill;
            this.dgvTienNghi.BackgroundColor =
                Color.White;

            this.dgvTienNghi.Columns.AddRange(
                new DataGridViewColumn[]
                {
                    this.colTienNghi,
                    this.colLoai,
                    this.colTinhTrang
                });

            this.dgvTienNghi.Location =
                new Point(245, 62);

            this.dgvTienNghi.Name =
                "dgvTienNghi";

            this.dgvTienNghi.ReadOnly = true;
            this.dgvTienNghi.RowHeadersVisible = false;

            this.dgvTienNghi.SelectionMode =
                DataGridViewSelectionMode.FullRowSelect;

            this.dgvTienNghi.Size =
                new Size(255, 130);

            this.colTienNghi.DataPropertyName =
                "Tiện nghi";
            this.colTienNghi.HeaderText =
                "Tiện nghi";
            this.colTienNghi.Name =
                "colTienNghi";

            this.colLoai.DataPropertyName =
                "Loại";
            this.colLoai.HeaderText =
                "Loại";
            this.colLoai.Name =
                "colLoai";

            this.colTinhTrang.DataPropertyName =
                "Tình trạng";
            this.colTinhTrang.HeaderText =
                "Tình trạng";
            this.colTinhTrang.Name =
                "colTinhTrang";

            // =================================================
            // dgvDenBu
            // =================================================
            this.dgvDenBu.AllowUserToAddRows = false;
            this.dgvDenBu.AllowUserToDeleteRows = false;
            this.dgvDenBu.AutoGenerateColumns = false;
            this.dgvDenBu.AutoSizeColumnsMode =
                DataGridViewAutoSizeColumnsMode.Fill;
            this.dgvDenBu.BackgroundColor =
                Color.White;

            this.dgvDenBu.Columns.AddRange(
                new DataGridViewColumn[]
                {
                    this.colTienNghiDenBu,
                    this.colMucDo,
                    this.colSoTien
                });

            this.dgvDenBu.Location =
                new Point(510, 62);

            this.dgvDenBu.Name =
                "dgvDenBu";

            this.dgvDenBu.ReadOnly = true;
            this.dgvDenBu.RowHeadersVisible = false;

            this.dgvDenBu.SelectionMode =
                DataGridViewSelectionMode.FullRowSelect;

            this.dgvDenBu.Size =
                new Size(265, 130);

            this.dgvDenBu.CellClick +=
                new DataGridViewCellEventHandler(
                    this.dgvDenBu_CellClick);

            this.colTienNghiDenBu.DataPropertyName =
                "Tiện nghi đền bù";

            this.colTienNghiDenBu.HeaderText =
                "Tiện nghi đền bù";

            this.colTienNghiDenBu.Name =
                "colTienNghiDenBu";

            this.colMucDo.DataPropertyName =
                "Mức độ";

            this.colMucDo.HeaderText =
                "Mức độ";

            this.colMucDo.Name =
                "colMucDo";

            this.colSoTien.DataPropertyName =
                "Số tiền";

            this.colSoTien.HeaderText =
                "Số tiền";

            this.colSoTien.Name =
                "colSoTien";

            // =================================================
            // Phiếu đền bù
            // =================================================
            this.lblSoPhieuDenBu.AutoSize = true;
            this.lblSoPhieuDenBu.Location =
                new Point(20, 215);
            this.lblSoPhieuDenBu.Name =
                "lblSoPhieuDenBu";
            this.lblSoPhieuDenBu.Text =
                "Số phiếu đền bù:";

            this.txtPhieuDenBu.Location =
                new Point(115, 212);
            this.txtPhieuDenBu.Name =
                "txtPhieuDenBu";
            this.txtPhieuDenBu.Size =
                new Size(120, 23);
            this.txtPhieuDenBu.TabIndex = 1;
            this.txtPhieuDenBu.Text =
                "DB001";

            // =================================================
            // Mức độ
            // =================================================
            this.lblMucDo.AutoSize = true;
            this.lblMucDo.Location =
                new Point(260, 215);
            this.lblMucDo.Name =
                "lblMucDo";
            this.lblMucDo.Text =
                "Mức độ:";

            this.txtMucDo.Location =
                new Point(315, 212);
            this.txtMucDo.Name =
                "txtMucDo";
            this.txtMucDo.Size =
                new Size(120, 23);
            this.txtMucDo.TabIndex = 2;
            this.txtMucDo.Text =
                "Hư hỏng nhẹ";

            // =================================================
            // Số tiền đền bù
            // =================================================
            this.lblSoTienDenBu.AutoSize = true;
            this.lblSoTienDenBu.Location =
                new Point(455, 215);
            this.lblSoTienDenBu.Name =
                "lblSoTienDenBu";
            this.lblSoTienDenBu.Text =
                "Số tiền:";

            this.txtSoTienDenBu.Location =
                new Point(505, 212);
            this.txtSoTienDenBu.Name =
                "txtSoTienDenBu";
            this.txtSoTienDenBu.Size =
                new Size(120, 23);
            this.txtSoTienDenBu.TabIndex = 3;
            this.txtSoTienDenBu.Text =
                "500000";

            // =================================================
            // Button lập phiếu đền bù
            // =================================================
            this.btnLapPhieuDenBu.Location =
                new Point(650, 208);

            this.btnLapPhieuDenBu.Name =
                "btnLapPhieuDenBu";

            this.btnLapPhieuDenBu.Size =
                new Size(125, 32);

            this.btnLapPhieuDenBu.TabIndex = 4;

            this.btnLapPhieuDenBu.Text =
                "Lập phiếu đền bù";

            this.btnLapPhieuDenBu.UseVisualStyleBackColor =
                true;

            this.btnLapPhieuDenBu.Click +=
                new System.EventHandler(
                    this.btnLapPhieuDenBu_Click);

            // =================================================
            // Số hóa đơn
            // =================================================
            this.lblSoHoaDon.AutoSize = true;
            this.lblSoHoaDon.Location =
                new Point(20, 258);

            this.lblSoHoaDon.Name =
                "lblSoHoaDon";

            this.lblSoHoaDon.Text =
                "Số hóa đơn:";

            this.txtSoHoaDon.Location =
                new Point(105, 255);

            this.txtSoHoaDon.Name =
                "txtSoHoaDon";

            this.txtSoHoaDon.Size =
                new Size(120, 23);

            this.txtSoHoaDon.TabIndex = 5;

            this.txtSoHoaDon.Text =
                "HD001";

            // =================================================
            // Số ngày
            // =================================================
            this.lblSoNgayTinhTien.AutoSize = true;

            this.lblSoNgayTinhTien.Location =
                new Point(250, 258);

            this.lblSoNgayTinhTien.Name =
                "lblSoNgayTinhTien";

            this.lblSoNgayTinhTien.Text =
                "Số ngày tính tiền:";

            this.txtSoNgayTinhTien.Location =
                new Point(350, 255);

            this.txtSoNgayTinhTien.Name =
                "txtSoNgayTinhTien";

            this.txtSoNgayTinhTien.Size =
                new Size(75, 23);

            this.txtSoNgayTinhTien.TabIndex = 6;

            this.txtSoNgayTinhTien.Text =
                "2";

            // =================================================
            // Button hóa đơn
            // =================================================
            this.btnLapHoaDon.Location =
                new Point(430, 250);

            this.btnLapHoaDon.Name =
                "btnLapHoaDon";

            this.btnLapHoaDon.Size =
                new Size(115, 32);

            this.btnLapHoaDon.TabIndex = 7;

            this.btnLapHoaDon.Text =
                "Lập hóa đơn";

            this.btnLapHoaDon.UseVisualStyleBackColor =
                true;

            this.btnLapHoaDon.Click +=
                new System.EventHandler(
                    this.btnLapHoaDon_Click);

            // =================================================
            // dgvHoaDon
            // =================================================
            this.dgvHoaDon.AllowUserToAddRows = false;
            this.dgvHoaDon.AllowUserToDeleteRows = false;
            this.dgvHoaDon.AutoGenerateColumns = false;
            this.dgvHoaDon.AutoSizeColumnsMode =
                DataGridViewAutoSizeColumnsMode.Fill;

            this.dgvHoaDon.BackgroundColor =
                Color.White;

            this.dgvHoaDon.Columns.AddRange(
                new DataGridViewColumn[]
                {
                    this.colHoaDon,
                    this.colPhieuDat,
                    this.colTienPhong,
                    this.colTienDichVu,
                    this.colTongTien,
                    this.colTrangThai
                });

            this.dgvHoaDon.Location =
                new Point(20, 300);

            this.dgvHoaDon.Name =
                "dgvHoaDon";

            this.dgvHoaDon.ReadOnly = true;
            this.dgvHoaDon.RowHeadersVisible = false;

            this.dgvHoaDon.SelectionMode =
                DataGridViewSelectionMode.FullRowSelect;

            this.dgvHoaDon.Size =
                new Size(755, 145);

            this.dgvHoaDon.CellClick +=
                new DataGridViewCellEventHandler(
                    this.dgvHoaDon_CellClick);

            // =================================================
            // Cột hóa đơn
            // =================================================
            this.colHoaDon.DataPropertyName =
                "Hóa đơn";

            this.colHoaDon.HeaderText =
                "Hóa đơn";

            this.colHoaDon.Name =
                "colHoaDon";

            // =================================================
            // Cột phiếu đặt
            // =================================================
            this.colPhieuDat.DataPropertyName =
                "Phiếu đặt";

            this.colPhieuDat.HeaderText =
                "Phiếu đặt";

            this.colPhieuDat.Name =
                "colPhieuDat";

            // =================================================
            // Cột tiền phòng
            // =================================================
            this.colTienPhong.DataPropertyName =
                "Tiền phòng";

            this.colTienPhong.HeaderText =
                "Tiền phòng";

            this.colTienPhong.Name =
                "colTienPhong";

            // =================================================
            // Cột tiền dịch vụ
            // =================================================
            this.colTienDichVu.DataPropertyName =
                "Tiền dịch vụ";

            this.colTienDichVu.HeaderText =
                "Tiền dịch vụ";

            this.colTienDichVu.Name =
                "colTienDichVu";

            // =================================================
            // Cột tổng tiền
            // =================================================
            this.colTongTien.DataPropertyName =
                "Tổng tiền";

            this.colTongTien.HeaderText =
                "Tổng tiền";

            this.colTongTien.Name =
                "colTongTien";

            // =================================================
            // Cột trạng thái
            // =================================================
            this.colTrangThai.DataPropertyName =
                "Trạng thái";

            this.colTrangThai.HeaderText =
                "Trạng thái";

            this.colTrangThai.Name =
                "colTrangThai";

            // =================================================
            // Hình thức
            // =================================================
            this.lblHinhThuc.AutoSize = true;

            this.lblHinhThuc.Location =
                new Point(20, 470);

            this.lblHinhThuc.Name =
                "lblHinhThuc";

            this.lblHinhThuc.Text =
                "Hình thức:";

            this.txtHinhThuc.Location =
                new Point(80, 467);

            this.txtHinhThuc.Name =
                "txtHinhThuc";

            this.txtHinhThuc.Size =
                new Size(100, 23);

            this.txtHinhThuc.TabIndex = 8;

            this.txtHinhThuc.Text =
                "Thẻ";

            // =================================================
            // Số tiền thanh toán
            // =================================================
            this.lblSoTienThanhToan.AutoSize = true;

            this.lblSoTienThanhToan.Location =
                new Point(195, 470);

            this.lblSoTienThanhToan.Name =
                "lblSoTienThanhToan";

            this.lblSoTienThanhToan.Text =
                "Số tiền:";

            this.txtSoTienThanhToan.Location =
                new Point(250, 467);

            this.txtSoTienThanhToan.Name =
                "txtSoTienThanhToan";

            this.txtSoTienThanhToan.Size =
                new Size(100, 23);

            this.txtSoTienThanhToan.TabIndex = 9;

            this.txtSoTienThanhToan.Text =
                "1200000";

            // =================================================
            // Thanh toán
            // =================================================
            this.btnThanhToan.Location =
                new Point(365, 462);

            this.btnThanhToan.Name =
                "btnThanhToan";

            this.btnThanhToan.Size =
                new Size(110, 32);

            this.btnThanhToan.TabIndex = 10;

            this.btnThanhToan.Text =
                "Thanh toán";

            this.btnThanhToan.UseVisualStyleBackColor =
                true;

            this.btnThanhToan.Click +=
                new System.EventHandler(
                    this.btnThanhToan_Click);

            // =================================================
            // Hoàn tất trả phòng
            // =================================================
            this.btnHoanTatTraPhong.Location =
                new Point(490, 462);

            this.btnHoanTatTraPhong.Name =
                "btnHoanTatTraPhong";

            this.btnHoanTatTraPhong.Size =
                new Size(145, 32);

            this.btnHoanTatTraPhong.TabIndex = 11;

            this.btnHoanTatTraPhong.Text =
                "Hoàn tất trả phòng";

            this.btnHoanTatTraPhong.UseVisualStyleBackColor =
                true;

            this.btnHoanTatTraPhong.Click +=
                new System.EventHandler(
                    this.btnHoanTatTraPhong_Click);

            // =================================================
            // FORM
            // =================================================
            this.AutoScaleDimensions =
                new SizeF(7F, 15F);

            this.AutoScaleMode =
                AutoScaleMode.Font;

            this.ClientSize =
                new Size(800, 515);

            this.Controls.Add(
                this.btnHoanTatTraPhong);

            this.Controls.Add(
                this.btnThanhToan);

            this.Controls.Add(
                this.txtSoTienThanhToan);

            this.Controls.Add(
                this.lblSoTienThanhToan);

            this.Controls.Add(
                this.txtHinhThuc);

            this.Controls.Add(
                this.lblHinhThuc);

            this.Controls.Add(
                this.dgvHoaDon);

            this.Controls.Add(
                this.btnLapHoaDon);

            this.Controls.Add(
                this.txtSoNgayTinhTien);

            this.Controls.Add(
                this.lblSoNgayTinhTien);

            this.Controls.Add(
                this.txtSoHoaDon);

            this.Controls.Add(
                this.lblSoHoaDon);

            this.Controls.Add(
                this.btnLapPhieuDenBu);

            this.Controls.Add(
                this.txtSoTienDenBu);

            this.Controls.Add(
                this.lblSoTienDenBu);

            this.Controls.Add(
                this.txtMucDo);

            this.Controls.Add(
                this.lblMucDo);

            this.Controls.Add(
                this.txtPhieuDenBu);

            this.Controls.Add(
                this.lblSoPhieuDenBu);

            this.Controls.Add(
                this.dgvDenBu);

            this.Controls.Add(
                this.dgvTienNghi);

            this.Controls.Add(
                this.dgvPhong);

            this.Controls.Add(
                this.txtPhieuDangO);

            this.Controls.Add(
                this.lblPhieuDangO);

            this.FormBorderStyle =
                FormBorderStyle.FixedSingle;

            this.MaximizeBox = false;

            this.Name =
                "FrmTraPhong";

            this.StartPosition =
                FormStartPosition.CenterScreen;

            this.Text =
                "Trả phòng - Đền bù - Hóa đơn - Thanh toán";

            this.Load +=
                new System.EventHandler(
                    this.FrmTraPhong_Load);

            ((System.ComponentModel.ISupportInitialize)
                (this.dgvPhong)).EndInit();

            ((System.ComponentModel.ISupportInitialize)
                (this.dgvTienNghi)).EndInit();

            ((System.ComponentModel.ISupportInitialize)
                (this.dgvDenBu)).EndInit();

            ((System.ComponentModel.ISupportInitialize)
                (this.dgvHoaDon)).EndInit();

            this.ResumeLayout(false);
            this.PerformLayout();
        }
    }
}