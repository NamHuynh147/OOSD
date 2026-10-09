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
    public partial class frmReport : Form
    {
        public frmReport()
        {
            InitializeComponent();
            this.Load += FrmReport_Load;
            cboSessions.SelectedIndexChanged += CboSessions_SelectedIndexChanged;
        }

        private void FrmReport_Load(object sender, EventArgs e)
        {
            string sql = "SELECT session_id, user_query FROM search_sessions WHERE status IN ('COMPLETED', 'CANCELLED')";
            DataTable dt = DatabaseHelper.ExecuteQuery(sql);
            cboSessions.DataSource = dt;
            cboSessions.DisplayMember = "user_query";
            cboSessions.ValueMember = "session_id";
        }

        private void CboSessions_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (cboSessions.SelectedValue == null || !(cboSessions.SelectedValue is int sessionId)) return;

            // Lấy báo cáo
            string sqlReport = "SELECT final_report FROM search_sessions WHERE session_id = @id";
            DataTable dtRep = DatabaseHelper.ExecuteQuery(sqlReport, new NpgsqlParameter("@id", sessionId));
            if (dtRep.Rows.Count > 0)
                rtbReport.Text = dtRep.Rows[0]["final_report"].ToString();

            // Lấy bằng chứng
            string sqlEv = "SELECT source_name as Nguồn, location as VịTrí, content_extracted as NộiDung FROM evidences WHERE session_id = @id";
            DataTable dtEv = DatabaseHelper.ExecuteQuery(sqlEv, new NpgsqlParameter("@id", sessionId));
            dgvEvidences.DataSource = dtEv;
        }
    }
}