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
    public partial class frmConfig : Form
    {
        public frmConfig()
        {
            InitializeComponent();
            this.Load += FrmConfig_Load;
            btnSave.Click += BtnSave_Click;
        }

        private void FrmConfig_Load(object sender, EventArgs e)
        {
            LoadConfig();
            LoadSources();
        }

        private void LoadConfig()
        {
            string sql = "SELECT default_budget_steps, default_budget_seconds FROM system_configs LIMIT 1";
            DataTable dt = DatabaseHelper.ExecuteQuery(sql);
            if (dt.Rows.Count > 0)
            {
                nudDefSteps.Value = Convert.ToDecimal(dt.Rows[0]["default_budget_steps"]);
                nudDefSecs.Value = Convert.ToDecimal(dt.Rows[0]["default_budget_seconds"]);
            }
        }

        private void LoadSources()
        {
            string sql = "SELECT source_name as Nguồn, source_type as Loại, endpoint_url as URL FROM data_sources";
            dgvSources.DataSource = DatabaseHelper.ExecuteQuery(sql);
        }

        private void BtnSave_Click(object sender, EventArgs e)
        {
            string sql = "UPDATE system_configs SET default_budget_steps = @s, default_budget_seconds = @t";
            try
            {
                DatabaseHelper.ExecuteNonQuery(sql,
                    new NpgsqlParameter("@s", (int)nudDefSteps.Value),
                    new NpgsqlParameter("@t", (int)nudDefSecs.Value));
                MessageBox.Show("Cập nhật cấu hình hệ thống thành công!");
            }
            catch (Exception ex)
            {
                MessageBox.Show("Lỗi: " + ex.Message);
            }
        }
    }
}