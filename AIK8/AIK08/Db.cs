using System.Data;
using Npgsql;

namespace AIK08;

/// <summary>Truy cập PostgreSQL. Mọi lệnh dùng tham số, không ghép chuỗi từ dữ liệu người dùng.</summary>
public static class Db
{
    public static string ConnectionString { get; set; }

    // Nhãn tiếng Việt cho mã trạng thái và lý do kết thúc (alias bảng: s = research_sessions)
    public const string StatusCase =
        "CASE s.status WHEN 'running' THEN 'Đang chạy' WHEN 'completed' THEN 'Hoàn tất' " +
        "WHEN 'budget_exhausted' THEN 'Dừng do hạn mức' WHEN 'cancelled' THEN 'Đã hủy' " +
        "WHEN 'error' THEN 'Lỗi' ELSE s.status END";

    public const string ReasonCase =
        "CASE s.end_reason WHEN 'enough_evidence' THEN 'Đủ bằng chứng' WHEN 'budget_steps' THEN 'Hết số bước' " +
        "WHEN 'budget_tokens' THEN 'Hết token' WHEN 'budget_seconds' THEN 'Hết thời gian' " +
        "WHEN 'user_cancelled' THEN 'Người dùng hủy' WHEN 'llm_unavailable' THEN 'LLM không phản hồi' " +
        "ELSE COALESCE(s.end_reason, '') END";

    public static string Build(string host, int port, string database, string user, string password)
    {
        var b = new NpgsqlConnectionStringBuilder
        {
            Host = host,
            Port = port,
            Database = database,
            Username = user,
            Password = password,
            Timeout = 5,
            CommandTimeout = 15,
            ApplicationName = "AIK08 WinForms"
        };
        return b.ConnectionString;
    }

    public static NpgsqlParameter P(string name, object value)
    {
        return new NpgsqlParameter(name, value ?? DBNull.Value);
    }

    public static DataTable Query(string sql, params NpgsqlParameter[] parameters)
    {
        using var conn = new NpgsqlConnection(ConnectionString);
        conn.Open();
        using var cmd = new NpgsqlCommand(sql, conn);
        if (parameters != null && parameters.Length > 0)
        {
            cmd.Parameters.AddRange(parameters);
        }
        using var adapter = new NpgsqlDataAdapter(cmd);
        var table = new DataTable();
        adapter.Fill(table);
        return table;
    }

    public static int Exec(string sql, params NpgsqlParameter[] parameters)
    {
        using var conn = new NpgsqlConnection(ConnectionString);
        conn.Open();
        using var cmd = new NpgsqlCommand(sql, conn);
        if (parameters != null && parameters.Length > 0)
        {
            cmd.Parameters.AddRange(parameters);
        }
        return cmd.ExecuteNonQuery();
    }

    public static object Scalar(string sql, params NpgsqlParameter[] parameters)
    {
        using var conn = new NpgsqlConnection(ConnectionString);
        conn.Open();
        using var cmd = new NpgsqlCommand(sql, conn);
        if (parameters != null && parameters.Length > 0)
        {
            cmd.Parameters.AddRange(parameters);
        }
        var value = cmd.ExecuteScalar();
        return value is DBNull ? null : value;
    }

    /// <summary>Thử kết nối và kiểm tra đã có lược đồ và dữ liệu mẫu chưa.</summary>
    public static (bool ok, string message) Test(string connectionString)
    {
        try
        {
            using var conn = new NpgsqlConnection(connectionString);
            conn.Open();

            using var check = new NpgsqlCommand(
                "SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'research_sessions'",
                conn);
            var hasSchema = Convert.ToInt32(check.ExecuteScalar()) > 0;
            if (!hasSchema)
            {
                return (false, "Kết nối được nhưng chưa có lược đồ. Chạy db/01_schema.sql rồi db/02_seed.sql.");
            }

            using var count = new NpgsqlCommand("SELECT count(*) FROM research_sessions", conn);
            var n = Convert.ToInt32(count.ExecuteScalar());
            return (true, $"Kết nối thành công, có {n} phiên trong cơ sở dữ liệu.");
        }
        catch (Exception ex)
        {
            return (false, "Không kết nối được: " + ex.Message);
        }
    }
}
