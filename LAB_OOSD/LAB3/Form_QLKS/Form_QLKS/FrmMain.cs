using System;
using System.Windows.Forms;

namespace Form_QLKS
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        // Nút Sử dụng dịch vụ
        private void btnPhong_Click(object? sender, EventArgs e)
        {
            FrmDichVu frm = new FrmDichVu();
            frm.ShowDialog();
        }

        // Nút Đặt/Nhận phòng
        private void btnDatPhong_Click(object? sender, EventArgs e)
        {
            FrmDatPhong frm = new FrmDatPhong();
            frm.ShowDialog();
        }

        // Nút Phòng - Tiện nghi
        private void phongTienNghi_Click(object? sender, EventArgs e)
        {
            FrmPhongTienNghi frm = new FrmPhongTienNghi();
            frm.ShowDialog();
        }

        // Nút Danh mục
        private void hsa_Click(object? sender, EventArgs e)
        {
            FrmDanhMuc frm = new FrmDanhMuc();
            frm.ShowDialog();
        }

        // Nút Trả phòng - thanh toán
        private void btnThanhToan_Click(object? sender, EventArgs e)
        {
            FrmTraPhong frm = new FrmTraPhong();
            frm.ShowDialog();
        }

        // Nút Thống kê
        private void btnThongKe_Click(object? sender, EventArgs e)
        {
            FrmThongKe frm = new FrmThongKe();
            frm.ShowDialog();
        }

        // Nút Thoát
        private void btnThoat_Click(object? sender, EventArgs e)
        {
            DialogResult result = MessageBox.Show(
                "Bạn có muốn thoát chương trình không?",
                "Xác nhận",
                MessageBoxButtons.YesNo,
                MessageBoxIcon.Question);

            if (result == DialogResult.Yes)
            {
                Application.Exit();
            }
        }

        // Tiêu đề
        private void lblTitle_Click(object? sender, EventArgs e)
        {
            // Không cần xử lý
        }
    }
}