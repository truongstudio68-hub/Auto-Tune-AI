# AutoTune AI

Project GitHub Actions để tự build file Windows `AutoTuneAI.exe`.

## Build không cần cài Python
1. Tạo repository mới trên GitHub.
2. Upload toàn bộ nội dung project.
3. Vào **Actions** → workflow **Build AutoTune AI**.
4. Chọn **Run workflow**.
5. Chờ hoàn tất → mở job → **Artifacts** → tải `AutoTuneAI-Windows`.
6. Giải nén và chạy `AutoTuneAI.exe`.

Bản này là prototype real-time: mic → dò pitch liên tục → ước lượng key/scale → pitch correction. Dùng tai nghe để tránh feedback.

Lưu ý: engine pitch-shift hiện là prototype nhẹ; để chất lượng vocal chuyên nghiệp cần DSP phase-vocoder/WSOLA tốt hơn.
