using Form_QLKS;
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

        // ==============================
        // LOAD FORM
        // ==============================
        private void FrmPhongTienNghi_Load(object sender, EventArgs e)
        {
            LoadData();
        }

        // ==============================
        // LOAD DANH SÁCH PHÒNG
        // ==============================
        private void LoadData()
        {
            try
            {
                string sql = @"
                    SELECT
                        SoPhong AS [Phòng],
                        KhuVuc AS [Khu],
                        SoNguoiToiDa AS [Sức chứa],
                        DonGiaNgay AS [Đơn giá],
                        TrangThai AS [Trạng thái]
                    FROM Phong
                    ORDER BY SoPhong";

                DataTable dt = Db.Query(sql);

                dgvPhong.DataSource = null;
                dgvPhong.DataSource = dt;

                // Không cho DataGridView tự tạo lại cột
                // vì Designer đã tạo sẵn 5 cột.
                if (dgvPhong.Columns.Count >= 5)
                {
                    dgvPhong.Columns[0].HeaderText = "Phòng";
                    dgvPhong.Columns[1].HeaderText = "Khu";
                    dgvPhong.Columns[2].HeaderText = "Sức chứa";
                    dgvPhong.Columns[3].HeaderText = "Đơn giá";
                    dgvPhong.Columns[4].HeaderText = "Trạng thái";
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(
                    "Không thể tải danh sách phòng!\n\n" + ex.Message,
                    "Lỗi",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error);
            }
        }

        // ==============================
        // CLICK LẬP PHIẾU
        // ==============================
        private void btnLapPhieu_Click(object sender, EventArgs e)
        {
            // Kiểm tra dữ liệu
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
                string soPhieu = txtPhieuLapDat.Text.Trim();
                string maTienNghi = txtTienNghi.Text.Trim();
                string soPhong = txtPhongBottom.Text.Trim();
                string tinhTrang = txtTinhTrang.Text.Trim();

                // Tránh lỗi khi dữ liệu có dấu '
                soPhieu = soPhieu.Replace("'", "''");
                maTienNghi = maTienNghi.Replace("'", "''");
                soPhong = soPhong.Replace("'", "''");
                tinhTrang = tinhTrang.Replace("'", "''");

                string sql = $@"
                    INSERT INTO PhieuLapDat
                    (
                        SoPhieuLapDat,
                        MaTienNghi,
                        SoPhong,
                        TinhTrang
                    )
                    VALUES
                    (
                        '{soPhieu}',
                        '{maTienNghi}',
                        '{soPhong}',
                        '{tinhTrang}'
                    )";

                int result = Db.Execute(sql);

                if (result > 0)
                {
                    MessageBox.Show(
                        "Lập phiếu lắp đặt thành công!",
                        "Thông báo",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Information);

                    ClearInput();

                    LoadData();
                }
                else
                {
                    MessageBox.Show(
                        "Không thể lập phiếu lắp đặt!",
                        "Thông báo",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Warning);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(
                    "Lỗi khi lập phiếu lắp đặt:\n\n" + ex.Message,
                    "Lỗi",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error);
            }
        }

        // ==============================
        // XÓA DỮ LIỆU NHẬP
        // ==============================
        private void ClearInput()
        {
            txtPhieuLapDat.Clear();
            txtTienNghi.Clear();
            txtPhongBottom.Clear();
            txtTinhTrang.Clear();

            txtPhieuLapDat.Focus();
        }

        // ==============================
        // CLICK VÀO PHÒNG TRÊN GRID
        // ==============================
        private void dgvPhong_CellClick(object sender, DataGridViewCellEventArgs e)
        {
            if (e.RowIndex < 0)
                return;

            if (dgvPhong.Rows[e.RowIndex].Cells.Count < 1)
                return;

            object value = dgvPhong.Rows[e.RowIndex].Cells[0].Value;

            if (value != null)
            {
                txtPhongBottom.Text = value.ToString();
            }
        }
    }
}