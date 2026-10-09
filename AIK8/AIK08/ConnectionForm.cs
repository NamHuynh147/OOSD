namespace AIK08;

public partial class ConnectionForm : Form
{
    public ConnectionForm()
    {
        InitializeComponent();
        AcceptButton = btnConnect;
        CancelButton = btnExit;
    }

    private void btnConnect_Click(object sender, EventArgs e)
    {
        var cs = Db.Build(
            txtHost.Text.Trim(),
            (int)numPort.Value,
            txtDatabase.Text.Trim(),
            txtUser.Text.Trim(),
            txtPassword.Text);

        btnConnect.Enabled = false;
        lblResult.ForeColor = SystemColors.ControlText;
        lblResult.Text = "Đang kết nối...";
        Cursor = Cursors.WaitCursor;
        Refresh();

        (bool ok, string message) result;
        try
        {
            result = Db.Test(cs);
        }
        finally
        {
            Cursor = Cursors.Default;
            btnConnect.Enabled = true;
        }

        if (result.ok)
        {
            Db.ConnectionString = cs;
            DialogResult = DialogResult.OK;
            Close();
        }
        else
        {
            lblResult.ForeColor = Color.Firebrick;
            lblResult.Text = result.message;
        }
    }
}
