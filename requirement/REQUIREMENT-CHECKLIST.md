# Requirement checklist - CS420 Seminar S06

Chủ đề: **Diffusion Models: From Adding Noise to Generating Images** (Generative AI).

Nguồn: [AI 24A Seminar Topics.pdf](<AI 24A Seminar Topics.pdf>), 4 trang, mục I-VII.
Checklist diễn giải yêu cầu bằng tiếng Việt; số mục/trang dưới mỗi requirement giúp tra ngược về đề gốc.

## Cách cập nhật

- Đổi `- [ ]` thành `- [x]` khi đã kiểm tra requirement đạt yêu cầu.
- Điền vị trí minh chứng (file, section, trang, slide), nhận xét và việc cần làm vào khối dưới từng mục. Có thể thêm dòng tùy ý.
- Mọi ô ban đầu đều để trống để bạn tự đánh giá; đây không phải kết quả audit báo cáo hiện tại.
- Với mục tùy chọn/khuyến nghị không thực hiện, giữ ô trống và ghi rõ “Bỏ qua” cùng lý do trong comment.
- Phần rubric dùng để tự đánh giá chất lượng, có thể dùng lại minh chứng của các mục trước; không phải các đầu ra bổ sung.

## Ghi chú về định dạng hiện tại của repo

Đề gốc yêu cầu **tiếng Việt, A4**. Theo quyết định đã ghi trong `AGENTS.md`, repo hiện dùng **tiếng Anh, template ICCV 2025, US Letter** theo yêu cầu người dùng. Đây là khác biệt cần theo dõi, không phải xác nhận giảng viên đã chấp thuận. Checklist giữ nguyên yêu cầu gốc ở REPORT-04/05 để bạn tự ghi nhận cách xử lý.

**Comment chung về định dạng:**

> Quyết định / căn cứ:
>
> Ghi chú thêm:
>

## 1. Mục tiêu học tập

- [ ] **OBJ-01 | Bắt buộc** - Giải thích forward noising, reverse denoising và vì sao latent diffusion giảm nhu cầu tính toán.

  Nguồn: I, trang 1.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

- [ ] **OBJ-02 | Bắt buộc** - Trả lời câu hỏi định hướng: Học cách loại bỏ nhiễu giúp mô hình tạo ảnh mới như thế nào?

  Nguồn: I, trang 1.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

## 2. Sáu nhiệm vụ nội dung

- [ ] **TASK-01 | Bắt buộc** - Phân biệt mô hình generative và discriminative; so sánh định tính GAN, autoregressive và diffusion.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

- [ ] **TASK-02 | Bắt buộc** - Giải thích forward process, lịch β, Gaussian noise, reverse process, noise predictor và sampling.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

- [ ] **TASK-03 | Bắt buộc** - Vẽ sơ đồ thể hiện cả chiều thêm nhiễu và chiều khử nhiễu.

  Nguồn: II.2 và IV, trang 1-2.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

- [ ] **TASK-04 | Bắt buộc** - Tính tay đầy đủ một bước forward noising một chiều: chọn x₀, β, ε; định nghĩa ký hiệu; diễn giải kỳ vọng của quá trình ngẫu nhiên.

  Nguồn: II.3, trang 1.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

- [ ] **TASK-05 | Bắt buộc** - Minh họa một ảnh nhỏ tại 5 mức nhiễu tăng dần; kích thước 28 × 28 là ví dụ, không phải kích thước bắt buộc.

  Nguồn: II.4 và IV, trang 1-2.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

- [ ] **TASK-06 | Tùy chọn** - Nếu đủ tài nguyên, minh họa khử nhiễu hoặc sinh ảnh bằng một mô hình pretrained nhỏ; không bắt buộc huấn luyện. Ví dụ sinh ảnh là đầu ra nếu có.

  Nguồn: II.4 và IV, trang 1-2.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

- [ ] **TASK-07 | Bắt buộc** - Giải thích latent diffusion: VAE encoder/decoder, thao tác trong latent space và cross-attention conditioning.

  Nguồn: II.5, trang 1.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

- [ ] **TASK-08 | Bắt buộc** - Minh họa pipeline latent diffusion bằng sơ đồ.

  Nguồn: II.5, trang 1.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

- [ ] **TASK-09 | Bắt buộc** - Thảo luận tốc độ sampling, chất lượng và khả năng điều khiển bằng prompt.

  Nguồn: II.6, trang 1.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

- [ ] **TASK-10 | Bắt buộc** - Thảo luận hạn chế liên quan đến dữ liệu huấn luyện, bản quyền và bias.

  Nguồn: II.6, trang 1.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

- [ ] **TASK-11 | Bắt buộc** - So sánh một cấu hình latent diffusion với pixel-space diffusion theo các tiêu chí rõ ràng và có bằng chứng hỗ trợ.

  Nguồn: II.6, IV và VI, trang 1-2.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

## 3. Phương trình và diễn giải

- [ ] **EQ-01 | Bắt buộc** - Trình bày và giải thích Gaussian forward transition: q(xₜ | xₜ₋₁) = N(√(1 − βₜ)xₜ₋₁, βₜI).

  Nguồn: III, trang 1.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

- [ ] **EQ-02 | Bắt buộc** - Trình bày và giải thích simplified noise-prediction loss: L_simple = E_{t,x₀,ε}[‖ε − ε_θ(xₜ,t)‖²].

  Nguồn: III, trang 1.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

- [ ] **EQ-03 | Bắt buộc** - Định nghĩa mọi ký hiệu; nêu đơn vị/miền giá trị phù hợp và các giả định mô hình.

  Nguồn: III, trang 1.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

- [ ] **EQ-04 | Bắt buộc** - Có ví dụ tính toán hoàn chỉnh, giải từng bước; có thể dùng lại ví dụ ở TASK-04.

  Nguồn: III, trang 1.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

## 4. Đọc và tổng hợp tài liệu

- [ ] **PAPER-01 | Bắt buộc** - Đọc Ho, Jain & Abbeel (2020), Denoising Diffusion Probabilistic Models (NeurIPS); tập trung forward noising, reverse denoising và noise-prediction objective.

  Nguồn: V và VI, trang 2.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

- [ ] **PAPER-02 | Khuyến nghị** - Đọc Rombach et al. (2022), High-Resolution Image Synthesis With Latent Diffusion Models (CVPR, tr. 10684-10695); tập trung khác biệt latent-space và pixel-space diffusion.

  Nguồn: V, trang 2.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

- [ ] **PAPER-03 | Bắt buộc** - Giải thích bằng lời của nhóm; phân biệt kết quả trong paper với ví dụ/thí nghiệm do nhóm thực hiện.

  Nguồn: VI, trang 2.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

## 5. Báo cáo và chuẩn bị

- [ ] **REPORT-01 | Khuyến nghị** - Nhóm 3 sinh viên.

  Nguồn: VI, trang 2.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

- [ ] **REPORT-02 | Khuyến nghị** - Thời gian chuẩn bị khoảng 2 tuần sau khi được giao đề tài.

  Nguồn: VI, trang 2.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

- [ ] **REPORT-03 | Bắt buộc** - Báo cáo dạng research-style dài 6-10 trang, không tính tài liệu tham khảo và phụ lục.

  Nguồn: VI, trang 2.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

- [ ] **REPORT-04 | Bắt buộc theo đề gốc** - Báo cáo bằng tiếng Việt. Xem ghi chú khác biệt với lựa chọn hiện tại của repo ở đầu file.

  Nguồn: VI, trang 2.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

- [ ] **REPORT-05 | Bắt buộc theo đề gốc** - Báo cáo dùng khổ A4. Xem ghi chú khác biệt với lựa chọn hiện tại của repo ở đầu file.

  Nguồn: VI, trang 2.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

- [ ] **REPORT-06 | Bắt buộc** - Có các phần: Abstract, Introduction, Background/Paper Review, Method/Worked Example, Results and Discussion, Conclusion, References.

  Nguồn: VI, trang 2.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

- [ ] **REPORT-07 | Bắt buộc** - Có đủ ví dụ số tính tay, mô hình minh họa và so sánh có bằng chứng; không được xem việc không làm thí nghiệm lập trình là miễn các đầu ra này.

  Nguồn: VI, trang 2.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

- [ ] **REPORT-08 | Khuyến khích** - Thực hiện thí nghiệm bằng lập trình nếu phù hợp; đề không bắt buộc thí nghiệm lập trình nói chung.

  Nguồn: VI, trang 2.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

- [ ] **REPORT-09 | Bắt buộc** - Trích dẫn mọi hình, bảng, dataset, phương trình và công cụ AI đã sử dụng.

  Nguồn: VI, trang 3.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

- [ ] **REPORT-10 | Bắt buộc** - Kiểm chứng độc lập mọi nhận định được gợi ý bởi nội dung do AI tạo.

  Nguồn: VI, trang 3.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

## 6. Slides, trình bày và Q&A

- [ ] **TALK-01 | Bắt buộc** - Chuẩn bị 8-12 slides nội dung.

  Nguồn: VI, trang 2.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

- [ ] **TALK-02 | Bắt buộc** - Thuyết trình trong 15 phút; dành khoảng 5 phút cho Q&A.

  Nguồn: VI, trang 2.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

- [ ] **TALK-03 | Bắt buộc** - Mỗi thành viên đều tham gia thuyết trình và trả lời ít nhất 1 câu hỏi.

  Nguồn: VI, trang 2.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

## 7. Tự đánh giá theo rubric (100 điểm)

- [ ] **RUBRIC-01 | 5 điểm** - Problem statement and objectives: có bối cảnh phù hợp, câu hỏi nghiên cứu rõ ràng và phạm vi thích hợp.

  Nguồn: VII, trang 3.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

- [ ] **RUBRIC-02 | 15 điểm** - Reading and synthesis of research papers: giải thích chính xác mục tiêu, đóng góp, phương pháp và kết quả của paper gốc; đối chiếu nguồn phù hợp.

  Nguồn: VII, trang 3.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

- [ ] **RUBRIC-03 | 15 điểm** - Explanation of algorithms and equations: định nghĩa biến/giả định, mô tả các bước thuật toán, có ít nhất một ví dụ số hoặc sơ đồ đúng.

  Nguồn: VII, trang 3.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

- [ ] **RUBRIC-04 | 10 điểm** - Evidence, comparison, or experimentation: có baseline hoặc nguồn tham chiếu phù hợp; dữ liệu/ví dụ kiểm chứng được; giải thích rõ hình và bảng.

  Nguồn: VII, trang 3.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

- [ ] **RUBRIC-05 | 10 điểm** - Critical analysis and limitations: phân tích điểm mạnh, điểm yếu và điều kiện áp dụng; không phóng đại kết luận từ minh họa nhỏ.

  Nguồn: VII, trang 3.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

- [ ] **RUBRIC-06 | 10 điểm** - Slide quality and citations: 8-12 slides rõ ràng, dễ đọc; trích nguồn hình, phương trình và paper liên quan; tránh sao chép nguyên văn.

  Nguồn: VII, trang 3.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

- [ ] **RUBRIC-07 | 15 điểm** - Seminar presentation: trình bày mạch lạc trong 15 phút, giải thích ví dụ rõ ràng và phân chia phần trình bày cân đối.

  Nguồn: VII, trang 3.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

- [ ] **RUBRIC-08 | 20 điểm** - Q&A and critical discussion: trả lời chính xác, giải thích được quyết định kỹ thuật; mỗi thành viên trả lời ít nhất một câu hỏi.

  Nguồn: VII, trang 3.

  > Minh chứng / vị trí:
  >
  > Comment:
  >
  >
  > Việc cần làm / người phụ trách:
  >

### Mức đánh giá rubric

Theo trang 4: **Excellent = 100%**, **Good = 75%**, **Satisfactory = 50%**, **Unsatisfactory = 0-25%** số điểm của từng tiêu chí, tùy chất lượng minh chứng.

Điểm tự đánh giá: …… / 100.

Comment tổng thể:

>
>
>
