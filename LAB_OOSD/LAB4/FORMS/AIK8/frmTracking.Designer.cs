namespace AIK08
{
    partial class frmTracking
    {
        private System.Windows.Forms.Label lblStatus;
        private System.Windows.Forms.ListBox lstSteps;
        private System.Windows.Forms.Button btnCancel;
        private System.Windows.Forms.ComboBox cboRunningSessions;

        private void InitializeComponent()
        {
            this.lblStatus = new System.Windows.Forms.Label();
            this.lstSteps = new System.Windows.Forms.ListBox();
            this.btnCancel = new System.Windows.Forms.Button();
            this.cboRunningSessions = new System.Windows.Forms.ComboBox();

            this.cboRunningSessions.Location = new System.Drawing.Point(20, 20);
            this.cboRunningSessions.Size = new System.Drawing.Size(400, 30);
            this.cboRunningSessions.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;

            this.lblStatus.Location = new System.Drawing.Point(20, 60);
            this.lblStatus.AutoSize = true;
            this.lblStatus.Text = "Trạng thái: Đang chờ...";
            this.lblStatus.Font = new System.Drawing.Font("Segoe UI", 10F, System.Drawing.FontStyle.Bold);

            this.lstSteps.Location = new System.Drawing.Point(20, 90);
            this.lstSteps.Size = new System.Drawing.Size(600, 180);

            this.btnCancel.Location = new System.Drawing.Point(20, 290);
            this.btnCancel.Size = new System.Drawing.Size(150, 40);
            this.btnCancel.Text = "HỦY PHIÊN";
            this.btnCancel.BackColor = System.Drawing.Color.IndianRed;
            this.btnCancel.ForeColor = System.Drawing.Color.White;
            this.btnCancel.FlatStyle = System.Windows.Forms.FlatStyle.Flat;

            this.Controls.Add(this.cboRunningSessions);
            this.Controls.Add(this.lblStatus);
            this.Controls.Add(this.lstSteps);
            this.Controls.Add(this.btnCancel);
        }
    }
}