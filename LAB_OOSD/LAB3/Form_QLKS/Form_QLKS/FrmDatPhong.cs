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
    public partial class FrmDatPhong : Form
    {
        public FrmDatPhong()
        {
            InitializeComponent();
        }

        // =========================================
        // FORM LOAD
        // =========================================
        private void FrmDatPhong_Load(object sender, EventArgs e)
        {
            LoadPhong();
            LoadPhieuDat();
        }

        // =========================================
        // LOAD DANH SÁCH PHÒNG
        // =========================================
        private void LoadPhong()
        {
            try
            {
                string sql = @"
                    SELECT
                        SoPhong AS [Phòng],
                        KhuVuc AS [Khu],
                        SoNguoiToiDa AS [Sức chứa],
                        DonGiaNgay AS [Đơn giá]
                    FROM Phong
                    ORDER BY SoPhong";

                DataTable dt = Db.Query(sql);

                dgvPhong.DataSource = dt;
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

        // =========================================
        // LOAD PHIẾU ĐẶT PHÒNG
        // =========================================
        private void LoadPhieuDat()
        {
            try
            {
                string sql = @"
                    SELECT
                        SoPhieuDat AS [Số phiếu],
                        Khach AS [Khách],
                        NgayNhan AS [Ngày nhận],
                        NgayTraDuKien AS [Ngày trả dự kiến],
                        TienCoc AS [Cọc],
                        KenhDat AS [Kênh],
                        TrangThai AS [Trạng thái]
                    FROM PhieuDatPhong
                    ORDER BY NgayNhan DESC";

                DataTable dt = Db.Query(sql);

                dgvPhieuDat.DataSource = dt;
            }
            catch (Exception ex)
            {
                MessageBox.Show(
                    "Không thể tải danh sách phiếu đặt!\n\n" + ex.Message,
                    "Lỗi",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error);
            }
        }

        // =========================================
        // CLICK CHỌN PHÒNG
        // =========================================
        private void dgvPhong_CellClick(
            object sender,
            DataGridViewCellEventArgs e)
        {
            if (e.RowIndex < 0)
                return;

            if (dgvPhong.Rows[e.RowIndex].Cells.Count < 4)
                return;

            object soPhong =
                dgvPhong.Rows[e.RowIndex].Cells[0].Value;

            object sucChua =
                dgvPhong.Rows[e.RowIndex].Cells[2].Value;

            object donGia =
                dgvPhong.Rows[e.RowIndex].Cells[3].Value;

            if (soPhong == null)
                return;

            // Kiểm tra phòng đã được chọn chưa
            foreach (DataGridViewRow row in dgvPhongChon.Rows)
            {
                if (row.IsNewRow)
                    continue;

                if (row.Cells[0].Value != null &&
                    row.Cells[0].Value.ToString() ==
                    soPhong.ToString())
                {
                    MessageBox.Show(
                        "Phòng này đã được chọn!",
                        "Thông báo",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Information);

                    return;
                }
            }

            dgvPhongChon.Rows.Add(
                soPhong.ToString(),
                sucChua != null ? sucChua.ToString() : "0",
                donGia != null ? donGia.ToString() : "0");
        }

        // =========================================
        // CLICK LẬP PHIẾU ĐẶT
        // =========================================
        private void btnLapPhieuDat_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(txtSoPhieuDat.Text))
            {
                MessageBox.Show(
                    "Vui lòng nhập số phiếu đặt!",
                    "Thông báo",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Warning);

                txtSoPhieuDat.Focus();
                return;
            }

            if (string.IsNullOrWhiteSpace(txtKhach.Text))
            {
                MessageBox.Show(
                    "Vui lòng nhập tên khách!",
                    "Thông báo",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Warning);

                txtKhach.Focus();
                return;
            }

            if (dgvPhongChon.Rows.Count == 0 ||
                (dgvPhongChon.Rows.Count == 1 &&
                 dgvPhongChon.Rows[0].IsNewRow))
            {
                MessageBox.Show(
                    "Vui lòng chọn ít nhất một phòng!",
                    "Thông báo",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Warning);

                return;
            }

            try
            {
                string soPhieu =
                    txtSoPhieuDat.Text.Trim().Replace("'", "''");

                string khach =
                    txtKhach.Text.Trim().Replace("'", "''");

                string kenh =
                    txtKenhDat.Text.Trim().Replace("'", "''");

                decimal tienCoc = 0;

                decimal.TryParse(
                    txtTienCoc.Text.Trim(),
                    out tienCoc);

                string sql = $@"
                    INSERT INTO PhieuDatPhong
                    (
                        SoPhieuDat,
                        Khach,
                        NgayNhan,
                        NgayTraDuKien,
                        TienCoc,
                        KenhDat,
                        TrangThai
                    )
                    VALUES
                    (
                        '{soPhieu}',
                        '{khach}',
                        GETDATE(),
                        DATEADD(DAY, 1, GETDATE()),
                        {tienCoc},
                        '{kenh}',
                        N'Đã đặt'
                    )";

                int result = Db.Execute(sql);

                if (result > 0)
                {
                    MessageBox.Show(
                        "Lập phiếu đặt phòng thành công!",
                        "Thông báo",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Information);

                    ClearInput();
                    LoadPhieuDat();
                }
                else
                {
                    MessageBox.Show(
                        "Không thể lập phiếu đặt phòng!",
                        "Thông báo",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Warning);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(
                    "Lỗi khi lập phiếu đặt phòng:\n\n" +
                    ex.Message,
                    "Lỗi",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error);
            }
        }

        // =========================================
        // XÓA DỮ LIỆU NHẬP
        // =========================================
        private void ClearInput()
        {
            txtSoPhieuDat.Clear();
            txtKhach.Clear();
            txtKenhDat.Clear();
            txtTienCoc.Clear();

            dgvPhongChon.Rows.Clear();

            txtSoPhieuDat.Focus();
        }

        // =========================================
        // CLICK PHIẾU ĐẶT
        // =========================================
        private void dgvPhieuDat_CellClick(
            object sender,
            DataGridViewCellEventArgs e)
        {
            if (e.RowIndex < 0)
                return;

            if (dgvPhieuDat.Rows[e.RowIndex].Cells.Count < 2)
                return;

            object soPhieu =
                dgvPhieuDat.Rows[e.RowIndex].Cells[0].Value;

            object khach =
                dgvPhieuDat.Rows[e.RowIndex].Cells[1].Value;

            if (soPhieu != null)
                txtSoPhieuDat.Text = soPhieu.ToString();

            if (khach != null)
                txtKhach.Text = khach.ToString();
        }

        private void dgvPhieuDat_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {

        }

        private void txtSoPhieuDat_TextChanged(object sender, EventArgs e)
        {

        }
    }
}