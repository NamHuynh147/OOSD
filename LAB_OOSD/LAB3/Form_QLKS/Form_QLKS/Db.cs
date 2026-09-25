using System.Data;
using Microsoft.Data.SqlClient;

namespace Form_QLKS
{
    public static class Db
    {
        private static readonly string connectionString =
            @"Server=MSI\MSSQLSERVER03;
              Database=QuanLyKhachSan;
              Trusted_Connection=True;
              TrustServerCertificate=True;";

        // Lấy dữ liệu dạng DataTable
        public static DataTable Query(string sql)
        {
            DataTable table = new DataTable();

            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                conn.Open();

                using (SqlCommand cmd = new SqlCommand(sql, conn))
                {
                    using (SqlDataAdapter adapter = new SqlDataAdapter(cmd))
                    {
                        adapter.Fill(table);
                    }
                }
            }

            return table;
        }

        // Giữ hàm này để tương thích với các form đang dùng Db.GetData(...)
        public static DataTable GetData(string sql)
        {
            return Query(sql);
        }

        // INSERT / UPDATE / DELETE
        public static int Execute(
            string sql,
            params SqlParameter[] parameters)
        {
            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                conn.Open();

                using (SqlCommand cmd = new SqlCommand(sql, conn))
                {
                    if (parameters != null && parameters.Length > 0)
                    {
                        cmd.Parameters.AddRange(parameters);
                    }

                    return cmd.ExecuteNonQuery();
                }
            }
        }
    }
}