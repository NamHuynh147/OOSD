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
using System.Drawing;
using System.Windows.Forms;

namespace AIK08
{
    public partial class frmAuditLog : Form
    {
        public frmAuditLog()
        {
            InitializeComponent();
            btnRefresh.Click += (s, e) => LoadData();
            dgvAuditLogs.CellFormatting += DgvAuditLogs_CellFormatting;
            this.Load += (s, e) => LoadData();
        }

        private void LoadData()
        {
            string sql = "SELECT log_id, session_id, event_type, description, created_at FROM audit_logs ORDER BY created_at DESC";
            dgvAuditLogs.DataSource = DatabaseHelper.ExecuteQuery(sql);
        }

        private void DgvAuditLogs_CellFormatting(object sender, DataGridViewCellFormattingEventArgs e)
        {
            if (dgvAuditLogs.Columns[e.ColumnIndex].Name == "event_type" && e.Value != null)
            {
                string eventType = e.Value.ToString();
                if (eventType == "INJECTION_DETECTED")
                {
                    dgvAuditLogs.Rows[e.RowIndex].DefaultCellStyle.BackColor = Color.LightCoral;
                }
                else if (eventType == "BLOCKED")
                {
                    dgvAuditLogs.Rows[e.RowIndex].DefaultCellStyle.BackColor = Color.LightYellow;
                }
            }
        }
    }
}