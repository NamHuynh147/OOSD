namespace AIK08
{
    partial class frmAuditLog
    {
        private System.Windows.Forms.DataGridView dgvAuditLogs;
        private System.Windows.Forms.Button btnRefresh;

        private void InitializeComponent()
        {
            this.dgvAuditLogs = new System.Windows.Forms.DataGridView();
            this.btnRefresh = new System.Windows.Forms.Button();

            this.btnRefresh.Text = "Tải lại dữ liệu";
            this.btnRefresh.Location = new System.Drawing.Point(20, 20);

            this.dgvAuditLogs.Location = new System.Drawing.Point(20, 60);
            this.dgvAuditLogs.Size = new System.Drawing.Size(750, 450);
            this.dgvAuditLogs.ReadOnly = true;
            this.dgvAuditLogs.AutoSizeColumnsMode = System.Windows.Forms.DataGridViewAutoSizeColumnsMode.Fill;

            this.Controls.Add(this.btnRefresh);
            this.Controls.Add(this.dgvAuditLogs);
        }
    }
}