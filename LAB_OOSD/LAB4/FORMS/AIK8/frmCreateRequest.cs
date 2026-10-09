using Npgsql;
using System;
using System.Data;
using System.Windows.Forms;

namespace AIK08
{
    public partial class frmCreateRequest : Form
    {
        public frmCreateRequest()
        {
            InitializeComponent();
            this.Load += FrmCreateRequest_Load;
            btnSubmit.Click += BtnSubmit_Click;
        }

        private void FrmCreateRequest_Load(object sender, EventArgs e)
        {
            try
            {
                string sql = "SELECT source_name FROM data_sources WHERE is_active = true";
                DataTable dt = DatabaseHelper.ExecuteQuery(sql);

                chkSources.Items.Clear();
                foreach (DataRow row in dt.Rows)
                {
                    chkSources.Items.Add(row["source_name"].ToString(), true);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Không thể tải danh sách nguồn dữ liệu từ CSDL: " + ex.Message, "Cảnh báo", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            }
        }

        private void BtnSubmit_Click(object sender, EventArgs e)
        {
            if (string.IsNullOrWhiteSpace(txtQuery.Text))
            {
                MessageBox.Show("Vui lòng nhập câu hỏi tra cứu!", "Cảnh báo", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            string sql = "INSERT INTO search_sessions (user_query, budget_steps, budget_seconds, status) VALUES (@q, @s, @t, 'RUNNING')";
            var p1 = new NpgsqlParameter("@q", txtQuery.Text);
            var p2 = new NpgsqlParameter("@s", (int)nudSteps.Value);
            var p3 = new NpgsqlParameter("@t", (int)nudSeconds.Value);

            try
            {
                DatabaseHelper.ExecuteNonQuery(sql, p1, p2, p3);
                MessageBox.Show("Khởi tạo phiên tra cứu thành công! Hệ thống đang xử lý.", "Thành công", MessageBoxButtons.OK, MessageBoxIcon.Information);
                txtQuery.Clear();
            }
            catch (Exception ex)
            {
                MessageBox.Show("Lỗi kết nối/lưu dữ liệu: " + ex.Message, "Lỗi", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}