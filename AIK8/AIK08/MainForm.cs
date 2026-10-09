using System.Data;

namespace AIK08;

public partial class MainForm : Form
{
    // Chỉ có tool đọc; hệ thống không có write tool
    private static readonly string[] ReadTools = { "document_search", "document_read", "http_get_api" };

    private int? _sessionId;
    private bool _loading;

    public MainForm()
    {
        InitializeComponent();

        foreach (var g in new[] { gridSessions, gridPlan, gridCalls, gridFindings, gridClaims, gridEvidence })
        {
            g.DefaultCellStyle.WrapMode = DataGridViewTriState.True;
            g.AutoSizeRowsMode = DataGridViewAutoSizeRowsMode.AllCells;
        }

        clbTools.Items.AddRange(ReadTools);
        cmbKind.SelectedIndex = 0;
    }

    // ---------------------------------------------------------------- chung

    private void SetStatus(string text)
    {
        lblStatus.Text = text;
    }

    private bool Run(Action action)
    {
        try
        {
            action();
            return true;
        }
        catch (Exception ex)
        {
            SetStatus("Lỗi: " + ex.Message);
            MessageBox.Show(this, ex.Message, "Lỗi cơ sở dữ liệu", MessageBoxButtons.OK, MessageBoxIcon.Error);
            return false;
        }
    }

    private static void Highlight(DataGridView grid, string column, Func<string, bool> match, Color color)
    {
        if (!grid.Columns.Contains(column))
        {
            return;
        }

        foreach (DataGridViewRow row in grid.Rows)
        {
            var value = Convert.ToString(row.Cells[column].Value) ?? string.Empty;
            if (match(value))
            {
                row.DefaultCellStyle.BackColor = color;
            }
        }
    }

    private static void SetWeight(DataGridView grid, string column, float weight)
    {
        if (grid.Columns.Contains(column))
        {
            grid.Columns[column].FillWeight = weight;
        }
    }

    private void MainForm_Load(object sender, EventArgs e)
    {
        try { splitSessions.SplitterDistance = Math.Max(120, splitSessions.Height * 45 / 100); } catch { }
        try { splitReport.SplitterDistance = Math.Max(100, splitReport.Height * 50 / 100); } catch { }

        if (Run(() =>
            {
                LoadPolicy();
                LoadSources();
                LoadSessions();
            }))
        {
            SetStatus("Đã kết nối PostgreSQL.");
        }
    }

    private void tabMain_SelectedIndexChanged(object sender, EventArgs e)
    {
        // Lưới ở tab chưa hiển thị có thể chưa dựng xong, nạp lại khi người dùng mở tab
        if (tabMain.SelectedTab == tabReport && _sessionId.HasValue)
        {
            Run(() => LoadReport(_sessionId.Value));
        }
    }

    private void tabDetail_SelectedIndexChanged(object sender, EventArgs e)
    {
        if (_sessionId.HasValue)
        {
            Run(() => LoadDetails(_sessionId.Value));
        }
    }

    // ------------------------------------------------- tab 1: phiên tra cứu

    private void LoadSessions()
    {
        var table = Db.Query($@"
            SELECT s.id AS ""Mã"",
                   s.question AS ""Câu hỏi"",
                   {Db.StatusCase} AS ""Trạng thái"",
                   s.used_steps::text || '/' || s.max_steps::text AS ""Bước"",
                   s.used_tokens::text || '/' || s.max_tokens::text AS ""Token"",
                   s.used_seconds::text || '/' || s.max_seconds::text AS ""Giây"",
                   to_char(s.started_at, 'DD/MM/YYYY HH24:MI:SS') AS ""Bắt đầu"",
                   {Db.ReasonCase} AS ""Lý do kết thúc""
            FROM research_sessions s
            ORDER BY s.id DESC");

        _loading = true;
        try
        {
            gridSessions.DataSource = table;
            gridSessions.ClearSelection();

            var target = -1;
            if (_sessionId.HasValue)
            {
                foreach (DataGridViewRow row in gridSessions.Rows)
                {
                    if (row.Cells["Mã"].Value is int id && id == _sessionId.Value)
                    {
                        target = row.Index;
                        break;
                    }
                }
            }

            if (target < 0 && gridSessions.Rows.Count > 0)
            {
                target = 0;
            }

            if (target >= 0)
            {
                gridSessions.Rows[target].Selected = true;
                gridSessions.CurrentCell = gridSessions.Rows[target].Cells[1];
            }
        }
        finally
        {
            _loading = false;
        }

        LoadSelected();
        SetStatus($"Có {table.Rows.Count} phiên. Cập nhật lúc {DateTime.Now:HH:mm:ss}.");
    }

    private void gridSessions_DataBindingComplete(object sender, DataGridViewBindingCompleteEventArgs e)
    {
        SetWeight(gridSessions, "Mã", 18);
        SetWeight(gridSessions, "Câu hỏi", 230);
        SetWeight(gridSessions, "Trạng thái", 70);
        SetWeight(gridSessions, "Bước", 45);
        SetWeight(gridSessions, "Token", 70);
        SetWeight(gridSessions, "Giây", 45);
        SetWeight(gridSessions, "Bắt đầu", 90);
        SetWeight(gridSessions, "Lý do kết thúc", 90);
        Highlight(gridSessions, "Trạng thái", v => v == "Đang chạy", Color.FromArgb(230, 244, 255));
        Highlight(gridSessions, "Trạng thái", v => v == "Lỗi" || v == "Dừng do hạn mức", Color.FromArgb(255, 244, 224));
    }

    private void gridSessions_SelectionChanged(object sender, EventArgs e)
    {
        if (_loading)
        {
            return;
        }

        Run(LoadSelected);
    }

    private void LoadSelected()
    {
        _sessionId = null;
        var status = string.Empty;

        var current = gridSessions.CurrentRow;
        if (current != null && gridSessions.Columns.Contains("Mã") && current.Cells["Mã"].Value is int id)
        {
            _sessionId = id;
            status = Convert.ToString(current.Cells["Trạng thái"].Value) ?? string.Empty;
        }

        btnCancelSession.Enabled = _sessionId.HasValue && status == "Đang chạy";

        if (!_sessionId.HasValue)
        {
            gridPlan.DataSource = null;
            gridCalls.DataSource = null;
            gridFindings.DataSource = null;
            gridClaims.DataSource = null;
            gridEvidence.DataSource = null;
            lblReportInfo.Text = "Chọn một phiên ở tab Phiên tra cứu.";
            txtReportBody.Clear();
            return;
        }

        LoadDetails(_sessionId.Value);
        LoadReport(_sessionId.Value);
    }

    private void LoadDetails(int sessionId)
    {
        gridPlan.DataSource = Db.Query(@"
            SELECT p.position AS ""Thứ tự"",
                   p.goal AS ""Mục tiêu"",
                   CASE p.status WHEN 'pending' THEN 'Chờ' WHEN 'running' THEN 'Đang làm'
                                 WHEN 'done' THEN 'Xong' ELSE 'Bỏ qua' END AS ""Trạng thái""
            FROM plan_steps p
            WHERE p.session_id = @id
            ORDER BY p.position", Db.P("id", sessionId));

        gridCalls.DataSource = Db.Query(@"
            SELECT c.id AS ""Mã"",
                   c.tool_name AS ""Tool"",
                   c.arguments::text AS ""Tham số"",
                   CASE c.guard_decision WHEN 'allowed' THEN 'Cho phép' ELSE 'Chặn' END AS ""Guard"",
                   COALESCE(c.guard_reason, '') AS ""Lý do chặn"",
                   c.outcome AS ""Kết quả"",
                   c.duration_ms AS ""ms""
            FROM tool_calls c
            WHERE c.session_id = @id
            ORDER BY c.id", Db.P("id", sessionId));

        gridFindings.DataSource = Db.Query(@"
            SELECT f.id AS ""Mã"",
                   CASE f.kind WHEN 'not_allowlisted' THEN 'Ngoài allowlist'
                               WHEN 'budget_exceeded' THEN 'Vượt ngân sách'
                               WHEN 'injection_suspected' THEN 'Nghi injection'
                               WHEN 'unsupported_claim' THEN 'Khẳng định chưa có nguồn'
                               ELSE f.kind END AS ""Loại"",
                   CASE f.severity WHEN 'low' THEN 'Thấp' WHEN 'medium' THEN 'Trung bình' ELSE 'Cao' END AS ""Mức độ"",
                   f.detail AS ""Chi tiết""
            FROM guard_findings f
            WHERE f.session_id = @id
            ORDER BY f.id", Db.P("id", sessionId));
    }

    private void gridCalls_DataBindingComplete(object sender, DataGridViewBindingCompleteEventArgs e)
    {
        SetWeight(gridCalls, "Mã", 20);
        SetWeight(gridCalls, "Tham số", 200);
        SetWeight(gridCalls, "Lý do chặn", 120);
        SetWeight(gridCalls, "ms", 25);
        Highlight(gridCalls, "Guard", v => v == "Chặn", Color.FromArgb(255, 228, 228));
    }

    private void btnNew_Click(object sender, EventArgs e)
    {
        var question = txtQuestion.Text.Trim();
        if (question.Length == 0)
        {
            MessageBox.Show(this, "Hãy nhập câu hỏi tra cứu.", "Thiếu câu hỏi", MessageBoxButtons.OK, MessageBoxIcon.Information);
            return;
        }

        Run(() =>
        {
            // Allowlist và hạn mức được chốt theo chính sách mặc định tại thời điểm tạo phiên
            var id = Db.Scalar(@"
                INSERT INTO research_sessions (question, status, allowlist, max_steps, max_tokens, max_seconds, started_at)
                SELECT @q, 'running', p.allowlist, p.default_max_steps, p.default_max_tokens, p.default_max_seconds, now()
                FROM admin_policy p
                WHERE p.id = 1
                RETURNING id", Db.P("q", question));

            if (id == null)
            {
                throw new InvalidOperationException("Thiếu chính sách mặc định (admin_policy id=1). Hãy chạy lại db/02_seed.sql.");
            }

            Db.Exec(@"
                INSERT INTO plan_steps (session_id, position, goal, status)
                VALUES (@s, 1, 'Tách yêu cầu thành các bước tra cứu', 'pending')", Db.P("s", id));

            _sessionId = Convert.ToInt32(id);
            txtQuestion.Clear();
            LoadSessions();
            SetStatus($"Đã tạo phiên #{id}. (Bản demo chỉ ghi phiên; tiến trình agent chạy ở dịch vụ backend.)");
        });
    }

    private void btnCancelSession_Click(object sender, EventArgs e)
    {
        if (!_sessionId.HasValue)
        {
            return;
        }

        var id = _sessionId.Value;
        var confirm = MessageBox.Show(this,
            $"Hủy phiên #{id}? Kết quả đã thu thập được giữ lại trong báo cáo một phần.",
            "Hủy phiên", MessageBoxButtons.YesNo, MessageBoxIcon.Question);
        if (confirm != DialogResult.Yes)
        {
            return;
        }

        Run(() =>
        {
            // Đổi trạng thái và tạo báo cáo một phần trong cùng một câu lệnh
            var affected = Db.Exec(@"
                WITH u AS (
                    UPDATE research_sessions
                       SET status = 'cancelled', ended_at = now(), end_reason = 'user_cancelled'
                     WHERE id = @id AND status = 'running'
                 RETURNING id)
                INSERT INTO reports (session_id, body, end_reason)
                SELECT id, 'Báo cáo một phần: phiên bị người dùng hủy trước khi kết thúc.', 'user_cancelled'
                FROM u
                ON CONFLICT (session_id) DO NOTHING", Db.P("id", id));

            if (affected == 0)
            {
                MessageBox.Show(this, "Phiên không còn ở trạng thái đang chạy, không đổi gì.", "Hủy phiên",
                    MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
            else
            {
                SetStatus($"Đã hủy phiên #{id}.");
            }

            LoadSessions();
        });
    }

    private void btnRefresh_Click(object sender, EventArgs e)
    {
        Run(LoadSessions);
    }

    private void chkAuto_CheckedChanged(object sender, EventArgs e)
    {
        timerRefresh.Enabled = chkAuto.Checked;
    }

    private void timerRefresh_Tick(object sender, EventArgs e)
    {
        try
        {
            LoadSessions();
        }
        catch (Exception ex)
        {
            chkAuto.Checked = false;
            SetStatus("Đã tắt tự làm mới: " + ex.Message);
        }
    }

    // ------------------------------------- tab 2: báo cáo và truy vết nguồn

    private void LoadReport(int sessionId)
    {
        var info = Db.Query($@"
            SELECT s.id, s.question, {Db.StatusCase} AS st, {Db.ReasonCase} AS rs
            FROM research_sessions s
            WHERE s.id = @id", Db.P("id", sessionId));

        if (info.Rows.Count == 0)
        {
            return;
        }

        var row = info.Rows[0];
        var reason = Convert.ToString(row["rs"]);
        lblReportInfo.Text =
            $"Phiên #{row["id"]}: {row["question"]}{Environment.NewLine}" +
            $"Trạng thái: {row["st"]}" + (string.IsNullOrEmpty(reason) ? string.Empty : $" - Lý do kết thúc: {reason}");

        var report = Db.Query("SELECT body FROM reports WHERE session_id = @id", Db.P("id", sessionId));
        txtReportBody.Text = report.Rows.Count > 0
            ? Convert.ToString(report.Rows[0]["body"]).Replace("\r\n", "\n").Replace("\n", Environment.NewLine)
            : "(Chưa có báo cáo: phiên đang chạy hoặc chưa tổng hợp.)";

        gridClaims.DataSource = Db.Query(@"
            SELECT c.id AS ""Mã"",
                   c.position AS ""STT"",
                   c.text AS ""Khẳng định"",
                   CASE c.status WHEN 'sourced' THEN 'Có nguồn' ELSE 'Chưa có nguồn' END AS ""Trạng thái"",
                   COALESCE((SELECT string_agg('E' || ci.evidence_id::text, ', ' ORDER BY ci.evidence_id)
                             FROM citations ci WHERE ci.claim_id = c.id), '') AS ""Trích dẫn""
            FROM claims c
            JOIN reports r ON r.id = c.report_id
            WHERE r.session_id = @id
            ORDER BY c.position", Db.P("id", sessionId));

        LoadEvidenceOfCurrentClaim();
    }

    private void gridClaims_DataBindingComplete(object sender, DataGridViewBindingCompleteEventArgs e)
    {
        SetWeight(gridClaims, "Mã", 15);
        SetWeight(gridClaims, "STT", 15);
        SetWeight(gridClaims, "Khẳng định", 250);
        SetWeight(gridClaims, "Trạng thái", 50);
        SetWeight(gridClaims, "Trích dẫn", 50);
        Highlight(gridClaims, "Trạng thái", v => v == "Chưa có nguồn", Color.FromArgb(255, 244, 224));
    }

    private void gridClaims_SelectionChanged(object sender, EventArgs e)
    {
        Run(LoadEvidenceOfCurrentClaim);
    }

    private void LoadEvidenceOfCurrentClaim()
    {
        var current = gridClaims.CurrentRow;
        if (current == null || !gridClaims.Columns.Contains("Mã") || !(current.Cells["Mã"].Value is int claimId))
        {
            gridEvidence.DataSource = null;
            lblEvidence.Text = "Bằng chứng gốc của khẳng định đã chọn";
            return;
        }

        var evidence = Db.Query(@"
            SELECT e.id AS ""Mã"",
                   s.display_name AS ""Nguồn"",
                   e.locator AS ""Vị trí"",
                   e.excerpt AS ""Trích đoạn gốc"",
                   ci.matched_excerpt AS ""Đoạn khớp"",
                   to_char(e.retrieved_at, 'DD/MM/YYYY HH24:MI') AS ""Lấy lúc"",
                   CASE WHEN e.suspicious THEN 'Nghi injection' ELSE '' END AS ""Cảnh báo""
            FROM citations ci
            JOIN evidence e ON e.id = ci.evidence_id
            JOIN sources s ON s.id = e.source_id
            WHERE ci.claim_id = @c
            ORDER BY e.id", Db.P("c", claimId));

        gridEvidence.DataSource = evidence;
        lblEvidence.Text = evidence.Rows.Count == 0
            ? "Khẳng định này chưa có nguồn: không có bằng chứng để truy vết."
            : $"Bằng chứng gốc của khẳng định đã chọn ({evidence.Rows.Count})";
    }

    private void gridEvidence_DataBindingComplete(object sender, DataGridViewBindingCompleteEventArgs e)
    {
        SetWeight(gridEvidence, "Mã", 15);
        SetWeight(gridEvidence, "Nguồn", 70);
        SetWeight(gridEvidence, "Vị trí", 70);
        SetWeight(gridEvidence, "Trích đoạn gốc", 160);
        SetWeight(gridEvidence, "Đoạn khớp", 110);
        SetWeight(gridEvidence, "Lấy lúc", 55);
        SetWeight(gridEvidence, "Cảnh báo", 45);
        Highlight(gridEvidence, "Cảnh báo", v => v.Length > 0, Color.FromArgb(255, 228, 228));
    }

    // ------------------------------------------------------ tab 3: quản trị

    private void LoadPolicy()
    {
        var table = Db.Query(@"
            SELECT allowlist, default_max_steps, default_max_tokens, default_max_seconds
            FROM admin_policy WHERE id = 1");

        if (table.Rows.Count == 0)
        {
            throw new InvalidOperationException("Thiếu dòng admin_policy (id=1). Hãy chạy lại db/02_seed.sql.");
        }

        var row = table.Rows[0];
        var allow = (string[])row["allowlist"];
        for (var i = 0; i < clbTools.Items.Count; i++)
        {
            clbTools.SetItemChecked(i, allow.Contains((string)clbTools.Items[i]));
        }

        numMaxSteps.Value = Convert.ToDecimal(row["default_max_steps"]);
        numMaxTokens.Value = Convert.ToDecimal(row["default_max_tokens"]);
        numMaxSeconds.Value = Convert.ToDecimal(row["default_max_seconds"]);
    }

    private void btnSavePolicy_Click(object sender, EventArgs e)
    {
        var tools = clbTools.CheckedItems.Cast<string>().ToArray();
        if (tools.Length == 0)
        {
            MessageBox.Show(this, "Phải bật ít nhất một tool đọc.", "Chính sách", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            return;
        }

        Run(() =>
        {
            Db.Exec(@"
                UPDATE admin_policy
                   SET allowlist = @a,
                       default_max_steps = @s,
                       default_max_tokens = @t,
                       default_max_seconds = @sec
                 WHERE id = 1",
                Db.P("a", tools),
                Db.P("s", (int)numMaxSteps.Value),
                Db.P("t", (int)numMaxTokens.Value),
                Db.P("sec", (int)numMaxSeconds.Value));

            SetStatus("Đã lưu chính sách mặc định. Chỉ áp cho phiên tạo sau đó.");
        });
    }

    private void LoadSources()
    {
        gridSources.DataSource = Db.Query(@"
            SELECT s.id AS ""Mã"",
                   CASE s.kind WHEN 'document' THEN 'Tài liệu' ELSE 'API' END AS ""Loại"",
                   s.display_name AS ""Tên"",
                   s.uri AS ""Địa chỉ"",
                   s.enabled AS ""Bật""
            FROM sources s
            ORDER BY s.id");

        // Chỉ cho sửa cột "Bật"; các cột còn lại chỉ đọc
        foreach (DataGridViewColumn col in gridSources.Columns)
        {
            col.ReadOnly = col.Name != "Bật";
        }

        SetWeight(gridSources, "Mã", 15);
        SetWeight(gridSources, "Loại", 30);
        SetWeight(gridSources, "Tên", 90);
        SetWeight(gridSources, "Địa chỉ", 200);
        SetWeight(gridSources, "Bật", 20);
    }

    private void btnAddSource_Click(object sender, EventArgs e)
    {
        var name = txtName.Text.Trim();
        var uri = txtUri.Text.Trim();
        var kind = cmbKind.SelectedIndex == 0 ? "document" : "api";

        if (name.Length == 0 || uri.Length == 0)
        {
            MessageBox.Show(this, "Nhập tên hiển thị và địa chỉ của nguồn.", "Thiếu thông tin", MessageBoxButtons.OK, MessageBoxIcon.Information);
            return;
        }

        if (kind == "api" && !(uri.StartsWith("https://") || uri.StartsWith("http://")))
        {
            MessageBox.Show(this, "Địa chỉ API phải bắt đầu bằng http:// hoặc https://.", "Địa chỉ không hợp lệ", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            return;
        }

        Run(() =>
        {
            Db.Exec("INSERT INTO sources (kind, uri, display_name) VALUES (@k, @u, @n)",
                Db.P("k", kind), Db.P("u", uri), Db.P("n", name));

            txtName.Clear();
            txtUri.Clear();
            LoadSources();
            SetStatus("Đã thêm nguồn (mặc định đang bật).");
        });
    }

    private void btnSaveSources_Click(object sender, EventArgs e)
    {
        gridSources.EndEdit();
        gridSources.CommitEdit(DataGridViewDataErrorContexts.Commit);

        if (gridSources.DataSource is not DataTable table)
        {
            return;
        }

        Run(() =>
        {
            var changed = 0;
            foreach (DataRow row in table.Rows)
            {
                changed += Db.Exec("UPDATE sources SET enabled = @e WHERE id = @id AND enabled <> @e",
                    Db.P("e", Convert.ToBoolean(row["Bật"])),
                    Db.P("id", Convert.ToInt32(row["Mã"])));
            }

            LoadSources();
            SetStatus($"Đã lưu trạng thái bật/tắt, {changed} nguồn thay đổi.");
        });
    }
}
