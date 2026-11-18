# Presentation script: Diffusion Models, From Adding Noise to Generating Images

Script thuyết trình cho deck [main.tex](main.tex) (12 slide nội dung + 2 slide backup).

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
| Xanh dương nhạt (`fwd`) | Forward noising: cố định, đã biết | dải FORWARD slide 5, khung slide 3 |
| Cam (`rev`) | Reverse denoising: học được; đồng thời là nhãn **OUR RUN** | dải REVERSE slide 5, khung sampling slide 6 |
| Xanh lá (`ok`) | Latent diffusion / autoencoder; nhãn **OUR EXAMPLE** | khung autoencoder slide 7–8 |
| Xanh đậm | Nhãn **PAPER REPORTS**: số liệu của paper, không phải của nhóm | slide 5, 8, 10 |

Mỗi khi đọc một con số, **chỉ vào nhãn PAPER REPORTS / OUR RUN / OUR EXAMPLE bên cạnh** để người nghe biết số đó của ai.

---

## Skeleton tổng thể

| # | Slide | Người nói | Thời lượng | Phần | Thông điệp một câu |
|---|---|---|---|---|---|
| 1 | Title + guiding question + learning objective | A | 45s | Mở đầu | Học khử nhiễu thì làm sao sinh ra ảnh mới? |
| 2 | Where diffusion fits | A | 70s | Mở đầu | Diffusion học cấu trúc ảnh bằng cách đảo ngược một quá trình làm hỏng đã biết. |
| 3 | Forward noising | A | 90s | A · Forward | Forward là chuỗi Gaussian đã biết; công thức đóng nhảy thẳng tới mọi bước $t$. |
| 4 | Forward by hand and by eye | A | 80s | A · Forward | Kỳ vọng khác mẫu ngẫu nhiên; SNR giảm thì cấu trúc biến mất. |
| 5 | Reverse denoising | B | 90s | B · Reverse | Mạng chỉ học dự đoán nhiễu; huấn luyện là hồi quy MSE. |
| 6 | From denoising to generation | B | 110s | B · Reverse | **Trả lời guiding question**: free supervision, shared structure, small stochastic steps. |
| 7 | Inside the autoencoder | B | 80s | C · Latent | Autoencoder nén ảnh thành latent và được đóng băng (frozen). |
| 8 | Why latent diffusion is cheaper | B | 90s | C · Latent | Vòng lặp giữ nguyên, trạng thái nhỏ hơn: mỗi bước rẻ hơn. |
| 9 | Cross-attention | C | 100s | C · Latent | Prompt điều khiển từng bước qua attention mềm; đổi màu được, đổi trái/phải thì không. |
| 10 | Pixel vs latent on LSUN Churches | C | 80s | D · Evidence | Nhanh hơn khoảng 2.5 lần nhưng tốn bộ nhớ đỉnh hơn; chỉ là minh họa. |
| 11 | Limitations | C | 50s | D · Evidence | Dữ liệu, bias, copyright, và giới hạn của chính thí nghiệm. |
| 12 | Conclusion | C | 45s | Kết | Trả lời lại guiding question và 3 vế của learning objective. |
| | **Tổng** | | **~930s ≈ 15.5 phút** | | Nếu cần đúng 15 phút, bỏ các câu **(cắt được)** ở slide 3, 6, 9. |

**Sợi chỉ xuyên suốt**: guiding question được đặt ở slide 1, trả lời ở slide 6, nhắc lại ở slide 12. Learning objective được nêu ở slide 1, phần latent được trả lời ở slide 8, tổng kết ở slide 12.

---

## Slide 1: Title, guiding question, learning objective (A · ~45s)

**Bố cục**: dải tiêu đề xanh phía trên · **trái**: khung cam GUIDING QUESTION, bên dưới là khung xanh LEARNING OBJECTIVE (3 cụm từ tô màu) · **phải**: 4 ảnh ngôi nhà $t=0\to1000$, mũi tên xanh "forward noising (fixed)" ở trên, mũi tên cam "reverse denoising (learned)" ở dưới.

> Good morning everyone. We are Cao Quang Hung, Nguyen Trong Van Viet and Huynh Chi Ton, and today we present *Diffusion Models: From Adding Noise to Generating Images*.

**👉 [Dải ảnh bên phải: quét theo mũi tên xanh từ $t=0$ đến $t=1000$]**

> Start with this small house. If we add a little Gaussian noise again and again, after a thousand steps nothing is left but noise. Destroying an image is easy.

**👉 [Mũi tên cam phía dưới: quét từ phải sang trái]**

> The hard direction is the reverse. A denoiser cleans an image that already exists, but a generator must produce an image that never existed.

**👉 [Khung cam GUIDING QUESTION] ✋**

> So our guiding question is: **how can learning to remove noise enable a model to generate new images?**

**👉 [Khung xanh LEARNING OBJECTIVE: chỉ lần lượt 3 cụm màu xanh dương → cam → xanh lá]**

> And our learning objective: by the end of this talk, you should be able to explain **forward noising**, **reverse denoising**, and **why latent diffusion reduces computational demands**. These three phrases are also the three parts of our talk.

**Chuyển ý**: "To see why this works, let's first place diffusion among other generative models."

---

## Slide 2: Where diffusion fits (A · ~70s)

**Bố cục**: **cột trái**: ô xám *Discriminative*, ô xanh *Generative*, bên dưới là *Timeline* 2015–2022 · **cột phải**: hình 3 panel GAN (tím) | Autoregressive (xanh) | Diffusion (xanh lá), thanh "Core difference" ở đáy.

**👉 [Ô xám Discriminative]**

> First, a discriminative model learns $p(y \mid x)$. To answer "is this a cat?", it only needs features that separate the classes.

**👉 [Ô xanh Generative]**

> A generative model learns $p(x)$ or $p(x \mid y)$. To *create* a cat, it must capture shape, texture, lighting and layout, which is much more information.

**👉 [Panel GAN màu tím: chỉ Generator → Discriminator → "adversarial training"]**

> There are three main families. A GAN maps noise to an image in one pass, but training is a game between a generator and a discriminator, and it can suffer from mode collapse.

**👉 [Panel Autoregressive: chuỗi token $x_1, x_2, \dots$]**

> An autoregressive model factorizes the image and generates it token by token. It gives good likelihood estimates, but sampling is slow and sequential.

**👉 [Panel Diffusion: hàng trên "forward process", rồi hàng dưới "reverse process"]**

> Diffusion adds noise in a fixed forward process and learns to remove it step by step. It trains stably and gives high quality and diversity, but sampling needs many steps. Remember that cost; it comes back later.

**👉 [Thanh "Core difference" dưới đáy hình]**

> In one line: one pass, token by token, or denoising over many steps.

**👉 [Timeline bên trái: chỉ nhanh 4 mốc]**

> Historically: the diffusion framework in 2015, score-based generation in 2019, then DDPM in 2020 and latent diffusion in 2022, which are the two papers we focus on.

**Chuyển ý**: "Let's start with the easy direction: forward noising."

⚠️ **Đừng nói** "diffusion luôn tốt hơn GAN". Hình chỉ mô tả hành vi điển hình, không phải đảm bảo.

---

## Slide 3: Forward noising (A · ~90s)

**Bố cục**: **dải sơ đồ trên**: $x_0 \to x_{t-1} \to$ [Known Gaussian kernel] $\to x_t \to x_T$, nhãn "clean data" / "nearly noise" · **khung xanh trái**: 2 phương trình (phương trình thứ hai đóng khung) · **3 gạch đầu dòng phải** · **khung cam dưới**: "Why $T=1000$ small steps?"

**👉 [Dải sơ đồ: quét từ $x_0$ (clean data) sang $x_T$ (nearly noise)]**

> The forward process takes a clean image $x_0$ and adds noise over $T$ steps, until $x_T$ is nearly pure noise.

**👉 [Ô "Known Gaussian kernel" ở giữa dải]**

> Each step is a *known* Gaussian: the mean is $\sqrt{1-\beta_t}$ times the previous state, and the variance is $\beta_t$. Nothing here is learned.

**👉 [Khung xanh, phương trình dòng 1]**

> As a sample: $x_t$ equals $\sqrt{1-\beta_t}$ times $x_{t-1}$, plus $\sqrt{\beta_t}$ times fresh Gaussian noise.

**👉 [Gạch đầu dòng 1 bên phải]**

> So $\beta_t$ plays two roles: it *shrinks* the old signal and *sets* the new noise level.

**👉 [Phương trình đóng khung] ✋**

> The key result is this boxed formula. Because Gaussian steps compose, we can jump from $x_0$ to *any* step $t$ in one shot, using $\bar\alpha_t$, the product of the alphas. Here $t$ counts steps; it is not physical time.

**👉 [Gạch đầu dòng 2 và 3]**

> The standard normal is stationary, so after $T$ steps $x_T$ is approximately $\mathcal N(0, I)$: we know exactly where generation will start. DDPM uses $T = 1000$, with $\beta_t$ growing linearly from $10^{-4}$ to $0.02$.

**👉 [Khung cam dưới cùng: chỉ (1) rồi (2)]**

> Why a thousand small steps instead of one big step? First, small steps keep each *reverse* step easy: nearly Gaussian, just a small correction. Second, every noise level becomes a training task, from fine detail to coarse layout; that second point is our reading. **(cắt được)** And training does not pay for $T$ steps, thanks to the closed form. The cost appears at sampling, as we'll see on slide 6.

---

## Slide 4: Forward noising by hand and by eye (A · ~80s)

**Bố cục**: **khung xanh lá trái** "1-D calculation" (nhãn OUR EXAMPLE) · **3 gạch đầu dòng phải** · **dưới**: 5 ảnh ngôi nhà 28×28 với nhãn SNR màu xanh ở dưới mỗi ảnh.

**👉 [Khung xanh lá, dòng đầu: $x_0 = 0.8, \beta_1 = 0.1, \varepsilon = -0.5$]**

> Let's do one step by hand. One pixel with value $x_0 = 0.8$, $\beta_1 = 0.1$, and suppose the noise draw is $\varepsilon = -0.5$. Then $\alpha_1 = 0.9$.

**👉 [Lần lượt 3 dòng của phép tính]**

> The signal part: $\sqrt{0.9}\times 0.8 = 0.7589$. The noise part: $\sqrt{0.1}\times(-0.5) = -0.1581$. Add them: $x_1 = 0.6008$.

**👉 [Gạch đầu dòng 1–2 bên phải] ✋**

> What does that mean? Given $x_0$, $x_1$ is Gaussian with mean $0.7589$ and variance $0.1$, so a standard deviation of about $0.32$. The *expected* value is $0.7589$ because the noise has mean zero. $0.6008$ is just *one* random realization; another draw gives another $x_1$.

**👉 [Gạch đầu dòng 3]**

> We chose $\beta = 0.1$ on purpose so the arithmetic is visible. The images below use the small DDPM schedule.

**👉 [Dải 5 ảnh: quét trái sang phải, dừng ở từng nhãn SNR]**

> Now by eye: our synthetic 28×28 house, one trajectory with $T = 1000$. Under each image is the signal-to-noise ratio, $\bar\alpha_t / (1-\bar\alpha_t)$. At $t = 50$, the SNR is 33.5 and the house is clearly visible. At $t = 200$, about 2. By $t = 500$ the SNR is below 0.1 and noise dominates. At $t = T$, almost nothing is left.

**Chuyển người (A → B)**: "So destroying structure is easy and fully known. [Tên B] will now show how we *learn* to undo it."

⚠️ **Đừng nói** ảnh ngôi nhà được sinh bởi một mô hình. Đây chỉ là forward noising, không có mạng nào.

---

## Slide 5: Reverse denoising (B · ~90s)

**Bố cục**: **sơ đồ hai dải**: dải xanh FORWARD ở trên (trái → phải), dải cam REVERSE ở dưới (**phải → trái**: $x_T \to x_t \to$ [neural net $\varepsilon_\theta$] $\to$ [sampler] $\to x_{t-1} \to x_0$) · **khung cam trái** "One reverse step" · **khung xanh phải** "Training objective" (nhãn PAPER REPORTS ở đáy).

**👉 [Dải xanh FORWARD phía trên]**

> Here are both directions together. The blue band is the forward process we just saw: known and fixed.

**👉 [Dải cam REVERSE: kéo tay từ $x_T$ bên phải sang $x_0$ bên trái] ✋**

> The orange band is what we *learn*, and it runs right to left, from $x_T$ back to $x_0$.

**👉 [Ô "neural net $\varepsilon_\theta(x_t,t)$" và nhãn "timestep $t$" phía trên]**

> At each step, a neural network receives the noisy state $x_t$ and the timestep $t$, and predicts the noise inside it.

**👉 [Ô "sampler $\mu_\theta + \sigma_t u_t$" và nhãn $u_t$]**

> A sampler turns that prediction into a mean, $\mu_\theta$, adds a little fresh noise $\sigma_t u_t$, and gives $x_{t-1}$.

**👉 [Khung cam, công thức $\mu_\theta$: chỉ vào $\varepsilon_\theta$ in đậm]**

> In formula form: the reverse step is Gaussian, and its mean is $x_t$ minus a scaled noise prediction, divided by $\sqrt{\alpha_t}$. The bold $\varepsilon_\theta$ is the only learned part.

**👉 [Dòng "Why predict $\varepsilon$, not $x_0$?"]**

> Why predict the noise rather than the clean image? The noise is standard normal, a simple and normalized target at every $t$. It also encodes the *score*, the direction toward higher data density.

**👉 [Khung xanh, công thức $L_{\text{simple}}$]**

> Training is just regression. $L_{\text{simple}}$ is the expected squared error between the true noise and the predicted noise.

**👉 [3 bước đánh số]**

> Pick an image, a random $t$ and random noise; build $x_t$ with the closed form from slide 3; predict the noise and take a gradient step.

**👉 [Nhãn PAPER REPORTS ở đáy khung]**

> This simple loss works well. On CIFAR-10, Ho et al. report an FID of 3.17, versus 13.51 when training on the full variational bound; lower is better. These are the paper's numbers, not ours.

⚠️ **Đừng nói** "$L_{\text{simple}}$ làm sampling nhanh hơn". Nó chỉ là bản reweighted của variational bound. Đạo hàm KL / posterior mean để dành cho Q&A.

---

## Slide 6: From denoising to generation (B · ~110s), slide quan trọng nhất

**Bố cục**: **trái**: khung cam "Sampling" (3 bước), danh sách "Why removing noise generates new images" (1–2–3), khung đỏ "Why not one step?" · **phải**: hình golden retriever 2 hàng × 4 cột (hàng trên **ADM** pixel, hàng dưới **LDM** latent; cột: *Noisy input* | *Predicted noise* / *Guided latent noise RMS* | **Clean estimate** | *Updated state*), nhãn OUR RUN, 2 gạch đầu dòng.

> Now we can answer the guiding question.

**👉 [Khung cam Sampling: chỉ lần lượt bước 1 → 2 → 3]**

> Generation needs no real image. Step one: draw fresh noise $x_T$. Step two: for $t$ from $T$ down to 1, apply the learned step, which is the mean plus a little fresh noise. Step three: return $x_0$. At the very last step, no noise is added.

**👉 [Danh sách 1–2–3 "Why removing noise generates new images"] ✋ (đây là câu trả lời chính)**

> Why does removing noise produce *new* images? Three reasons.
> **One, free supervision**: the forward process gives us pairs of noisy input and true noise at every level, with no labels.
> **Two, shared structure**: to predict the noise across many images, the network must learn what images have in common: edges, textures, object shapes.
> **Three, small stochastic steps**: each step is a gentle correction, and the fresh noise $u_t$ means every seed leads to a different image.

**👉 [Khung đỏ "Why not one step?"]**

> Why not jump straight from noise to an image? If we train $x_T \to x_0$ with squared error, the best answer is the conditional mean. But $x_T$ carries almost no information about $x_0$, so that mean is just the average image, a blur. Small forward steps are what make small reverse steps possible.

**👉 [Hình bên phải: nhãn OUR RUN và tiêu đề "Inside DDIM step 25"]**

> Here is what this looks like in our run with pretrained models: halfway through generation, at DDIM update 25 of 50, for the class "golden retriever".

**👉 [Hàng trên (ADM): cột 1 "Noisy input", rồi nhảy sang cột 3 "Clean estimate"] ✋**

> Top row: the pixel-space ADM model. The current state still looks like noise, but the network's *clean estimate* already shows a head and a muzzle.

**👉 [Hàng dưới (LDM): cột 3]**

> Bottom row: the latent model. Same story: the dog is already there in the estimate.

**👉 [Cột 4 "Updated state" của cả hai hàng]**

> But the updated state moves only a small step toward that estimate. That is the mechanism: the estimate guides, and small steps refine.

> **(cắt được)** If we run the forward process from the final image instead, the retriever's features fade out gradually, just like the house on slide 4.

**Chuyển ý**: "This loop works, but every step processes a full-resolution image, many times. Making each step cheaper is the job of latent diffusion."

💡 Nếu bị hỏi về cột 2 hàng LDM (heatmap tím): đó là độ lớn RMS theo kênh của nhiễu latent dự đoán (đã có guidance) tại từng vị trí, không phải một ảnh.

⚠️ **Đừng nói** 50 bước DDIM là của DDPM gốc. Khung sampling bên trái là Algorithm 2 của DDPM; run của nhóm dùng sampler DDIM 50 bước.

---

## Slide 7: Inside the autoencoder (B · ~80s)

**Bố cục**: **chuỗi trên cùng**: $x_0$ → [Encoder $\mathcal E_\phi$] → [$\mu_\phi, \sigma_\phi$] → [cam: $\tilde z = \mu + \sigma\odot\xi$] → [Decoder $D_\psi$] → $\hat x_0$ · **3 khung dưới**: *VAE objective* (xanh) | *LDM: a perceptual compressor* (xanh lá) | *What changes for diffusion* (cam).

> Latent diffusion begins with an autoencoder.

**👉 [Chuỗi trên: $x_0$ (nhãn $H\times W\times 3$) → Encoder → ô $\mu, \sigma$]**

> The encoder takes an $H \times W \times 3$ image and outputs a distribution: a mean and a standard deviation for every latent value.

**👉 [Ô cam $\tilde z = \mu + \sigma\odot\xi$ và nhãn latent bên dưới]**

> We sample a latent with the reparameterization trick. It has size $h \times w \times c$, where $h = H/f$ and $f$ is the downsampling factor.

**👉 [Decoder → $\hat x_0$ "reconstruction"]**

> The decoder maps the latent back to an image.

**👉 [Khung xanh VAE objective: chỉ "Reconstruction", rồi "KL", rồi chữ **Problem**]**

> A textbook VAE trains this with two terms: reconstruction, plus a KL term that keeps the codes close to $\mathcal N(0, I)$. The problem: pixel-wise squared error averages plausible details, so reconstructions turn blurry.

**👉 [Khung xanh lá: chỉ 1 → 2 → 3, rồi dòng "Ours"]**

> So LDM trains a *perceptual* compressor: a perceptual loss that compares deep features, a patch-based adversarial loss for realistic texture, and only a light regularizer, either a weak KL or a VQ codebook. Our runs use both kinds: KL with $f = 8$ for Churches, and VQ with $f = 4$ for ImageNet.

**👉 [Khung cam "What changes for diffusion": lần lượt 4 dấu chấm] ✋ ở dấu chấm 3**

> For diffusion, four points matter. The latent keeps its 2-D layout, so a U-Net can still process it. The autoencoder is trained once, then **frozen**. Clean latents are *not* standard normal, so we cannot simply decode random noise; diffusion has to learn the distribution of latents. And the encoder noise $\xi$ is not the diffusion noise $\varepsilon_z$.

⚠️ Sơ đồ vẽ biến thể KL ($\mu, \sigma$). Biến thể VQ không có $\mu, \sigma$. Nếu bị hỏi, nói rõ điều này.

---

## Slide 8: Why latent diffusion is cheaper (B · ~90s)

**Bố cục**: **hàng TRAINING**: $x_0$ → [Encoder, frozen, scale $a$] → $z_0$ → [add noise] → [conditional U-Net] ← [$\tau_\eta(y)$] (nhãn "cross-attn") · **hàng GENERATION**: [$z_T$ noise] → [U-Net + sampler] → [Decoder (frozen)] → $\hat x_0$, chú thích "no real image or encoder needed" · **khung xanh lá trái** "Smaller state per denoising step" · **khung xanh phải** "Same principle, new space".

> Here is the full pipeline, and our answer to the last part of the learning objective.

**👉 [Hàng TRAINING: quét trái → phải tới ô U-Net]**

> Training: encode a real image with the frozen encoder, scale it by $a$, and get $z_0$. Add noise exactly as before. A conditional U-Net predicts the noise $\varepsilon_z$.

**👉 [Ô $\tau_\eta(y)$ bên phải và nhãn "cross-attn"]**

> The condition $y$, such as text or a class, enters through an encoder $\tau_\eta$ and cross-attention. That is the next slide.

**👉 [Hàng GENERATION: $z_T$ → U-Net + sampler → Decoder → $\hat x_0$]**

> Generation: start from latent noise $z_T$, run the U-Net and sampler for many steps, and decode **once** at the end.

**👉 [Chú thích "no real image or encoder needed"]**

> No real image and no encoder are needed at generation time.

**👉 [Khung xanh lá "Smaller state per denoising step": gạch 1 (PAPER REPORTS), gạch 2 (OUR EXAMPLE)] ✋**

> So why is it cheaper? The loop is identical; the *state* is smaller. With $f = 4$, a 256×256 image becomes 64×64: **16 times fewer spatial positions**, as in the paper. For our LSUN Churches model, 196,608 values become 4,096, **about 48 times fewer**. Every one of the many U-Net calls works on that small state.

**👉 [Khung xanh: công thức $L_{\text{LDM}}$]**

> The loss is the same noise-prediction loss, now on latents and with a condition.

**👉 [Chữ **Caveat** trong khung xanh]**

> Two cautions. Forty-eight times fewer values does *not* mean forty-eight times faster, because runtime and memory depend on the networks too. And DDIM, which uses fewer steps, is a separate speedup. Compression also caps quality: fine text and small objects can be lost.

**Chuyển người (B → C)**: "[Tên C] will now show how the condition actually steers the denoiser."

⚠️ **Đừng nói** "LDM nhanh hơn 16× / 48×" hay "tiết kiệm 16× bộ nhớ". Đó là tỉ lệ số phần tử, không phải tốc độ hay bộ nhớ đo được.

---

## Slide 9: Cross-attention and prompt control (C · ~100s)

**Bố cục**: **trái**: khung xanh lá "Prompt → tokens → attention" (công thức $Q, K, V$, $O$; câu in đậm), 3 gạch đầu dòng · **phải**: nhãn OUR RUN, 3 ảnh *Reference* | *red → green* | *left → right* (seed 2027), 3 gạch đầu dòng với ✓/✗.

**👉 [Khung xanh lá, dòng $C = \tau_\eta(y)$]**

> The prompt is first encoded into tokens. In Stable Diffusion v1.4, a frozen CLIP text encoder does this.

**👉 [$Q = FW_Q$, rồi $K = CW_K$, $V = CW_V$] ✋**

> In cross-attention, **queries come from the image** features $F$, while **keys and values come from the text** tokens $C$.

**👉 [Công thức $O = \mathrm{softmax}(\cdot)V$]**

> Each image position computes a weighted mix of the tokens.

**👉 [Câu in đậm cuối khung]**

> So a region that is becoming a bus can draw on the tokens "red" and "bus".

**👉 [3 gạch đầu dòng bên trái, lần lượt]**

> This happens at every layer and every step: the prompt steers each prediction; it is not pasted onto the final image. Only $\tau_\eta$ depends on the modality: text, a single class token as in our ImageNet model, or a layout. Maps and masks are concatenated with $z_t$ instead. **(cắt được)** Classifier-free guidance then pushes predictions toward the prompt: a larger $s$ means closer to the prompt but less diverse.

**👉 [Nhãn OUR RUN và dòng "seed 2027, same initial latent"]**

> Does it work? Our small test: same seed, same initial latent, three prompts.

**👉 [Ảnh 1 "Reference"]**

> Reference: "a red bus to the left of a blue car."

**👉 [Ảnh 2 "red → green" rồi gạch đầu dòng ✓ bên dưới]**

> Change red to green: the bus turns green, at all four seeds we tried. But the blue car does not clearly appear, and at this seed we even get two green buses.

**👉 [Ảnh 3 "left → right" rồi gạch đầu dòng ✗]**

> Change left to right: no clear swap. The red bus stays on the left.

**👉 [Gạch đầu dòng cuối "Cross-attention is soft"] ✋**

> Cross-attention is **soft**: an attribute can bind to the wrong object, and a token can be ignored. And to be clear: this is 16 images checked by eye, an illustration and not a general conclusion.

---

## Slide 10: Pixel vs latent on LSUN Churches (C · ~80s)

**Bố cục**: **dòng thiết lập trên cùng** (OUR RUN: T4, batch 1, 50 DDIM, 4 seeds) · **trái**: bảng 3 hàng, khung xanh PAPER REPORTS · **phải**: lưới ảnh 2 × 4 (hàng DDPM, hàng LDM; cột seed 2026–2029) và chú thích · **khung cam Takeaway** dưới cùng.

**👉 [Dòng thiết lập trên cùng]**

> Now our own efficiency test. Pretrained checkpoints, no training by us; one Tesla T4, batch size 1, 50 DDIM steps, four seeds, warm-up excluded.

**👉 [Bảng, hàng "Denoising state"]**

> The pixel DDPM denoises a 256×256×3 state; the latent model works on 32×32×4.

**👉 [Hàng "Median latency": chỉ vào **2.44**]**

> Median latency: 6.10 seconds per image versus 2.44, about **2.5 times faster**, and that includes the decoder.

**👉 [Hàng "Peak CUDA alloc.": chỉ vào **0.75** rồi 1.68] ✋**

> But peak GPU allocation: 0.75 versus 1.68 GiB. The latent model used **more** memory in our setup.

**👉 [Khung xanh PAPER REPORTS]**

> As external evidence, the LDM paper on inpainting at 256²: sampling throughput rises from 0.26 to 0.97 samples per second, and FID@2k drops from 24.74 to 15.21. That is a different task, and these are the paper's numbers.

**👉 [Lưới ảnh: hàng DDPM (seed 2028, 2029), rồi hàng LDM (2027–2029, 2026)]**

> Quality by eye: both give plausible churches. Pixel model: a clear steeple at seed 2028, while the dark 2029 image hides detail. Latent model: clear facades at 2027 to 2029, and 2026 is a distant complex. The seeds match, but each model draws noise in its own space, so the columns are *not* paired images.

**👉 [Khung cam Takeaway]**

> Takeaway: faster is not the same as cheaper in every resource. Four images per model, one checkpoint pair, no FID: an illustration, not a benchmark.

⚠️ **Đừng nói** lý do LDM tốn bộ nhớ hơn như một sự thật. Nhóm chỉ đo, chưa phân tích (xem phần Q&A bên dưới).

---

## Slide 11: Limitations (C · ~50s)

**Bố cục**: 3 khung ngang: *1. Training data* (xanh) | *2. Bias* (cam) | *3. Copyright and memorization* (đỏ), khung xám *Method limits* dưới cùng.

**👉 [Khung 1 Training data]**

> First, data: a model only knows what its data contains. Our church model only makes churches, ImageNet conditioning has a fixed class list, and text models inherit what their captions describe.

**👉 [Khung 2 Bias: chỉ dòng in đậm cuối]**

> Second, bias: Bianchi et al. show that ordinary prompts can produce demographic stereotypes at scale. Our bus-and-car demo does *not* measure bias.

**👉 [Khung 3 Copyright: lần lượt 3 gạch đầu dòng]**

> Third, copyright: Carlini et al. extracted memorized training images from diffusion models, so data provenance matters. The U.S. Copyright Office analysis is about U.S. law, not Vietnamese law, and none of this means every generated image is a copy.

**👉 [Khung xám Method limits]**

> And the method itself has limits: many sampling steps, quality capped by the autoencoder, soft cross-attention, and our experiments are small illustrations, not benchmarks.

---

## Slide 12: Conclusion (C · ~45s)

**Bố cục**: **khung cam lớn** (guiding question + câu trả lời có 3 cụm in đậm) · **3 thẻ**: *1. Forward noising* (xanh dương) | *2. Reverse denoising* (cam) | *3. Latent diffusion* (xanh lá) · dòng nghiêng · "Thank you · Questions?"

**👉 [Khung cam: dòng câu hỏi in đậm]**

> Back to our guiding question: how can learning to remove noise enable a model to generate new images?

**👉 [3 cụm in đậm trong câu trả lời, lần lượt] ✋**

> Because the forward process gives **free training pairs at every noise level**, a network trained to predict the noise learns **shared image structure**, and running it from **fresh noise in many small stochastic steps** turns noise into a new sample.

**👉 [3 thẻ: trái → giữa → phải]**

> Our learning objective in three cards. Forward noising is a known Gaussian chain with a closed form. Reverse denoising learns to predict the noise and samples step by step. Latent diffusion applies the same principle to compact latents: about 2.5 times faster in our run, with prompts through cross-attention, at the cost of a reconstruction limit and not necessarily lower memory.

**👉 [Dòng nghiêng]**

> Capability is bounded by the training data, and by what we actually measured.

> Thank you. We are happy to take your questions.

---

## Q&A: câu hỏi → slide để quay lại → người trả lời

| Câu hỏi có thể gặp | Quay về | Ai trả lời | Ý chính |
|---|---|---|---|
| Vì sao dự đoán $\varepsilon$ mà không phải $x_0$? | 5 | A/B | Target $\mathcal N(0,I)$ đã chuẩn hóa ở mọi $t$; liên hệ score $-\varepsilon_\theta/\sqrt{1-\bar\alpha_t}$. |
| Vì sao $T$ bước nhỏ thay vì một bước? | 3, 6 | A | Bước ngược gần Gaussian nên dễ học; mọi mức nhiễu là một bài toán; training dùng closed form. |
| Vì sao $x_T \approx \mathcal N(0,I)$? | 3, 4 | A | $\bar\alpha_T$ rất nhỏ, SNR ≈ $4\times10^{-5}$; với $T$ hữu hạn thì chỉ xấp xỉ, không bằng chính xác. |
| Vì sao không sinh ảnh trong một bước? | 6 (khung đỏ) | B | MSE cho $\mathbb E[x_0 \mid x_T] \approx \mathbb E[x_0]$, tức ảnh trung bình bị mờ. |
| VAE khác autoencoder thường? Sao không decode $z\sim\mathcal N(0,I)$? | 7 | B | Encoder xuất phân phối + KL + reparameterization; latent sạch không phải $\mathcal N(0,I)$. |
| Vì sao perceptual + adversarial thay vì MSE? | 7 | B | MSE theo pixel lấy trung bình các chi tiết khả dĩ nên ảnh mờ. |
| Cross-attention khác self-attention? | 9 | C | Q từ ảnh; K, V từ điều kiện (với self-attention thì cả ba từ ảnh). |
| Vì sao LDM nhanh hơn mà tốn bộ nhớ đỉnh hơn? | 10 | C | Nói thật: nhóm chỉ đo, chưa phân tích. Hai checkpoint khác kiến trúc/decoder; đây là giả thuyết chưa kiểm chứng. |
| Thí nghiệm có chứng minh latent tốt hơn pixel? | 10 | C | Không: 4 mẫu, 1 cặp checkpoint, không FID. Chỉ là minh họa, kèm số liệu Table 6 của paper. |
| Diffusion có sao chép ảnh huấn luyện? | 11 | C | Carlini et al.: memorization có thể xảy ra, nhưng không phải mọi ảnh sinh ra đều là bản sao. |
| Nguồn hình/số liệu? | Backup 13–14 | ai cũng được | Sơ đồ là hình tự vẽ; run dùng checkpoint pretrained; số paper ghi rõ nguồn. |

**Mẹo khi trả lời**: luôn bấm về slide liên quan và **chỉ vào đúng khung** trước khi trả lời. Như vậy người hỏi thấy câu trả lời đã nằm trong bài.

---

## Checklist trước giờ trình bày

- [ ] Mỗi người tập riêng phần của mình với đồng hồ (A ≈ 4.8 phút, B ≈ 6.2 phút, C ≈ 4.6 phút).
- [ ] Tập 2 lần chuyển người (sau slide 4, sau slide 8) cho liền mạch.
- [ ] Chuẩn bị laser/pointer. Nếu không có, đứng cạnh màn hình và chỉ bằng tay theo các 👉.
- [ ] Đánh dấu sẵn các câu **(cắt được)** để bỏ nếu trễ hơn 30 giây.
- [ ] Mỗi thành viên nhận ít nhất một câu Q&A trong bảng trên.
