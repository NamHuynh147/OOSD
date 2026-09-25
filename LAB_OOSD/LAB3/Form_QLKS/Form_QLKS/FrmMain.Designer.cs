using System.Drawing.Printing;
using System.Windows.Forms;
using System.Xml.Linq;
using static System.Net.Mime.MediaTypeNames;
using Font = System.Drawing.Font;

namespace Form_QLKS
{
    partial class Form1
    {
        private System.ComponentModel.IContainer components = null;

        private System.Windows.Forms.Label lblTitle;

        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }

            base.Dispose(disposing);
        }

        private void InitializeComponent()
        {
            lblTitle = new Label();
            hsa = new Button();
            phongTienNghi = new Button();
            button2 = new Button();
            button3 = new Button();
            button1 = new Button();
            button4 = new Button();
            button5 = new Button();
            SuspendLayout();
            // 
            // lblTitle
            // 
            lblTitle.AutoSize = true;
            lblTitle.Font = new Font("Arial", 20F, FontStyle.Bold);
            lblTitle.ForeColor = Color.FromArgb(0, 70, 130);
            lblTitle.Location = new Point(313, 31);
            lblTitle.Name = "lblTitle";
            lblTitle.Size = new Size(572, 40);
            lblTitle.TabIndex = 0;
            lblTitle.Text = "HỆ THỐNG QUẢN LÝ KHÁCH SẠN";
            lblTitle.Click += lblTitle_Click;
            // 
            // hsa
            // 
            hsa.Font = new Font("Segoe UI", 13.8F);
            hsa.Location = new Point(127, 145);
            hsa.Name = "hsa";
            hsa.Size = new Size(193, 70);
            hsa.TabIndex = 1;
            hsa.Text = "Danh mục";
            hsa.UseVisualStyleBackColor = true;
            hsa.Click += hsa_Click;
            // 
            // phongTienNghi
            // 
            phongTienNghi.Font = new Font("Segoe UI", 13.8F);
            phongTienNghi.Location = new Point(352, 281);
            phongTienNghi.Name = "phongTienNghi";
            phongTienNghi.Size = new Size(376, 82);
            phongTienNghi.TabIndex = 1;
            phongTienNghi.Text = "Trả phòng - thanh toán";
            phongTienNghi.UseVisualStyleBackColor = true;
            phongTienNghi.Click += hsa_Click;
            // 
            // button2
            // 
            button2.Font = new Font("Segoe UI", 13.8F);
            button2.Location = new Point(352, 145);
            button2.Name = "button2";
            button2.Size = new Size(376, 70);
            button2.TabIndex = 1;
            button2.Text = "Phòng -Tiện nghi";
            button2.UseVisualStyleBackColor = true;
            button2.Click += hsa_Click;
            // 
            // button3
            // 
            button3.Font = new Font("Segoe UI", 13.8F);
            button3.Location = new Point(127, 281);
            button3.Name = "button3";
            button3.Size = new Size(193, 82);
            button3.TabIndex = 1;
            button3.Text = "Sử dụng dịch vụ";
            button3.UseVisualStyleBackColor = true;
            button3.Click += hsa_Click;
            // 
            // button1
            // 
            button1.Font = new Font("Segoe UI", 13.8F);
            button1.Location = new Point(780, 145);
            button1.Name = "button1";
            button1.Size = new Size(376, 70);
            button1.TabIndex = 1;
            button1.Text = "Đặt/Nhận phòng";
            button1.UseVisualStyleBackColor = true;
            button1.Click += hsa_Click;
            // 
            // button4
            // 
            button4.Font = new Font("Segoe UI", 13.8F);
            button4.Location = new Point(780, 281);
            button4.Name = "button4";
            button4.Size = new Size(376, 82);
            button4.TabIndex = 1;
            button4.Text = "Thống kê 📋";
            button4.UseVisualStyleBackColor = true;
            button4.Click += hsa_Click;
            // 
            // button5
            // 
            button5.Font = new Font("Segoe UI", 13.8F);
            button5.Location = new Point(352, 412);
            button5.Name = "button5";
            button5.Size = new Size(376, 82);
            button5.TabIndex = 1;
            button5.Text = "Thoát";
            button5.UseVisualStyleBackColor = true;
            button5.Click += hsa_Click;
            // 
            // Form1
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = Color.White;
            ClientSize = new Size(1266, 538);
            Controls.Add(button3);
            Controls.Add(button1);
            Controls.Add(button2);
            Controls.Add(button4);
            Controls.Add(button5);
            Controls.Add(phongTienNghi);
            Controls.Add(hsa);
            Controls.Add(lblTitle);
            Margin = new Padding(3, 4, 3, 4);
            Name = "Form1";
            StartPosition = FormStartPosition.CenterScreen;
            Text = "Quản lý khách sạn";
            ResumeLayout(false);
            PerformLayout();
        }

        private void TaoButton(
            System.Windows.Forms.Button button,
            string text,
            int x,
            int y)
        {
            button.Location = new System.Drawing.Point(x, y);

            button.Size =
                new System.Drawing.Size(210, 65);

            button.Text = text;

            button.Font =
                new System.Drawing.Font("Arial", 11F);

            button.BackColor =
                System.Drawing.Color.White;

            button.FlatStyle =
                System.Windows.Forms.FlatStyle.Standard;

            button.UseVisualStyleBackColor = true;
        }
        private Button hsa;
        private Button phongTienNghi;
        private Button button2;
        private Button button3;
        private Button button1;
        private Button button4;
        private Button button5;
    }
}