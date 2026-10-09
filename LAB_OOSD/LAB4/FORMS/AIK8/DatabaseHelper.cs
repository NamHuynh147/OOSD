using Npgsql;
using System;
using System.Data;
using System.Windows.Forms;

namespace AIK08
{
    public static class DatabaseHelper
    {
        public static readonly string ConnectionString = "Host=localhost;Port=5432;Username=postgres;Password=123456;Database=aik08_db";

        public static bool TestConnection()
        {
            try
            {
                using (var conn = new NpgsqlConnection(ConnectionString))
                {
                    conn.Open();
                    return true;
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Lỗi kết nối cơ sở dữ liệu: " + ex.Message, "Thông báo", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return false;
            }
        }

        public static DataTable ExecuteQuery(string query, params NpgsqlParameter[] parameters)
        {
            using (var conn = new NpgsqlConnection(ConnectionString))
            {
                using (var cmd = new NpgsqlCommand(query, conn))
                {
                    if (parameters != null) cmd.Parameters.AddRange(parameters);
                    var dt = new DataTable();
                    new NpgsqlDataAdapter(cmd).Fill(dt);
                    return dt;
                }
            }
        }

        public static int ExecuteNonQuery(string query, params NpgsqlParameter[] parameters)
        {
            using (var conn = new NpgsqlConnection(ConnectionString))
            {
                conn.Open();
                using (var cmd = new NpgsqlCommand(query, conn))
                {
                    if (parameters != null) cmd.Parameters.AddRange(parameters);
                    return cmd.ExecuteNonQuery();
                }
            }
        }
    }
}