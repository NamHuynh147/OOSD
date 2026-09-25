using System;
using System.Data;
using System.Windows.Forms;

namespace Form_QLKS
{
    public partial class FrmPhongTienNghi : Form
    {
        public FrmPhongTienNghi()
        {
            InitializeComponent();
        }

        private void FrmPhongTienNghi_Load(object? sender, EventArgs e)
        {
            LoadData();
        }

        private void LoadData()
        {
            try
            {
                string sql = @"
                    SELECT
                        p.SoPhong AS Phong,
                        k.TenKhuVuc AS Khu,
                        p.SoNguoiToiDa AS SucChua,
                        p.DonGiaNgay AS DonGia,
                        p.TrangThai AS TrangThai
                    FROM Phong p 
                    LEFT JOIN KhuVuc k
                        ON p.MaKhuVuc = k.MaKhuVuc
                    ORDER BY p.SoPhong";

                DataTable dt = Db.GetData(sql);

                dgvPhong.DataSource = dt;

                // Đặt lại tên hiển thị cho các cột
                if (dgvPhong.Columns["Phong"] != null)
                    dgvPhong.Columns["Phong"].HeaderText = "Phòng";

                if (dgvPhong.Columns["Khu"] != null)
                    dgvPhong.Columns["Khu"].HeaderText = "Khu";

                if (dgvPhong.Columns["SucChua"] != null)
                    dgvPhong.Columns["SucChua"].HeaderText = "Sức chứa";

                if (dgvPhong.Columns["DonGia"] != null)
                    dgvPhong.Columns["DonGia"].HeaderText = "Đơn giá";

                if (dgvPhong.Columns["TrangThai"] != null)
                    dgvPhong.Columns["TrangThai"].HeaderText = "Trạng thái";
            }
            catch (Exception ex)
            {
                MessageBox.Show(
                    "Lỗi tải danh sách phòng:\n" + ex.Message,
                    "Lỗi",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error);
            }
        }

        private void btnLapPhieu_Click(object? sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(txtPhieuLapDat.Text))
            {
                MessageBox.Show(
                    "Vui lòng nhập số phiếu lắp đặt!",
                    "Thông báo",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Warning);

                txtPhieuLapDat.Focus();
                return;
            }

            if (string.IsNullOrWhiteSpace(txtTienNghi.Text))
            {
                MessageBox.Show(
                    "Vui lòng nhập mã tiện nghi!",
                    "Thông báo",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Warning);

                txtTienNghi.Focus();
                return;
            }

            if (string.IsNullOrWhiteSpace(txtPhongBottom.Text))
            {
                MessageBox.Show(
                    "Vui lòng nhập số phòng!",
                    "Thông báo",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Warning);

                txtPhongBottom.Focus();
                return;
            }

            try
            {
                string sql = @"
            INSERT INTO PhieuLapDat
            (
                SoPhieuLapDat,
                MaTienNghi,
                SoPhong,
                NgayLap,
                TinhTrang
            )
            VALUES
            (
                @SoPhieuLapDat,
                @MaTienNghi,
                @SoPhong,
                @NgayLap,
                @TinhTrang
            )";

                var parameters = new[]
                {
            new Microsoft.Data.SqlClient.SqlParameter(
                "@SoPhieuLapDat",
                txtPhieuLapDat.Text.Trim()),

            new Microsoft.Data.SqlClient.SqlParameter(
                "@MaTienNghi",
                txtTienNghi.Text.Trim()),

            new Microsoft.Data.SqlClient.SqlParameter(
                "@SoPhong",
                txtPhongBottom.Text.Trim()),

            new Microsoft.Data.SqlClient.SqlParameter(
                "@NgayLap",
                DateTime.Now),

            new Microsoft.Data.SqlClient.SqlParameter(
                "@TinhTrang",
                txtTinhTrang.Text.Trim())
        };

                int rows = Db.Execute(sql, parameters);

                if (rows > 0)
                {
                    MessageBox.Show(
                        "Lập phiếu lắp đặt thành công!",
                        "Thông báo",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Information);

                    ClearInput();
                    LoadData();
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(
                    "Lỗi lập phiếu:\n" + ex.Message,
                    "Lỗi",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error);
            }
        }

        private void ClearInput()
        {
            txtPhieuLapDat.Clear();
            txtTienNghi.Clear();
            txtPhongBottom.Clear();
            txtTinhTrang.Clear();

            txtPhieuLapDat.Focus();
        }

        private string GetConnectionString()
        {
            return @"Server=MSI\MSSQLSERVER03;
                     Database=QuanLyKhachSan;
                     Trusted_Connection=True;
                     TrustServerCertificate=True;";
        }

        // Add this method to handle the DataGridView CellClick event
        private void dgvPhong_CellClick(object? sender, DataGridViewCellEventArgs e)
        {
            // Example: Select the clicked row and populate the top input fields with its data
            if (e.RowIndex >= 0 && dgvPhong.Rows.Count > e.RowIndex)
            {
                DataGridViewRow row = dgvPhong.Rows[e.RowIndex];
                txtSoPhong.Text = row.Cells["colPhong"].Value?.ToString() ?? string.Empty;
                txtKhuVuc.Text = row.Cells["colKhu"].Value?.ToString() ?? string.Empty;
                txtSoNguoiToiDa.Text = row.Cells["colSucChua"].Value?.ToString() ?? string.Empty;
                txtDonGiaNgay.Text = row.Cells["colDonGia"].Value?.ToString() ?? string.Empty;
            }
        }
    }
}