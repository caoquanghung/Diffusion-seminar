# Presentation script: Diffusion Models, From Adding Noise to Generating Images

Script thuyết trình cho deck [main.tex](main.tex): 13 slide (slide 1 là title kèm guiding question; 12 slide nội dung), cộng 5 slide backup (14: Notation, 15: Inside one denoising step, 16: LDM details, 17–18: References).

**Cách đọc file này**

- Lời nói để trong khung trích dẫn (`>`) và viết bằng **tiếng Anh**, khớp với chữ trên slide. Chỉ dẫn sân khấu viết bằng tiếng Việt.
- **👉 [ ... ]**: chỉ tay / laser vào đúng vùng đó **trước khi** đọc câu ngay sau.
- **✋**: dừng khoảng 1 giây và nhấn giọng. Đây là các câu người nghe cần nhớ.
- **(cắt được)**: câu có thể bỏ khi trễ giờ.
- **⚠️ Đừng nói**: những phát biểu vượt quá bằng chứng của nhóm.
- Phân công người nói theo [slide-outline.md](../slide-outline.md): **A** slide 1–4, **B** slide 5–8, **C** slide 9–13. Có thể đổi tên tùy nhóm.

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
| 7 | From DDPM to LDM: the cost of pixels, and three ideas | B | 60s | C · Latent | Pixel diffusion tốn kém vì mọi bước chạm mọi pixel; LDM có 3 ý tưởng chính. |
| 8 | Latent space: an autoencoder that compresses images (stage 1) | B | 65s | C · Latent | Autoencoder nén ảnh thành lưới latent 2-D nhỏ, rồi được đóng băng. |
| 9 | Operations in latent space: the whole LDM pipeline | C | 75s | C · Latent | Vòng lặp DDPM giữ nguyên nhưng chạy trên $z$ nhỏ; encoder chỉ dùng khi train, decoder chạy một lần. |
| 10 | Cross-attention: steering the denoiser with a prompt | C | 80s | C · Latent | Vùng ảnh "hỏi", từ trong prompt "trả lời"; đổi màu được, đổi trái/phải thì không. |
| 11 | Pixel vs. latent diffusion on LSUN Churches | C | 70s | D · Evidence | Nhanh hơn khoảng 2.5 lần nhưng tốn bộ nhớ đỉnh hơn; chỉ là minh họa. |
| 12 | Limitations: training data, copyright and bias | C | 40s | D · Evidence | Dữ liệu, bias, copyright, và giới hạn của chính thí nghiệm. |
| 13 | Conclusion: answering the guiding question | C | 35s | Kết | Trả lời lại guiding question và 3 vế của learning objective. |
| | **Tổng** | | **~885s ≈ 14.75 phút** | | Chỉ còn khoảng 15s dự phòng trong giới hạn 15 phút. Hãy tập với đồng hồ và sẵn sàng bỏ các câu **(cắt được)**. |

**Sợi chỉ xuyên suốt**: guiding question được đặt ở slide 1, trả lời ở khung xanh lá slide 6, nhắc lại ở slide 13. Learning objective được nêu ở slide 1; vế "forward" là slide 3–4, vế "reverse" là slide 5–6, vế "latent" là slide 7–10; tổng kết ở slide 13.

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

> This is also the backbone of today's text-to-image systems, such as Stable Diffusion, which we test on slide 10.

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

💡 Nếu bị hỏi "có bằng chứng nào cho clean estimate không?", mở **backup 15** (hình golden retriever, run của nhóm): ở bước DDIM 25/50, clean estimate đã thấy con chó trong khi trạng thái hiện tại vẫn còn nhiễu.

---

## Slide 7: From DDPM to LDM: the cost of pixels, and three ideas (B · ~60s)

**Bố cục**: **trái**, hai khung độc lập xếp dọc: khung đỏ *Limitation 1: cost (every step, every pixel)* (một câu, công thức chi phí "cost ≈ #steps × one pass on all pixels" có chú thích dưới hai thừa số, 2 gạch đầu dòng PAPER REPORTS và OUR RUN, dòng nguồn xám, "→ ideas 1, 2") và khung cam *Limitation 2: no control (unconditional)* (một câu, "→ idea 3") · **phải**: tiêu đề xanh lá "LDM (Rombach et al. 2022): three ideas", 3 thẻ xanh lá đánh số 1–2–3, mỗi thẻ có mũi tên xám chỉ tới slide sẽ giải thích.

> DDPM has two separate limitations, and LDM answers each of them.

**👉 [Khung đỏ "Limitation 1": câu đầu]**

> The first is **cost**. Most pixels of an image hold fine detail we barely perceive, yet the network re-processes *all* of them at *every* step.

**👉 [Công thức chi phí: chỉ "#steps" (25–1000), rồi "one pass on all pixels" (196,608 values)] ✋**

> So the cost is roughly the number of steps times one network pass over all pixels, and **both factors are large**: 25 to 1000 steps, each over almost 200,000 values for a 256 by 256 image.

**👉 [Gạch PAPER REPORTS, chỉ dòng nguồn xám]**

> The LDM paper quotes 150 to 1000 V100 GPU-days to train strong pixel models, and about five days on one A100 to sample 50,000 images. Those numbers are cited from Dhariwal and Nichol.

**👉 [Gạch OUR RUN, rồi "→ ideas 1, 2"]**

> We see it in our own run too: 6.10 seconds for one 256 by 256 image, even with only 50 steps; more on slide 11. Ideas one and two on the right fix this.

**👉 [Khung cam "Limitation 2", rồi "→ idea 3"]**

> The second limitation is **control**. DDPM learns the image distribution only: it returns *some* image, and we cannot ask for "a red bus". Idea three fixes this.

**👉 [Tiêu đề xanh lá bên phải, rồi thẻ 1] ✋**

> Latent diffusion answers this with three ideas. **One**: run diffusion in a compressed *latent* space and train in two stages; an autoencoder is trained once, frozen and reused, then diffusion runs on its small latents.

**👉 [Thẻ 2]**

> **Two**: keep the latent as a 2-D grid with only mild compression, 4 to 8 times per side, so a U-Net still works and reconstructions stay faithful.

**👉 [Thẻ 3]**

> **Three**: a general conditioning mechanism, cross-attention, that lets any input such as text, a class or a layout steer the denoiser. The next three slides unpack these ideas, in this order.

⚠️ **Đừng nói** các con số GPU-days là của LDM tự đo. LDM trích chúng từ Dhariwal & Nichol 2021.

---

## Slide 8: Latent space: an autoencoder that compresses images (stage 1) (B · ~65s)

**Bố cục**: **sơ đồ ngang trên cùng**: [image $x_0$, $256\times256\times3$] → [Encoder $\mathcal E$] → hình lưới xanh "latent $z$: $32\times32\times4$" → [Decoder $D$] → [reconstruction $\hat x_0\approx x_0$], chú thích "a small 2-D grid: $h=H/f$" · **3 khung dưới**: *What the latent looks like* (xanh) | *How stage 1 is trained* (xanh lá) | *Why we still need diffusion* (cam).

**👉 [Sơ đồ: quét từ image → Encoder → hình lưới latent → Decoder → reconstruction]**

> Stage one is an autoencoder. The encoder compresses a 256 by 256 image into a small latent grid, and the decoder expands it back into an image that looks like the original.

**👉 [Hình lưới latent, rồi khung xanh "What the latent looks like"] ✋**

> The key point: the latent is a small **2-D grid**, not a flat vector, so the image layout survives. With a factor of 4, the paper reduces 256 by 256 to 64 by 64, 16 times fewer positions. Our Churches model uses a factor of 8: 32 by 32 by 4, about **48 times fewer values**.

**👉 [Khung xanh lá "How stage 1 is trained": 3 mục in đậm, rồi dòng "Ours"]**

> To keep reconstructions sharp, it is trained with a perceptual loss, so the output must *look* like the input, and a patch-based adversarial loss for realistic texture; a plain pixel loss would give blur. A light regularizer keeps the latent well behaved: a weak KL, or a codebook in the decoder. Our two models use one of each.

**👉 [Khung cam "Why we still need diffusion"]**

> After stage one the autoencoder is **frozen**. But we cannot just decode a random latent: clean latents are not standard Gaussian, so random ones decode to poor images. Diffusion must learn where real latents lie. And compression caps quality: fine text and small objects can be lost.

⚠️ Công thức VAE (ELBO, reparameterization) đã chuyển xuống **backup 16**. Chỉ mở khi bị hỏi.

**Chuyển người (B → C)**: "Now that we have a latent space, [Tên C] will show how diffusion runs inside it."

---

## Slide 9: Operations in latent space: the whole LDM pipeline (C · ~75s)

**Bố cục**: **sơ đồ lớn** chiếm gần cả slide: vùng nền xanh nhạt "LATENT SPACE: every diffusion operation runs on the small $z$" · **làn trên TRAINING (stage 2)**: [real image $x_0$] → [Encoder, frozen] → [$z_0$] → [add noise] → [U-Net, predict the noise] · **làn dưới GENERATION** (chú thích "no real image, no encoder"): [$z_T$ noise] → [U-Net + sampler, $T$ steps] (mũi tên cam "repeat") → [Decoder, frozen, **once**] → [new image] · **bên phải**: [prompt $y$] → [condition encoder $\tau_\eta$], hai mũi tên xanh "cross-attn" vào cả hai U-Net · **3 thẻ dưới**: *Same DDPM operations, now on $z$* (xanh) | *Encoder only for training* (xanh lá) | *Cheaper per step* (cam).

**👉 [Vùng nền xanh "LATENT SPACE"] ✋**

> This is the whole pipeline. The shaded area is the latent space: **everything diffusion does happens here**, on the small grid, not on pixels.

**👉 [Làn TRAINING: trái → phải]**

> Training: take a real image, encode it once with the frozen encoder, add noise exactly as on slide 3, and train the U-Net to predict that noise. It is DDPM, just on $z$.

**👉 [Làn GENERATION: $z_T$ → U-Net + sampler (chỉ mũi tên "repeat") → Decoder → new image]**

> Generation: start from latent noise, run the U-Net and sampler for $T$ steps, and call the decoder **once** at the end. No real image and no encoder are needed.

**👉 [prompt $y$ → $\tau_\eta$ → hai mũi tên "cross-attn"]**

> A prompt is encoded by $\tau_\eta$ and enters both U-Nets through cross-attention, which is the next slide.

**👉 [3 thẻ dưới: trái → giữa → phải]**

> So: the same DDPM operations, now on $z$; the encoder only for training and the decoder once; and each U-Net call is cheaper because it sees about 48 times fewer values. DDIM's fewer steps are a separate speedup. We measure the real cost on slide 11.

⚠️ **Đừng nói** "LDM nhanh hơn 48×". Đó là 48× ít giá trị hơn mỗi bước, không phải tốc độ đo được (đo thật: 2.5×, slide 11).

---

## Slide 10: Cross-attention: steering the denoiser with a prompt (C · ~80s)

**Bố cục**: **trái**: khung xanh lá *Image regions ask, prompt words answer* (lưới latent với một ô cam; các token a / red / bus / left / blue / car; đường nối dày tới "red" và "bus"), 3 gạch đầu dòng · **phải**: nhãn OUR RUN "Stable Diffusion v1.4, seed 2027, same initial latent", 3 ảnh *Reference* | *red → green* | *left → right*, 3 gạch đầu dòng với ✓/✗.

**👉 [Hình bên trái: ô cam trên lưới latent, rồi các đường nối dày tới "red" và "bus"] ✋**

> How does the prompt steer the denoiser? Through cross-attention: **image regions ask, prompt words answer**. Each region of the latent, like this orange one, looks up the prompt tokens; thick lines mean high attention. A region that is becoming a bus pulls information from "red" and "bus".

**👉 [3 gạch đầu dòng bên trái, lần lượt]**

> This happens at every U-Net layer and every step, so the prompt steers each noise prediction; nothing is pasted onto the final pixels. The same mechanism works for any condition: only the encoder changes, for text, a class or a layout. **(cắt được)** A guidance scale controls how strongly the prompt is followed: higher means closer to the prompt but less diverse.

**👉 [Nhãn OUR RUN, rồi ảnh 1 "Reference"]**

> Does it work? Our small test with Stable Diffusion: same seed, same initial latent, three prompts. Reference: "a red bus to the left of a blue car."

**👉 [Ảnh 2 "red → green" rồi gạch ✓ bên dưới]**

> Change red to green: the bus turns green at all four seeds we tried. But the blue car does not clearly appear, and at this seed we even get two green buses.

**👉 [Ảnh 3 "left → right" rồi gạch ✗]**

> Change left to right: no clear swap. The red bus stays on the left.

**👉 [Gạch cuối "Cross-attention is soft"] ✋**

> Cross-attention is **soft**: an attribute can bind to the wrong object, and a token can be ignored. To be clear: this is 16 images checked by eye, an illustration and not a general conclusion.

⚠️ Công thức $Q, K, V$, softmax và CFG đã chuyển xuống **backup 16**. Chỉ mở khi bị hỏi.

---

## Slide 11: Pixel vs. latent diffusion on LSUN Churches (C · ~70s)

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

## Slide 12: Limitations: training data, copyright and bias (C · ~40s)

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

## Slide 13: Conclusion: answering the guiding question (C · ~35s)

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
| Vì sao pixel diffusion tốn kém, và LDM sửa bằng cách nào? | 7 | B | Mỗi bước chạy mạng trên mọi pixel; LDM cho diffusion chạy trên latent nhỏ (hai giai đoạn), giữ cấu trúc 2-D, thêm cross-attention. Số GPU-days là LDM trích từ Dhariwal & Nichol 2021. |
| VAE khác autoencoder thường? Sao không decode $z\sim\mathcal N(0,I)$? | 8 (khung cam); công thức ở backup 16 | B | Encoder xuất phân phối + KL + reparameterization; latent sạch không phải $\mathcal N(0,I)$ nên phải dùng diffusion để học phân phối latent. |
| Vì sao latent phải giữ dạng lưới 2-D và chỉ nén nhẹ? | 7 (thẻ 2), 8 | B | U-Net xử lý được lưới 2-D; nén nhẹ ($f=4$–$8$) giữ ảnh tái tạo trung thực; các mô hình hai giai đoạn trước đó làm phẳng thành chuỗi token 1-D và phải nén mạnh hơn. |
| Vì sao perceptual + adversarial thay vì MSE? | 8 | B | MSE theo pixel lấy trung bình các chi tiết khả dĩ nên ảnh mờ. |
| Encoder có dùng khi sinh ảnh không? | 9 | C | Không: sinh ảnh bắt đầu từ nhiễu latent $z_T$; encoder chỉ dùng khi train, decoder chạy một lần ở cuối. |
| Cross-attention khác self-attention? Công thức cụ thể? | 10; công thức ở backup 16 | C | Q từ ảnh; K, V từ điều kiện (với self-attention thì cả ba từ ảnh); $O=\mathrm{softmax}(QK^\top/\sqrt d)V$. |
| Vì sao LDM nhanh hơn mà tốn bộ nhớ đỉnh hơn? | 11 | C | Nói thật: nhóm chỉ đo, chưa phân tích. Hai checkpoint khác kiến trúc/decoder; đây là giả thuyết chưa kiểm chứng. |
| Thí nghiệm có chứng minh latent tốt hơn pixel? | 11 | C | Không: 4 mẫu, 1 cặp checkpoint, không FID. Chỉ là minh họa, kèm số liệu Table 6 của paper. |
| Diffusion có sao chép ảnh huấn luyện? | 12 | C | Carlini et al.: memorization có thể xảy ra, nhưng không phải mọi ảnh sinh ra đều là bản sao. |
| Một ký hiệu nghĩa là gì / miền giá trị? | Backup 14 | ai cũng được | Bảng Notation, value ranges and modelling assumptions. |
| Có bằng chứng nào mạng "thấy" ảnh khi trạng thái còn đầy nhiễu? | Backup 15 | B | Run của nhóm: ở bước DDIM 25/50, clean estimate $\hat x_0$ đã thấy con chó (cả pixel ADM và latent LDM); updated state chỉ nhích một bước nhỏ. |
| Nguồn hình/số liệu? | Backup 17–18 | ai cũng được | Sơ đồ là hình tự vẽ; run dùng checkpoint pretrained; số paper ghi rõ nguồn. |

**Mẹo khi trả lời**: luôn bấm về slide liên quan và **chỉ vào đúng khung** trước khi trả lời. Như vậy người hỏi thấy câu trả lời đã nằm trong bài.

---

## Checklist trước giờ trình bày

- [ ] Mỗi người tập riêng phần của mình với đồng hồ: **A ≈ 4.6 phút** (slide 1–4, 275s), **B ≈ 5.2 phút** (slide 5–8, 310s), **C ≈ 5.0 phút** (slide 9–13, 300s). Tổng 885s, chỉ dư khoảng 15s so với giới hạn 15 phút.
- [ ] Tập 2 lần chuyển người (sau slide 4, sau slide 8) cho liền mạch.
- [ ] Chuẩn bị laser/pointer. Nếu không có, đứng cạnh màn hình và chỉ bằng tay theo các 👉.
- [ ] Đánh dấu sẵn các câu **(cắt được)** để bỏ nếu trễ hơn 30 giây.
- [ ] Mỗi thành viên nhận ít nhất một câu Q&A trong bảng trên.
