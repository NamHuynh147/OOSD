using System;
using System.Windows.Forms;
using Microsoft.Data.SqlClient;

namespace Form_QLKS
{
    public partial class FrmDanhMuc : Form
    {
        public FrmDanhMuc()
        {
            InitializeComponent();
            LoadData();
        }

        private void LoadData()
        {
            dgvKhuVuc.DataSource = Db.Query(
                "SELECT MaKhuVuc AS [Mã Khu], " +
                "TenKhuVuc AS [Tên Khu Vực] " +
                "FROM KhuVuc"
            );

            dgvDichVu.DataSource = Db.Query(
                "SELECT MaDV AS [Mã DV], " +
                "TenDV AS [Tên Dịch Vụ], " +
                "DonViTinh AS [ĐVT], " +
                "DonGia AS [Đơn Giá] " +
                "FROM DichVu"
            );

            dgvLoaiTN.DataSource = Db.Query(
                "SELECT MaLoaiTN AS [Mã Loại], " +
                "TenLoaiTN AS [Tên Loại Tiện Nghi] " +
                "FROM LoaiTienNghi"
            );
        }

        private void btnThemKhu_Click(object sender, EventArgs e)
        {
            string sql =
                "INSERT INTO KhuVuc(MaKhuVuc, TenKhuVuc) " +
                "VALUES(@Ma, @Ten)";

            int result = Db.Execute(
                sql,
                new SqlParameter("@Ma", txtMaKhu.Text),
                new SqlParameter("@Ten", txtTenKhu.Text)
            );

            if (result > 0)
            {
                MessageBox.Show("Thêm khu vực thành công!");
                LoadData();
            }
        }

        private void btnThemDV_Click(object sender, EventArgs e)
        {
            if (!decimal.TryParse(
                    txtDonGia.Text,
                    out decimal donGia))
            {
                MessageBox.Show("Đơn giá không hợp lệ!");
                return;
            }

            string sql =
                "INSERT INTO DichVu " +
                "(MaDV, TenDV, DonViTinh, DonGia) " +
                "VALUES(@Ma, @Ten, @DVT, @Gia)";

            SqlParameter[] parameters =
            {
                new SqlParameter("@Ma", txtMaDV.Text),
                new SqlParameter("@Ten", txtTenDV.Text),
                new SqlParameter("@DVT", txtDVT.Text),
                new SqlParameter("@Gia", donGia)
            };

            int result = Db.Execute(sql, parameters);

            if (result > 0)
            {
                MessageBox.Show("Thêm dịch vụ thành công!");
                LoadData();
            }
        }
    }
}
