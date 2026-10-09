namespace AIK08;

internal static class Program
{
    [STAThread]
    private static void Main()
    {
        ApplicationConfiguration.Initialize();

        // Bước 1: hỏi thông tin kết nối và thử kết nối PostgreSQL
        using (var login = new ConnectionForm())
        {
            if (login.ShowDialog() != DialogResult.OK)
            {
                return;
            }
        }

        // Bước 2: mở màn hình chính
        Application.Run(new MainForm());
    }
}
