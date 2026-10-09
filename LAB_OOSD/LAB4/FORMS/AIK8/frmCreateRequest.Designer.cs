namespace AIK08
{
    partial class frmCreateRequest
    {
        private System.ComponentModel.IContainer components = null;
        private System.Windows.Forms.TextBox txtQuery;
        private System.Windows.Forms.NumericUpDown nudSteps;
        private System.Windows.Forms.NumericUpDown nudSeconds;
        private System.Windows.Forms.Button btnSubmit;
        private System.Windows.Forms.Label lblTitle;
        private System.Windows.Forms.Label lblSteps;
        private System.Windows.Forms.Label lblSeconds;
        private System.Windows.Forms.Label lblSources;
        private System.Windows.Forms.CheckedListBox chkSources;

        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null)) components.Dispose();
            base.Dispose(disposing);
        }

        private void InitializeComponent()
        {
            this.txtQuery = new System.Windows.Forms.TextBox();
            this.nudSteps = new System.Windows.Forms.NumericUpDown();
            this.nudSeconds = new System.Windows.Forms.NumericUpDown();
            this.btnSubmit = new System.Windows.Forms.Button();
            this.lblTitle = new System.Windows.Forms.Label();
            this.lblSteps = new System.Windows.Forms.Label();
            this.lblSeconds = new System.Windows.Forms.Label();
            this.lblSources = new System.Windows.Forms.Label();
            this.chkSources = new System.Windows.Forms.CheckedListBox();

            this.lblTitle.Text = "NHẬP YÊU CẦU TRA CỨU";
            this.lblTitle.Location = new System.Drawing.Point(20, 20);
            this.lblTitle.AutoSize = true;
            this.lblTitle.Font = new System.Drawing.Font("Segoe UI", 11F, System.Drawing.FontStyle.Bold);

            this.txtQuery.Location = new System.Drawing.Point(20, 50);
            this.txtQuery.Multiline = true;
            this.txtQuery.Size = new System.Drawing.Size(650, 90);

            // Cấu hình nhãn và ô nhập số bước
            this.lblSteps.Text = "Hạn mức Bước (Steps):";
            this.lblSteps.Location = new System.Drawing.Point(20, 155);
            this.lblSteps.AutoSize = true;

            this.nudSteps.Location = new System.Drawing.Point(180, 153);
            this.nudSteps.Size = new System.Drawing.Size(100, 25);
            this.nudSteps.Value = 10;

            // Cấu hình nhãn và ô nhập thời gian
            this.lblSeconds.Text = "Hạn mức Thời gian (Giây):";
            this.lblSeconds.Location = new System.Drawing.Point(310, 155);
            this.lblSeconds.AutoSize = true;

            this.nudSeconds.Location = new System.Drawing.Point(470, 153);
            this.nudSeconds.Size = new System.Drawing.Size(100, 25);
            this.nudSeconds.Value = 60;

            // Cấu hình danh sách chọn nguồn dữ liệu
            this.lblSources.Text = "Chọn Nguồn Dữ Liệu Tra Cứu (Allowlist):";
            this.lblSources.Location = new System.Drawing.Point(20, 195);
            this.lblSources.AutoSize = true;

            this.chkSources.Location = new System.Drawing.Point(20, 220);
            this.chkSources.Size = new System.Drawing.Size(650, 100);

            // Nút Gửi yêu cầu
            this.btnSubmit.Text = "Gửi Yêu Cầu";
            this.btnSubmit.Location = new System.Drawing.Point(20, 335);
            this.btnSubmit.Size = new System.Drawing.Size(140, 40);
            this.btnSubmit.BackColor = System.Drawing.Color.FromArgb(0, 122, 204);
            this.btnSubmit.ForeColor = System.Drawing.Color.White;
            this.btnSubmit.FlatStyle = System.Windows.Forms.FlatStyle.Flat;

            this.Controls.Add(this.lblTitle);
            this.Controls.Add(this.txtQuery);
            this.Controls.Add(this.lblSteps);
            this.Controls.Add(this.nudSteps);
            this.Controls.Add(this.lblSeconds);
            this.Controls.Add(this.nudSeconds);
            this.Controls.Add(this.lblSources);
            this.Controls.Add(this.chkSources);
            this.Controls.Add(this.btnSubmit);
        }
    }
}