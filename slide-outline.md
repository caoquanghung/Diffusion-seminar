# Đề xuất nội dung 12 slide — Diffusion Models: From Adding Noise to Generating Images

Nguồn: [report.tex](iccv-diffusion-report/content/report.tex), [KeyQuestions.md](KeyQuestions.md), [REQUIREMENT-CHECKLIST.md](requirement/REQUIREMENT-CHECKLIST.md).
Ngôn ngữ: phần giải thích bằng tiếng Việt; **text trên slide đề xuất để tiếng Anh** cho khớp report (đúng quyết định trong AGENTS.md). Đổi sang tiếng Việt nếu giảng viên yêu cầu.

---

## 0. Nguyên tắc xây dựng

**Learning objective (LO):** Explain forward noising and reverse denoising, including why latent diffusion reduces computational demands.
**Guiding question (GQ):** How can learning to remove noise enable a model to generate new images?

LO tách thành 3 vế → mỗi vế là một "chương" của bài nói, GQ là sợi chỉ xuyên suốt và được trả lời tường minh ở slide 6 và 12:

| Chương | Slide | Vế của LO |
|---|---|---|
| Mở đầu | 1–2 | Đặt GQ, định vị diffusion |
| A. Forward noising | 3–4 | "forward noising" |
| B. Reverse denoising | 5–6 | "reverse denoising" + trả lời GQ (có bằng chứng quỹ đạo) |
| C. Latent diffusion | 7–9 | "why latent diffusion reduces computational demands": autoencoder → chi phí/pipeline → điều kiện hóa |
| D. Bằng chứng & giới hạn | 10–11 | Kiểm chứng bằng thí nghiệm của nhóm, không phóng đại |
| Kết | 12 | Quay lại GQ |

**Quy tắc cho mỗi slide:**
- Mỗi slide có **một thông điệp** (dòng "Takeaway") và nối được về LO hoặc GQ ("GQ hook").
- Chỉ giữ phương trình bắt buộc (EQ-01, EQ-02) + vài công thức nhỏ; phần chứng minh (variational bound, score, Appendix) để Q&A.
- Phân biệt rõ **"Paper reports"** và **"Our run"** (PAPER-03) bằng nhãn/màu trên slide.
- 15 phút / 12 slide ≈ 75 giây/slide; slide 1, 11, 12 ngắn hơn, slide 6, 7, 9 dài hơn.

**Gợi ý chia người nói (3 thành viên, TALK-03):** A: slide 1–4 · B: slide 5–8 · C: slide 9–12. Mỗi người có phần Q&A riêng ở Phụ lục C.

---

## Slide 1 — Title + Guiding question  *(~45s)*

**Takeaway:** Hôm nay ta trả lời một câu hỏi: *học khử nhiễu thì sao tạo được ảnh mới?*

**Nội dung slide**
- Title: *Diffusion Models: From Adding Noise to Generating Images*; tên nhóm, CS420, HCMUS.
- Hộp lớn: **Guiding question** — "How can learning to remove noise enable a model to generate new images?"
- Roadmap 4 ô ngang, nối với LO: **Forward noising → Reverse denoising → Latent diffusion → Evidence & limits**.
- Hai paper trọng tâm: DDPM (Ho et al., 2020), LDM (Rombach et al., 2022).

**Hình:** `figures/diffusion_overview/state_0 … state_1000.png` làm dải ảnh mờ dần ở dưới title (gợi ý hướng "ảnh → nhiễu").

**Speaker note:** Một câu hook: "Bộ khử nhiễu sửa một ảnh có sẵn; bộ sinh ảnh phải tạo ra ảnh *chưa từng tồn tại*. Cầu nối giữa hai việc đó là gì?"

---

## Slide 2 — Where diffusion fits: generative vs discriminative, GAN / AR / diffusion  *(~70s)*

**Takeaway:** Diffusion không học ranh giới giữa các lớp mà học *cấu trúc thống kê của ảnh*, bằng cách đảo ngược một quá trình làm hỏng ảnh đã biết.

**Nội dung slide**
- Trái: **Discriminative** learns p(y | x) — "is it a cat?" vs **Generative** learns p(x) or p(x | y) — shape, texture, lighting, layout → needs richer information.
- Phải: bảng 3 hàng so sánh định tính (TASK-01):

| Family | How it generates | Sampling | Training |
|---|---|---|---|
| GAN | Generator maps noise → image; discriminator judges | ~1 network pass | Balance two competing networks |
| Autoregressive | One pixel/token at a time | Sequential, can be slow | Explicit factorization |
| **Diffusion** | Denoise a random state over many steps | Many network evaluations | Simple regression target (noise) |

- Dòng cuối: *Cost of diffusion = many sampling steps and a big state per step* → quay lại ở slide 8.

**Hình:** Fig. "families" ở Appendix report (nếu muốn thay bảng bằng sơ đồ). Slide này chỉ để định vị.

**Cắt bớt:** lịch sử Sohl-Dickstein 2015 / Song & Ermon 2019 chỉ nhắc 1 dòng timeline nhỏ ("2015 framework → 2019 score → 2020 DDPM → 2022 LDM").

---

## Slide 3 — Forward noising: destroying structure with a known process  *(~90s)*

**Takeaway:** Forward process là **đã biết, không cần học** → cho ta cặp (ảnh nhiễu, nhiễu đã thêm) ở *mọi* mức nhiễu để huấn luyện.

**Nội dung slide**
- Sơ đồ nửa trên của Fig. `ddpm` (xanh): x₀ → x₁ → … → x_T, nhãn "clean data" → "nearly noise".
- Công thức (EQ-01), kèm chú thích từng ký hiệu:
  - q(xₜ | xₜ₋₁) = 𝒩(√(1−βₜ) xₜ₋₁ , βₜ I)
  - xₜ = √(1−βₜ) xₜ₋₁ + √βₜ ε, ε ~ 𝒩(0, I)
  - β_t ∈ (0,1): variance schedule; α_t = 1−β_t; ᾱ_t = ∏ α_j
- **Closed form (jump to any t):** xₜ = √ᾱₜ x₀ + √(1−ᾱₜ) ε — "no need to run t steps".
- Ba bullet ý nghĩa:
  1. β_t vừa *làm yếu tín hiệu* (√(1−β_t)) vừa *đặt độ lớn nhiễu* (√β_t).
  2. 𝒩(0, I) là điểm dừng: giữ nguyên phương sai → sau T bước ≈ standard normal → ta biết điểm xuất phát khi sinh ảnh.
  3. Schedule trong DDPM: T = 1000, β tuyến tính 10⁻⁴ → 0.02.

**Câu hỏi dẫn (callout cuối slide): "Why corrupt in T = 1000 small steps instead of one big step?"**
- *Short answer trên slide (2 ý):*
  1. **Small steps keep the reverse step easy.** Mỗi bước thêm nhiễu rất nhỏ (β_t ≤ 0.02) nên bước ngược p(x_{t−1} | x_t) xấp xỉ Gaussian và chỉ cần sửa nhẹ — mạng chỉ phải học "bớt một chút nhiễu".
  2. **Every noise level becomes a training task.** Từ gần-sạch (t nhỏ) đến gần-nhiễu (t lớn), mạng học cả chi tiết mịn lẫn bố cục thô. *(Diễn giải của nhóm, report không viết rõ — nên tự kiểm chứng trước khi nói.)*
- *Nếu bị hỏi "one step cũng nhảy thẳng tới x_T được mà":* đúng — closed form cho phép **huấn luyện không cần chạy T bước**. T bước không tốn thêm chi phí lúc training; chi phí chỉ xuất hiện lúc **sampling** (T lần gọi mạng). Một bước nhiễu duy nhất vẫn cho ra nhiễu thuần, nhưng bước ngược tương ứng là "nhiễu → ảnh" trong một lần, tức là bài toán ở slide 6.
- Chỉ trả lời ngắn ở slide 3; **phần "tại sao reverse một bước thất bại" để slide 6 giải thích đầy đủ**.

**GQ hook:** "A known corruption = free supervised training data."

**Lưu ý trình bày:** nói rõ t là chỉ số bước, không phải thời gian vật lý; ε^(t) (nhiễu từng bước) khác ε (nhiễu gộp).

---

## Slide 4 — Forward noising by hand and by eye (worked examples)  *(~80s)*

**Takeaway:** Cùng một công thức, nhìn bằng số (1 chiều) và bằng ảnh (5 mức nhiễu).

**Nội dung slide — chia đôi**

*Trái — 1-D calculation (TASK-04, EQ-04):* chọn x₀ = 0.8, β₁ = 0.1, ε = −0.5
- α₁ = 0.9
- √α₁·x₀ = 0.758947
- √β₁·ε = −0.158114
- **x₁ = 0.600833**
- Diễn giải: q(x₁ | x₀ = 0.8) = 𝒩(0.758947, 0.1); kỳ vọng 𝔼[x₁ | x₀] = √0.9·x₀; mẫu 0.6008 lệch khỏi kỳ vọng vì ε là một lần rút ngẫu nhiên, độ lệch chuẩn 0.316.

*Phải — 5 noise levels on a 28×28 "house" image (TASK-05):* `figures/noise_sequence.pdf` (hoặc `figures/diffusion_overview/state_*.png`).
- Caption: SNR = ᾱ_t/(1−ᾱ_t): **33.5 at t = 50** (house clearly visible) → **< 0.1 at t = 500** (noise dominates) → ≈ 0 at T.
- Nhãn "Our worked example — corruption only, no model involved".

**GQ hook:** "By t = T nothing is left of the image → generation can start from pure N(0, I)."

**Ghi chú:** hai ví dụ dùng β khác nhau (0.1 cho dễ tính, schedule nhỏ cho ảnh) — nói một câu để tránh bị hỏi.

---

## Slide 5 — Reverse denoising: learning to undo one small step  *(~90s)*

**Takeaway:** Mô hình không học "ảnh = f(nhiễu)" trong một bước, mà học **đảo ngược từng bước nhỏ** bằng cách *dự đoán nhiễu*.

**Nội dung slide**
- Sơ đồ đầy đủ hai chiều (TASK-03): **Fig. `ddpm`** — xanh (forward, known) trên, cam (backward, learned) dưới. Hình trung tâm của cả bài; để to.
- Reverse model: p_θ(x_{t−1} | x_t) = 𝒩(μ_θ(x_t, t), σ_t² I) — Gaussian vì bước đủ nhỏ.
- Noise-prediction parameterization:
  - μ_θ(x_t, t) = (1/√α_t)·( x_t − β_t/√(1−ᾱ_t) · **ε_θ(x_t, t)** )
- **Training loss (EQ-02):** L_simple = 𝔼_{t, x₀, ε} [ ‖ε − ε_θ(x_t, t)‖² ]
- Thuật toán training trong 4 dòng: lấy ảnh x₀ → chọn t ngẫu nhiên → tạo x_t bằng closed form → gradient step trên ‖ε − ε_θ‖².
- Callout nhỏ "Why predict noise, not x₀?" (KeyQuestions Q1): ε có phân phối đơn giản 𝒩(0, I) → target chuẩn hóa, dễ tối ưu; liên hệ score: −ε_θ/√(1−ᾱ_t) ≈ ∇ log q_t(x_t).

**Ghi chú:** variational bound, KL, posterior q(x_{t−1}|x_t, x₀) chỉ nói một câu: "the simplified loss is a reweighted version of the variational bound; Ho et al. report FID 3.17 vs 13.51 on CIFAR-10 (**paper reports**)". Chi tiết để Q&A.

---

## Slide 6 — From denoising to generation: answering the guiding question  *(~110s)*

**Takeaway:** Sinh ảnh = bắt đầu từ nhiễu mới rút ra và **áp dụng bộ khử nhiễu lặp đi lặp lại**; nhiều bước nhỏ + ngẫu nhiên là chìa khóa — và ta *thấy* cấu trúc xuất hiện dần.

**Nội dung slide — chia đôi**

*Trái — lý thuyết:*
- Sampling (3 dòng): x_T ~ 𝒩(0, I) → for t = T…1: x_{t−1} = μ_θ(x_t, t) + σ_t·u_t → output x₀. (Không cần ảnh thật nào.)
- **Câu trả lời cho GQ — 3 ý:**
  1. *Supervision for free:* forward process cung cấp (x_t, ε) ở mọi mức nhiễu.
  2. *Shared structure:* để dự đoán nhiễu, mạng phải học cấu trúc chung của nhiều ảnh.
  3. *Small stochastic steps:* mỗi bước chỉ chỉnh nhẹ; phần ngẫu nhiên u_t làm các seed khác nhau → ảnh khác nhau.
- Hộp **"Why not one step?"** (KeyQuestions Q2; nối với câu hỏi dẫn ở slide 3): MSE từ x_T → x₀ cho nghiệm tối ưu 𝔼[x₀ | x_T] ≈ 𝔼[x₀] vì x_T gần như độc lập với x₀ → *ảnh trung bình, mờ*. Nhiều bước nhỏ tránh điều này.
  - Câu nối: "Forward in T small steps is what *makes* reverse in small steps possible."

*Phải — bằng chứng (Our run, ImageNet, pretrained, ADM pixel vs LDM latent):*
- Hình `figures/colab/retriever_step25.png` (DDIM update 25, golden retriever): đọc từ *noisy input → predicted noise → clean estimate → updated state*.
- Quan sát: ở update 25, clean estimate **đã thấy đầu và mõm**, trong khi trạng thái cập nhật vẫn còn nhiễu → mạng "nhìn trước" ảnh sạch ở mỗi bước.
- Một dòng: forward từ ảnh cuối làm đặc điểm retriever biến mất dần (khớp slide 4). Thumbnail `imagenet_comparison.png` (5 lớp × 2 model) nếu còn chỗ.
- Caveat: 1 mẫu/lớp, hai guidance khác nhau → minh họa, không phải so sánh.

**GQ hook:** "Removing noise *is* generating, once you can run it from noise and in small random steps."

> **Lưu ý:** đây là slide dày nhất. Nếu chật, bỏ thumbnail ImageNet và rút hộp "Why not one step?" còn 2 dòng.

---

## Slide 7 — Inside the autoencoder: how images become latents  *(~80s)*  — **slide mới**

**Takeaway:** Autoencoder là bước **nén có học**: ℰ gói ảnh thành tensor latent nhỏ giữ ngữ nghĩa, D dựng lại ảnh; diffusion chỉ cần làm việc trên tensor nhỏ đó.

**Nội dung slide**
- **(a) Ý tưởng VAE** (diagram trái → phải, 3 hộp): `x₀` →[Encoder ℰ_φ]→ `(μ, σ)` → `z̃ = μ + σ ⊙ ξ, ξ ~ 𝒩(0, I)` →[Decoder D_ψ]→ `x̂₀`.
  - Encoder không xuất 1 điểm mà xuất **phân phối** (μ_φ, σ_φ); lấy mẫu bằng *reparameterization* để gradient chảy qua.
  - Loss = **reconstruction** (ảnh dựng lại giống ảnh gốc) + **KL** kéo mã hóa về 𝒩(0, I). Phát biểu 1 dòng: "−log p(x₀) ≤ recon + KL" (ELBO) — không cần chứng minh.
  - Vấn đề của VAE thuần: reconstruction bằng MSE theo pixel → **ảnh bị mờ** (trung bình các chi tiết khả dĩ).
- **(b) LDM sửa VAE thành "perceptual compressor"** (3 thành phần loss):
  1. *Perceptual loss* (so feature của mạng sâu): ảnh dựng lại phải *trông giống*, không cần khớp từng pixel.
  2. *Patch-based adversarial loss*: discriminator chấm từng patch → texture thật hơn, bớt mờ.
  3. *Light regularizer*: **KL-reg** (KL nhỏ) hoặc **VQ-reg** (gán mỗi vector latent vào codebook gần nhất, nằm trong decoder).
- **(c) Latent giữ cấu trúc không gian:** z̃ ∈ ℝ^{h×w×c}, h = H/f, w = W/f (f = downsampling factor). Ví dụ f = 4: 256×256×3 → 64×64×3. Giữ layout 2D → U-Net xử lý được.
- **(d) Hai điểm khác VAE thường:**
  - Autoencoder được **huấn luyện trước một lần rồi đóng băng**; diffusion học *phân phối của latent*, thay cho prior 𝒩(0, I) của VAE (vì latent sạch không đúng 𝒩(0, I)).
  - Nhiễu ξ của encoder ≠ nhiễu diffusion ε_z thêm ở giai đoạn 2 — tránh nhầm hai loại "noise".
- Gắn với checkpoint của nhóm: ImageNet LDM = **VQ, f = 4**; LSUN Churches = **KL, f = 8** (256 → 32×32×4).

**Hình:** nửa trái `Method LDM Overview.png` (pixel space ↔ latent space) hoặc tự vẽ chuỗi 3 hộp (a). Nên có 1 ảnh minh họa ảnh gốc / ảnh dựng lại nếu có.

**GQ hook:** "Same denoising idea — but the thing being denoised is 48× smaller." (số liệu đầy đủ ở slide 8)

**Cắt bớt cho vừa:** ELBO đầy đủ, chi tiết VQ-vs-KL (4 lý do VQ trong decoder) → Q&A. Nếu vẫn dày, bỏ (b.3) chỉ nhắc "regularizer".

---

## Slide 8 — Why latent diffusion is cheaper + the LDM pipeline  *(~90s)*

**Takeaway:** DDPM tốn kém vì **mỗi bước** chạy U-Net trên ảnh full-resolution; LDM chạy cùng vòng lặp trên **trạng thái nhỏ hơn nhiều**, rồi decode đúng một lần.

**Nội dung slide**
- Vấn đề: sampling cần nhiều lần gọi mạng, mỗi lần trên x ∈ ℝ^{H×W×3}.
- Con số (tính từ report):
  - LDM f = 4: 256×256×3 → 64×64×3 ⇒ **16× fewer spatial positions** (Rombach et al., Table 8).
  - Run LSUN Churches của nhóm: pixel state 256×256×3 = 196,608 giá trị vs latent 32×32×4 = 4,096 giá trị (**≈ 48× fewer values**, nhóm tự tính).
- Sơ đồ pipeline (TASK-08): **Fig. `ldm`** — hàng *Training* (x₀ → ℰ → z₀ → add noise → U-Net) và hàng *Generation* (z_T → U-Net + sampler → D → x̂). Chỉ làm rõ: autoencoder **đóng băng** khi huấn luyện U-Net.
- Điều gì giữ nguyên: forward noising, ε-prediction, loss L_LDM = 𝔼‖ε_z − ε_θ(z_t, t, τ(y))‖² — **cùng nguyên lý, đổi không gian**.
- Sinh ảnh: z_T ~ 𝒩(0, I) → denoise → **decode đúng một lần** D(z₀/a). Sampler như DDIM giảm thêm số bước (bổ sung cho việc mỗi bước rẻ hơn).
- Cảnh báo ngắn: nén quá mạnh làm mất chi tiết nhỏ/chữ → chất lượng bị chặn bởi autoencoder; và runtime/memory không chỉ phụ thuộc kích thước state (bằng chứng ở slide 10).

**Vì sao slide này quan trọng:** trả lời trực tiếp vế "why latent diffusion reduces computational demands" của LO.

---

## Slide 9 — Cross-attention conditioning, and what prompts can and cannot control  *(~100s)*

**Takeaway:** Prompt điều khiển *từng bước khử nhiễu* qua cross-attention, không phải dán lên ảnh cuối — nhưng điều khiển này "mềm" và có giới hạn.

**Nội dung slide — chia đôi**

*Trái — cơ chế:*
- Condition y → encoder τ_η → token embeddings C; cross-attention chèn trong U-Net:
  - Q = F·W_Q (từ image features), K = C·W_K, V = C·W_V (từ condition)
  - O = softmax(QKᵀ/√d)·V
  - Câu nhớ: **"Queries come from the image; keys and values come from the condition."**
  - Ví dụ: vùng đang thành xe buýt "lấy" thông tin từ token *red*, *bus*.
- Modality-agnostic: chỉ τ_η đổi — text (CLIP trong Stable Diffusion v1.4), class label (1 token, như ImageNet LDM của nhóm), layout; spatial input (mask, semantic map) thì concat với z_t.
- Classifier-free guidance: ε_u + s(ε_c − ε_u); s lớn → bám prompt hơn, kém đa dạng hơn (không đảm bảo đúng đếm/vị trí/gán thuộc tính).
- Hình tùy chọn: Fig. cross-attention (TikZ trong report) — nhỏ.

*Phải — Our run: Stable Diffusion v1.4, seed 2027, cùng initial latent* (`figures/colab/prompt/2027_{reference,change_color,change_side}.png`)
- Reference: *red bus left of blue car*.
- Đổi red → green: bus xanh lá ở **cả 4 seed** (thuộc tính ✔), nhưng không có xe xanh dương rõ ràng; seed 2027 ra hai bus xanh (danh tính đối tượng ✘).
- Đổi left → right: **không** đảo vị trí rõ ràng (quan hệ không gian ✘).
- Giải thích: cross-attention là "soft", thuộc tính có thể gắn nhầm đối tượng (Chefer et al., 2023).
- Caveat: 16 ảnh, kiểm bằng mắt — minh họa, không phải kết luận chung.

**GQ hook:** "Same denoising loop — now steered by words."

---

## Slide 10 — Our experiment: pixel vs latent diffusion on LSUN Churches  *(~80s)*

**Takeaway:** Latent nhanh hơn ≈ 2.5× nhưng **không** tiết kiệm bộ nhớ đỉnh trong cấu hình của nhóm → "giảm tính toán" ≠ "giảm mọi thứ".

**Nội dung slide**
- Setup một dòng: pretrained checkpoints (no training by us), Tesla T4, batch 1, 50 DDIM steps, η = 0, 4 seeds (2026–2029), warm-up bị loại, đồng bộ GPU.
- Bảng (TASK-11), nhãn **"Our run"**:

| Criterion | Pixel DDPM | LDM-KL-8 |
|---|---|---|
| Denoising state | 256×256×3 | 32×32×4 |
| Median latency (s/img) | 6.10 | **2.44** (2.50× faster) |
| Peak CUDA tensor alloc. (GiB) | **0.75** | 1.68 |
| Visual quality | Clear steeple at 2028; 2029 dark, details lost | Clear facades at 2027–2029; 2026 distant complex |

- Hình: lưới 2×4 `figures/colab/churches/{ddpm,ldm}_{2026..2029}.png`.
- Dòng **"Paper reports"** (khác nhãn/màu): Rombach et al. Table 6 (Places inpainting, 256²): pixel LDM-1 0.26 vs latent LDM-4 **0.97 samples/s**; FID@2k 24.74 → 15.21.
- Dòng caveat: 4 mẫu/model, một cặp checkpoint; không phải benchmark, không đo FID.

**Điểm cần chuẩn bị cho Q&A:** vì sao peak memory của LDM cao hơn? Report chỉ ghi nhận số đo, không quy nguyên nhân — trả lời trung thực: "chúng tôi chưa phân tích; có thể liên quan đến kiến trúc/độ chính xác/decoder của hai checkpoint khác nhau, đây là giả thuyết chưa kiểm chứng."

---

## Slide 11 — Limitations: training data, copyright, bias (+ method limits)  *(~50s)*

**Takeaway:** Mô hình chỉ "biết" những gì dữ liệu huấn luyện chứa; và tạo ảnh đẹp không đồng nghĩa với quyền sử dụng hay công bằng.

**Nội dung slide (TASK-10, RUBRIC-05) — 3 cột + 1 dải**
1. **Training data:** checkpoint churches chỉ biết churches; ImageNet conditioning dùng tập nhãn cố định; text model phụ thuộc thuộc tính/quan hệ có trong caption.
2. **Bias:** Bianchi et al. (2023) — định kiến nhân khẩu học xuất hiện với prompt thông thường. *Demo xe buýt của nhóm không đo bias.*
3. **Copyright / memorization:** Carlini et al. (2023) trích xuất được ảnh huấn luyện từ diffusion model; nguồn gốc dữ liệu liên quan bản quyền (US Copyright Office 2025 — luật Mỹ, không phải luật Việt Nam; không kết luận mọi ảnh sinh ra đều là bản sao).
4. Dải dưới — **Method limits:** sampling nhiều bước; autoencoder chặn chất lượng; cross-attention chưa chắc đúng đếm/quan hệ (slide 9); thí nghiệm của nhóm nhỏ, không phải benchmark.

**Nhấn:** đây là "critical analysis" — nói thẳng điều gì thí nghiệm *không* chứng minh.

---

## Slide 12 — Conclusion: answering the guiding question  *(~45s)*

**Takeaway:** Quay lại GQ với câu trả lời 3 ý, nối thẳng LO.

**Nội dung slide**
- **GQ → answer:** *Learning to remove noise generates new images because the forward process gives free training pairs at every noise level, a network trained to predict the noise learns shared image structure, and running it from fresh noise in many small stochastic steps turns noise into a new sample.*
- Recap 3 dòng theo LO:
  1. **Forward noising:** known Gaussian chain, closed form, schedule β_t.
  2. **Reverse denoising:** learned p_θ(x_{t−1}|x_t) via ε-prediction, L_simple.
  3. **Latent diffusion:** same principle on autoencoder latents → cheaper denoising steps (≈2.5× faster in our run; 0.26 → 0.97 samples/s in the paper), conditioned by cross-attention; costs: reconstruction limit, memory not necessarily lower.
- Take-home 1 dòng cho limits: *capability is bounded by data, and by what we actually measured.*
- Cuối slide: References (DDPM, LDM, Sohl-Dickstein 2015, SD v1.4, các nguồn ở slide 11) — font nhỏ — và "Q&A / Thank you".

---

## Phụ lục A — Phân bổ thời gian (15 phút)

| Slide | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | Tổng |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Giây | 45 | 70 | 90 | 80 | 90 | 110 | 80 | 90 | 100 | 80 | 50 | 45 | **~930s ≈ 15.5 phút** |

Hơi dài ~30s: rút 10s ở các slide 3, 6, 9 là đủ. Slide 6, 7, 9 dày nhất — ưu tiên cắt chữ thay vì cắt hình.

## Phụ lục B — Mapping slide ↔ yêu cầu

| Yêu cầu | Slide |
|---|---|
| OBJ-01 (forward, reverse, vì sao latent giảm tính toán) | 3–8 |
| OBJ-02 (guiding question) | 1, 6, 12 |
| TASK-01 (generative vs discriminative; GAN/AR/diffusion) | 2 |
| TASK-02, EQ-01/02/03 | 3, 5, 6 |
| TASK-03 (sơ đồ hai chiều) | 5 (Fig. ddpm) |
| TASK-04, EQ-04 (ví dụ 1-D) | 4 |
| TASK-05 (5 mức nhiễu) | 4 |
| TASK-06 (pretrained demo) | 6 (quỹ đạo), 9 (prompt), 10 |
| TASK-07 (VAE encoder/decoder, latent space, cross-attention) | 7, 8, 9 |
| TASK-08 (pipeline LDM) | 8 |
| TASK-09 (tốc độ, chất lượng, prompt control) | 9, 10 |
| TASK-10 (data, copyright, bias) | 11 |
| TASK-11 (latent vs pixel có bằng chứng) | 10 |
| PAPER-03 (paper vs nhóm tự làm) | nhãn "Paper reports" / "Our run" ở 5, 6, 9, 10 |
| RUBRIC-05 (critical analysis) | 9, 10 (memory caveat), 11 |

## Phụ lục C — Câu hỏi Q&A nên chuẩn bị (mỗi thành viên ≥ 1)

- *(Người A)* Tại sao dự đoán ε mà không phải x₀? → KeyQuestions Q1: target 𝒩(0, I) chuẩn hóa; liên hệ score −ε/√(1−ᾱ_t).
- *(Người A)* Tại sao noise qua T bước thay vì một bước? → bước nhỏ ⇒ bước ngược xấp xỉ Gaussian, dễ học; mọi mức nhiễu đều là bài toán huấn luyện; training dùng closed form nên không tốn T lần, chi phí T bước nằm ở sampling.
- *(Người A)* Tại sao x_T xấp xỉ 𝒩(0, I)? → ᾱ_T nhỏ; SNR ≈ 0; "finite schedule không làm bằng chính xác".
- *(Người B)* Tại sao không sinh ảnh trong một bước? → KeyQuestions Q2: 𝔼[x₀ | x_T] ≈ ảnh trung bình.
- *(Người B)* VAE khác autoencoder thường chỗ nào? Encoder xuất phân phối + KL kéo về 𝒩(0, I) + reparameterization; và vì sao LDM không sinh bằng cách decode z ~ 𝒩(0, I)? → latent sạch không đúng 𝒩(0, I), nên dùng diffusion để học phân phối latent.
- *(Người B)* Vì sao dùng perceptual + adversarial loss thay vì MSE? → MSE theo pixel trung bình các chi tiết khả dĩ → mờ.
- *(Người C)* Cross-attention khác self-attention thế nào? Q từ ảnh, K/V từ điều kiện.
- *(Người C)* Vì sao LDM nhanh hơn nhưng dùng nhiều bộ nhớ đỉnh hơn? → nêu trung thực: chỉ đo, chưa quy nguyên nhân; hai checkpoint khác kiến trúc.
- *(Người C)* Thí nghiệm của nhóm có đủ kết luận "latent tốt hơn pixel" không? → Không: 4 mẫu, 1 cặp checkpoint, không FID; chỉ là minh họa, kết hợp số liệu paper (Table 6).
- *(Chung)* Diffusion có "sao chép" ảnh huấn luyện không? → Carlini et al.: memorization có thể xảy ra; không phải mọi ảnh là bản sao.

## Phụ lục D — Danh sách hình/asset nên dùng

| Slide | File |
|---|---|
| 1, 4 | [iccv-diffusion-report/figures/diffusion_overview/](iccv-diffusion-report/figures/diffusion_overview/) (`state_0/100/300/1000.png`), [noise_sequence.pdf](iccv-diffusion-report/figures/noise_sequence.pdf) |
| 2 | Fig. "families" (Appendix report); [qualitative_comparison.png](iccv-diffusion-report/figures/qualitative_comparison.png) — đã kiểm tra: đúng là hình so sánh GAN / autoregressive / diffusion (dùng ở slide backup) |
| 5 | Fig. `ddpm` (TikZ trong [report.tex](iccv-diffusion-report/content/report.tex)) — export từ [main.pdf](iccv-diffusion-report/main.pdf) hoặc vẽ lại |
| 6 | [retriever_step25.png](iccv-diffusion-report/figures/colab/retriever_step25.png), [imagenet_comparison.png](iccv-diffusion-report/figures/colab/imagenet_comparison.png) |
| 7 | Tự vẽ chuỗi encoder → latent → decoder (TikZ). *Lưu ý:* [Method LDM Overview.png](<Method LDM Overview.png>) là hình forward/reverse diffusion trong latent, **không** phải hình autoencoder; công thức VAE Eq. (1)–(3) trong report |
| 8 | Fig. `ldm` (TikZ trong report) |
| 9 | Fig. cross-attention (TikZ trong report), [figures/colab/prompt/](iccv-diffusion-report/figures/colab/prompt/) |
| 10 | [figures/colab/churches/](iccv-diffusion-report/figures/colab/churches/) |

Mọi hình/phương trình lấy từ paper cần ghi nguồn ở chân slide (RUBRIC-06): ví dụ "Fig. adapted from Rombach et al., 2022".
