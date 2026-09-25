using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using System.Data;
using Microsoft.Data.SqlClient;

namespace Form_QLKS
{
    public static class Db
    {
        private static readonly string connectionString =
            @"Server= MSI\MSSQLSERVER03;
              Database=QuanLyKhachSan;
              Trusted_Connection=True;
              TrustServerCertificate=True;";

        public static DataTable Query(string sql)
        {
            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                conn.Open();

                using (SqlCommand cmd = new SqlCommand(sql, conn))
                {
                    using (SqlDataAdapter adapter =
                           new SqlDataAdapter(cmd))
                    {
                        DataTable table = new DataTable();

                        adapter.Fill(table);

                        return table;
                    }
                }
            }
        }

        public static int Execute(
            string sql,
            params SqlParameter[] parameters)
        {
            using (SqlConnection conn = new SqlConnection(connectionString))
            {
                conn.Open();

                using (SqlCommand cmd = new SqlCommand(sql, conn))
                {
                    if (parameters != null)
                    {
                        cmd.Parameters.AddRange(parameters);
                    }

                    return cmd.ExecuteNonQuery();
                }
            }
        }
    }
}
