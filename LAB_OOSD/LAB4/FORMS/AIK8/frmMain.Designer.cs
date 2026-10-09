namespace AIK08
{
    partial class frmMain
    {
        private System.ComponentModel.IContainer components = null;
        private System.Windows.Forms.Panel pnlSidebar;
        private System.Windows.Forms.Panel pnlContent;
        private System.Windows.Forms.Button btnUC01;
        private System.Windows.Forms.Button btnUC02; // Thêm nút Tiến độ / Hủy
        private System.Windows.Forms.Button btnUC03;
        private System.Windows.Forms.Button btnUC05; // Thêm nút Cấu hình
        private System.Windows.Forms.Button btnUC06;

        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null)) components.Dispose();
            base.Dispose(disposing);
        }

        private void InitializeComponent()
        {
            this.pnlSidebar = new System.Windows.Forms.Panel();
            this.btnUC06 = new System.Windows.Forms.Button();
            this.btnUC05 = new System.Windows.Forms.Button();
            this.btnUC03 = new System.Windows.Forms.Button();
            this.btnUC02 = new System.Windows.Forms.Button();
            this.btnUC01 = new System.Windows.Forms.Button();
            this.pnlContent = new System.Windows.Forms.Panel();
            this.pnlSidebar.SuspendLayout();
            this.SuspendLayout();
            // 
            // pnlSidebar
            // 
            this.pnlSidebar.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(45)))), ((int)(((byte)(45)))), ((int)(((byte)(48)))));
            this.pnlSidebar.Controls.Add(this.btnUC06);
            this.pnlSidebar.Controls.Add(this.btnUC05);
            this.pnlSidebar.Controls.Add(this.btnUC03);
            this.pnlSidebar.Controls.Add(this.btnUC02);
            this.pnlSidebar.Controls.Add(this.btnUC01);
            this.pnlSidebar.Dock = System.Windows.Forms.DockStyle.Left;
            this.pnlSidebar.Location = new System.Drawing.Point(0, 0);
            this.pnlSidebar.Name = "pnlSidebar";
            this.pnlSidebar.Size = new System.Drawing.Size(220, 650);
            this.pnlSidebar.TabIndex = 1;
            // 
            // btnUC06
            // 
            this.btnUC06.Dock = System.Windows.Forms.DockStyle.Top;
            this.btnUC06.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.btnUC06.ForeColor = System.Drawing.Color.White;
            this.btnUC06.Location = new System.Drawing.Point(0, 200);
            this.btnUC06.Name = "btnUC06";
            this.btnUC06.Size = new System.Drawing.Size(220, 50);
            this.btnUC06.TabIndex = 0;
            this.btnUC06.Text = "Vết Kiểm Toán (UC06)";
            this.btnUC06.Click += new System.EventHandler(this.btnUC06_Click);
            // 
            // btnUC05
            // 
            this.btnUC05.Dock = System.Windows.Forms.DockStyle.Top;
            this.btnUC05.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.btnUC05.ForeColor = System.Drawing.Color.White;
            this.btnUC05.Location = new System.Drawing.Point(0, 150);
            this.btnUC05.Name = "btnUC05";
            this.btnUC05.Size = new System.Drawing.Size(220, 50);
            this.btnUC05.TabIndex = 1;
            this.btnUC05.Text = "Cấu Hình (UC05)";
            // 
            // btnUC03
            // 
            this.btnUC03.Dock = System.Windows.Forms.DockStyle.Top;
            this.btnUC03.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.btnUC03.ForeColor = System.Drawing.Color.White;
            this.btnUC03.Location = new System.Drawing.Point(0, 100);
            this.btnUC03.Name = "btnUC03";
            this.btnUC03.Size = new System.Drawing.Size(220, 50);
            this.btnUC03.TabIndex = 2;
            this.btnUC03.Text = "Xem Báo Cáo (UC03)";
            // 
            // btnUC02
            // 
            this.btnUC02.Dock = System.Windows.Forms.DockStyle.Top;
            this.btnUC02.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.btnUC02.ForeColor = System.Drawing.Color.White;
            this.btnUC02.Location = new System.Drawing.Point(0, 50);
            this.btnUC02.Name = "btnUC02";
            this.btnUC02.Size = new System.Drawing.Size(220, 50);
            this.btnUC02.TabIndex = 3;
            this.btnUC02.Text = "Tiến Độ && Hủy (UC02, UC04)";
            // 
            // btnUC01
            // 
            this.btnUC01.Dock = System.Windows.Forms.DockStyle.Top;
            this.btnUC01.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.btnUC01.ForeColor = System.Drawing.Color.White;
            this.btnUC01.Location = new System.Drawing.Point(0, 0);
            this.btnUC01.Name = "btnUC01";
            this.btnUC01.Size = new System.Drawing.Size(220, 50);
            this.btnUC01.TabIndex = 4;
            this.btnUC01.Text = "Gửi Yêu Cầu (UC01)";
            // 
            // pnlContent
            // 
            this.pnlContent.BackColor = System.Drawing.Color.WhiteSmoke;
            this.pnlContent.Dock = System.Windows.Forms.DockStyle.Fill;
            this.pnlContent.Location = new System.Drawing.Point(220, 0);
            this.pnlContent.Name = "pnlContent";
            this.pnlContent.Size = new System.Drawing.Size(880, 650);
            this.pnlContent.TabIndex = 0;
            // 
            // frmMain
            // 
            this.ClientSize = new System.Drawing.Size(1100, 650);
            this.Controls.Add(this.pnlContent);
            this.Controls.Add(this.pnlSidebar);
            this.Name = "frmMain";
            this.Text = "AIK08 - Hệ thống Điều phối Agent Tra Cứu";
            this.pnlSidebar.ResumeLayout(false);
            this.ResumeLayout(false);

        }
    }
}