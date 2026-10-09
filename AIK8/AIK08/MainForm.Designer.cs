namespace AIK08
{
    partial class MainForm
    {
        private System.ComponentModel.IContainer components = null;

        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.statusStrip1 = new System.Windows.Forms.StatusStrip();
            this.lblStatus = new System.Windows.Forms.ToolStripStatusLabel();
            this.tabMain = new System.Windows.Forms.TabControl();
            this.tabSessions = new System.Windows.Forms.TabPage();
            this.tabReport = new System.Windows.Forms.TabPage();
            this.tabAdmin = new System.Windows.Forms.TabPage();
            this.pnlTop = new System.Windows.Forms.Panel();
            this.lblQuestion = new System.Windows.Forms.Label();
            this.txtQuestion = new System.Windows.Forms.TextBox();
            this.btnNew = new System.Windows.Forms.Button();
            this.btnCancelSession = new System.Windows.Forms.Button();
            this.btnRefresh = new System.Windows.Forms.Button();
            this.chkAuto = new System.Windows.Forms.CheckBox();
            this.splitSessions = new System.Windows.Forms.SplitContainer();
            this.gridSessions = new System.Windows.Forms.DataGridView();
            this.tabDetail = new System.Windows.Forms.TabControl();
            this.tabPlan = new System.Windows.Forms.TabPage();
            this.tabCalls = new System.Windows.Forms.TabPage();
            this.tabFindings = new System.Windows.Forms.TabPage();
            this.gridPlan = new System.Windows.Forms.DataGridView();
            this.gridCalls = new System.Windows.Forms.DataGridView();
            this.gridFindings = new System.Windows.Forms.DataGridView();
            this.lblReportInfo = new System.Windows.Forms.Label();
            this.txtReportBody = new System.Windows.Forms.TextBox();
            this.splitReport = new System.Windows.Forms.SplitContainer();
            this.lblClaims = new System.Windows.Forms.Label();
            this.gridClaims = new System.Windows.Forms.DataGridView();
            this.lblEvidence = new System.Windows.Forms.Label();
            this.gridEvidence = new System.Windows.Forms.DataGridView();
            this.grpPolicy = new System.Windows.Forms.GroupBox();
            this.lblTools = new System.Windows.Forms.Label();
            this.clbTools = new System.Windows.Forms.CheckedListBox();
            this.lblNoWrite = new System.Windows.Forms.Label();
            this.lblMaxSteps = new System.Windows.Forms.Label();
            this.numMaxSteps = new System.Windows.Forms.NumericUpDown();
            this.lblMaxTokens = new System.Windows.Forms.Label();
            this.numMaxTokens = new System.Windows.Forms.NumericUpDown();
            this.lblMaxSeconds = new System.Windows.Forms.Label();
            this.numMaxSeconds = new System.Windows.Forms.NumericUpDown();
            this.btnSavePolicy = new System.Windows.Forms.Button();
            this.grpSources = new System.Windows.Forms.GroupBox();
            this.gridSources = new System.Windows.Forms.DataGridView();
            this.pnlAddSource = new System.Windows.Forms.Panel();
            this.cmbKind = new System.Windows.Forms.ComboBox();
            this.txtName = new System.Windows.Forms.TextBox();
            this.txtUri = new System.Windows.Forms.TextBox();
            this.btnAddSource = new System.Windows.Forms.Button();
            this.btnSaveSources = new System.Windows.Forms.Button();
            this.timerRefresh = new System.Windows.Forms.Timer(this.components);
            this.statusStrip1.SuspendLayout();
            this.tabMain.SuspendLayout();
            this.tabSessions.SuspendLayout();
            this.tabReport.SuspendLayout();
            this.tabAdmin.SuspendLayout();
            this.pnlTop.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.splitSessions)).BeginInit();
            this.splitSessions.Panel1.SuspendLayout();
            this.splitSessions.Panel2.SuspendLayout();
            this.splitSessions.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.gridSessions)).BeginInit();
            this.tabDetail.SuspendLayout();
            this.tabPlan.SuspendLayout();
            this.tabCalls.SuspendLayout();
            this.tabFindings.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.gridPlan)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.gridCalls)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.gridFindings)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.splitReport)).BeginInit();
            this.splitReport.Panel1.SuspendLayout();
            this.splitReport.Panel2.SuspendLayout();
            this.splitReport.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.gridClaims)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.gridEvidence)).BeginInit();
            this.grpPolicy.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.numMaxSteps)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.numMaxTokens)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.numMaxSeconds)).BeginInit();
            this.grpSources.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.gridSources)).BeginInit();
            this.pnlAddSource.SuspendLayout();
            this.SuspendLayout();
            //
            // statusStrip1
            //
            this.statusStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] { this.lblStatus });
            this.statusStrip1.Location = new System.Drawing.Point(0, 699);
            this.statusStrip1.Name = "statusStrip1";
            this.statusStrip1.Size = new System.Drawing.Size(1184, 22);
            this.statusStrip1.TabIndex = 1;
            //
            // lblStatus
            //
            this.lblStatus.Name = "lblStatus";
            this.lblStatus.Size = new System.Drawing.Size(39, 17);
            this.lblStatus.Text = "Sẵn sàng";
            //
            // tabMain
            //
            this.tabMain.Controls.Add(this.tabSessions);
            this.tabMain.Controls.Add(this.tabReport);
            this.tabMain.Controls.Add(this.tabAdmin);
            this.tabMain.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tabMain.Location = new System.Drawing.Point(0, 0);
            this.tabMain.Name = "tabMain";
            this.tabMain.SelectedIndex = 0;
            this.tabMain.Size = new System.Drawing.Size(1184, 699);
            this.tabMain.TabIndex = 0;
            this.tabMain.SelectedIndexChanged += new System.EventHandler(this.tabMain_SelectedIndexChanged);
            //
            // tabSessions
            //
            this.tabSessions.Controls.Add(this.splitSessions);
            this.tabSessions.Controls.Add(this.pnlTop);
            this.tabSessions.Location = new System.Drawing.Point(4, 24);
            this.tabSessions.Name = "tabSessions";
            this.tabSessions.Padding = new System.Windows.Forms.Padding(3);
            this.tabSessions.Size = new System.Drawing.Size(1176, 671);
            this.tabSessions.TabIndex = 0;
            this.tabSessions.Text = "Phiên tra cứu";
            this.tabSessions.UseVisualStyleBackColor = true;
            //
            // tabReport
            //
            this.tabReport.Controls.Add(this.splitReport);
            this.tabReport.Controls.Add(this.txtReportBody);
            this.tabReport.Controls.Add(this.lblReportInfo);
            this.tabReport.Location = new System.Drawing.Point(4, 24);
            this.tabReport.Name = "tabReport";
            this.tabReport.Padding = new System.Windows.Forms.Padding(3);
            this.tabReport.Size = new System.Drawing.Size(1176, 671);
            this.tabReport.TabIndex = 1;
            this.tabReport.Text = "Báo cáo và nguồn";
            this.tabReport.UseVisualStyleBackColor = true;
            //
            // tabAdmin
            //
            this.tabAdmin.Controls.Add(this.grpSources);
            this.tabAdmin.Controls.Add(this.grpPolicy);
            this.tabAdmin.Location = new System.Drawing.Point(4, 24);
            this.tabAdmin.Name = "tabAdmin";
            this.tabAdmin.Padding = new System.Windows.Forms.Padding(3);
            this.tabAdmin.Size = new System.Drawing.Size(1176, 671);
            this.tabAdmin.TabIndex = 2;
            this.tabAdmin.Text = "Quản trị";
            this.tabAdmin.UseVisualStyleBackColor = true;
            //
            // pnlTop
            //
            this.pnlTop.Controls.Add(this.chkAuto);
            this.pnlTop.Controls.Add(this.btnRefresh);
            this.pnlTop.Controls.Add(this.btnCancelSession);
            this.pnlTop.Controls.Add(this.btnNew);
            this.pnlTop.Controls.Add(this.txtQuestion);
            this.pnlTop.Controls.Add(this.lblQuestion);
            this.pnlTop.Dock = System.Windows.Forms.DockStyle.Top;
            this.pnlTop.Location = new System.Drawing.Point(3, 3);
            this.pnlTop.Name = "pnlTop";
            this.pnlTop.Size = new System.Drawing.Size(1170, 52);
            this.pnlTop.TabIndex = 0;
            //
            // lblQuestion
            //
            this.lblQuestion.AutoSize = true;
            this.lblQuestion.Location = new System.Drawing.Point(8, 18);
            this.lblQuestion.Name = "lblQuestion";
            this.lblQuestion.Size = new System.Drawing.Size(70, 15);
            this.lblQuestion.TabIndex = 0;
            this.lblQuestion.Text = "Câu hỏi mới:";
            //
            // txtQuestion
            //
            this.txtQuestion.Location = new System.Drawing.Point(92, 14);
            this.txtQuestion.Name = "txtQuestion";
            this.txtQuestion.PlaceholderText = "Nhập câu hỏi tra cứu rồi bấm Tạo phiên";
            this.txtQuestion.Size = new System.Drawing.Size(420, 23);
            this.txtQuestion.TabIndex = 1;
            //
            // btnNew
            //
            this.btnNew.Location = new System.Drawing.Point(522, 11);
            this.btnNew.Name = "btnNew";
            this.btnNew.Size = new System.Drawing.Size(100, 29);
            this.btnNew.TabIndex = 2;
            this.btnNew.Text = "Tạo phiên";
            this.btnNew.UseVisualStyleBackColor = true;
            this.btnNew.Click += new System.EventHandler(this.btnNew_Click);
            //
            // btnCancelSession
            //
            this.btnCancelSession.Enabled = false;
            this.btnCancelSession.Location = new System.Drawing.Point(630, 11);
            this.btnCancelSession.Name = "btnCancelSession";
            this.btnCancelSession.Size = new System.Drawing.Size(150, 29);
            this.btnCancelSession.TabIndex = 3;
            this.btnCancelSession.Text = "Hủy phiên đã chọn";
            this.btnCancelSession.UseVisualStyleBackColor = true;
            this.btnCancelSession.Click += new System.EventHandler(this.btnCancelSession_Click);
            //
            // btnRefresh
            //
            this.btnRefresh.Location = new System.Drawing.Point(788, 11);
            this.btnRefresh.Name = "btnRefresh";
            this.btnRefresh.Size = new System.Drawing.Size(90, 29);
            this.btnRefresh.TabIndex = 4;
            this.btnRefresh.Text = "Làm mới";
            this.btnRefresh.UseVisualStyleBackColor = true;
            this.btnRefresh.Click += new System.EventHandler(this.btnRefresh_Click);
            //
            // chkAuto
            //
            this.chkAuto.AutoSize = true;
            this.chkAuto.Location = new System.Drawing.Point(890, 17);
            this.chkAuto.Name = "chkAuto";
            this.chkAuto.Size = new System.Drawing.Size(150, 19);
            this.chkAuto.TabIndex = 5;
            this.chkAuto.Text = "Tự làm mới (3 giây)";
            this.chkAuto.UseVisualStyleBackColor = true;
            this.chkAuto.CheckedChanged += new System.EventHandler(this.chkAuto_CheckedChanged);
            //
            // splitSessions
            //
            this.splitSessions.Dock = System.Windows.Forms.DockStyle.Fill;
            this.splitSessions.Location = new System.Drawing.Point(3, 55);
            this.splitSessions.Name = "splitSessions";
            this.splitSessions.Orientation = System.Windows.Forms.Orientation.Horizontal;
            this.splitSessions.Panel1.Controls.Add(this.gridSessions);
            this.splitSessions.Panel2.Controls.Add(this.tabDetail);
            this.splitSessions.Size = new System.Drawing.Size(1170, 613);
            this.splitSessions.TabIndex = 1;
            //
            // gridSessions
            //
            this.gridSessions.AllowUserToAddRows = false;
            this.gridSessions.AllowUserToDeleteRows = false;
            this.gridSessions.AutoSizeColumnsMode = System.Windows.Forms.DataGridViewAutoSizeColumnsMode.Fill;
            this.gridSessions.BackgroundColor = System.Drawing.Color.White;
            this.gridSessions.Dock = System.Windows.Forms.DockStyle.Fill;
            this.gridSessions.Location = new System.Drawing.Point(0, 0);
            this.gridSessions.MultiSelect = false;
            this.gridSessions.Name = "gridSessions";
            this.gridSessions.ReadOnly = true;
            this.gridSessions.RowHeadersVisible = false;
            this.gridSessions.SelectionMode = System.Windows.Forms.DataGridViewSelectionMode.FullRowSelect;
            this.gridSessions.Size = new System.Drawing.Size(1170, 300);
            this.gridSessions.TabIndex = 0;
            this.gridSessions.DataBindingComplete += new System.Windows.Forms.DataGridViewBindingCompleteEventHandler(this.gridSessions_DataBindingComplete);
            this.gridSessions.SelectionChanged += new System.EventHandler(this.gridSessions_SelectionChanged);
            //
            // tabDetail
            //
            this.tabDetail.Controls.Add(this.tabPlan);
            this.tabDetail.Controls.Add(this.tabCalls);
            this.tabDetail.Controls.Add(this.tabFindings);
            this.tabDetail.Dock = System.Windows.Forms.DockStyle.Fill;
            this.tabDetail.Location = new System.Drawing.Point(0, 0);
            this.tabDetail.Name = "tabDetail";
            this.tabDetail.SelectedIndex = 0;
            this.tabDetail.Size = new System.Drawing.Size(1170, 309);
            this.tabDetail.TabIndex = 0;
            this.tabDetail.SelectedIndexChanged += new System.EventHandler(this.tabDetail_SelectedIndexChanged);
            //
            // tabPlan
            //
            this.tabPlan.Controls.Add(this.gridPlan);
            this.tabPlan.Location = new System.Drawing.Point(4, 24);
            this.tabPlan.Name = "tabPlan";
            this.tabPlan.Size = new System.Drawing.Size(1162, 281);
            this.tabPlan.TabIndex = 0;
            this.tabPlan.Text = "Kế hoạch";
            this.tabPlan.UseVisualStyleBackColor = true;
            //
            // tabCalls
            //
            this.tabCalls.Controls.Add(this.gridCalls);
            this.tabCalls.Location = new System.Drawing.Point(4, 24);
            this.tabCalls.Name = "tabCalls";
            this.tabCalls.Size = new System.Drawing.Size(1162, 281);
            this.tabCalls.TabIndex = 1;
            this.tabCalls.Text = "Lời gọi tool";
            this.tabCalls.UseVisualStyleBackColor = true;
            //
            // tabFindings
            //
            this.tabFindings.Controls.Add(this.gridFindings);
            this.tabFindings.Location = new System.Drawing.Point(4, 24);
            this.tabFindings.Name = "tabFindings";
            this.tabFindings.Size = new System.Drawing.Size(1162, 281);
            this.tabFindings.TabIndex = 2;
            this.tabFindings.Text = "Cảnh báo của guard";
            this.tabFindings.UseVisualStyleBackColor = true;
            //
            // gridPlan
            //
            this.gridPlan.AllowUserToAddRows = false;
            this.gridPlan.AllowUserToDeleteRows = false;
            this.gridPlan.AutoSizeColumnsMode = System.Windows.Forms.DataGridViewAutoSizeColumnsMode.Fill;
            this.gridPlan.BackgroundColor = System.Drawing.Color.White;
            this.gridPlan.Dock = System.Windows.Forms.DockStyle.Fill;
            this.gridPlan.Location = new System.Drawing.Point(0, 0);
            this.gridPlan.MultiSelect = false;
            this.gridPlan.Name = "gridPlan";
            this.gridPlan.ReadOnly = true;
            this.gridPlan.RowHeadersVisible = false;
            this.gridPlan.SelectionMode = System.Windows.Forms.DataGridViewSelectionMode.FullRowSelect;
            this.gridPlan.Size = new System.Drawing.Size(1162, 281);
            this.gridPlan.TabIndex = 0;
            //
            // gridCalls
            //
            this.gridCalls.AllowUserToAddRows = false;
            this.gridCalls.AllowUserToDeleteRows = false;
            this.gridCalls.AutoSizeColumnsMode = System.Windows.Forms.DataGridViewAutoSizeColumnsMode.Fill;
            this.gridCalls.BackgroundColor = System.Drawing.Color.White;
            this.gridCalls.Dock = System.Windows.Forms.DockStyle.Fill;
            this.gridCalls.Location = new System.Drawing.Point(0, 0);
            this.gridCalls.MultiSelect = false;
            this.gridCalls.Name = "gridCalls";
            this.gridCalls.ReadOnly = true;
            this.gridCalls.RowHeadersVisible = false;
            this.gridCalls.SelectionMode = System.Windows.Forms.DataGridViewSelectionMode.FullRowSelect;
            this.gridCalls.Size = new System.Drawing.Size(1162, 281);
            this.gridCalls.TabIndex = 0;
            this.gridCalls.DataBindingComplete += new System.Windows.Forms.DataGridViewBindingCompleteEventHandler(this.gridCalls_DataBindingComplete);
            //
            // gridFindings
            //
            this.gridFindings.AllowUserToAddRows = false;
            this.gridFindings.AllowUserToDeleteRows = false;
            this.gridFindings.AutoSizeColumnsMode = System.Windows.Forms.DataGridViewAutoSizeColumnsMode.Fill;
            this.gridFindings.BackgroundColor = System.Drawing.Color.White;
            this.gridFindings.Dock = System.Windows.Forms.DockStyle.Fill;
            this.gridFindings.Location = new System.Drawing.Point(0, 0);
            this.gridFindings.MultiSelect = false;
            this.gridFindings.Name = "gridFindings";
            this.gridFindings.ReadOnly = true;
            this.gridFindings.RowHeadersVisible = false;
            this.gridFindings.SelectionMode = System.Windows.Forms.DataGridViewSelectionMode.FullRowSelect;
            this.gridFindings.Size = new System.Drawing.Size(1162, 281);
            this.gridFindings.TabIndex = 0;
            //
            // lblReportInfo
            //
            this.lblReportInfo.Dock = System.Windows.Forms.DockStyle.Top;
            this.lblReportInfo.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Bold);
            this.lblReportInfo.Location = new System.Drawing.Point(3, 3);
            this.lblReportInfo.Name = "lblReportInfo";
            this.lblReportInfo.Padding = new System.Windows.Forms.Padding(4, 4, 4, 0);
            this.lblReportInfo.Size = new System.Drawing.Size(1170, 44);
            this.lblReportInfo.TabIndex = 0;
            this.lblReportInfo.Text = "Chọn một phiên ở tab Phiên tra cứu.";
            //
            // txtReportBody
            //
            this.txtReportBody.BackColor = System.Drawing.Color.White;
            this.txtReportBody.Dock = System.Windows.Forms.DockStyle.Top;
            this.txtReportBody.Location = new System.Drawing.Point(3, 47);
            this.txtReportBody.Multiline = true;
            this.txtReportBody.Name = "txtReportBody";
            this.txtReportBody.ReadOnly = true;
            this.txtReportBody.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this.txtReportBody.Size = new System.Drawing.Size(1170, 96);
            this.txtReportBody.TabIndex = 1;
            //
            // splitReport
            //
            this.splitReport.Dock = System.Windows.Forms.DockStyle.Fill;
            this.splitReport.Location = new System.Drawing.Point(3, 143);
            this.splitReport.Name = "splitReport";
            this.splitReport.Orientation = System.Windows.Forms.Orientation.Horizontal;
            this.splitReport.Panel1.Controls.Add(this.gridClaims);
            this.splitReport.Panel1.Controls.Add(this.lblClaims);
            this.splitReport.Panel2.Controls.Add(this.gridEvidence);
            this.splitReport.Panel2.Controls.Add(this.lblEvidence);
            this.splitReport.Size = new System.Drawing.Size(1170, 525);
            this.splitReport.TabIndex = 2;
            //
            // lblClaims
            //
            this.lblClaims.Dock = System.Windows.Forms.DockStyle.Top;
            this.lblClaims.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Bold);
            this.lblClaims.Location = new System.Drawing.Point(0, 0);
            this.lblClaims.Name = "lblClaims";
            this.lblClaims.Size = new System.Drawing.Size(1170, 24);
            this.lblClaims.TabIndex = 0;
            this.lblClaims.Text = "Khẳng định trong báo cáo (chọn một dòng để truy vết nguồn)";
            this.lblClaims.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            //
            // gridClaims
            //
            this.gridClaims.AllowUserToAddRows = false;
            this.gridClaims.AllowUserToDeleteRows = false;
            this.gridClaims.AutoSizeColumnsMode = System.Windows.Forms.DataGridViewAutoSizeColumnsMode.Fill;
            this.gridClaims.BackgroundColor = System.Drawing.Color.White;
            this.gridClaims.Dock = System.Windows.Forms.DockStyle.Fill;
            this.gridClaims.Location = new System.Drawing.Point(0, 24);
            this.gridClaims.MultiSelect = false;
            this.gridClaims.Name = "gridClaims";
            this.gridClaims.ReadOnly = true;
            this.gridClaims.RowHeadersVisible = false;
            this.gridClaims.SelectionMode = System.Windows.Forms.DataGridViewSelectionMode.FullRowSelect;
            this.gridClaims.Size = new System.Drawing.Size(1170, 232);
            this.gridClaims.TabIndex = 1;
            this.gridClaims.DataBindingComplete += new System.Windows.Forms.DataGridViewBindingCompleteEventHandler(this.gridClaims_DataBindingComplete);
            this.gridClaims.SelectionChanged += new System.EventHandler(this.gridClaims_SelectionChanged);
            //
            // lblEvidence
            //
            this.lblEvidence.Dock = System.Windows.Forms.DockStyle.Top;
            this.lblEvidence.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Bold);
            this.lblEvidence.Location = new System.Drawing.Point(0, 0);
            this.lblEvidence.Name = "lblEvidence";
            this.lblEvidence.Size = new System.Drawing.Size(1170, 24);
            this.lblEvidence.TabIndex = 0;
            this.lblEvidence.Text = "Bằng chứng gốc của khẳng định đã chọn";
            this.lblEvidence.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            //
            // gridEvidence
            //
            this.gridEvidence.AllowUserToAddRows = false;
            this.gridEvidence.AllowUserToDeleteRows = false;
            this.gridEvidence.AutoSizeColumnsMode = System.Windows.Forms.DataGridViewAutoSizeColumnsMode.Fill;
            this.gridEvidence.BackgroundColor = System.Drawing.Color.White;
            this.gridEvidence.Dock = System.Windows.Forms.DockStyle.Fill;
            this.gridEvidence.Location = new System.Drawing.Point(0, 24);
            this.gridEvidence.MultiSelect = false;
            this.gridEvidence.Name = "gridEvidence";
            this.gridEvidence.ReadOnly = true;
            this.gridEvidence.RowHeadersVisible = false;
            this.gridEvidence.SelectionMode = System.Windows.Forms.DataGridViewSelectionMode.FullRowSelect;
            this.gridEvidence.Size = new System.Drawing.Size(1170, 233);
            this.gridEvidence.TabIndex = 1;
            this.gridEvidence.DataBindingComplete += new System.Windows.Forms.DataGridViewBindingCompleteEventHandler(this.gridEvidence_DataBindingComplete);
            //
            // grpPolicy
            //
            this.grpPolicy.Controls.Add(this.btnSavePolicy);
            this.grpPolicy.Controls.Add(this.numMaxSeconds);
            this.grpPolicy.Controls.Add(this.lblMaxSeconds);
            this.grpPolicy.Controls.Add(this.numMaxTokens);
            this.grpPolicy.Controls.Add(this.lblMaxTokens);
            this.grpPolicy.Controls.Add(this.numMaxSteps);
            this.grpPolicy.Controls.Add(this.lblMaxSteps);
            this.grpPolicy.Controls.Add(this.lblNoWrite);
            this.grpPolicy.Controls.Add(this.clbTools);
            this.grpPolicy.Controls.Add(this.lblTools);
            this.grpPolicy.Dock = System.Windows.Forms.DockStyle.Top;
            this.grpPolicy.Location = new System.Drawing.Point(3, 3);
            this.grpPolicy.Name = "grpPolicy";
            this.grpPolicy.Size = new System.Drawing.Size(1170, 210);
            this.grpPolicy.TabIndex = 0;
            this.grpPolicy.TabStop = false;
            this.grpPolicy.Text = "Chính sách mặc định (do quản trị viên đặt; agent không có công cụ sửa mục này)";
            //
            // lblTools
            //
            this.lblTools.AutoSize = true;
            this.lblTools.Location = new System.Drawing.Point(12, 26);
            this.lblTools.Name = "lblTools";
            this.lblTools.Size = new System.Drawing.Size(200, 15);
            this.lblTools.TabIndex = 0;
            this.lblTools.Text = "Allowlist công cụ (phạm vi tối đa):";
            //
            // clbTools
            //
            this.clbTools.CheckOnClick = true;
            this.clbTools.FormattingEnabled = true;
            this.clbTools.Location = new System.Drawing.Point(12, 48);
            this.clbTools.Name = "clbTools";
            this.clbTools.Size = new System.Drawing.Size(280, 76);
            this.clbTools.TabIndex = 1;
            //
            // lblNoWrite
            //
            this.lblNoWrite.Location = new System.Drawing.Point(12, 132);
            this.lblNoWrite.Name = "lblNoWrite";
            this.lblNoWrite.Size = new System.Drawing.Size(420, 60);
            this.lblNoWrite.TabIndex = 2;
            this.lblNoWrite.Text = "Danh sách chỉ gồm tool đọc, không có write tool. Chính sách chỉ áp cho phiên tạo sau khi lưu; phiên đã tạo giữ nguyên allowlist và hạn mức đã chốt.";
            //
            // lblMaxSteps
            //
            this.lblMaxSteps.AutoSize = true;
            this.lblMaxSteps.Location = new System.Drawing.Point(460, 52);
            this.lblMaxSteps.Name = "lblMaxSteps";
            this.lblMaxSteps.Size = new System.Drawing.Size(100, 15);
            this.lblMaxSteps.TabIndex = 3;
            this.lblMaxSteps.Text = "Số bước tối đa:";
            //
            // numMaxSteps
            //
            this.numMaxSteps.Location = new System.Drawing.Point(640, 48);
            this.numMaxSteps.Maximum = new decimal(new int[] { 100, 0, 0, 0 });
            this.numMaxSteps.Minimum = new decimal(new int[] { 1, 0, 0, 0 });
            this.numMaxSteps.Name = "numMaxSteps";
            this.numMaxSteps.Size = new System.Drawing.Size(120, 23);
            this.numMaxSteps.TabIndex = 4;
            this.numMaxSteps.Value = new decimal(new int[] { 10, 0, 0, 0 });
            //
            // lblMaxTokens
            //
            this.lblMaxTokens.AutoSize = true;
            this.lblMaxTokens.Location = new System.Drawing.Point(460, 86);
            this.lblMaxTokens.Name = "lblMaxTokens";
            this.lblMaxTokens.Size = new System.Drawing.Size(100, 15);
            this.lblMaxTokens.TabIndex = 5;
            this.lblMaxTokens.Text = "Token tối đa:";
            //
            // numMaxTokens
            //
            this.numMaxTokens.Increment = new decimal(new int[] { 1000, 0, 0, 0 });
            this.numMaxTokens.Location = new System.Drawing.Point(640, 82);
            this.numMaxTokens.Maximum = new decimal(new int[] { 1000000, 0, 0, 0 });
            this.numMaxTokens.Minimum = new decimal(new int[] { 100, 0, 0, 0 });
            this.numMaxTokens.Name = "numMaxTokens";
            this.numMaxTokens.Size = new System.Drawing.Size(120, 23);
            this.numMaxTokens.TabIndex = 6;
            this.numMaxTokens.Value = new decimal(new int[] { 20000, 0, 0, 0 });
            //
            // lblMaxSeconds
            //
            this.lblMaxSeconds.AutoSize = true;
            this.lblMaxSeconds.Location = new System.Drawing.Point(460, 120);
            this.lblMaxSeconds.Name = "lblMaxSeconds";
            this.lblMaxSeconds.Size = new System.Drawing.Size(150, 15);
            this.lblMaxSeconds.TabIndex = 7;
            this.lblMaxSeconds.Text = "Thời gian tối đa (giây):";
            //
            // numMaxSeconds
            //
            this.numMaxSeconds.Location = new System.Drawing.Point(640, 116);
            this.numMaxSeconds.Maximum = new decimal(new int[] { 3600, 0, 0, 0 });
            this.numMaxSeconds.Minimum = new decimal(new int[] { 5, 0, 0, 0 });
            this.numMaxSeconds.Name = "numMaxSeconds";
            this.numMaxSeconds.Size = new System.Drawing.Size(120, 23);
            this.numMaxSeconds.TabIndex = 8;
            this.numMaxSeconds.Value = new decimal(new int[] { 60, 0, 0, 0 });
            //
            // btnSavePolicy
            //
            this.btnSavePolicy.Location = new System.Drawing.Point(460, 156);
            this.btnSavePolicy.Name = "btnSavePolicy";
            this.btnSavePolicy.Size = new System.Drawing.Size(300, 32);
            this.btnSavePolicy.TabIndex = 9;
            this.btnSavePolicy.Text = "Lưu chính sách";
            this.btnSavePolicy.UseVisualStyleBackColor = true;
            this.btnSavePolicy.Click += new System.EventHandler(this.btnSavePolicy_Click);
            //
            // grpSources
            //
            this.grpSources.Controls.Add(this.gridSources);
            this.grpSources.Controls.Add(this.pnlAddSource);
            this.grpSources.Dock = System.Windows.Forms.DockStyle.Fill;
            this.grpSources.Location = new System.Drawing.Point(3, 213);
            this.grpSources.Name = "grpSources";
            this.grpSources.Size = new System.Drawing.Size(1170, 455);
            this.grpSources.TabIndex = 1;
            this.grpSources.TabStop = false;
            this.grpSources.Text = "Danh mục nguồn (chỉ nguồn được bật mới tra cứu được)";
            //
            // gridSources
            //
            this.gridSources.AllowUserToAddRows = false;
            this.gridSources.AllowUserToDeleteRows = false;
            this.gridSources.AutoSizeColumnsMode = System.Windows.Forms.DataGridViewAutoSizeColumnsMode.Fill;
            this.gridSources.BackgroundColor = System.Drawing.Color.White;
            this.gridSources.Dock = System.Windows.Forms.DockStyle.Fill;
            this.gridSources.Location = new System.Drawing.Point(3, 19);
            this.gridSources.MultiSelect = false;
            this.gridSources.Name = "gridSources";
            this.gridSources.RowHeadersVisible = false;
            this.gridSources.SelectionMode = System.Windows.Forms.DataGridViewSelectionMode.FullRowSelect;
            this.gridSources.Size = new System.Drawing.Size(1164, 385);
            this.gridSources.TabIndex = 0;
            //
            // pnlAddSource
            //
            this.pnlAddSource.Controls.Add(this.btnSaveSources);
            this.pnlAddSource.Controls.Add(this.btnAddSource);
            this.pnlAddSource.Controls.Add(this.txtUri);
            this.pnlAddSource.Controls.Add(this.txtName);
            this.pnlAddSource.Controls.Add(this.cmbKind);
            this.pnlAddSource.Dock = System.Windows.Forms.DockStyle.Bottom;
            this.pnlAddSource.Location = new System.Drawing.Point(3, 404);
            this.pnlAddSource.Name = "pnlAddSource";
            this.pnlAddSource.Size = new System.Drawing.Size(1164, 48);
            this.pnlAddSource.TabIndex = 1;
            //
            // cmbKind
            //
            this.cmbKind.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.cmbKind.FormattingEnabled = true;
            this.cmbKind.Items.AddRange(new object[] { "Tài liệu", "API" });
            this.cmbKind.Location = new System.Drawing.Point(8, 12);
            this.cmbKind.Name = "cmbKind";
            this.cmbKind.Size = new System.Drawing.Size(110, 23);
            this.cmbKind.TabIndex = 0;
            //
            // txtName
            //
            this.txtName.Location = new System.Drawing.Point(128, 12);
            this.txtName.Name = "txtName";
            this.txtName.PlaceholderText = "Tên hiển thị";
            this.txtName.Size = new System.Drawing.Size(220, 23);
            this.txtName.TabIndex = 1;
            //
            // txtUri
            //
            this.txtUri.Location = new System.Drawing.Point(358, 12);
            this.txtUri.Name = "txtUri";
            this.txtUri.PlaceholderText = "Đường dẫn tài liệu hoặc URL API (http/https)";
            this.txtUri.Size = new System.Drawing.Size(340, 23);
            this.txtUri.TabIndex = 2;
            //
            // btnAddSource
            //
            this.btnAddSource.Location = new System.Drawing.Point(708, 9);
            this.btnAddSource.Name = "btnAddSource";
            this.btnAddSource.Size = new System.Drawing.Size(110, 29);
            this.btnAddSource.TabIndex = 3;
            this.btnAddSource.Text = "Thêm nguồn";
            this.btnAddSource.UseVisualStyleBackColor = true;
            this.btnAddSource.Click += new System.EventHandler(this.btnAddSource_Click);
            //
            // btnSaveSources
            //
            this.btnSaveSources.Location = new System.Drawing.Point(828, 9);
            this.btnSaveSources.Name = "btnSaveSources";
            this.btnSaveSources.Size = new System.Drawing.Size(180, 29);
            this.btnSaveSources.TabIndex = 4;
            this.btnSaveSources.Text = "Lưu trạng thái bật/tắt";
            this.btnSaveSources.UseVisualStyleBackColor = true;
            this.btnSaveSources.Click += new System.EventHandler(this.btnSaveSources_Click);
            //
            // timerRefresh
            //
            this.timerRefresh.Interval = 3000;
            this.timerRefresh.Tick += new System.EventHandler(this.timerRefresh_Tick);
            //
            // MainForm
            //
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1184, 721);
            this.Controls.Add(this.tabMain);
            this.Controls.Add(this.statusStrip1);
            this.MinimumSize = new System.Drawing.Size(900, 600);
            this.Name = "MainForm";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "AIK-08 - Hệ thống điều phối agent tra cứu (chế độ read-only)";
            this.Load += new System.EventHandler(this.MainForm_Load);
            this.statusStrip1.ResumeLayout(false);
            this.statusStrip1.PerformLayout();
            this.tabMain.ResumeLayout(false);
            this.tabSessions.ResumeLayout(false);
            this.tabReport.ResumeLayout(false);
            this.tabReport.PerformLayout();
            this.tabAdmin.ResumeLayout(false);
            this.pnlTop.ResumeLayout(false);
            this.pnlTop.PerformLayout();
            this.splitSessions.Panel1.ResumeLayout(false);
            this.splitSessions.Panel2.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.splitSessions)).EndInit();
            this.splitSessions.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.gridSessions)).EndInit();
            this.tabDetail.ResumeLayout(false);
            this.tabPlan.ResumeLayout(false);
            this.tabCalls.ResumeLayout(false);
            this.tabFindings.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.gridPlan)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.gridCalls)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.gridFindings)).EndInit();
            this.splitReport.Panel1.ResumeLayout(false);
            this.splitReport.Panel2.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.splitReport)).EndInit();
            this.splitReport.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.gridClaims)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.gridEvidence)).EndInit();
            this.grpPolicy.ResumeLayout(false);
            this.grpPolicy.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.numMaxSteps)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.numMaxTokens)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.numMaxSeconds)).EndInit();
            this.grpSources.ResumeLayout(false);
            ((System.ComponentModel.ISupportInitialize)(this.gridSources)).EndInit();
            this.pnlAddSource.ResumeLayout(false);
            this.pnlAddSource.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();
        }

        #endregion

        private System.Windows.Forms.StatusStrip statusStrip1;
        private System.Windows.Forms.ToolStripStatusLabel lblStatus;
        private System.Windows.Forms.TabControl tabMain;
        private System.Windows.Forms.TabPage tabSessions;
        private System.Windows.Forms.TabPage tabReport;
        private System.Windows.Forms.TabPage tabAdmin;
        private System.Windows.Forms.Panel pnlTop;
        private System.Windows.Forms.Label lblQuestion;
        private System.Windows.Forms.TextBox txtQuestion;
        private System.Windows.Forms.Button btnNew;
        private System.Windows.Forms.Button btnCancelSession;
        private System.Windows.Forms.Button btnRefresh;
        private System.Windows.Forms.CheckBox chkAuto;
        private System.Windows.Forms.SplitContainer splitSessions;
        private System.Windows.Forms.DataGridView gridSessions;
        private System.Windows.Forms.TabControl tabDetail;
        private System.Windows.Forms.TabPage tabPlan;
        private System.Windows.Forms.TabPage tabCalls;
        private System.Windows.Forms.TabPage tabFindings;
        private System.Windows.Forms.DataGridView gridPlan;
        private System.Windows.Forms.DataGridView gridCalls;
        private System.Windows.Forms.DataGridView gridFindings;
        private System.Windows.Forms.Label lblReportInfo;
        private System.Windows.Forms.TextBox txtReportBody;
        private System.Windows.Forms.SplitContainer splitReport;
        private System.Windows.Forms.Label lblClaims;
        private System.Windows.Forms.DataGridView gridClaims;
        private System.Windows.Forms.Label lblEvidence;
        private System.Windows.Forms.DataGridView gridEvidence;
        private System.Windows.Forms.GroupBox grpPolicy;
        private System.Windows.Forms.Label lblTools;
        private System.Windows.Forms.CheckedListBox clbTools;
        private System.Windows.Forms.Label lblNoWrite;
        private System.Windows.Forms.Label lblMaxSteps;
        private System.Windows.Forms.NumericUpDown numMaxSteps;
        private System.Windows.Forms.Label lblMaxTokens;
        private System.Windows.Forms.NumericUpDown numMaxTokens;
        private System.Windows.Forms.Label lblMaxSeconds;
        private System.Windows.Forms.NumericUpDown numMaxSeconds;
        private System.Windows.Forms.Button btnSavePolicy;
        private System.Windows.Forms.GroupBox grpSources;
        private System.Windows.Forms.DataGridView gridSources;
        private System.Windows.Forms.Panel pnlAddSource;
        private System.Windows.Forms.ComboBox cmbKind;
        private System.Windows.Forms.TextBox txtName;
        private System.Windows.Forms.TextBox txtUri;
        private System.Windows.Forms.Button btnAddSource;
        private System.Windows.Forms.Button btnSaveSources;
        private System.Windows.Forms.Timer timerRefresh;
    }
}
