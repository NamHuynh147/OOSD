using System.Drawing;
using System.Windows.Forms;

namespace Form_QLKS
{
    partial class Form1
    {
        private System.ComponentModel.IContainer components = null;

        private Label lblTitle;

        private Button btnDanhMuc;
        private Button btnPhongTienNghi;
        private Button btnDatPhong;
        private Button btnDichVu;
        private Button btnTraPhong;
        private Button btnThongKe;
        private Button btnThoat;

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
            lblTitle = new Label();

            btnDanhMuc = new Button();
            btnPhongTienNghi = new Button();
            btnDatPhong = new Button();
            btnDichVu = new Button();
            btnTraPhong = new Button();
            btnThongKe = new Button();
            btnThoat = new Button();

            SuspendLayout();

            // 
            // lblTitle
            // 
            lblTitle.AutoSize = true;
            lblTitle.Font = new Font(
                "Arial",
                20F,
                FontStyle.Bold,
                GraphicsUnit.Point);

            lblTitle.ForeColor = Color.FromArgb(0, 70, 130);

            lblTitle.Location = new Point(313, 31);
            lblTitle.Name = "lblTitle";
            lblTitle.Size = new Size(572, 40);
            lblTitle.TabIndex = 0;
            lblTitle.Text = "HỆ THỐNG QUẢN LÝ KHÁCH SẠN";

            // 
            // btnDanhMuc
            // 
            btnDanhMuc.Font = new Font(
                "Segoe UI",
                13.8F,
                FontStyle.Regular,
                GraphicsUnit.Point);

            btnDanhMuc.Location = new Point(127, 145);
            btnDanhMuc.Name = "btnDanhMuc";
            btnDanhMuc.Size = new Size(193, 70);
            btnDanhMuc.TabIndex = 1;
            btnDanhMuc.Text = "Danh mục";
            btnDanhMuc.UseVisualStyleBackColor = true;
            btnDanhMuc.Click += hsa_Click;

            // 
            // btnPhongTienNghi
            // 
            btnPhongTienNghi.Font = new Font(
                "Segoe UI",
                13.8F,
                FontStyle.Regular,
                GraphicsUnit.Point);

            btnPhongTienNghi.Location = new Point(352, 145);
            btnPhongTienNghi.Name = "btnPhongTienNghi";
            btnPhongTienNghi.Size = new Size(376, 70);
            btnPhongTienNghi.TabIndex = 2;
            btnPhongTienNghi.Text = "Phòng - Tiện nghi";
            btnPhongTienNghi.UseVisualStyleBackColor = true;
            btnPhongTienNghi.Click += phongTienNghi_Click;

            // 
            // btnDatPhong
            // 
            btnDatPhong.Font = new Font(
                "Segoe UI",
                13.8F,
                FontStyle.Regular,
                GraphicsUnit.Point);

            btnDatPhong.Location = new Point(780, 145);
            btnDatPhong.Name = "btnDatPhong";
            btnDatPhong.Size = new Size(376, 70);
            btnDatPhong.TabIndex = 3;
            btnDatPhong.Text = "Đặt/Nhận phòng";
            btnDatPhong.UseVisualStyleBackColor = true;
            btnDatPhong.Click += btnDatPhong_Click;

            // 
            // btnDichVu
            // 
            btnDichVu.Font = new Font(
                "Segoe UI",
                13.8F,
                FontStyle.Regular,
                GraphicsUnit.Point);

            btnDichVu.Location = new Point(127, 281);
            btnDichVu.Name = "btnDichVu";
            btnDichVu.Size = new Size(193, 82);
            btnDichVu.TabIndex = 4;
            btnDichVu.Text = "Sử dụng dịch vụ";
            btnDichVu.UseVisualStyleBackColor = true;
            btnDichVu.Click += btnPhong_Click;

            // 
            // btnTraPhong
            // 
            btnTraPhong.Font = new Font(
                "Segoe UI",
                13.8F,
                FontStyle.Regular,
                GraphicsUnit.Point);

            btnTraPhong.Location = new Point(352, 281);
            btnTraPhong.Name = "btnTraPhong";
            btnTraPhong.Size = new Size(376, 82);
            btnTraPhong.TabIndex = 5;
            btnTraPhong.Text = "Trả phòng - thanh toán";
            btnTraPhong.UseVisualStyleBackColor = true;
            btnTraPhong.Click += btnThanhToan_Click;

            // 
            // btnThongKe
            // 
            btnThongKe.Font = new Font(
                "Segoe UI",
                13.8F,
                FontStyle.Regular,
                GraphicsUnit.Point);

            btnThongKe.Location = new Point(780, 281);
            btnThongKe.Name = "btnThongKe";
            btnThongKe.Size = new Size(376, 82);
            btnThongKe.TabIndex = 6;
            btnThongKe.Text = "Thống kê 📋";
            btnThongKe.UseVisualStyleBackColor = true;
            btnThongKe.Click += btnThongKe_Click;

            // 
            // btnThoat
            // 
            btnThoat.Font = new Font(
                "Segoe UI",
                13.8F,
                FontStyle.Regular,
                GraphicsUnit.Point);

            btnThoat.Location = new Point(352, 412);
            btnThoat.Name = "btnThoat";
            btnThoat.Size = new Size(376, 82);
            btnThoat.TabIndex = 7;
            btnThoat.Text = "Thoát";
            btnThoat.UseVisualStyleBackColor = true;
            btnThoat.Click += btnThoat_Click;

            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.White;

            ClientSize = new Size(1266, 538);

            Controls.Add(btnThoat);
            Controls.Add(btnThongKe);
            Controls.Add(btnTraPhong);
            Controls.Add(btnDichVu);
            Controls.Add(btnDatPhong);
            Controls.Add(btnPhongTienNghi);
            Controls.Add(btnDanhMuc);
            Controls.Add(lblTitle);

            Margin = new Padding(3, 4, 3, 4);
            Name = "Form1";
            StartPosition = FormStartPosition.CenterScreen;
            Text = "Quản lý khách sạn";

            ResumeLayout(false);
            PerformLayout();
        }
    }
}