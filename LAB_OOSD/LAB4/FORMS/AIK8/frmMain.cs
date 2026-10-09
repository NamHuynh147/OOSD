using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

using System;
using System.Windows.Forms;
using AIK08;


namespace AIK08
{
    public partial class frmMain : Form
    {
        public frmMain()
        {
            InitializeComponent();

            // Gắn sự kiện click mở các Form con tương ứng
            btnUC01.Click += (s, e) => OpenChildForm(new frmCreateRequest());
            btnUC02.Click += (s, e) => OpenChildForm(new frmTracking()); // Mở form Tiến độ / Hủy
            btnUC03.Click += (s, e) => OpenChildForm(new frmReport());
            btnUC05.Click += (s, e) => OpenChildForm(new frmConfig());   // Mở form Cấu hình
            btnUC06.Click += (s, e) => OpenChildForm(new frmAuditLog());
        }

        private void OpenChildForm(Form childForm)
        {
            pnlContent.Controls.Clear(); // Xóa nội dung cũ
            childForm.TopLevel = false;
            childForm.FormBorderStyle = FormBorderStyle.None;
            childForm.Dock = DockStyle.Fill;
            pnlContent.Controls.Add(childForm);
            childForm.Show();
        }

        private void btnUC06_Click(object sender, EventArgs e)
        {

        }
    }
}