using Form_QLKS;
using System;
using System.Data;
using System.Windows.Forms;

namespace Form_QLKS
{
    public partial class FrmTraPhong : Form
    {
        public FrmTraPhong()
        {
            InitializeComponent();
        }

        // =====================================================
        // FORM LOAD
        // =====================================================
        private void FrmTraPhong_Load(object sender, EventArgs e)
        {
            LoadPhong();
            LoadTienNghi();
            LoadHoaDon();
        }

        // =====================================================
        // LOAD PHÒNG ĐANG Ở
        // =====================================================
        private void LoadPhong()
        {
            try
            {
                string sql = @"
                    SELECT
                        SoPhong AS [Phòng],
                        DonGiaNgay AS [Đơn giá/ngày]
                    FROM Phong
                    WHERE TrangThai = N'Đang ở'
                       OR TrangThai = N'Đang sử dụng'
                    ORDER BY SoPhong";

                DataTable dt = Db.Query(sql);

                dgvPhong.DataSource = dt;
            }
            catch (Exception ex)
            {
                MessageBox.Show(
                    "Không thể tải danh sách phòng!\n\n" +
                    ex.Message,
                    "Lỗi",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error);
            }
        }

        // =====================================================
        // LOAD TIỆN NGHI
        // =====================================================
        private void LoadTienNghi()
        {
            try
            {
                string sql = @"
                    SELECT
                        MaTienNghi AS [Tiện nghi],
                        Loai AS [Loại],
                        TinhTrang AS [Tình trạng]
                    FROM TienNghi
                    ORDER BY MaTienNghi";

                DataTable dt = Db.Query(sql);

                dgvTienNghi.DataSource = dt;
            }
            catch (Exception ex)
            {
                MessageBox.Show(
                    "Không thể tải danh sách tiện nghi!\n\n" +
                    ex.Message,
                    "Lỗi",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error);
            }
        }

        // =====================================================
        // LOAD DANH SÁCH ĐỀN BÙ
        // =====================================================
        private void LoadDenBu()
        {
            try
            {
                string sql = @"
                    SELECT
                        MaTienNghi AS [Tiện nghi đền bù],
                        MucDo AS [Mức độ],
                        SoTien AS [Số tiền]
                    FROM DenBu
                    WHERE SoPhieu = '" +
                    txtPhieuDangO.Text.Trim().Replace("'", "''") +
                    @"'
                    ORDER BY MaTienNghi";

                DataTable dt = Db.Query(sql);

                dgvDenBu.DataSource = dt;
            }
            catch (Exception ex)
            {
                MessageBox.Show(
                    "Không thể tải danh sách đền bù!\n\n" +
                    ex.Message,
                    "Lỗi",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error);
            }
        }

        // =====================================================
        // LOAD HÓA ĐƠN
        // =====================================================
        private void LoadHoaDon()
        {
            try
            {
                string sql = @"
                    SELECT
                        SoHoaDon AS [Hóa đơn],
                        SoPhieuDat AS [Phiếu đặt],
                        TienPhong AS [Tiền phòng],
                        TienDichVu AS [Tiền dịch vụ],
                        TongTien AS [Tổng tiền],
                        TrangThai AS [Trạng thái]
                    FROM HoaDon
                    ORDER BY SoHoaDon DESC";

                DataTable dt = Db.Query(sql);

                dgvHoaDon.DataSource = dt;
            }
            catch (Exception ex)
            {
                MessageBox.Show(
                    "Không thể tải danh sách hóa đơn!\n\n" +
                    ex.Message,
                    "Lỗi",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error);
            }
        }

        // =====================================================
        // LẬP PHIẾU ĐỀN BÙ
        // =====================================================
        private void btnLapPhieuDenBu_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(txtPhieuDenBu.Text))
            {
                MessageBox.Show(
                    "Vui lòng nhập số phiếu đền bù!",
                    "Thông báo",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Warning);

                txtPhieuDenBu.Focus();
                return;
            }

            if (string.IsNullOrWhiteSpace(txtMucDo.Text))
            {
                MessageBox.Show(
                    "Vui lòng nhập mức độ đền bù!",
                    "Thông báo",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Warning);

                txtMucDo.Focus();
                return;
            }

            if (string.IsNullOrWhiteSpace(txtSoTienDenBu.Text))
            {
                MessageBox.Show(
                    "Vui lòng nhập số tiền đền bù!",
                    "Thông báo",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Warning);

                txtSoTienDenBu.Focus();
                return;
            }

            decimal soTien;

            if (!decimal.TryParse(
                txtSoTienDenBu.Text.Trim(),
                out soTien) ||
                soTien < 0)
            {
                MessageBox.Show(
                    "Số tiền đền bù không hợp lệ!",
                    "Thông báo",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Warning);

                txtSoTienDenBu.Focus();
                return;
            }

            try
            {
                string soPhieu =
                    txtPhieuDenBu.Text.Trim()
                    .Replace("'", "''");

                string mucDo =
                    txtMucDo.Text.Trim()
                    .Replace("'", "''");

                string sql = $@"
                    INSERT INTO DenBu
                    (
                        SoPhieu,
                        MucDo,
                        SoTien
                    )
                    VALUES
                    (
                        '{soPhieu}',
                        '{mucDo}',
                        {soTien.ToString(
                            System.Globalization.CultureInfo.InvariantCulture)}
                    )";

                int result = Db.Execute(sql);

                if (result > 0)
                {
                    MessageBox.Show(
                        "Lập phiếu đền bù thành công!",
                        "Thông báo",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Information);

                    LoadDenBu();
                }
                else
                {
                    MessageBox.Show(
                        "Không thể lập phiếu đền bù!",
                        "Thông báo",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Warning);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(
                    "Lỗi lập phiếu đền bù:\n\n" +
                    ex.Message,
                    "Lỗi",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error);
            }
        }

        // =====================================================
        // LẬP HÓA ĐƠN
        // =====================================================
        private void btnLapHoaDon_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(txtSoHoaDon.Text))
            {
                MessageBox.Show(
                    "Vui lòng nhập số hóa đơn!",
                    "Thông báo",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Warning);

                txtSoHoaDon.Focus();
                return;
            }

            int soNgay;

            if (!int.TryParse(
                txtSoNgayTinhTien.Text.Trim(),
                out soNgay) ||
                soNgay <= 0)
            {
                MessageBox.Show(
                    "Số ngày tính tiền không hợp lệ!",
                    "Thông báo",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Warning);

                txtSoNgayTinhTien.Focus();
                return;
            }

            try
            {
                string soHoaDon =
                    txtSoHoaDon.Text.Trim()
                    .Replace("'", "''");

                string phieu =
                    txtPhieuDangO.Text.Trim()
                    .Replace("'", "''");

                // Tính tiền phòng
                decimal tienPhong = 0;

                string sqlPhong = $@"
                    SELECT ISNULL(SUM(DonGiaNgay), 0)
                    FROM Phong
                    WHERE SoPhong IN
                    (
                        SELECT SoPhong
                        FROM PhieuDatPhong
                        WHERE SoPhieuDat = '{phieu}'
                    )";

                DataTable dtPhong = Db.Query(sqlPhong);

                if (dtPhong.Rows.Count > 0 &&
                    dtPhong.Rows[0][0] != DBNull.Value)
                {
                    decimal.TryParse(
                        dtPhong.Rows[0][0].ToString(),
                        out tienPhong);
                }

                tienPhong *= soNgay;

                // Tính tiền dịch vụ
                decimal tienDichVu = 0;

                string sqlDichVu = $@"
                    SELECT ISNULL(SUM(ThanhTien), 0)
                    FROM SuDungDichVu
                    WHERE SoPhieu = '{phieu}'";

                DataTable dtDichVu = Db.Query(sqlDichVu);

                if (dtDichVu.Rows.Count > 0 &&
                    dtDichVu.Rows[0][0] != DBNull.Value)
                {
                    decimal.TryParse(
                        dtDichVu.Rows[0][0].ToString(),
                        out tienDichVu);
                }

                // Tính tiền đền bù
                decimal tienDenBu = 0;

                string sqlDenBu = $@"
                    SELECT ISNULL(SUM(SoTien), 0)
                    FROM DenBu
                    WHERE SoPhieu = '{phieu}'";

                DataTable dtDenBu = Db.Query(sqlDenBu);

                if (dtDenBu.Rows.Count > 0 &&
                    dtDenBu.Rows[0][0] != DBNull.Value)
                {
                    decimal.TryParse(
                        dtDenBu.Rows[0][0].ToString(),
                        out tienDenBu);
                }

                decimal tongTien =
                    tienPhong +
                    tienDichVu +
                    tienDenBu;

                string sql = $@"
                    INSERT INTO HoaDon
                    (
                        SoHoaDon,
                        SoPhieuDat,
                        TienPhong,
                        TienDichVu,
                        TongTien,
                        TrangThai
                    )
                    VALUES
                    (
                        '{soHoaDon}',
                        '{phieu}',
                        {tienPhong.ToString(
                            System.Globalization.CultureInfo.InvariantCulture)},
                        {tienDichVu.ToString(
                            System.Globalization.CultureInfo.InvariantCulture)},
                        {tongTien.ToString(
                            System.Globalization.CultureInfo.InvariantCulture)},
                        N'Chưa thanh toán'
                    )";

                int result = Db.Execute(sql);

                if (result > 0)
                {
                    MessageBox.Show(
                        "Lập hóa đơn thành công!\n\n" +
                        "Tiền phòng: " +
                        tienPhong.ToString("N0") +
                        "\nTiền dịch vụ: " +
                        tienDichVu.ToString("N0") +
                        "\nTiền đền bù: " +
                        tienDenBu.ToString("N0") +
                        "\nTổng tiền: " +
                        tongTien.ToString("N0"),
                        "Thông báo",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Information);

                    LoadHoaDon();

                    txtSoTienThanhToan.Text =
                        tongTien.ToString("0");
                }
                else
                {
                    MessageBox.Show(
                        "Không thể lập hóa đơn!",
                        "Thông báo",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Warning);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(
                    "Lỗi lập hóa đơn:\n\n" +
                    ex.Message,
                    "Lỗi",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error);
            }
        }

        // =====================================================
        // THANH TOÁN
        // =====================================================
        private void btnThanhToan_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(txtSoTienThanhToan.Text))
            {
                MessageBox.Show(
                    "Vui lòng nhập số tiền thanh toán!",
                    "Thông báo",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Warning);

                txtSoTienThanhToan.Focus();
                return;
            }

            decimal soTien;

            if (!decimal.TryParse(
                txtSoTienThanhToan.Text.Trim(),
                out soTien) ||
                soTien < 0)
            {
                MessageBox.Show(
                    "Số tiền thanh toán không hợp lệ!",
                    "Thông báo",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Warning);

                return;
            }

            try
            {
                string soHoaDon = "";

                if (dgvHoaDon.CurrentRow != null &&
                    dgvHoaDon.CurrentRow.Cells.Count > 0 &&
                    dgvHoaDon.CurrentRow.Cells[0].Value != null)
                {
                    soHoaDon =
                        dgvHoaDon.CurrentRow.Cells[0]
                        .Value.ToString();
                }

                if (string.IsNullOrWhiteSpace(soHoaDon))
                {
                    MessageBox.Show(
                        "Vui lòng chọn hóa đơn cần thanh toán!",
                        "Thông báo",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Warning);

                    return;
                }

                soHoaDon =
                    soHoaDon.Replace("'", "''");

                string hinhThuc =
                    txtHinhThuc.Text.Trim()
                    .Replace("'", "''");

                string sql = $@"
                    INSERT INTO ThanhToan
                    (
                        SoHoaDon,
                        HinhThuc,
                        SoTien,
                        NgayThanhToan
                    )
                    VALUES
                    (
                        '{soHoaDon}',
                        '{hinhThuc}',
                        {soTien.ToString(
                            System.Globalization.CultureInfo.InvariantCulture)},
                        GETDATE()
                    )";

                int result = Db.Execute(sql);

                if (result > 0)
                {
                    string sqlUpdate = $@"
                        UPDATE HoaDon
                        SET TrangThai = N'Đã thanh toán'
                        WHERE SoHoaDon = '{soHoaDon}'";

                    Db.Execute(sqlUpdate);

                    MessageBox.Show(
                        "Thanh toán thành công!",
                        "Thông báo",
                        MessageBoxButtons.OK,
                        MessageBoxIcon.Information);

                    LoadHoaDon();
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(
                    "Lỗi thanh toán:\n\n" +
                    ex.Message,
                    "Lỗi",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error);
            }
        }

        // =====================================================
        // HOÀN TẤT TRẢ PHÒNG
        // =====================================================
        private void btnHoanTatTraPhong_Click(
            object sender,
            EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(txtPhieuDangO.Text))
            {
                MessageBox.Show(
                    "Vui lòng nhập phiếu đang ở!",
                    "Thông báo",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Warning);

                return;
            }

            try
            {
                string phieu =
                    txtPhieuDangO.Text.Trim()
                    .Replace("'", "''");

                string sql = $@"
                    UPDATE PhieuDatPhong
                    SET TrangThai = N'Đã trả phòng'
                    WHERE SoPhieuDat = '{phieu}'";

                Db.Execute(sql);

                MessageBox.Show(
                    "Hoàn tất trả phòng thành công!",
                    "Thông báo",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Information);

                LoadPhong();
                LoadHoaDon();
            }
            catch (Exception ex)
            {
                MessageBox.Show(
                    "Lỗi hoàn tất trả phòng:\n\n" +
                    ex.Message,
                    "Lỗi",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error);
            }
        }

        // =====================================================
        // CLICK CHỌN HÓA ĐƠN
        // =====================================================
        private void dgvHoaDon_CellClick(
            object sender,
            DataGridViewCellEventArgs e)
        {
            if (e.RowIndex < 0)
                return;

            if (dgvHoaDon.Rows[e.RowIndex].Cells.Count < 5)
                return;

            object tongTien =
                dgvHoaDon.Rows[e.RowIndex]
                .Cells[4].Value;

            if (tongTien != null)
            {
                txtSoTienThanhToan.Text =
                    tongTien.ToString();
            }
        }

        // =====================================================
        // CLICK CHỌN PHIẾU ĐỀN BÙ
        // =====================================================
        private void dgvDenBu_CellClick(
            object sender,
            DataGridViewCellEventArgs e)
        {
            if (e.RowIndex < 0)
                return;

            if (dgvDenBu.Rows[e.RowIndex].Cells.Count < 3)
                return;

            object mucDo =
                dgvDenBu.Rows[e.RowIndex]
                .Cells[1].Value;

            object soTien =
                dgvDenBu.Rows[e.RowIndex]
                .Cells[2].Value;

            if (mucDo != null)
                txtMucDo.Text =
                    mucDo.ToString();

            if (soTien != null)
                txtSoTienDenBu.Text =
                    soTien.ToString();
        }
    }
}