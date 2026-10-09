namespace AIK08
{
    partial class frmConfig
    {
        private System.Windows.Forms.NumericUpDown nudDefSteps;
        private System.Windows.Forms.NumericUpDown nudDefSecs;
        private System.Windows.Forms.Label lblSteps;
        private System.Windows.Forms.Label lblSecs;
        private System.Windows.Forms.Button btnSave;
        private System.Windows.Forms.DataGridView dgvSources;
        private System.Windows.Forms.Label lblGridTitle;

        private void InitializeComponent()
        {
            this.nudDefSteps = new System.Windows.Forms.NumericUpDown();
            this.nudDefSecs = new System.Windows.Forms.NumericUpDown();
            this.lblSteps = new System.Windows.Forms.Label();
            this.lblSecs = new System.Windows.Forms.Label();
            this.btnSave = new System.Windows.Forms.Button();
            this.dgvSources = new System.Windows.Forms.DataGridView();
            this.lblGridTitle = new System.Windows.Forms.Label();

            this.lblSteps.Text = "Ngân sách Bước (Mặc định):";
            this.lblSteps.Location = new System.Drawing.Point(20, 20);
            this.lblSteps.AutoSize = true;

            this.nudDefSteps.Location = new System.Drawing.Point(200, 20);

            this.lblSecs.Text = "Ngân sách Giây (Mặc định):";
            this.lblSecs.Location = new System.Drawing.Point(20, 60);
            this.lblSecs.AutoSize = true;

            this.nudDefSecs.Location = new System.Drawing.Point(200, 60);

            this.btnSave.Text = "Lưu Cấu Hình";
            this.btnSave.Location = new System.Drawing.Point(20, 100);
            this.btnSave.Size = new System.Drawing.Size(120, 35);

            this.lblGridTitle.Text = "DANH SÁCH NGUỒN DỮ LIỆU ĐÃ ĐĂNG KÝ";
            this.lblGridTitle.Location = new System.Drawing.Point(20, 160);
            this.lblGridTitle.AutoSize = true;
            this.lblGridTitle.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Bold);

            this.dgvSources.Location = new System.Drawing.Point(20, 190);
            this.dgvSources.Size = new System.Drawing.Size(600, 200);
            this.dgvSources.AutoSizeColumnsMode = System.Windows.Forms.DataGridViewAutoSizeColumnsMode.Fill;
            this.dgvSources.ReadOnly = true;

            this.Controls.Add(this.lblSteps);
            this.Controls.Add(this.nudDefSteps);
            this.Controls.Add(this.lblSecs);
            this.Controls.Add(this.nudDefSecs);
            this.Controls.Add(this.btnSave);
            this.Controls.Add(this.lblGridTitle);
            this.Controls.Add(this.dgvSources);
        }
    }
}