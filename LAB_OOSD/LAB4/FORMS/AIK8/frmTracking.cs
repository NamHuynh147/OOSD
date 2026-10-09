using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

using Npgsql;
using System;
using System.Data;
using System.Windows.Forms;

namespace AIK08
{
    public partial class frmTracking : Form
    {
        public frmTracking()
        {
            InitializeComponent();
            this.Load += FrmTracking_Load;
            btnCancel.Click += BtnCancel_Click;
        }

        private void FrmTracking_Load(object sender, EventArgs e)
        {
            LoadRunningSessions();
        }

        private void LoadRunningSessions()
        {
            string sql = "SELECT session_id, user_query FROM search_sessions WHERE status = 'RUNNING'";
            DataTable dt = DatabaseHelper.ExecuteQuery(sql);
            cboRunningSessions.DataSource = dt;
            cboRunningSessions.DisplayMember = "user_query";
            cboRunningSessions.ValueMember = "session_id";
        }

        private void BtnCancel_Click(object sender, EventArgs e)
        {
            if (cboRunningSessions.SelectedValue == null) return;

            int sessionId = (int)cboRunningSessions.SelectedValue;
            // Thực hiện lệnh ngắt phiên và tạo báo cáo một phần
            string sql = "UPDATE search_sessions SET status = 'CANCELLED', final_report = 'Báo cáo một phần: Phiên bị hủy bởi người dùng.' WHERE session_id = @id";

            try
            {
                DatabaseHelper.ExecuteNonQuery(sql, new NpgsqlParameter("@id", sessionId));
                MessageBox.Show("Đã gửi lệnh HỦY PHIÊN thành công!");
                LoadRunningSessions(); // Tải lại danh sách
                lblStatus.Text = "Trạng thái: Đã hủy";
                lstSteps.Items.Add($"[{DateTime.Now:HH:mm:ss}] - HỆ THỐNG ĐÃ DỪNG GỌI TOOL");
            }
            catch (Exception ex)
            {
                MessageBox.Show("Lỗi: " + ex.Message);
            }
        }
    }
}
