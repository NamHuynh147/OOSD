using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System;
using System.Data;
using System.Windows.Forms;

namespace Form_QLKS
{
    public partial class FrmDichVu : Form
    {
        public FrmDichVu()
        {
            InitializeComponent();
        }

        private void FrmDichVu_Load(object sender, EventArgs e)
        {
            LoadDichVu();
        }

        // ==========================================
        // LOAD DANH SÁCH DỊCH VỤ ĐÃ SỬ DỤNG
        // ==========================================
        private void LoadDichVu()
        {
            try
            {
                string sql = @"
                    SELECT
                        SoPhieu AS [Số phiếu],
                        SoPhong AS [Phòng],
                        NgaySuDung AS [Ngày],
                        MaDichVu AS [Dịch vụ],
                        SoLuong AS [Số lượng],
                        DonGia AS [Đơn giá],
                        ThanhTien AS [Thành tiền]
                    FROM SuDungDichVu
                    ORDER BY NgaySuDung DESC";

                DataTable dt = Db.Query(sql);

                dgvDichVu.DataSource = dt;
            }
            catch (Exception ex)
            {
                MessageBox.Show(
                    "Không thể tải danh sách dịch vụ!\n\n" +
                    ex.Message,
                    "Lỗi",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error);
            }
        }

        // ==========================================
        // GHI NHẬN SỬ DỤNG DỊCH VỤ
        // ==========================================
        private void btnGhiNhan_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(txtPhieuLuuTru.Text))
            {
                MessageBox.Show(
                    "Vui lòng nhập phiếu lưu trú!",
                    "Thông báo",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Warning);

                txtPhieuLuuTru.Focus();
                return;
            }

            if (string.IsNullOrWhiteSpace(txtPhong.Text))
            {
                MessageBox.Show(
                    "Vui lòng nhập số phòng!",
                    "Thông báo",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Warning);

                txtPhong.Focus();
                return;
            }

            if (string.IsNullOrWhiteSpace(txtDichVu.Text))
            {
                MessageBox.Show(
                    "Vui lòng nhập dịch vụ!",
                    "Thông báo",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Warning);

                txtDichVu.Focus();
                return;
            }

            if (string.IsNullOrWhiteSpace(txtSoLuong.Text))
            {
                MessageBox.Show(
                    "Vui lòng nhập số lượng!",
                    "Thông báo",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Warning);

                txtSoLuong.Focus();
                return;
            }

            int soLuong;

            if (!int.TryParse(txtSoLuong.Text.Trim(), out soLuong) ||
                soLuong <= 0)
            {
                MessageBox.Show(
                    "Số lượng phải là số nguyên lớn hơn 0!",
                    "Thông báo",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Warning);

                txtSoLuong.Focus();
                return;
            }

            try
            {
                string soPhieu =
                    txtPhieuLuuTru.Text.Trim()
                    .Replace("'", "''");

                string soPhong =
                    txtPhong.Text.Trim()
                    .Replace("'", "''");

                string dichVu =
                    txtDichVu.Text.Trim()
                    .Replace("'", "''");

                DateTime ngaySuDung;

                if (!DateTime.TryParse(
                    txtNgaySuDung.Text.Trim(),
                    out ngaySuDung))
                {
                    MessageBox.Show(
                        "Ngày sử dụng không hợp lệ!",
                        "Thông báo",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Warning);

                    txtNgaySuDung.Focus();
                    return;
                }

                // Nếu bảng dịch vụ của bạn có cột DonGia,
                // có thể lấy đơn giá từ bảng DichVu.
                string sqlGia = $@"
                    SELECT TOP 1 DonGia
                    FROM DichVu
                    WHERE MaDichVu = '{dichVu}'
                       OR TenDichVu = '{dichVu}'";

                DataTable dtGia = Db.Query(sqlGia);

                decimal donGia = 0;

                if (dtGia != null &&
                    dtGia.Rows.Count > 0 &&
                    dtGia.Rows[0]["DonGia"] != DBNull.Value)
                {
                    decimal.TryParse(
                        dtGia.Rows[0]["DonGia"].ToString(),
                        out donGia);
                }

                decimal thanhTien =
                    donGia * soLuong;

                string sql = $@"
                    INSERT INTO SuDungDichVu
                    (
                        SoPhieu,
                        SoPhong,
                        NgaySuDung,
                        MaDichVu,
                        SoLuong,
                        DonGia,
                        ThanhTien
                    )
                    VALUES
                    (
                        '{soPhieu}',
                        '{soPhong}',
                        '{ngaySuDung:yyyy-MM-dd HH:mm:ss}',
                        '{dichVu}',
                        {soLuong},
                        {donGia.ToString(
                            System.Globalization.CultureInfo.InvariantCulture)},
                        {thanhTien.ToString(
                            System.Globalization.CultureInfo.InvariantCulture)}
                    )";

                int result = Db.Execute(sql);

                if (result > 0)
                {
                    MessageBox.Show(
                        "Ghi nhận sử dụng dịch vụ thành công!",
                        "Thông báo",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Information);

                    ClearInput();
                    LoadDichVu();
                }
                else
                {
                    MessageBox.Show(
                        "Không thể ghi nhận dịch vụ!",
                        "Thông báo",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Warning);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(
                    "Lỗi ghi nhận dịch vụ:\n\n" +
                    ex.Message,
                    "Lỗi",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error);
            }
        }

        // ==========================================
        // XÓA Ô NHẬP
        // ==========================================
        private void ClearInput()
        {
            txtPhieuLuuTru.Clear();
            txtPhong.Clear();
            txtDichVu.Clear();
            txtNgaySuDung.Text =
                DateTime.Now.ToString("dd/MM/yyyy");
            txtSoLuong.Clear();

            txtPhieuLuuTru.Focus();
        }

        // ==========================================
        // CLICK DÒNG DỊCH VỤ
        // ==========================================
        private void dgvDichVu_CellClick(
            object sender,
            DataGridViewCellEventArgs e)
        {
            if (e.RowIndex < 0)
                return;

            if (dgvDichVu.Rows[e.RowIndex].Cells.Count < 4)
                return;

            object soPhieu =
                dgvDichVu.Rows[e.RowIndex].Cells[0].Value;

            object phong =
                dgvDichVu.Rows[e.RowIndex].Cells[1].Value;

            object dichVu =
                dgvDichVu.Rows[e.RowIndex].Cells[3].Value;

            if (soPhieu != null)
                txtPhieuLuuTru.Text =
                    soPhieu.ToString();

            if (phong != null)
                txtPhong.Text =
                    phong.ToString();

            if (dichVu != null)
                txtDichVu.Text =
                    dichVu.ToString();
        }
    }
}