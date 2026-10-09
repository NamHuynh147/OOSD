namespace AIK08
{
    partial class frmReport
    {
        private System.Windows.Forms.ComboBox cboSessions;
        private System.Windows.Forms.RichTextBox rtbReport;
        private System.Windows.Forms.DataGridView dgvEvidences;

        private void InitializeComponent()
        {
            this.cboSessions = new System.Windows.Forms.ComboBox();
            this.rtbReport = new System.Windows.Forms.RichTextBox();
            this.dgvEvidences = new System.Windows.Forms.DataGridView();

            this.cboSessions.Location = new System.Drawing.Point(20, 20);
            this.cboSessions.Size = new System.Drawing.Size(400, 30);
            this.cboSessions.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;

            this.rtbReport.Location = new System.Drawing.Point(20, 60);
            this.rtbReport.Size = new System.Drawing.Size(700, 150);
            this.rtbReport.ReadOnly = true;

            this.dgvEvidences.Location = new System.Drawing.Point(20, 230);
            this.dgvEvidences.Size = new System.Drawing.Size(700, 250);
            this.dgvEvidences.ReadOnly = true;
            this.dgvEvidences.AutoSizeColumnsMode = System.Windows.Forms.DataGridViewAutoSizeColumnsMode.Fill;

            this.Controls.Add(this.cboSessions);
            this.Controls.Add(this.rtbReport);
            this.Controls.Add(this.dgvEvidences);
        }
    }
}