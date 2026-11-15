import { defineConfig } from "@playwright/test";

declare const process: { env: Record<string, string | undefined> };

// Chạy: cần PostgreSQL đã migrate + seed và các biến *_DATABASE_URL trong môi trường (xem README).
// Backend và UI do cấu hình này tự dựng; khóa API và độ trễ mock chỉ dùng cho e2e.
export const E2E_API_KEY = "e2e-key-0123456789abcdef";
const python = process.env.E2E_PYTHON || "python";

export default defineConfig({
  testDir: "./e2e",
  timeout: 60_000,
  expect: { timeout: 30_000 },
  workers: 1,
  reporter: [["list"]],
  use: { baseURL: "http://127.0.0.1:5173", trace: "retain-on-failure" },
  webServer: [
    {
      command: `${python} -m uvicorn app.api.main:app --host 127.0.0.1 --port 8000`,
      cwd: "../backend",
      url: "http://127.0.0.1:8000/health",
      reuseExistingServer: false,
      env: {
        ...(process.env as Record<string, string>),
        API_KEYS: E2E_API_KEY,
        LLM_PROVIDER: "mock",
        MOCK_LLM_DELAY_SECONDS: "1.5",
        RECOVER_ON_START: "false",
        API_AUTH_DISABLED: "false",
      },
    },
    {
      command: "npm run build && npm run preview -- --port 5173 --strictPort",
      url: "http://127.0.0.1:5173",
      reuseExistingServer: false,
      timeout: 120_000,
    },
  ],
});
