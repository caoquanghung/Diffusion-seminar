# Presentation script: Diffusion Models, From Adding Noise to Generating Images

Script thuyết trình cho deck [main.tex](main.tex): 12 slide nội dung, cộng 4 slide backup (13: Notation, 14: Inside one denoising step, 15–16: References).

**Cách đọc file này**

- Lời nói để trong khung trích dẫn (`>`) và viết bằng **tiếng Anh**, khớp với chữ trên slide. Chỉ dẫn sân khấu viết bằng tiếng Việt.
- **👉 [ ... ]**: chỉ tay / laser vào đúng vùng đó **trước khi** đọc câu ngay sau.
- **✋**: dừng khoảng 1 giây và nhấn giọng. Đây là các câu người nghe cần nhớ.
- **(cắt được)**: câu có thể bỏ khi trễ giờ.
- **⚠️ Đừng nói**: những phát biểu vượt quá bằng chứng của nhóm.
- Phân công người nói theo [slide-outline.md](../slide-outline.md): **A** slide 1–4, **B** slide 5–8, **C** slide 9–12. Có thể đổi tên tùy nhóm.

**Mã màu trên slide**: hãy dùng màu để dẫn mắt người nghe.

| Màu | Ý nghĩa | Ví dụ |
|---|---|---|
| Xanh dương nhạt (`fwd`) | Forward noising: cố định, đã biết | khung "Forward noising equations" slide 3, đường "signal" trong biểu đồ |
| Cam (`rev`) | Reverse denoising: học được; đồng thời là nhãn **OUR RUN** | dải REVERSE và khung Sampling slide 5 |
| Xanh lá (`ok`) | Latent diffusion / autoencoder; nhãn **OUR EXAMPLE**; khung câu trả lời slide 6 | khung "Chosen values" slide 4, khung "Why removing noise generates new images" slide 6 |
| Xanh đậm | Nhãn **PAPER REPORTS**: số liệu của paper, không phải của nhóm | thẻ Paper review slide 1, bảng FID slide 5, slide 8, 10 |

Mỗi khi đọc một con số, **chỉ vào nhãn PAPER REPORTS / OUR RUN / OUR EXAMPLE bên cạnh** để người nghe biết số đó của ai.

---

## Skeleton tổng thể

| # | Slide | Người nói | Thời lượng | Phần | Thông điệp một câu |
|---|---|---|---|---|---|
| 1 | Title, guiding question, learning objective, paper review | A | 40s | Mở đầu | Học khử nhiễu thì làm sao sinh ra ảnh mới? DDPM và LDM đứng ở đâu trong dòng paper. |
| 2 | Where diffusion fits: three ways to generate images | A | 60s | Mở đầu | Diffusion học cấu trúc ảnh bằng cách đảo ngược một quá trình làm hỏng đã biết. |
| 3 | Forward noising: a known way to destroy structure | A | 85s | A · Forward | Một bước Gaussian đã biết; công thức đóng nhảy thẳng tới mọi $t$; tín hiệu được đổi dần sang nhiễu. |
| 4 | Forward noising by hand and by eye | A | 90s | A · Forward | Hai bước tính tay theo hai cách cho cùng $x_2$; kỳ vọng khác một lần rút ngẫu nhiên. |
| 5 | Reverse denoising: from noise back to an image | B | 85s | B · Reverse | Sinh ảnh = lặp bước ngược từ nhiễu; mạng chỉ cần dự đoán ε, và dự đoán ε tốt hơn dự đoán mean. |
| 6 | Training the noise predictor, and why it works | B | 100s | B · Reverse | $L_{\text{simple}}$ là hồi quy MSE; ε dự đoán là score; **trả lời guiding question**: biết nhiễu thì biết ảnh sạch. |
| 7 | Inside the autoencoder: how images become latents | B | 70s | C · Latent | Autoencoder nén ảnh thành latent và được đóng băng. |
| 8 | Why latent diffusion is cheaper: same loop, smaller state | B | 80s | C · Latent | Vòng lặp giữ nguyên, trạng thái nhỏ hơn: mỗi bước rẻ hơn. |
| 9 | Cross-attention: steering the denoiser with a prompt | C | 90s | C · Latent | Prompt điều khiển từng bước qua attention mềm; đổi màu được, đổi trái/phải thì không. |
| 10 | Pixel vs. latent diffusion on LSUN Churches | C | 75s | D · Evidence | Nhanh hơn khoảng 2.5 lần nhưng tốn bộ nhớ đỉnh hơn; chỉ là minh họa. |
| 11 | Limitations: training data, copyright and bias | C | 45s | D · Evidence | Dữ liệu, bias, copyright, và giới hạn của chính thí nghiệm. |
| 12 | Conclusion: answering the guiding question | C | 40s | Kết | Trả lời lại guiding question và 3 vế của learning objective. |
| | **Tổng** | | **~860s ≈ 14.3 phút** | | Còn khoảng 40s dự phòng trong giới hạn 15 phút. Nếu trễ, bỏ các câu **(cắt được)**. |

**Sợi chỉ xuyên suốt**: guiding question được đặt ở slide 1, trả lời ở khung xanh lá slide 6, nhắc lại ở slide 12. Learning objective được nêu ở slide 1; vế "forward" là slide 3–4, vế "reverse" là slide 5–6, vế "latent" là slide 7–8; tổng kết ở slide 12.

---

## Slide 1: Title, guiding question, learning objective, paper review (A · ~40s)

**Bố cục**: dải tiêu đề xanh phía trên, bên dưới tiêu đề là 3 khối tên người trình bày (tên in đậm, MSSV bên dưới) · **trái**: khung cam GUIDING QUESTION, bên dưới là khung xanh LEARNING OBJECTIVE (3 cụm từ tô màu) · **phải**: thẻ xám PAPER REVIEW với 4 mục 2015 / 2019 / 2020 DDPM (required, có nhãn PAPER REPORTS) / 2022 LDM.

**👉 [3 khối tên trên dải tiêu đề]**

> Good morning everyone. We are Cao Quang Hung, Nguyen Trong Van Viet and Huynh Chi Ton, and today we present *Diffusion Models: From Adding Noise to Generating Images*.

> A denoiser cleans an image that already exists. A generator must produce an image that never existed. What connects the two?

**👉 [Khung cam GUIDING QUESTION] ✋**

> That is our guiding question: **how can learning to remove noise enable a model to generate new images?**

**👉 [Khung xanh LEARNING OBJECTIVE: chỉ lần lượt 3 cụm màu xanh dương → cam → xanh lá]**

> By the end of this talk, you should be able to explain **forward noising**, **reverse denoising**, and **why latent diffusion reduces computational demands**. These three phrases are the three parts of the talk.

**👉 [Thẻ PAPER REVIEW: quét từ 2015 xuống 2022, dừng ở dòng DDPM]**

> We build on four papers. The 2015 framework introduced the forward and reverse Gaussian chains; Song and Ermon learned scores at many noise levels; **DDPM**, our required paper, predicts the noise; and **LDM** runs the same idea in a compressed latent space. **(cắt được)** DDPM reports an FID of 3.17, but its likelihood is not competitive.

**Chuyển ý**: "First, where does diffusion fit among generative models?"

⚠️ **Đừng nói** rằng nhóm đã tự train mô hình. Mọi thí nghiệm dùng checkpoint pretrained.

---

## Slide 2: Where diffusion fits: three ways to generate images (A · ~60s)

**Bố cục**: **cột trái**: tiêu đề "Generative vs. discriminative", ô xám *Discriminative*, ô xanh *Generative*, dòng chữ nhỏ về Stable Diffusion · **cột phải**: tiêu đề "Qualitative comparison: GAN vs. autoregressive vs. diffusion", hình 3 panel GAN (tím) | Autoregressive (xanh) | Diffusion (xanh lá), thanh "Core difference" ở đáy hình.

**👉 [Ô xám Discriminative]**

> A discriminative model learns $p(y \mid x)$. To answer "is this a cat?", it only needs features that separate the classes.

**👉 [Ô xanh Generative]**

> A generative model learns $p(x)$ or $p(x \mid y)$. To *create* a cat, it must capture shape, texture, lighting and layout, which is much more information.

**👉 [Panel GAN màu tím: Generator → Discriminator → "adversarial training"]**

> There are three main families. A GAN maps noise to an image in one pass, but training is a game between two networks, and it can suffer from mode collapse.

**👉 [Panel Autoregressive: chuỗi token $x_1, x_2, \dots$]**

> An autoregressive model generates the image token by token: good likelihoods, but slow, sequential sampling.

**👉 [Panel Diffusion: hàng trên "forward process", rồi hàng dưới "reverse process"]**

> Diffusion adds noise in a fixed forward process and learns to remove it step by step. It trains stably and gives high quality and diversity, but sampling needs many steps.

**👉 [Thanh "Core difference" dưới đáy hình]**

> In one line: one pass, token by token, or denoising over many steps.

**👉 [Dòng chữ nhỏ dưới ô Generative] (cắt được)**

> This is also the backbone of today's text-to-image systems, such as Stable Diffusion, which we test on slide 9.

**Chuyển ý**: "Let's start with the easy direction: forward noising."

⚠️ **Đừng nói** "diffusion luôn tốt hơn GAN". Hình chỉ mô tả hành vi điển hình, không phải đảm bảo.

---

## Slide 3: Forward noising: a known way to destroy structure (A · ~85s)

**Bố cục**: **dải sơ đồ trên**: $x_0 \to x_{t-1} \to$ [Known Gaussian kernel] $\to x_t \to x_T$, nhãn "clean data" / "nearly noise" · **khung xanh trái "Forward noising equations"**: (1) ONE STEP có chú thích dưới hai số hạng "shrink old signal" / "add fresh noise"; (2) JUMP TO ANY $t$ IN ONE SHOT (phương trình đóng khung); bảng ký hiệu 4 hàng · **cột phải**: 3 gạch đầu dòng (**Why $x_T\approx\mathcal N(0,\mathbf I)$**, **Signal traded for noise**, **Assumptions**) và biểu đồ "DDPM schedule" với đường xanh $\sqrt{\bar\alpha_t}$, đường cam $\sqrt{1-\bar\alpha_t}$, vạch đứt "SNR = 1, $t\approx260$".

**👉 [Dải sơ đồ: quét từ $x_0$ (clean data) sang $x_T$ (nearly noise), dừng ở ô "Known Gaussian kernel"]**

> The forward process takes a clean image $x_0$ and adds noise over $T$ steps until it is nearly pure noise. Each step is a *known* Gaussian kernel. Nothing here is learned.

**👉 [Phương trình (1): chỉ chú thích "shrink old signal", rồi "add fresh noise"]**

> Equation one is a single step. The first term **shrinks the old signal** by $\sqrt{1-\beta_t}$; the second **adds fresh noise** with scale $\sqrt{\beta_t}$.

**👉 [Phương trình (2) đóng khung] ✋**

> Equation two is the key result. Because Gaussian steps compose, we can jump from $x_0$ to *any* step $t$ in one shot, using $\bar\alpha_t$, the product of the alphas.

**👉 [Bảng ký hiệu dưới khung: quét nhanh]**

> The symbols: $x_0$ is the clean image, rescaled to $[-1,1]$ and unitless; $\beta_t$ between 0 and 1 is the noise schedule; $t$ is a step index, not physical time; and $\varepsilon$ is standard Gaussian noise.

**👉 [Gạch đầu dòng "Why $x_T\approx\mathcal N(0,\mathbf I)$"]**

> Why does the chain end at pure noise? If a state is already standard normal, one step keeps it standard normal: $(1-\beta_t) + \beta_t = 1$. And at the last step $\bar\alpha_T$ is about $4\times10^{-5}$, so almost no signal is left. Generation can start from pure noise.

**👉 [Gạch đầu dòng "Signal traded for noise", rồi biểu đồ: đường xanh đi xuống, đường cam đi lên, vạch đứt ở $t\approx260$] ✋**

> In equation two, the squared weights always sum to one. So the forward process does not just add noise; it *trades* signal for noise. On the plot, the blue signal weight falls and the orange noise weight rises, and they cross at about $t = 260$, where the signal-to-noise ratio is one.

**👉 [Gạch đầu dòng "Assumptions"]**

> The assumptions: a Markov chain, independent noise at every step, and small $\beta_t$, using DDPM's schedule of $T=1000$ steps from $10^{-4}$ to $0.02$.

**Chuyển ý**: "Let's make this concrete with numbers."

---

## Slide 4: Forward noising by hand and by eye (A · ~90s)

**Bố cục**: **dải xanh lá trên cùng** "Chosen values" (nhãn OUR EXAMPLE) · **hai khung giữa**: *Way 1: step by step with the schedule $\beta_1,\beta_2$* (xanh nhạt, trái) và *Way 2: one jump with the shortcut $\bar\alpha_2$* (xanh đậm, phải) · **khung cam** "Interpreting the stochastic expectation" · **dưới cùng**: ảnh 28×28 ngôi nhà ở 5 mức nhiễu (trái) và chú thích SNR (phải).

**👉 [Dải xanh lá "Chosen values": chỉ lần lượt $x_0$, $\beta$, $\varepsilon$, $\alpha$, $\bar\alpha_2$]**

> Let's do two steps by hand. One pixel $x_0 = 0.8$, rescaled to $[-1,1]$. A schedule $\beta_1 = 0.1$ and $\beta_2 = 0.2$, chosen large on purpose so the arithmetic is visible. Two noise draws, $\varepsilon_1 = -0.5$ and $\varepsilon_2 = -0.4$. So $\alpha_1 = 0.9$, $\alpha_2 = 0.8$, and $\bar\alpha_2 = 0.72$.

**👉 [Khung Way 1: dòng Step 1, rồi dòng Step 2, dừng ở ô $x_2 = 0.3585$]**

> Way one, step by step. Step one: $\sqrt{0.9}$ times $0.8$ is $0.7589$, plus $\sqrt{0.1}$ times $-0.5$ is $-0.1581$, so $x_1 = 0.6008$. Step two starts from $x_1$: $\sqrt{0.8}$ times $0.6008$ is $0.5374$, minus $0.1789$, so **$x_2 = 0.3585$**.

**👉 [Khung Way 2: dòng "Shortcut (2)", rồi công thức $\bar\varepsilon$, rồi ô kết quả có dấu ✓]**

> Way two uses the shortcut from slide 3 and jumps straight from $x_0$: $\sqrt{0.72}$ times $0.8$ is $0.6788$, plus $0.5292$ times a single noise $\bar\varepsilon$. The two noise draws merge into **one** Gaussian, $\bar\varepsilon = -0.6053$; its variance is $(0.08 + 0.2)/0.28 = 1$. The result is again **$0.3585$**, the same as way one.

**👉 [Khung cam "Interpreting the stochastic expectation"] ✋**

> What does this number mean? Because the noise has mean zero, the *expected* value of $x_2$ given $x_0$ is $\sqrt{\bar\alpha_2}\,x_0 = 0.6788$, with variance $0.28$. Both ways describe the **same distribution**. Our $0.3585$ is just **one random draw**, about 0.6 standard deviations below the mean. Averaging many draws would give $0.6788$.

**👉 [Ảnh ngôi nhà: quét trái sang phải, rồi chỉ chú thích SNR bên phải]**

> Now by eye, with the real DDPM schedule: our 28×28 house at five noise levels. At $t = 50$ the SNR is 33.5 and the house is clear. At $t = 500$ the SNR is below 0.1 and noise dominates. At $t = T$ almost nothing is left.

**Chuyển người (A → B)**: "So destroying structure is easy and fully known. [Tên B] will now show how we *learn* to undo it."

⚠️ **Đừng nói** ảnh ngôi nhà được sinh bởi một mô hình. Đây chỉ là forward noising, không có mạng nào.

---

## Slide 5: Reverse denoising: from noise back to an image (B · ~85s)

**Bố cục**: **dải cam trên cùng** "REVERSE: learned denoising", đọc **từ phải sang trái**: $x_T \to x_t \to$ [neural net $\varepsilon_\theta(x_t,t)$, nhãn "timestep $t$"] $\to$ [sampler $\mu_\theta+\sigma_t u_t$, nhãn $u_t\sim\mathcal N(0,\mathbf I)$] $\to x_{t-1} \to x_0$ · **giữa trái (40%)**: khung cam *Sampling: generate a new image* · **giữa phải (60%)**: khung xanh *Why predict ε, not the mean $\tilde\mu_t$?* với bảng FID 2×2 (nhãn PAPER REPORTS) · **dải cam dưới cùng**: *One reverse step: turn the noise prediction into $\mu_\theta$* chia 3 phần.

**👉 [Dải REVERSE: kéo tay từ $x_T$ bên phải sang $x_0$ bên trái] ✋**

> Now the direction we learn. The reverse chain runs right to left, from pure noise $x_T$ back to an image $x_0$. At each step, a neural net looks at the noisy state and the timestep, and a sampler takes one small step.

**👉 [Khung Sampling: chỉ bước 1 → 2 → 3, rồi dòng chữ xám cuối khung]**

> Generating an image is just this loop. One: draw fresh noise. Two: for $t$ from $T$ down to 1, set $x_{t-1}$ to the mean $\mu_\theta$ plus a little fresh noise. Three: return $x_0$; no noise is added at the last step. Notice: **no real image is used**. The network only has to supply $\mu_\theta$ at each step.

**👉 [Khung "Why predict ε, not the mean $\tilde\mu_t$?": đọc câu hỏi]**

> So what should the network predict? The obvious choice is the mean $\tilde\mu_t$ of $x_{t-1}$ directly. DDPM predicts the **noise** instead. Why?

**👉 [Bảng FID: chỉ nhãn PAPER REPORTS, rồi hàng "mean", rồi hàng "noise ε", dừng ở 3.17]**

> Ho et al. tested both on CIFAR-10. Predicting the mean works only with the weighted variational bound, at FID 13.22, and was unstable with plain MSE. Predicting the noise with plain MSE gives **FID 3.17**; lower is better. These are the paper's numbers. The reason: the noise has the same scale at every step, so a plain, unweighted loss works. We'll see that loss on the next slide.

**👉 [Dải "One reverse step": phần trái → công thức giữa (chỉ $\varepsilon_\theta$ in đậm) → phần phải]**

> Finally, how the predicted noise becomes one step. The reverse step is Gaussian with a fixed variance $\sigma_t^2 = \beta_t$. Its mean takes $x_t$ and subtracts a scaled noise prediction. The bold $\varepsilon_\theta$, from a U-Net, is the **only learned part**; everything else comes from the fixed schedule.

⚠️ **Đừng nói** "dự đoán mean hoàn toàn không học được". Paper chỉ báo là không ổn định khi dùng plain MSE; với weighted bound nó đạt FID 13.22.

---

## Slide 6: Training the noise predictor, and why it works (B · ~100s)

**Bố cục**: **cột trái (hẹp)**: khung xanh *Training: learn to predict the noise* ($L_{\text{simple}}$ + 3 bước + dòng xám "Uses real images"), khung xanh nhạt *Connection to the score (Song & Ermon 2019)* (hai công thức $s_\theta$ và $\mu_\theta$ xếp dọc) · **cột phải (rộng)**: khung xanh lá *Why removing noise generates new images*: dòng in đậm "Core idea: know the noise ⇒ know the clean image", 5 gạch đầu dòng (**Noise and image: same information**, **Remove a little at a time**, **Why a real image, not any image**, **Coarse to fine**, **Why ε, not $x_0$?**) và câu nghiêng về nhà điêu khắc.

**👉 [Khung Training: công thức $L_{\text{simple}}$, rồi 3 bước đánh số]**

> Training is plain regression. $L_{\text{simple}}$ is the squared error between the true noise and the predicted noise. Pick a real image, a random step $t$ and random noise; build $x_t$ with the closed form from slide 3; predict the noise and take a gradient step. Training uses real images; sampling, on the previous slide, did not.

**👉 [Khung score: câu đầu, rồi công thức $s_\theta$, rồi công thức $\mu_\theta$]**

> The *score* is the direction in which the density of noisy images increases. At the optimum of this squared loss, the network predicts the *average* noise given $x_t$, and that average is a scaled score. Rewriting the mean with the score, each reverse step moves **uphill in density**, then adds a little noise, like annealed Langevin dynamics.

**👉 [Khung xanh lá: dòng "Core idea"] ✋ (đây là câu trả lời chính cho guiding question)**

> So, our answer to the guiding question. The core idea: **if you know the noise, you know the clean image.**

**👉 [Gạch 1 "Noise and image: same information": chỉ công thức $\hat x_0$]**

> Invert the closed form: given $x_t$ and the predicted noise, we can solve for a clean estimate $\hat x_0$. Predicting the noise and predicting the image carry the same information.

**👉 [Gạch 2 "Remove a little at a time"]**

> When generating, we start from pure noise and remove only a **small part** of the predicted noise at each step, adding a little fresh noise to keep samples diverse. Each step is an easy correction, unlike a VAE decoder that must produce the whole image in one pass.

**👉 [Gạch 3 "Why a real image, not any image"] ✋**

> Why does this give a *realistic* image and not just any image? To guess the noise correctly, the network must know what real images look like: whatever does not look like a real image *is* the noise. Since the noise prediction is proportional to minus the score, removing it climbs toward regions dense with real images.

**👉 [Gạch 4 "Coarse to fine"]**

> Different noise levels teach different things: at large $t$, the layout, shapes and colours; at small $t$, edges and texture. Ho et al. observe that sampling follows the same order: large-scale features first, details last.

**👉 [Gạch 5 "Why ε, not $x_0$?"] (cắt được)**

> And why noise rather than the clean image directly? The noise has the same scale at every step, while $x_0$ is nearly unguessable when $t$ is large; DDPM reports better samples with $\varepsilon$, as we saw on slide 5.

**👉 [Câu nghiêng cuối khung]**

> Think of a sculptor: the model learns what is *not* the statue, and chips it away layer by layer.

**Chuyển ý**: "This loop works, but every step processes a full-resolution image, many times. Making each step cheaper is the job of latent diffusion."

⚠️ **Đừng nói** $s_\theta$ *bằng* đúng score thật. Đó chỉ là xấp xỉ, đúng tại điểm tối ưu lý tưởng của MSE.
⚠️ **Đừng nói** "diffusion luôn sắc nét hơn VAE". Slide chỉ so sánh cách giải mã (nhiều bước nhỏ so với một lần), không có thí nghiệm so sánh chất lượng.
⚠️ Ý "nhiễu lớn dạy bố cục, nhiễu nhỏ dạy chi tiết" là cách hiểu của nhóm; phần có nguồn là *thứ tự xuất hiện khi sampling* (Ho et al. 2020, Sec. 4.3).

💡 Nếu bị hỏi "có bằng chứng nào cho clean estimate không?", mở **backup 14** (hình golden retriever, run của nhóm): ở bước DDIM 25/50, clean estimate đã thấy con chó trong khi trạng thái hiện tại vẫn còn nhiễu.

---

## Slide 7: Inside the autoencoder: how images become latents (B · ~70s)

**Bố cục**: **chuỗi trên cùng**: $x_0$ → [Encoder $\mathcal E_\phi$] → [$\mu_\phi, \sigma_\phi$] → [cam: $\tilde z = \mu + \sigma\odot\xi$] → [Decoder $D_\psi$] → $\hat x_0$ · **3 khung dưới**: *VAE objective* (xanh) | *LDM: a perceptual compressor* (xanh lá) | *What changes for diffusion* (cam).

> Latent diffusion begins with an autoencoder.

**👉 [Chuỗi trên: $x_0$ (nhãn $H\times W\times 3$) → Encoder → ô $\mu, \sigma$ → ô cam $\tilde z$]**

> The encoder turns an $H \times W \times 3$ image into a distribution, a mean and a standard deviation for every latent value, and we sample a latent of size $h \times w \times c$, where $h = H/f$.

**👉 [Decoder → $\hat x_0$ "reconstruction"]**

> The decoder maps the latent back to an image.

**👉 [Khung xanh VAE objective: "Reconstruction", "KL", rồi chữ **Problem**]**

> A textbook VAE trains this with reconstruction plus a KL term that keeps codes near $\mathcal N(0, I)$. The problem: pixel-wise squared error averages plausible details, so images turn blurry.

**👉 [Khung xanh lá: 1 → 2 → 3, rồi dòng "Ours"]**

> So LDM trains a *perceptual* compressor: a perceptual loss on deep features, a patch-based adversarial loss for realistic texture, and only a light regularizer, weak KL or a VQ codebook. Our runs use both: KL with $f = 8$ for Churches, VQ with $f = 4$ for ImageNet.

**👉 [Khung cam "What changes for diffusion": lần lượt 4 dấu chấm] ✋ ở dấu chấm 3**

> For diffusion, four points matter. The latent keeps its 2-D layout, so a U-Net can process it. The autoencoder is trained once, then **frozen**. Clean latents are *not* standard normal, so we cannot just decode random noise; diffusion must learn the distribution of latents. And the encoder noise $\xi$ is not the diffusion noise $\varepsilon_z$.

⚠️ Sơ đồ vẽ biến thể KL ($\mu, \sigma$). Biến thể VQ không có $\mu, \sigma$. Nếu bị hỏi, nói rõ điều này.

---

## Slide 8: Why latent diffusion is cheaper: same loop, smaller state (B · ~80s)

**Bố cục**: **hàng TRAINING**: $x_0$ → [Encoder, frozen, scale $a$] → $z_0$ → [add noise] → [conditional U-Net] ← [$\tau_\eta(y)$] (nhãn "cross-attn") · **hàng GENERATION**: [$z_T$ noise] → [U-Net + sampler] → [Decoder (frozen)] → $\hat x_0$, chú thích "no real image or encoder needed" · **khung xanh lá trái** "Smaller state per denoising step" · **khung xanh phải** "Same principle, new space" ($L_{\text{LDM}}$, dòng định nghĩa $z_0=a\,\mathcal E_\phi(x_0)$, chữ **Caveat**).

> Here is the full pipeline, and our answer to the last part of the learning objective.

**👉 [Hàng TRAINING: quét trái → phải tới ô U-Net, rồi ô $\tau_\eta(y)$]**

> Training: encode a real image with the frozen encoder, scale it by a fixed $a$, add noise exactly as before, and train a U-Net to predict the noise. A condition $y$, text or a class, enters through $\tau_\eta$ and cross-attention.

**👉 [Hàng GENERATION, rồi chú thích "no real image or encoder needed"]**

> Generation: start from latent noise, denoise for many steps, and decode **once** at the end. No real image and no encoder are needed.

**👉 [Khung xanh lá: gạch 1 (PAPER REPORTS), gạch 2 (OUR EXAMPLE)] ✋**

> Why is it cheaper? The loop is identical; the *state* is smaller. With $f = 4$, a 256×256 image becomes 64×64: **16 times fewer spatial positions**, as in the paper. In our LSUN Churches model, 196,608 values become 4,096, **about 48 times fewer**. Every U-Net call works on that small state.

**👉 [Khung xanh: công thức $L_{\text{LDM}}$, rồi chữ **Caveat**]**

> The loss is the same noise-prediction loss, now on latents with a condition. Two cautions: fewer values is *not* automatically 48 times faster, and DDIM's fewer steps are a separate speedup. Compression also caps quality: fine text and small objects can be lost. We test the real cost on slide 10.

**Chuyển người (B → C)**: "[Tên C] will now show how the condition actually steers the denoiser."

⚠️ **Đừng nói** "LDM nhanh hơn 16× / 48×" hay "tiết kiệm 16× bộ nhớ". Đó là tỉ lệ số phần tử, không phải tốc độ hay bộ nhớ đo được.

---

## Slide 9: Cross-attention: steering the denoiser with a prompt (C · ~90s)

**Bố cục**: **trái**: khung xanh lá "Prompt → tokens → attention" ($C=\tau_\eta(y)$, công thức $Q,K,V$ và $O$, dòng ký hiệu nhỏ, câu in đậm), 3 gạch đầu dòng · **phải**: nhãn OUR RUN "Stable Diffusion v1.4, seed 2027, same initial latent", 3 ảnh *Reference* | *red → green* | *left → right*, 3 gạch đầu dòng với ✓/✗.

**👉 [Dòng $C = \tau_\eta(y)$]**

> The prompt is first turned into tokens. In Stable Diffusion v1.4, a frozen CLIP text encoder does this.

**👉 [$Q = FW_Q$, rồi $K$, $V$; sau đó dòng ký hiệu nhỏ] ✋**

> In cross-attention, **queries come from the image** features $F$, one row per position, while **keys and values come from the text** tokens $C$. The $W$ matrices are learned projections, and $d$ is the key width.

**👉 [Công thức $O$, rồi câu in đậm cuối khung]**

> Each image position takes a weighted mix of the tokens. So a region that is becoming a bus can draw on "red" and "bus".

**👉 [3 gạch đầu dòng bên trái, lần lượt]**

> This happens at every layer and every step: the prompt steers each prediction; it is not pasted onto the image. Only $\tau_\eta$ depends on the modality: text, a single class token as in our ImageNet model, or a layout. **(cắt được)** Classifier-free guidance mixes the predictions without and with the prompt: a larger $s$ means closer to the prompt but less diverse.

**👉 [Nhãn OUR RUN, rồi ảnh 1 "Reference"]**

> Does it work? Our small test: same seed, same initial latent, three prompts. Reference: "a red bus to the left of a blue car."

**👉 [Ảnh 2 "red → green" rồi gạch ✓ bên dưới]**

> Change red to green: the bus turns green at all four seeds we tried. But the blue car does not clearly appear, and at this seed we even get two green buses.

**👉 [Ảnh 3 "left → right" rồi gạch ✗]**

> Change left to right: no clear swap. The red bus stays on the left.

**👉 [Gạch cuối "Cross-attention is soft"] ✋**

> Cross-attention is **soft**: an attribute can bind to the wrong object, and a token can be ignored. To be clear: this is 16 images checked by eye, an illustration and not a general conclusion.

---

## Slide 10: Pixel vs. latent diffusion on LSUN Churches (C · ~75s)

**Bố cục**: **dòng thiết lập trên cùng** (OUR RUN: T4, batch 1, 50 DDIM steps η = 0, 4 seeds) · **trái**: bảng 3 hàng, khung xanh PAPER REPORTS · **phải**: lưới ảnh 2 × 4 (hàng DDPM, hàng LDM; cột seed 2026–2029) và chú thích · **khung cam Takeaway** dưới cùng.

**👉 [Dòng thiết lập trên cùng]**

> Now our own efficiency test. Pretrained checkpoints, no training by us; one Tesla T4, batch size 1, 50 DDIM steps, four seeds, warm-up excluded.

**👉 [Bảng, hàng "Denoising state"]**

> The pixel DDPM denoises a 256×256×3 state; the latent model works on 32×32×4.

**👉 [Hàng "Median latency": chỉ vào **2.44**]**

> Median latency: 6.10 seconds per image versus 2.44, about **2.5 times faster**, including the decoder.

**👉 [Hàng "Peak CUDA alloc.": chỉ vào **0.75** rồi 1.68] ✋**

> But peak GPU allocation: 0.75 versus 1.68 GiB. The latent model used **more** memory in our setup.

**👉 [Khung xanh PAPER REPORTS]**

> As external evidence, the LDM paper on inpainting: throughput rises from 0.26 to 0.97 samples per second, and FID@2k drops from 24.74 to 15.21. That is a different task, and these are the paper's numbers.

**👉 [Lưới ảnh: hàng DDPM, rồi hàng LDM]**

> By eye, both give plausible churches: a clear steeple from the pixel model at 2028, clear facades from the latent model at 2027 to 2029. The seeds match, but each model draws noise in its own space, so the columns are *not* paired images.

**👉 [Khung cam Takeaway]**

> Takeaway: faster is not the same as cheaper in every resource. Four images per model, one checkpoint pair, no FID: an illustration, not a benchmark.

⚠️ **Đừng nói** lý do LDM tốn bộ nhớ hơn như một sự thật. Nhóm chỉ đo, chưa phân tích (xem phần Q&A bên dưới).

---

## Slide 11: Limitations: training data, copyright and bias (C · ~45s)

**Bố cục**: 3 khung ngang: *1. Training data* (xanh) | *2. Bias* (cam) | *3. Copyright and memorization* (đỏ), khung xám *Method limits* dưới cùng.

**👉 [Khung 1 Training data]**

> First, data: a model only knows what its data contains. Our church model only makes churches; ImageNet conditioning has a fixed class list; text models inherit what their captions describe.

**👉 [Khung 2 Bias: chỉ dòng in đậm cuối]**

> Second, bias: Bianchi et al. show that ordinary prompts can produce demographic stereotypes at scale. Our bus-and-car demo does *not* measure bias.

**👉 [Khung 3 Copyright: lần lượt 3 gạch đầu dòng]**

> Third, copyright: Carlini et al. extracted memorized training images from diffusion models. The U.S. Copyright Office analysis is about U.S. law, not Vietnamese law, and none of this means every generated image is a copy.

**👉 [Khung xám Method limits] (cắt được)**

> And the method itself: many sampling steps, quality capped by the autoencoder, soft cross-attention, and small experiments.

---

## Slide 12: Conclusion: answering the guiding question (C · ~40s)

**Bố cục**: **khung cam lớn** (guiding question + câu trả lời có 3 cụm in đậm) · **3 thẻ**: *1. Forward noising* (xanh dương) | *2. Reverse denoising* (cam) | *3. Latent diffusion* (xanh lá) · dòng nghiêng · "Thank you · Questions?"

**👉 [Khung cam: dòng câu hỏi in đậm, rồi 3 cụm in đậm] ✋**

> Back to our question. Learning to remove noise generates new images because the forward process gives **free training pairs at every noise level**, a network trained to predict the noise learns **shared image structure**, and running it from **fresh noise in many small stochastic steps** turns noise into a new sample.

**👉 [3 thẻ: trái → giữa → phải]**

> Our learning objective in three cards: forward noising is a known Gaussian chain with a closed form; reverse denoising learns to predict the noise and samples step by step; latent diffusion does the same on compact latents, about 2.5 times faster in our run, but with a reconstruction limit and not necessarily lower memory.

**👉 [Dòng nghiêng]**

> Capability is bounded by the training data, and by what we actually measured. Thank you; we are happy to take your questions.

---

## Q&A: câu hỏi → slide để quay lại → người trả lời

| Câu hỏi có thể gặp | Quay về | Ai trả lời | Ý chính |
|---|---|---|---|
| Vì sao dự đoán ε mà không dự đoán mean $\tilde\mu_t$ (hay $x_0$)? | 5 (bảng FID) | B | Cùng một bước Gaussian, nhưng dự đoán mean chỉ tốt với weighted bound (FID 13.22) và không ổn định với plain MSE; ε cùng thang đo ở mọi $t$ nên $L_{\text{simple}}$ đạt FID 3.17. DDPM cũng ghi dự đoán $x_0$ cho chất lượng kém hơn ở thí nghiệm ban đầu (Sec. 3.2). |
| Vì sao ε dự đoán lại là score? | 6 (khung score) | B | Tối ưu MSE cho $\varepsilon_\theta\approx\mathbb E[\varepsilon\mid x_t]$, và $\nabla\log q_t=-\mathbb E[\varepsilon\mid x_t]/\sqrt{1-\bar\alpha_t}$; chỉ là xấp xỉ, đúng ở điểm tối ưu lý tưởng. |
| Vì sao 2 cách ở slide 4 cho cùng $x_2$? | 4 (Way 2) | A | Hai nhiễu Gaussian độc lập gộp thành một Gaussian; phương sai $\alpha_2\beta_1+\beta_2=0.28=1-\bar\alpha_2$. |
| Vì sao $T$ bước nhỏ thay vì một bước? | 3 (gạch Assumptions, biểu đồ) | A | Bước nhỏ thì bước ngược gần Gaussian, dễ học; mọi mức nhiễu là một bài toán huấn luyện; training dùng closed form nên không tốn $T$ bước, chi phí $T$ bước nằm ở sampling. |
| Vì sao $x_T \approx \mathcal N(0, I)$? | 3 (gạch "Why…", biểu đồ) | A | $\mathcal N(0,I)$ được giữ qua mỗi bước; $\bar\alpha_T\approx4\times10^{-5}$; với $T$ hữu hạn thì chỉ xấp xỉ. |
| Vì sao không sinh ảnh trong một bước? | 6 (gạch "Remove a little at a time") | B | Train $x_T\to x_0$ bằng MSE cho $\mathbb E[x_0\mid x_T]\approx\mathbb E[x_0]$, tức ảnh trung bình bị mờ, vì $x_T$ gần như không chứa thông tin về $x_0$. |
| VAE khác autoencoder thường? Sao không decode $z\sim\mathcal N(0,I)$? | 7 | B | Encoder xuất phân phối + KL + reparameterization; latent sạch không phải $\mathcal N(0,I)$. |
| Vì sao perceptual + adversarial thay vì MSE? | 7 | B | MSE theo pixel lấy trung bình các chi tiết khả dĩ nên ảnh mờ. |
| Cross-attention khác self-attention? | 9 | C | Q từ ảnh; K, V từ điều kiện (với self-attention thì cả ba từ ảnh). |
| Vì sao LDM nhanh hơn mà tốn bộ nhớ đỉnh hơn? | 10 | C | Nói thật: nhóm chỉ đo, chưa phân tích. Hai checkpoint khác kiến trúc/decoder; đây là giả thuyết chưa kiểm chứng. |
| Thí nghiệm có chứng minh latent tốt hơn pixel? | 10 | C | Không: 4 mẫu, 1 cặp checkpoint, không FID. Chỉ là minh họa, kèm số liệu Table 6 của paper. |
| Diffusion có sao chép ảnh huấn luyện? | 11 | C | Carlini et al.: memorization có thể xảy ra, nhưng không phải mọi ảnh sinh ra đều là bản sao. |
| Một ký hiệu nghĩa là gì / miền giá trị? | Backup 13 | ai cũng được | Bảng Notation, value ranges and modelling assumptions. |
| Có bằng chứng nào mạng "thấy" ảnh khi trạng thái còn đầy nhiễu? | Backup 14 | B | Run của nhóm: ở bước DDIM 25/50, clean estimate $\hat x_0$ đã thấy con chó (cả pixel ADM và latent LDM); updated state chỉ nhích một bước nhỏ. |
| Nguồn hình/số liệu? | Backup 15–16 | ai cũng được | Sơ đồ là hình tự vẽ; run dùng checkpoint pretrained; số paper ghi rõ nguồn. |

**Mẹo khi trả lời**: luôn bấm về slide liên quan và **chỉ vào đúng khung** trước khi trả lời. Như vậy người hỏi thấy câu trả lời đã nằm trong bài.

---

## Checklist trước giờ trình bày

- [ ] Mỗi người tập riêng phần của mình với đồng hồ: **A ≈ 4.6 phút** (slide 1–4, 275s), **B ≈ 5.6 phút** (slide 5–8, 335s), **C ≈ 4.2 phút** (slide 9–12, 250s). B đang dài hơn hai người còn lại khoảng 1 phút; nếu muốn cân hơn, chuyển slide 8 cho C (A 275s, B 255s, C 330s).
- [ ] Tập 2 lần chuyển người (sau slide 4, sau slide 8) cho liền mạch.
- [ ] Chuẩn bị laser/pointer. Nếu không có, đứng cạnh màn hình và chỉ bằng tay theo các 👉.
- [ ] Đánh dấu sẵn các câu **(cắt được)** để bỏ nếu trễ hơn 30 giây.
- [ ] Mỗi thành viên nhận ít nhất một câu Q&A trong bảng trên.
