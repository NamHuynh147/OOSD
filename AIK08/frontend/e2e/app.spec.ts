import { expect, test, type Page } from '@playwright/test';
import { E2E_API_KEY } from '../playwright.config';

const QUERY = 'Cam kết SLA của dịch vụ thanh toán là bao nhiêu?';

async function signIn(page: Page, key = E2E_API_KEY) {
  await page.goto('/');
  await page.getByLabel(/API key của máy chủ/).fill(key);
  await page.getByRole('button', { name: 'Lưu và tiếp tục' }).click();
}

async function createSession(page: Page, query = QUERY) {
  await page.getByLabel('Bạn muốn tra cứu điều gì?').fill(query);
  await page.getByRole('button', { name: /Tạo phiên tra cứu/ }).click();
}

test.describe('xác thực', () => {
  test('chưa có khóa thì hỏi khóa và không hiện không gian làm việc', async ({ page }) => {
    await page.goto('/');
    await expect(page.getByRole('heading', { name: 'Nhập API key' })).toBeVisible();
    await expect(page.getByLabel('Bạn muốn tra cứu điều gì?')).toHaveCount(0);
  });

  test('khóa sai bị báo lỗi, khóa đúng vào được', async ({ page }) => {
    await signIn(page, 'khoa-sai-khoa-sai-khoa-sai');
    await expect(page.getByRole('alert')).toContainText('Khóa không đúng');
    await page.getByLabel(/API key của máy chủ/).fill(E2E_API_KEY);
    await page.getByRole('button', { name: 'Lưu và tiếp tục' }).click();
    await expect(page.getByLabel('Bạn muốn tra cứu điều gì?')).toBeVisible();
  });
});

test.describe('luồng tra cứu', () => {
  test('tạo phiên → hoàn tất → báo cáo có trích dẫn và chuỗi băm toàn vẹn', async ({ page }) => {
    await signIn(page);
    await createSession(page);
    const card = page.locator('.query-card');
    await expect(card.getByText('Hoàn tất')).toBeVisible({ timeout: 45_000 });
    await expect(page.locator('.report-card')).toBeVisible();
    await expect(page.locator('.report-card .report-state')).toHaveText('Hoàn tất');
    await expect(page.locator('.markdown-report .cite').first()).toBeVisible();
    await expect(page.locator('.integrity.ok')).toBeVisible();
    await expect(page.locator('.evidence-card')).not.toHaveCount(0);
    await expect(page.getByRole('button', { name: 'Hủy phiên' })).toHaveCount(0); // phiên xong thì không còn nút Hủy
  });

  test('hủy phiên đang chạy → trả báo cáo một phần', async ({ page }) => {
    await signIn(page);
    await createSession(page, 'quy trình sao lưu và khôi phục dữ liệu');
    const cancel = page.getByRole('button', { name: 'Hủy phiên' });
    await expect(cancel).toBeVisible();
    await cancel.click();
    await expect(page.locator('.query-card').getByText('Đã hủy')).toBeVisible({ timeout: 45_000 });
    await expect(page.locator('.report-card')).toBeVisible();
    await expect(page.locator('.report-card .report-state')).toHaveText('Một phần');
    await expect(cancel).toHaveCount(0);
  });

  test('câu hỏi quá ngắn: nút tạo bị khóa; nội dung có HTML không được thực thi', async ({ page }) => {
    await signIn(page);
    await page.getByLabel('Bạn muốn tra cứu điều gì?').fill('ab');
    await expect(page.getByRole('button', { name: /Tạo phiên tra cứu/ })).toBeDisabled();
    let dialogs = 0;
    page.on('dialog', (d) => { dialogs += 1; void d.dismiss(); });
    await createSession(page, '<img src=x onerror=alert(1)> SLA thanh toán');
    await expect(page.locator('.query-card h4')).toContainText('<img src=x');
    await page.waitForTimeout(1500);
    expect(dialogs).toBe(0);
    expect(await page.locator('.query-card img').count()).toBe(0);
  });
});
