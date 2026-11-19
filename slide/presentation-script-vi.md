# Script thuyết trình (tiếng Việt): Diffusion Models, From Adding Noise to Generating Images

Bản tiếng Việt của [presentation-script.md](presentation-script.md), cho deck [main.tex](main.tex): 13 slide (slide 1 là title kèm guiding question; 12 slide nội dung), cộng 7 slide backup (14: Notation, 15: Inside one denoising step, 16: LDM details, 17: our LSUN run, 18: our Stable Diffusion test, 19–20: References). Mọi bằng chứng trên slide chính đều lấy từ paper. Run tự chạy của nhóm chỉ xuất hiện dưới dạng minh họa: ảnh bus ở slide 10, lưới ảnh nhà thờ ở slide 11, và backup 15, 17, 18.

**Cách đọc file này**

- Lời nói để trong khung trích dẫn (`>`), viết bằng **tiếng Việt**; thuật ngữ chuyên ngành giữ nguyên **tiếng Anh** (forward noising, reverse denoising, latent, score, guidance, FID, U-Net, VAE, encoder, decoder, sampler…) để khớp với chữ trên slide.
- **👉 [ ... ]**: chỉ tay / laser vào đúng vùng đó **trước khi** đọc câu ngay sau. Tên khung và nhãn giữ nguyên tiếng Anh như trên slide.
- **✋**: dừng khoảng 1 giây và nhấn giọng. Đây là các câu người nghe cần nhớ.
- **(cắt được)**: câu có thể bỏ khi trễ giờ.
- **⚠️ Đừng nói**: những phát biểu vượt quá bằng chứng của nhóm.
- Phân công người nói theo [slide-outline.md](../slide-outline.md): **A** slide 1–4, **B** slide 5–8, **C** slide 9–13. Có thể đổi tên tùy nhóm.
- Nói tiếng Việt thường dài hơn tiếng Anh một chút; nếu trễ giờ, ưu tiên bỏ các câu **(cắt được)**.

**Mã màu trên slide**: hãy dùng màu để dẫn mắt người nghe.

| Màu | Ý nghĩa | Ví dụ |
|---|---|---|
| Xanh dương nhạt (`fwd`) | Forward noising: cố định, đã biết | khung "Forward noising equations" slide 3, đường "signal" trong biểu đồ |
| Cam (`rev`) | Reverse denoising: học được; nhãn **OUR RUN** (ảnh minh họa slide 10, 11 và backup) | dải REVERSE và khung Sampling slide 5 |
| Xanh lá (`ok`) | Latent diffusion / autoencoder; nhãn **OUR EXAMPLE**; khung câu trả lời slide 6 | khung "Chosen values" slide 4, khung "Why removing noise generates new images" slide 6 |
| Xanh đậm | Nhãn **PAPER REPORTS**: số liệu của paper, không phải của nhóm | thẻ Paper review slide 1, bảng FID slide 5, khung chi phí slide 7, bảng guidance slide 10, bảng Table 6 slide 11 |

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
| 8 | Latent space: what it is, and why it helps | B | 65s | C · Latent | VAE nén ảnh thành latent gọn (mean, spread, sample); mỗi bước xử lý ít hơn 48× giá trị; vẫn cần diffusion để *tạo* latent mới. |
| 9 | Operations in latent space: the whole LDM pipeline | C | 75s | C · Latent | Vòng lặp DDPM giữ nguyên nhưng chạy trên $z$ nhỏ; encoder chỉ dùng khi train, decoder chạy một lần. |
| 10 | Cross-attention: steering the denoiser with a prompt | C | 80s | C · Latent | Vùng ảnh "hỏi", từ trong prompt "trả lời"; minh họa bus: đổi màu được, đổi trái/phải thì không, vì attention mềm. |
| 11 | Pixel vs. latent diffusion: what the LDM paper measured | C | 70s | D · Evidence | Số liệu của paper: latent sample nhanh 3.7–4.9×, mỗi epoch nhanh 2.7×, FID không tệ hơn; ảnh nhà thờ của nhóm chỉ để minh họa. |
| 12 | Limitations, and when to use diffusion | C | 40s | D · Evidence | 5 giới hạn, mỗi giới hạn một lý do ngắn; khi nào dùng latent, pixel, hay không dùng diffusion. |
| 13 | Conclusion: the recipe behind today's image generators | C | 35s | Kết | Bức tranh tổng: nhiều bước dễ (DDPM), bước rẻ (latent), điều khiển được (cross-attention); 3 thẻ theo learning objective. |
| | **Tổng** | | **~885s ≈ 14.75 phút** | | Chỉ còn khoảng 15s dự phòng trong giới hạn 15 phút. Hãy tập với đồng hồ và sẵn sàng bỏ các câu **(cắt được)**. |

**Sợi chỉ xuyên suốt**: guiding question được đặt ở slide 1 và trả lời ở khung xanh lá slide 6. Slide 13 không trả lời lại mà đưa ra bức tranh tổng. Learning objective được nêu ở slide 1; vế "forward" là slide 3–4, vế "reverse" là slide 5–6, vế "latent" là slide 7–10; tổng kết ở slide 13.

---

## Slide 1: Title, guiding question, learning objective, paper review (A · ~40s)

**Bố cục**: dải tiêu đề xanh phía trên, bên dưới tiêu đề là 3 khối tên người trình bày (tên in đậm, MSSV bên dưới) · **trái**: khung cam GUIDING QUESTION, bên dưới là khung xanh LEARNING OBJECTIVE (3 cụm từ tô màu) · **phải**: thẻ xám PAPER REVIEW với 4 mục 2015 / 2019 / 2020 DDPM (required, có nhãn PAPER REPORTS) / 2022 LDM.

**👉 [3 khối tên trên dải tiêu đề]**

> Xin chào thầy cô và các bạn. Nhóm chúng em gồm Cao Quang Hung, Nguyen Trong Van Viet và Huynh Chi Ton, và hôm nay chúng em trình bày về *Diffusion Models: From Adding Noise to Generating Images*.

> Một denoiser làm sạch một bức ảnh *đã có sẵn*. Còn một generator phải tạo ra một bức ảnh *chưa từng tồn tại*. Vậy điều gì nối hai việc này với nhau?

**👉 [Khung cam GUIDING QUESTION] ✋**

> Đó chính là guiding question của chúng em: **làm sao việc học khử nhiễu lại giúp một mô hình sinh ra ảnh mới?**

**👉 [Khung xanh LEARNING OBJECTIVE: chỉ lần lượt 3 cụm màu xanh dương → cam → xanh lá]**

> Kết thúc bài này, các bạn sẽ giải thích được **forward noising**, **reverse denoising**, và **vì sao latent diffusion giảm chi phí tính toán**. Ba cụm từ này cũng là ba phần của bài.

**👉 [Thẻ PAPER REVIEW: quét từ 2015 xuống 2022, dừng ở dòng DDPM]**

> Bài dựa trên bốn paper. Framework năm 2015 đưa ra hai chuỗi Gaussian forward và reverse; Song và Ermon học score ở nhiều mức nhiễu; **DDPM**, paper bắt buộc của đề, cho mạng dự đoán nhiễu; và **LDM** chạy cùng ý tưởng đó trong một latent space đã được nén. **(cắt được)** DDPM đạt FID 3.17, nhưng likelihood thì không cạnh tranh được.

**Chuyển ý**: "Trước hết, diffusion đứng ở đâu so với các mô hình sinh khác?"

⚠️ **Đừng nói** rằng nhóm đã tự train mô hình. Mọi thí nghiệm dùng checkpoint pretrained.

---

## Slide 2: Where diffusion fits: three ways to generate images (A · ~60s)

**Bố cục**: **cột trái**: tiêu đề "Generative vs. discriminative", ô xám *Discriminative*, ô xanh *Generative*, dòng chữ nhỏ về Stable Diffusion · **cột phải**: tiêu đề "Qualitative comparison: GAN vs. autoregressive vs. diffusion", hình 3 panel GAN (tím) | Autoregressive (xanh) | Diffusion (xanh lá), thanh "Core difference" ở đáy hình.

**👉 [Ô xám Discriminative]**

> Một mô hình discriminative học $p(y \mid x)$. Để trả lời "đây có phải con mèo không?", nó chỉ cần những đặc trưng giúp tách các lớp ra.

**👉 [Ô xanh Generative]**

> Một mô hình generative học $p(x)$ hoặc $p(x \mid y)$. Để *tạo ra* một con mèo, nó phải nắm được hình dạng, texture, ánh sáng và bố cục, tức là nhiều thông tin hơn hẳn.

**👉 [Panel GAN màu tím: Generator → Discriminator → "adversarial training"]**

> Có ba họ mô hình chính. GAN biến nhiễu thành ảnh chỉ trong một lần chạy, nhưng việc train là một trò chơi giữa hai mạng, và có thể bị mode collapse.

**👉 [Panel Autoregressive: chuỗi token $x_1, x_2, \dots$]**

> Mô hình autoregressive sinh ảnh lần lượt từng token: likelihood tốt, nhưng sampling chậm vì phải tuần tự.

**👉 [Panel Diffusion: hàng trên "forward process", rồi hàng dưới "reverse process"]**

> Diffusion thêm nhiễu bằng một forward process cố định, rồi học cách gỡ nhiễu từng bước. Train ổn định, ảnh có chất lượng và độ đa dạng cao, nhưng sampling cần rất nhiều bước.

**👉 [Thanh "Core difference" dưới đáy hình]**

> Tóm lại trong một câu: một lần chạy, từng token một, hay khử nhiễu qua nhiều bước.

**👉 [Dòng chữ nhỏ dưới ô Generative] (cắt được)**

> Diffusion cũng là nền tảng của các hệ text-to-image hiện nay như Stable Diffusion, mà chúng em sẽ phân tích ở slide 7 đến 10.

**Chuyển ý**: "Mình bắt đầu từ chiều dễ trước: forward noising."

⚠️ **Đừng nói** "diffusion luôn tốt hơn GAN". Hình chỉ mô tả hành vi điển hình, không phải đảm bảo.

---

## Slide 3: Forward noising: a known way to destroy structure (A · ~85s)

**Bố cục**: **dải sơ đồ trên**: $x_0 \to x_{t-1} \to$ [Known Gaussian kernel] $\to x_t \to x_T$, nhãn "clean data" / "nearly noise" · **khung xanh trái "Forward noising equations"**: (1) ONE STEP có chú thích dưới hai số hạng "shrink old signal" / "add fresh noise"; (2) JUMP TO ANY $t$ IN ONE SHOT (phương trình đóng khung); bảng ký hiệu 4 hàng · **cột phải**: 3 gạch đầu dòng (**Why $x_T\approx\mathcal N(0,\mathbf I)$**, **Signal traded for noise**, **Assumptions**) và biểu đồ "DDPM schedule" với đường xanh $\sqrt{\bar\alpha_t}$, đường cam $\sqrt{1-\bar\alpha_t}$, vạch đứt "SNR = 1, $t\approx260$".

**👉 [Dải sơ đồ: quét từ $x_0$ (clean data) sang $x_T$ (nearly noise), dừng ở ô "Known Gaussian kernel"]**

> Forward process lấy một ảnh sạch $x_0$ và thêm nhiễu qua $T$ bước, cho tới khi gần như chỉ còn nhiễu. Mỗi bước là một Gaussian kernel *đã biết trước*. Ở đây không có gì phải học cả.

**👉 [Phương trình (1): chỉ chú thích "shrink old signal", rồi "add fresh noise"]**

> Phương trình một là một bước. Số hạng đầu **thu nhỏ tín hiệu cũ** theo hệ số $\sqrt{1-\beta_t}$; số hạng thứ hai **thêm nhiễu mới** với độ lớn $\sqrt{\beta_t}$.

**👉 [Phương trình (2) đóng khung] ✋**

> Phương trình hai là kết quả quan trọng nhất. Vì các bước Gaussian ghép lại được với nhau, ta có thể nhảy thẳng từ $x_0$ tới *bất kỳ* bước $t$ nào chỉ trong một lần, dùng $\bar\alpha_t$ là tích của các alpha.

**👉 [Bảng ký hiệu dưới khung: quét nhanh]**

> Về ký hiệu: $x_0$ là ảnh sạch, đã scale về $[-1,1]$ và không có đơn vị; $\beta_t$ nằm giữa 0 và 1 là noise schedule; $t$ là chỉ số bước, không phải thời gian vật lý; còn $\varepsilon$ là nhiễu Gaussian chuẩn.

**👉 [Gạch đầu dòng "Why $x_T\approx\mathcal N(0,\mathbf I)$"]**

> Vì sao chuỗi kết thúc ở nhiễu thuần? Nếu một trạng thái đã là Gaussian chuẩn, thì sau một bước nó vẫn là Gaussian chuẩn: $(1-\beta_t) + \beta_t = 1$. Và ở bước cuối, $\bar\alpha_T$ chỉ khoảng $4\times10^{-5}$, gần như không còn tín hiệu. Vì vậy quá trình sinh ảnh có thể bắt đầu từ nhiễu thuần.

**👉 [Gạch đầu dòng "Signal traded for noise", rồi biểu đồ: đường xanh đi xuống, đường cam đi lên, vạch đứt ở $t\approx260$] ✋**

> Trong phương trình hai, bình phương hai trọng số luôn cộng lại bằng một. Nghĩa là forward process không chỉ thêm nhiễu, mà nó *đổi* tín hiệu lấy nhiễu. Trên biểu đồ, trọng số tín hiệu màu xanh giảm dần, trọng số nhiễu màu cam tăng dần, và hai đường cắt nhau ở khoảng $t = 260$, chỗ SNR bằng một.

**👉 [Gạch đầu dòng "Assumptions"]**

> Các giả định: một Markov chain, nhiễu độc lập ở mỗi bước, và $\beta_t$ nhỏ, theo schedule của DDPM với $T=1000$ bước, $\beta_t$ tăng từ $10^{-4}$ đến $0.02$.

**Chuyển ý**: "Giờ mình làm cụ thể bằng con số."

---

## Slide 4: Forward noising by hand and by eye (A · ~90s)

**Bố cục**: **dải xanh lá trên cùng** "Chosen values" (nhãn OUR EXAMPLE) · **hai khung giữa**: *Way 1: step by step with the schedule $\beta_1,\beta_2$* (xanh nhạt, trái) và *Way 2: one jump with the shortcut $\bar\alpha_2$* (xanh đậm, phải) · **khung cam** "Interpreting the stochastic expectation" · **dưới cùng**: ảnh 28×28 ngôi nhà ở 5 mức nhiễu (trái) và chú thích SNR (phải).

**👉 [Dải xanh lá "Chosen values": chỉ lần lượt $x_0$, $\beta$, $\varepsilon$, $\alpha$, $\bar\alpha_2$]**

> Mình tính tay hai bước. Một pixel $x_0 = 0.8$, đã scale về $[-1,1]$. Schedule $\beta_1 = 0.1$ và $\beta_2 = 0.2$, cố ý chọn lớn để phép tính dễ thấy. Hai lần rút nhiễu: $\varepsilon_1 = -0.5$ và $\varepsilon_2 = -0.4$. Suy ra $\alpha_1 = 0.9$, $\alpha_2 = 0.8$, và $\bar\alpha_2 = 0.72$.

**👉 [Khung Way 1: dòng Step 1, rồi dòng Step 2, dừng ở ô $x_2 = 0.3585$]**

> Cách một, tính từng bước. Bước một: $\sqrt{0.9}$ nhân $0.8$ được $0.7589$, cộng $\sqrt{0.1}$ nhân $-0.5$ là $-0.1581$, nên $x_1 = 0.6008$. Bước hai đi tiếp từ $x_1$: $\sqrt{0.8}$ nhân $0.6008$ được $0.5374$, trừ $0.1789$, ra **$x_2 = 0.3585$**.

**👉 [Khung Way 2: dòng "Shortcut (2)", rồi công thức $\bar\varepsilon$, rồi ô kết quả có dấu ✓]**

> Cách hai dùng công thức tắt ở slide 3, nhảy thẳng từ $x_0$: $\sqrt{0.72}$ nhân $0.8$ được $0.6788$, cộng $0.5292$ nhân một nhiễu duy nhất $\bar\varepsilon$. Hai lần rút nhiễu gộp lại thành **một** Gaussian, $\bar\varepsilon = -0.6053$; phương sai của nó là $(0.08 + 0.2)/0.28 = 1$. Kết quả vẫn là **$0.3585$**, giống hệt cách một.

**👉 [Khung cam "Interpreting the stochastic expectation"] ✋**

> Con số này có ý nghĩa gì? Vì nhiễu có trung bình bằng không, nên *kỳ vọng* của $x_2$ khi biết $x_0$ là $\sqrt{\bar\alpha_2}\,x_0 = 0.6788$, với phương sai $0.28$. Cả hai cách đều mô tả **cùng một phân phối**. Giá trị $0.3585$ chỉ là **một lần rút ngẫu nhiên**, thấp hơn trung bình khoảng 0.6 độ lệch chuẩn. Nếu lấy trung bình rất nhiều lần rút, ta sẽ được $0.6788$.

**👉 [Ảnh ngôi nhà: quét trái sang phải, rồi chỉ chú thích SNR bên phải]**

> Giờ nhìn bằng mắt, với schedule thật của DDPM: ngôi nhà 28×28 của nhóm ở năm mức nhiễu. Ở $t = 50$, SNR là 33.5 và ngôi nhà còn rõ. Ở $t = 500$, SNR dưới 0.1 và nhiễu đã lấn át. Tới $t = T$ thì gần như không còn gì.

**Chuyển người (A → B)**: "Vậy là phá hủy cấu trúc thì dễ và hoàn toàn đã biết. Giờ [Tên B] sẽ trình bày cách mình *học* để đảo ngược nó."

⚠️ **Đừng nói** ảnh ngôi nhà được sinh bởi một mô hình. Đây chỉ là forward noising, không có mạng nào.

---

## Slide 5: Reverse denoising: from noise back to an image (B · ~85s)

**Bố cục**: **dải cam trên cùng** "REVERSE: learned denoising", đọc **từ phải sang trái**: $x_T \to x_t \to$ [neural net $\varepsilon_\theta(x_t,t)$, nhãn "timestep $t$"] $\to$ [sampler $\mu_\theta+\sigma_t u_t$, nhãn $u_t\sim\mathcal N(0,\mathbf I)$] $\to x_{t-1} \to x_0$ · **giữa trái (40%)**: khung cam *Sampling: generate a new image* · **giữa phải (60%)**: khung xanh *Why predict ε, not the mean $\tilde\mu_t$?* với bảng FID 2×2 (nhãn PAPER REPORTS) · **dải cam dưới cùng**: *One reverse step: turn the noise prediction into $\mu_\theta$* chia 3 phần.

**👉 [Dải REVERSE: kéo tay từ $x_T$ bên phải sang $x_0$ bên trái] ✋**

> Giờ tới chiều mà mình phải học. Reverse chain chạy từ phải sang trái, từ nhiễu thuần $x_T$ quay về ảnh $x_0$. Ở mỗi bước, một neural net nhìn trạng thái nhiễu và timestep, rồi một sampler đi một bước nhỏ.

**👉 [Khung Sampling: chỉ bước 1 → 2 → 3, rồi dòng chữ xám cuối khung]**

> Sinh một ảnh chỉ là vòng lặp này. Một: rút nhiễu mới. Hai: với $t$ từ $T$ về 1, đặt $x_{t-1}$ bằng mean $\mu_\theta$ cộng thêm một chút nhiễu mới. Ba: trả về $x_0$; ở bước cuối không thêm nhiễu. Chú ý: **không dùng ảnh thật nào cả**. Mạng chỉ cần cung cấp $\mu_\theta$ ở mỗi bước.

**👉 [Khung "Why predict ε, not the mean $\tilde\mu_t$?": đọc câu hỏi]**

> Vậy mạng nên dự đoán cái gì? Lựa chọn hiển nhiên là dự đoán trực tiếp mean $\tilde\mu_t$ của $x_{t-1}$. Nhưng DDPM lại dự đoán **nhiễu**. Tại sao?

**👉 [Bảng FID: chỉ nhãn PAPER REPORTS, rồi hàng "mean", rồi hàng "noise ε", dừng ở 3.17]**

> Ho và cộng sự đã thử cả hai trên CIFAR-10. Dự đoán mean chỉ chạy tốt khi train bằng weighted variational bound, đạt FID 13.22, và không ổn định khi train bằng plain MSE. Dự đoán nhiễu với plain MSE đạt **FID 3.17**; FID càng thấp càng tốt. Đây là số liệu của paper. Lý do là nhiễu có cùng thang đo ở mọi bước, nên một loss đơn giản, không trọng số vẫn hoạt động. Loss đó sẽ được trình bày ở slide tiếp theo.

**👉 [Dải "One reverse step": phần trái → công thức giữa (chỉ $\varepsilon_\theta$ in đậm) → phần phải]**

> Cuối cùng, nhiễu dự đoán biến thành một bước như thế nào. Bước ngược là một Gaussian với variance cố định $\sigma_t^2 = \beta_t$. Mean của nó lấy $x_t$ trừ đi một phần nhiễu dự đoán đã được scale. $\varepsilon_\theta$ in đậm, do một U-Net đưa ra, là **phần duy nhất được học**; mọi thứ còn lại đến từ schedule cố định.

⚠️ **Đừng nói** "dự đoán mean hoàn toàn không học được". Paper chỉ báo là không ổn định khi dùng plain MSE; với weighted bound nó đạt FID 13.22.

---

## Slide 6: Training the noise predictor, and why it works (B · ~100s)

**Bố cục**: **cột trái (hẹp)**: khung xanh *Training: learn to predict the noise* ($L_{\text{simple}}$ + 3 bước + dòng xám "Uses real images"), khung xanh nhạt *Connection to the score (Song & Ermon 2019)* (hai công thức $s_\theta$ và $\mu_\theta$ xếp dọc) · **cột phải (rộng)**: khung xanh lá *Why removing noise generates new images*: dòng in đậm "Core idea: know the noise ⇒ know the clean image", 5 gạch đầu dòng (**Noise and image: same information**, **Remove a little at a time**, **Why a real image, not any image**, **Coarse to fine**, **Why ε, not $x_0$?**) và câu nghiêng về nhà điêu khắc.

**👉 [Khung Training: công thức $L_{\text{simple}}$, rồi 3 bước đánh số]**

> Train mô hình chỉ là một bài toán hồi quy. $L_{\text{simple}}$ là bình phương sai số giữa nhiễu thật và nhiễu dự đoán. Lấy một ảnh thật, một bước $t$ ngẫu nhiên và nhiễu ngẫu nhiên; dựng $x_t$ bằng công thức đóng ở slide 3; dự đoán nhiễu rồi cập nhật gradient. Train thì dùng ảnh thật; còn sampling ở slide trước thì không.

**👉 [Khung score: câu đầu, rồi công thức $s_\theta$, rồi công thức $\mu_\theta$]**

> *Score* là hướng mà mật độ của ảnh nhiễu tăng lên. Tại điểm tối ưu của loss bình phương này, mạng dự đoán *trung bình* của nhiễu khi biết $x_t$, và trung bình đó chính là score đã được scale. Viết lại mean theo score, ta thấy mỗi bước ngược **đi lên theo mật độ**, rồi thêm một chút nhiễu, giống annealed Langevin dynamics.

**👉 [Khung xanh lá: dòng "Core idea"] ✋ (đây là câu trả lời chính cho guiding question)**

> Vậy, câu trả lời của nhóm cho guiding question. Ý cốt lõi là: **biết nhiễu thì biết ảnh sạch.**

**👉 [Gạch 1 "Noise and image: same information": chỉ công thức $\hat x_0$]**

> Đảo ngược công thức đóng: khi có $x_t$ và nhiễu dự đoán, ta giải ra được một ước lượng ảnh sạch $\hat x_0$. Dự đoán nhiễu và dự đoán ảnh mang cùng một lượng thông tin.

**👉 [Gạch 2 "Remove a little at a time"]**

> Khi sinh ảnh, ta bắt đầu từ nhiễu thuần và mỗi bước chỉ bỏ đi **một phần nhỏ** của nhiễu dự đoán, kèm thêm chút nhiễu mới để giữ độ đa dạng. Mỗi bước là một chỉnh sửa dễ, khác với VAE decoder phải tạo cả bức ảnh chỉ trong một lần.

**👉 [Gạch 3 "Why a real image, not any image"] ✋**

> Tại sao kết quả là một ảnh *giống thật* chứ không phải ảnh bất kỳ? Để đoán đúng nhiễu, mạng phải biết ảnh thật trông như thế nào: phần nào không giống ảnh thật thì *chính là* nhiễu. Vì nhiễu dự đoán tỉ lệ với trừ score, nên bỏ nó đi tức là leo dần về những vùng có nhiều ảnh thật.

**👉 [Gạch 4 "Coarse to fine"]**

> Mỗi mức nhiễu dạy một thứ khác nhau: ở $t$ lớn là bố cục, hình dạng và màu sắc; ở $t$ nhỏ là cạnh và texture. Ho và cộng sự cũng quan sát thấy sampling đi đúng thứ tự đó: đặc trưng lớn xuất hiện trước, chi tiết đến sau.

**👉 [Gạch 5 "Why ε, not $x_0$?"] (cắt được)**

> Thế sao không dự đoán thẳng ảnh sạch? Vì nhiễu có cùng thang đo ở mọi bước, còn $x_0$ thì gần như không đoán nổi khi $t$ lớn; DDPM cũng báo cáo dự đoán $\varepsilon$ cho ảnh tốt hơn, như ta đã thấy ở slide 5.

**👉 [Câu nghiêng cuối khung]**

> Hãy hình dung một nhà điêu khắc: mô hình học được phần nào *không phải* bức tượng, rồi đẽo bỏ dần từng lớp.

**Chuyển ý**: "Vòng lặp này hoạt động, nhưng mỗi bước đều xử lý cả bức ảnh độ phân giải đầy đủ, lặp lại rất nhiều lần. Làm cho mỗi bước rẻ hơn chính là việc của latent diffusion."

⚠️ **Đừng nói** $s_\theta$ *bằng* đúng score thật. Đó chỉ là xấp xỉ, đúng tại điểm tối ưu lý tưởng của MSE.
⚠️ **Đừng nói** "diffusion luôn sắc nét hơn VAE". Slide chỉ so sánh cách giải mã (nhiều bước nhỏ so với một lần), không có thí nghiệm so sánh chất lượng.
⚠️ Ý "nhiễu lớn dạy bố cục, nhiễu nhỏ dạy chi tiết" là cách hiểu của nhóm; phần có nguồn là *thứ tự xuất hiện khi sampling* (Ho et al. 2020, Sec. 4.3).

💡 Nếu bị hỏi "có bằng chứng nào cho clean estimate không?", mở **backup 15** (hình golden retriever, run của nhóm): ở bước DDIM 25/50, clean estimate đã thấy con chó trong khi trạng thái hiện tại vẫn còn nhiễu.

---

## Slide 7: From DDPM to LDM: the cost of pixels, and three ideas (B · ~60s)

**Bố cục**: **trái**, hai khung độc lập xếp dọc: khung đỏ *Limitation 1: cost (every step, every pixel)* (một câu, công thức chi phí "cost ≈ #steps × one pass on all pixels" có chú thích dưới hai thừa số, 2 gạch đầu dòng PAPER REPORTS (GPU-days; Fig. 6 so sánh thời gian train), dòng nguồn xám, "→ ideas 1, 2") và khung cam *Limitation 2: no control (unconditional)* (một câu, "→ idea 3") · **phải**: tiêu đề xanh lá "LDM (Rombach et al. 2022): three ideas", 3 thẻ xanh lá đánh số 1–2–3, mỗi thẻ có mũi tên xám chỉ tới slide sẽ giải thích.

> DDPM có hai giới hạn tách biệt nhau, và LDM giải quyết từng cái một.

**👉 [Khung đỏ "Limitation 1": câu đầu]**

> Giới hạn thứ nhất là **chi phí**. Phần lớn pixel trong ảnh chứa chi tiết nhỏ mà mắt gần như không nhận ra, nhưng mạng vẫn phải xử lý lại *tất cả* chúng ở *mọi* bước.

**👉 [Công thức chi phí: chỉ "#steps" (25–1000), rồi "one pass on all pixels" (196,608 values)] ✋**

> Nên chi phí xấp xỉ bằng số bước nhân với một lần chạy mạng trên toàn bộ pixel, và **cả hai thừa số đều lớn**: từ 25 đến 1000 bước, mỗi bước xử lý gần 200 nghìn giá trị cho một ảnh 256 nhân 256.

**👉 [Gạch PAPER REPORTS, chỉ dòng nguồn xám]**

> Paper LDM trích dẫn rằng train các pixel model mạnh tốn từ 150 đến 1000 GPU-day trên V100, và sinh 50 nghìn ảnh mất khoảng năm ngày trên một GPU A100. Các con số này được trích từ Dhariwal và Nichol.

**👉 [Gạch PAPER REPORTS thứ hai, rồi "→ ideas 1, 2"]**

> Paper LDM cũng cho thấy, với cùng ngân sách tính toán, pixel-space model cần thời gian train lâu hơn hẳn so với latent model. Ý tưởng một và hai ở bên phải giải quyết vấn đề này.

**👉 [Khung cam "Limitation 2", rồi "→ idea 3"]**

> Giới hạn thứ hai là **khả năng điều khiển**. DDPM chỉ học phân phối ảnh: nó trả về *một* ảnh nào đó, và ta không thể yêu cầu "a red bus". Ý tưởng ba giải quyết vấn đề này.

**👉 [Tiêu đề xanh lá bên phải, rồi thẻ 1] ✋**

> Latent diffusion trả lời bằng ba ý tưởng. **Một**: chạy diffusion trong một *latent* space đã được nén, và train theo hai giai đoạn; một autoencoder được train một lần, đóng băng và dùng lại, rồi diffusion chạy trên các latent nhỏ của nó.

**👉 [Thẻ 2]**

> **Hai**: giữ latent ở dạng lưới 2-D và chỉ nén nhẹ, từ 4 đến 8 lần mỗi chiều, để U-Net vẫn xử lý được và ảnh tái tạo vẫn trung thực.

**👉 [Thẻ 3]**

> **Ba**: một cơ chế conditioning tổng quát là cross-attention, cho phép bất kỳ đầu vào nào như text, class hay layout điều khiển denoiser. Ba slide tiếp theo sẽ lần lượt giải thích các ý tưởng này.

⚠️ **Đừng nói** các con số GPU-days là của LDM tự đo. LDM trích chúng từ Dhariwal & Nichol 2021.

---

## Slide 8: Latent space: what it is, and why it helps (B · ~65s)

**Bố cục**: **sơ đồ ngang trên cùng**: [image $x_0$, "196,608 values"] → [VAE encoder, "mean $\mu$, spread $\sigma$"] → mũi tên "sample $z$" → hình lưới xanh "latent $z$: $32\times32\times4$", "4,096 values" → [VAE decoder, "latent → image"] → [reconstruction $\hat x_0\approx x_0$]; khung đứt nét xanh lá "stage 1: trained once, then frozen"; dưới decoder có dòng xanh lá "48× fewer values ($f=8$, 4 channels)" · **4 khung xếp lưới 2×2, đọc theo hàng**: *1. What is a latent?* | *2. VAE encoder and decoder* (hàng trên, xanh) · *3. Why does it cut the cost?* (xanh lá) | *4. Why still need diffusion?* (cam) (hàng dưới).

**👉 [Khung 1 "What is a latent?": câu "In general", rồi chỉ hình lưới latent ở giữa sơ đồ (chỉ "4,096 values") khi nói "In LDM"] ✋**

> Trước hết, latent là gì? Nói chung, latent là một **biểu diễn ẩn, đã được nén** của dữ liệu, mà từ đó có thể dựng lại dữ liệu; một VAE kinh điển dùng một vector phẳng và ngắn. Latent của **LDM** là một lựa chọn cụ thể: một lưới nhỏ có hình dạng như ảnh, ở đây là 32 nhân 32 nhân 4 con số, giữ lại bố cục, hình dạng và màu sắc, và bỏ đi những chi tiết khó thấy.

**👉 [Sơ đồ: VAE encoder → "sample $z$" → lưới → VAE decoder → reconstruction; rồi khung 2 "VAE encoder and decoder"]**

> Làm sao có được latent? Bằng một VAE. Encoder không ánh xạ ảnh thành một điểm duy nhất, mà thành một *đám mây* nhỏ các latent khả dĩ, gồm một mean và một spread, rồi ta lấy mẫu $z$ từ đó. Decoder ánh xạ $z$ ngược lại thành ảnh.

**👉 [Khung đứt nét "stage 1: trained once, then frozen"]**

> VAE này là giai đoạn một: train một lần, rồi đóng băng.

**👉 [Khung 3 "Why does it cut the cost?", rồi nhãn "48× fewer values" trên sơ đồ] ✋**

> Vì sao nó giảm chi phí? Nhớ lại slide 7: chi phí bằng số bước nhân với một lần chạy mạng. LDM giữ nguyên số bước, nhưng mỗi lần chạy giờ làm trên latent, với **ít hơn 48 lần số giá trị** khi nén 8 lần mỗi chiều và dùng 4 channel, đúng cấu hình mà Stable Diffusion dùng; còn VAE thì chỉ chạy một lần cho mỗi ảnh.

**👉 [Khung 4 "Why still need diffusion?"] ✋**

> Nhưng nếu đã có decoder rồi thì sao vẫn cần diffusion? Vì VAE chỉ nén và khôi phục những ảnh **đã có sẵn**. Một ảnh *mới* cần một latent mới, mà decode một latent ngẫu nhiên thì ra ảnh vô nghĩa. Diffusion học cách **tạo ra latent giống thật**, rồi decoder biến chúng thành pixel. Đó là nội dung của slide tiếp theo.

⚠️ 48× là phép tính từ cấu hình ($256\times256\times3$ so với $32\times32\times4$), không phải số đo. KL trong LDM chỉ là lực kéo yếu, nên latent *không* thành Gaussian chuẩn; đó là lý do decode một latent ngẫu nhiên cho ảnh xấu (khung 4).
⚠️ Cách train autoencoder (perceptual loss, adversarial loss, KL/VQ) đã chuyển xuống **backup 16**. Nếu bị hỏi "vì sao ảnh tái tạo không mờ", mở backup 16.
⚠️ Công thức VAE (ELBO, reparameterization) cũng ở **backup 16**. Chỉ mở khi bị hỏi.

**Chuyển người (B → C)**: "Giờ đã có latent space, [Tên C] sẽ trình bày diffusion chạy bên trong nó như thế nào."

---

## Slide 9: Operations in latent space: the whole LDM pipeline (C · ~75s)

**Bố cục**: **sơ đồ lớn** chiếm gần cả slide: vùng nền xanh nhạt "LATENT SPACE: every diffusion operation runs on the small $z$" · **làn trên TRAINING (stage 2)**: [real image $x_0$] → [Encoder, frozen] → [$z_0$] → [add noise] → [U-Net, predict the noise] · **làn dưới GENERATION** (chú thích "no real image, no encoder"): [$z_T$ noise] → [U-Net + sampler, $T$ steps] (mũi tên cam "repeat") → [Decoder, frozen, **once**] → [new image] · **bên phải**: [prompt $y$] → [condition encoder $\tau_\eta$], hai mũi tên xanh "cross-attn" vào cả hai U-Net · **3 thẻ dưới**: *Same DDPM operations, now on $z$* (xanh) | *Encoder only for training* (xanh lá) | *Cheaper per step* (cam).

**👉 [Vùng nền xanh "LATENT SPACE"] ✋**

> Đây là toàn bộ pipeline. Vùng tô màu là latent space: **mọi thao tác của diffusion đều diễn ra ở đây**, trên lưới nhỏ, chứ không phải trên pixel.

**👉 [Làn TRAINING: trái → phải]**

> Khi train: lấy một ảnh thật, encode một lần bằng encoder đã đóng băng, thêm nhiễu y như ở slide 3, rồi train U-Net dự đoán nhiễu đó. Đây chính là DDPM, chỉ là chạy trên $z$.

**👉 [Làn GENERATION: $z_T$ → U-Net + sampler (chỉ mũi tên "repeat") → Decoder → new image]**

> Khi sinh ảnh: bắt đầu từ nhiễu trong latent, chạy U-Net và sampler qua $T$ bước, rồi gọi decoder **một lần duy nhất** ở cuối. Không cần ảnh thật, cũng không cần encoder.

**👉 [prompt $y$ → $\tau_\eta$ → hai mũi tên "cross-attn"]**

> Prompt được encode bởi $\tau_\eta$ và đi vào cả hai U-Net thông qua cross-attention, nội dung của slide tiếp theo.

**👉 [3 thẻ dưới: trái → giữa → phải]**

> Tóm lại: vẫn là các thao tác của DDPM, nhưng giờ trên $z$; encoder chỉ dùng khi train, decoder chỉ chạy một lần; và mỗi lần gọi U-Net rẻ hơn vì chỉ xử lý khoảng 48 lần ít giá trị hơn, ở mọi bước trong số rất nhiều bước. Chi phí đo thực tế của paper nằm ở slide 11.

⚠️ **Đừng nói** "LDM nhanh hơn 48×". Đó là 48× ít giá trị hơn mỗi bước, không phải tốc độ đo được (paper đo được: sampling nhanh 3.7–4.9×, slide 11).

---

## Slide 10: Cross-attention: steering the denoiser with a prompt (C · ~80s)

**Bố cục**: **trái**: khung xanh lá *Image regions ask, prompt words answer* (lưới latent với một ô cam; các token a / red / bus / left / blue / car; đường nối dày tới "red" và "bus"), 3 gạch đầu dòng (gạch cuối về guidance, có nhãn PAPER REPORTS) · **phải**: nhãn OUR RUN "Stable Diffusion v1.4, same seed and initial latent", 3 ảnh *Reference* | *red → green* | *left → right*, 2 gạch đầu dòng với ✓/✗, khung cam *Why: attention is soft* (Chefer et al. 2023).

**👉 [Hình bên trái: ô cam trên lưới latent, rồi các đường nối dày tới "red" và "bus"] ✋**

> Prompt điều khiển denoiser bằng cách nào? Bằng cross-attention: **vùng ảnh hỏi, từ trong prompt trả lời**. Mỗi vùng của latent, như ô màu cam này, tra cứu các prompt token; đường càng dày thì attention càng cao. Một vùng đang dần thành chiếc xe buýt sẽ lấy thông tin từ "red" và "bus".

**👉 [3 gạch đầu dòng bên trái]**

> Việc này lặp lại ở mọi layer của U-Net và mọi bước, nên prompt điều khiển từng lần dự đoán nhiễu, chứ không dán thẳng lên pixel cuối cùng. Cùng một cơ chế dùng được cho mọi loại điều kiện: chỉ có encoder thay đổi, cho text, class hay layout. **(cắt được)** Và guidance scale kéo ảnh bám sát prompt hơn, nhưng làm ảnh kém đa dạng hơn: trong paper LDM, recall giảm từ 0.62 xuống 0.48.

**👉 [Nhãn OUR RUN, rồi ảnh 1 "Reference"]**

> Vậy cách này có luôn đúng không? Một minh họa nhỏ với Stable Diffusion: cùng seed, cùng latent ban đầu, ba prompt khác nhau. Ảnh gốc: "a red bus to the left of a blue car."

**👉 [Ảnh 2 "red → green" rồi gạch ✓ đầu tiên]**

> Đổi red thành green: xe buýt chuyển sang màu xanh lá ở cả bốn seed nhóm thử, nhưng không thấy rõ chiếc xe màu xanh dương.

**👉 [Ảnh 3 "left → right" rồi gạch ✗ thứ hai]**

> Đổi left thành right: không có thay đổi vị trí. Chiếc xe buýt đỏ vẫn ở bên trái.

**👉 [Khung cam "Why: attention is soft"] ✋**

> Tại sao vậy? Vì attention là **mềm**: không có gì ép mỗi từ phải gắn đúng vào một đối tượng hay một vị trí. Chefer và cộng sự báo cáo đúng những lỗi này ở Stable Diffusion: chủ thể bị bỏ sót, và thuộc tính bị gán nhầm đối tượng.

⚠️ Ảnh bus là **minh họa** (16 ảnh, kiểm bằng mắt), không phải bằng chứng; bằng chứng là Chefer et al. 2023. Công thức $Q, K, V$, softmax và CFG ở **backup 16**; đủ 4 seed của thí nghiệm ở **backup 18**.

---

## Slide 11: Pixel vs. latent diffusion: what the LDM paper measured (C · ~70s)

**Bố cục**: **dòng trên cùng**: nhãn PAPER REPORTS, Rombach et al. 2022 Table 6 (inpainting on Places, LDM-1 pixel so với LDM-4 latent, một A100) · **trái**: bảng 5 tiêu chí (Training, Sampling @256², Sampling @512², Time per epoch, FID@2k) với cột Ratio, dòng chú thích xám · **phải**: lưới ảnh nhà thờ 2 × 4 (hàng DDPM, hàng LDM; cột seed 2026–2029), chú thích có nhãn OUR RUN "Illustration only" · **dưới cùng**: khung xanh *Takeaway*.

**👉 [Dòng PAPER REPORTS trên cùng]**

> Latent diffusion có thật sự giảm chi phí không? Đây là số đo của chính paper LDM: cùng một tác vụ inpainting và cùng phần cứng, so sánh pixel model với latent model nén 4 lần.

**👉 [Bảng: hàng Training, rồi hai hàng Sampling (chỉ 3.7× và 4.9×), rồi Time per epoch] ✋**

> Training throughput cao hơn 2.9 lần. Sampling **nhanh hơn 3.7 lần** ở 256 bình phương và **4.9 lần** ở 512 bình phương, và mỗi epoch mất ít thời gian hơn 2.7 lần.

**👉 [Hàng FID@2k, rồi dòng chú thích xám]**

> Và chất lượng không bị giảm: sau sáu epoch, FID là 15.21 so với 24.74, càng thấp càng tốt. Có hai lưu ý: số epoch được cố định, và thời gian pre-train của autoencoder chưa được tính.

**👉 [Lưới ảnh nhà thờ: hàng DDPM, rồi hàng LDM; chỉ nhãn OUR RUN "Illustration only"]**

> Bên phải, chỉ để minh họa, là các ảnh nhóm sinh bằng pixel model và latent model pretrained trên ảnh nhà thờ: cả hai đều trông hợp lý. Bằng chứng là bảng của paper bên trái.

**👉 [Khung Takeaway]**

> Vậy trên một latent nén 4 lần, cùng một quá trình diffusion sample nhanh hơn từ 3.7 đến 4.9 lần và train nhanh hơn 2.7 lần mỗi epoch, với FID bằng hoặc tốt hơn. Nhưng paper cũng cho thấy nén quá mức, ở hệ số 32, sẽ làm giảm chất lượng.

⚠️ **Đừng nói** FID giảm 38% nghĩa là ảnh "đẹp hơn 38%". Đây là điểm số thấp hơn, trên một tác vụ inpainting.
⚠️ **Đừng dùng** lưới ảnh nhà thờ làm bằng chứng so sánh chất lượng: chỉ 4 ảnh mỗi model, mỗi model lấy nhiễu trong không gian riêng nên các cột không phải cặp ảnh tương ứng.
💡 Nếu bị hỏi "nhóm có tự đo tốc độ không?", mở **backup 17** (nhanh 2.5× nhưng bộ nhớ đỉnh cao hơn; chỉ 4 ảnh, không phải benchmark).

---

## Slide 12: Limitations, and when to use diffusion (C · ~40s)

**Bố cục**: **trái**: tiêu đề "Limitations and why", khung đỏ với 5 dòng *giới hạn: lý do* (Slow sampling, Quality ceiling, Soft prompt control, Data bias, Weak likelihood) · **phải**: tiêu đề "When to use which", 3 khung ngắn: *Latent diffusion* (xanh lá) | *Pixel diffusion* (xanh) | *Neither* (cam).

**👉 [Khung đỏ: đọc nhanh từng dòng từ trên xuống]**

> Mỗi giới hạn đều có một nguyên nhân đơn giản. Sampling **chậm** vì cần nhiều bước nhỏ, chạy lần lượt. Chất lượng có **trần**: decoder chỉ khôi phục được những gì latent giữ lại. Prompt control thì **mềm**: từ trong prompt có thể bị bỏ sót hoặc gán nhầm đối tượng. Mô hình sao chép **bias** của dữ liệu. **(cắt được)** Và $L_{\text{simple}}$ ưu tiên chất lượng ảnh hơn likelihood.

**👉 [3 khung bên phải, lần lượt] ✋**

> Vậy khi nào nên dùng cái gì? **Latent** diffusion cho ảnh độ phân giải cao hoặc text-to-image, khi chấp nhận mất các chi tiết rất nhỏ. **Pixel** diffusion cho ảnh nhỏ, hoặc khi cần chi tiết nhỏ chính xác. Và **không dùng cả hai** cho ứng dụng real-time, trừ khi có một sampler nhanh hơn để giảm số bước.

⚠️ Phần "When to use which" là cách hiểu của nhóm dựa trên các paper, không phải kết luận của một paper cụ thể. Nói rõ nếu bị hỏi.

---

## Slide 13: Conclusion: the recipe behind today's image generators (C · ~35s)

**Bố cục**: **khung xanh "The big picture"** trên cùng (3 cụm in đậm: *many small, easy denoising steps*, *cheap*, *controllable*) · **3 thẻ**: *1. Forward noising* (xanh dương) | *2. Reverse denoising* (cam) | *3. Latent diffusion* (xanh lá) · dòng nghiêng · "Thank you · Questions?"

**👉 [Khung "The big picture": lần lượt 3 cụm in đậm] ✋**

> Để kết lại, đây là bức tranh tổng. Diffusion biến việc sinh ảnh thành **nhiều bước khử nhiễu nhỏ và dễ**. LDM làm mỗi bước **rẻ** hơn nhờ làm việc trên một latent gọn, và cross-attention làm nó **điều khiển được** bằng prompt. Ghép lại, đó là công thức đứng sau các hệ text-to-image như Stable Diffusion.

**👉 [3 thẻ: trái → giữa → phải]**

> Learning objective gói trong ba thẻ: forward noising đổi tín hiệu lấy nhiễu bằng một chuỗi Gaussian đã biết; reverse denoising học cách dự đoán nhiễu, và biết nhiễu thì biết ảnh; latent diffusion chạy cùng vòng lặp trên một latent ít hơn 48 lần số giá trị, và theo paper thì sample nhanh hơn từ 3.7 đến 4.9 lần, đổi lại có một trần chất lượng do tái tạo.

**👉 [Dòng nghiêng]**

> Mọi giai đoạn đều bị giới hạn bởi dữ liệu train và bởi những gì latent giữ lại được. Cảm ơn thầy cô và các bạn đã lắng nghe; chúng em xin nhận câu hỏi.

⚠️ Không trả lời lại guiding question ở đây; câu trả lời đầy đủ đã ở slide 6. Nếu được hỏi lại, quay về khung xanh lá slide 6.

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
| VAE khác autoencoder thường? Sao không decode $z\sim\mathcal N(0,I)$? | 8 (khung 2 và 4); công thức ở backup 16 | B | Encoder xuất phân phối + KL + reparameterization; latent sạch không phải $\mathcal N(0,I)$ nên phải dùng diffusion để học phân phối latent. |
| Vì sao latent phải giữ dạng lưới 2-D và chỉ nén nhẹ? | 7 (thẻ 2), 8 | B | U-Net xử lý được lưới 2-D; nén nhẹ ($f=4$–$8$) giữ ảnh tái tạo trung thực; các mô hình hai giai đoạn trước đó làm phẳng thành chuỗi token 1-D và phải nén mạnh hơn. |
| Vì sao perceptual + adversarial thay vì MSE? | Backup 16 | B | MSE theo pixel lấy trung bình các chi tiết khả dĩ nên ảnh mờ. |
| Encoder có dùng khi sinh ảnh không? | 9 | C | Không: sinh ảnh bắt đầu từ nhiễu latent $z_T$; encoder chỉ dùng khi train, decoder chạy một lần ở cuối. |
| Cross-attention khác self-attention? Công thức cụ thể? | 10; công thức ở backup 16 | C | Q từ ảnh; K, V từ điều kiện (với self-attention thì cả ba từ ảnh); $O=\mathrm{softmax}(QK^\top/\sqrt d)V$. |
| Latent diffusion thực sự rẻ hơn bao nhiêu? | 11 | C | Theo LDM Table 6: sampling nhanh 3.7–4.9×, mỗi epoch nhanh 2.7×, FID@2k 24.74 → 15.21; caveat: số epoch cố định, chưa tính thời gian pre-train autoencoder. |
| Ảnh bus có phải bằng chứng không? | 10; đủ 4 seed ở backup 18 | C | Không: chỉ là minh họa 16 ảnh (4 seed × 4 prompt) kiểm bằng mắt; bằng chứng là Chefer et al. 2023, và kết quả của nhóm khớp với lỗi họ mô tả. |
| Nhóm có tự kiểm chứng tốc độ không? | Backup 17 | C | Run LSUN Churches: nhanh 2.5× nhưng bộ nhớ đỉnh cao hơn (1.68 so với 0.75 GiB); chỉ 4 ảnh, 1 cặp checkpoint, không FID; lý do bộ nhớ cao hơn chưa được phân tích. |
| Guidance có đánh đổi gì? | 10 | C | LDM Table 3: guidance s = 1.5 giảm FID 10.56 → 3.60, tăng precision, nhưng recall giảm 0.62 → 0.48 (kém đa dạng hơn). |
| Vì sao sampling chậm, và có cách nào nhanh hơn? | 12 (dòng 1 và khung "Neither") | C | Bước ngược phải nhỏ để gần Gaussian nên cần nhiều lượt gọi mạng tuần tự; các sampler nhanh hơn có thể giảm số bước, đổi lại chất lượng giảm phần nào. |
| Một ký hiệu nghĩa là gì / miền giá trị? | Backup 14 | ai cũng được | Bảng Notation, value ranges and modelling assumptions. |
| Có bằng chứng nào mạng "thấy" ảnh khi trạng thái còn đầy nhiễu? | Backup 15 | B | Run của nhóm: ở bước DDIM 25/50, clean estimate $\hat x_0$ đã thấy con chó (cả pixel ADM và latent LDM); updated state chỉ nhích một bước nhỏ. |
| Nguồn hình/số liệu? | Backup 19–20 | ai cũng được | Sơ đồ là hình tự vẽ; run dùng checkpoint pretrained; số paper ghi rõ nguồn. |

**Mẹo khi trả lời**: luôn bấm về slide liên quan và **chỉ vào đúng khung** trước khi trả lời. Như vậy người hỏi thấy câu trả lời đã nằm trong bài.

---

## Checklist trước giờ trình bày

- [ ] Mỗi người tập riêng phần của mình với đồng hồ: **A ≈ 4.6 phút** (slide 1–4, 275s), **B ≈ 5.2 phút** (slide 5–8, 310s), **C ≈ 5.0 phút** (slide 9–13, 300s). Tổng 885s, chỉ dư khoảng 15s so với giới hạn 15 phút. Nói tiếng Việt thường dài hơn bản tiếng Anh, nên hãy bấm giờ với chính bản này.
- [ ] Tập 2 lần chuyển người (sau slide 4, sau slide 8) cho liền mạch.
- [ ] Chuẩn bị laser/pointer. Nếu không có, đứng cạnh màn hình và chỉ bằng tay theo các 👉.
- [ ] Đánh dấu sẵn các câu **(cắt được)** để bỏ nếu trễ hơn 30 giây.
- [ ] Mỗi thành viên nhận ít nhất một câu Q&A trong bảng trên.
