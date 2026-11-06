Để hiểu chính xác từ mục tiêu học $p_{\text{data}}(x)$ đến predict noise trong DDPM, cần nối ba công trình:

1. Sohl-Dickstein et al. (2015) – [Deep Unsupervised Learning using Nonequilibrium Thermodynamics](https://proceedings.mlr.press/v37/sohl-dickstein15.pdf?utm_source=chatgpt.com): đặt nền tảng cho diffusion probabilistic models.
2. Song & Ermon (2019) – [Generative Modeling by Estimating Gradients of the Data Distribution](https://arxiv.org/pdf/1907.05600?utm_source=chatgpt.com): phát triển hướng học score để sinh dữ liệu.
3. Ho et al. (2020) – [Denoising Diffusion Probabilistic Models (DDPM)](https://arxiv.org/pdf/2006.11239?utm_source=chatgpt.com): chỉ ra kết nối giữa diffusion, denoising score matching và noise prediction.

Một điểm quan trọng về lịch sử: DDPM không bắt đầu bằng score matching rồi mới suy ra diffusion. Paper bắt đầu từ một mô hình xác suất với variational inference, sau đó chứng minh rằng parameterization dự đoán noise có liên hệ với denoising score matching.

Nhưng để hiểu cơ chế, ta có thể đi theo con đường tuyến tính mà bạn muốn:

Học $p_{\text{data}}(x)$

Học score $\nabla_x\log p(x)$

Học score ở nhiều mức Gaussian noise

Chuyển score estimation thành noise prediction

Dùng predicted noise để xây dựng reverse transition

Lặp reverse transitions để sinh $x_0$

## 1. Objective ban đầu: Học phân phối dữ liệu

Giả sử ta có dataset gồm $N$ ảnh:

$$
\mathcal D=\{x^{(1)},x^{(2)},\ldots,x^{(N)}\}
$$

Các ảnh được lấy từ một phân phối không biết trước:

$$
x^{(i)}\sim p_{\text{data}}(x)
$$

Ta muốn xây dựng một generative model $p_\theta(x)$ sao cho:

$$
\boxed{p_\theta(x)\approx p_{\text{data}}(x)}
$$

Một cách truyền thống là Maximum Likelihood Estimation (MLE):

$$
\theta^*= \arg\max_\theta \mathbb E_{x\sim p_{\text{data}}} [\log p_\theta(x)]
$$

Tương đương với việc tối thiểu hóa:

$$
D_{\mathrm{KL}}(p_{\text{data}}\|p_\theta)
$$

bỏ qua entropy của $p_{\text{data}}$, vốn không phụ thuộc vào $\theta$.

Vấn đề: Phân phối ảnh trong không gian nhiều chiều cực kỳ phức tạp. Việc xây dựng một density model có normalized likelihood dễ tính và đồng thời sinh được ảnh tốt là không đơn giản.

Đây là động lực để tìm những cách học phân phối mà không nhất thiết phải trực tiếp tính giá trị $p_{\text{data}}(x)$.

## 2. Từ probability density đến score function

Song & Ermon (2019, Section 2) sử dụng một đại lượng gọi là score:

$$
\boxed{s(x)=\nabla_x\log p_{\text{data}}(x)}
$$

Nó trả lời câu hỏi:

> Nếu đang đứng tại một điểm $x$ trong không gian ảnh, ta cần dịch chuyển theo hướng nào để log-probability tăng nhanh nhất?

Xét ví dụ đơn giản:

$$
p(x)=\mathcal N(0,1)
$$

Khi đó:

$$
\log p(x)=-\frac{x^2}{2}+C
$$

và:

$$
s(x)=\frac{d}{dx}\log p(x)=-x
$$

- $x=3$: score bằng $-3$, hướng về phía trái.
- $x=-2$: score bằng $2$, hướng về phía phải.
- $x=0$: score bằng $0$, không có hướng tăng mật độ cục bộ.

Tại sao score hữu ích?

Vì có thể dùng nó trong Langevin Dynamics:

$$
\boxed{ x_{k+1}=x_k+\frac{\eta}{2}s(x_k)+\sqrt{\eta}z_k }
$$

với $z_k\sim\mathcal N(0,I)$.

Hai thành phần có ý nghĩa khác nhau:

- $s(x_k)$: drift, điều hướng theo phân phối mục tiêu.
- $z_k$: stochastic noise, giúp quá trình khám phá phân phối thay vì chỉ hội tụ về một mode.

Với score chính xác và các điều kiện phù hợp, Langevin dynamics có thể tạo mẫu từ phân phối $p(x)$, không cần biết trực tiếp normalized density của nó. Đây là Eq. (4) trong Song & Ermon (2019).

Từ đây, bài toán generative modeling chuyển thành:

$$
\boxed{ s_\theta(x)\approx\nabla_x\log p_{\text{data}}(x) }
$$

Nhưng ta gặp vấn đề mới: không biết $p_{\text{data}}$, vậy lấy đâu ra ground-truth score để training?

Đó là nơi Gaussian noise xuất hiện.

## 3. Từ score matching đến Gaussian noise

Ta muốn training:

$$
s_\theta(x)\approx\nabla_x\log p_{\text{data}}(x)
$$

Nhưng không có ground-truth score.

Ý tưởng của Denoising Score Matching (DSM) là cố tình thêm Gaussian noise vào dữ liệu. Khi đó, ta biết chính xác score của noise corruption distribution.

Đây là cơ sở cho bước chuyển quan trọng nhất.

### 3.1. Xây dựng một noisy distribution

Cho:

$$
x_0\sim p_{\text{data}}(x)
$$

Thêm Gaussian noise:

$$
x_t=a_tx_0+b_t\epsilon
$$

với:

$$
\epsilon\sim\mathcal N(0,I)
$$

Trong DDPM:

$$
a_t=\sqrt{\bar\alpha_t}, \qquad b_t=\sqrt{1-\bar\alpha_t}
$$

Do đó:

$$
\boxed{ q(x_t|x_0)= \mathcal N(a_tx_0,b_t^2I) }
$$

Đây là một Gaussian có mean và variance đã biết.

Từ nó, ta có phân phối dữ liệu ở noise level $t$:

$$
\boxed{ q_t(x_t)= \int p_{\text{data}}(x_0)q(x_t|x_0)\,dx_0 }
$$

Nghĩa là $q_t$ chính là phân phối dữ liệu ban đầu sau khi được làm nhiễu.

- $q_0$: phân phối ảnh thật.
- $q_t$: phân phối ảnh đã thêm nhiễu.
- $q_T$: xấp xỉ standard Gaussian.

Mục tiêu mới là học score của từng $q_t$:

$$
s_\theta(x_t,t)\approx\nabla_{x_t}\log q_t(x_t)
$$

Thêm noise giúp các phân phối trở nên trơn hơn và score dễ học hơn, đặc biệt khi dữ liệu tập trung gần các low-dimensional manifolds. Đây là động lực chính trong Song & Ermon (2019), Sections 3–4.

### 3.2. Tại sao Gaussian noise giải quyết được vấn đề ground truth?

Hãy tính score của $q(x_t|x_0)$:

$$
\log q(x_t|x_0) = -\frac{\|x_t-a_tx_0\|^2}{2b_t^2}+C
$$

Đạo hàm theo $x_t$:

$$
\nabla_{x_t}\log q(x_t|x_0) = -\frac{x_t-a_tx_0}{b_t^2}
$$

Nhưng ta đã biết:

$$
x_t-a_tx_0=b_t\epsilon
$$

Vậy:

$$
\boxed{ \nabla_{x_t}\log q(x_t|x_0) =-\frac{\epsilon}{b_t} }
$$

Đây chính là bước chuyển từ score estimation sang noise prediction.

Ta không cần biết $p_{\text{data}}$ để tính target này. Chỉ cần $x_0$ và noise $\epsilon$ do chính ta sinh ra.

Tuy nhiên có một câu hỏi:

Đây là score của $q(x_t|x_0)$, không phải score của $q_t(x_t)$. Tại sao học nó lại giúp tìm score của phân phối dữ liệu nhiễu?

### 3.3. Chứng minh Denoising Score Matching

Từ định nghĩa marginal:

$$
q_t(x_t)=\int p_{\text{data}}(x_0)q(x_t|x_0)\,dx_0
$$

Lấy gradient và dùng Bayes:

$$
\begin{aligned}
\nabla_{x_t}\log q_t(x_t) &=\frac{\nabla_{x_t}q_t(x_t)}{q_t(x_t)}\\
&=\int q(x_0|x_t) \nabla_{x_t}\log q(x_t|x_0)\,dx_0
\end{aligned}
$$

Từ bước 3.2:

$$
\nabla_{x_t}\log q(x_t|x_0) =-\frac{\epsilon}{b_t}
$$

Suy ra:

$$
\boxed{ \nabla_{x_t}\log q_t(x_t) = -\frac{\mathbb E[\epsilon|x_t]}{b_t} }
$$

Đây là kết quả cốt lõi.

Nó nói rằng:

> Score của noisy data distribution có thể được suy ra từ kỳ vọng có điều kiện của Gaussian noise đã tạo ra dữ liệu nhiễu.

Vì vậy, ta có thể training bằng:

$$
\mathcal L_{\mathrm{DSM}} = \mathbb E\left[ \left\| s_\theta(x_t,t)+\frac{\epsilon}{b_t} \right\|^2 \right]
$$

Đặt:

$$
\epsilon_\theta(x_t,t)=-b_ts_\theta(x_t,t)
$$

Ta được:

$$
\boxed{ \mathcal L_{\mathrm{noise}} = \mathbb E\left[ \|\epsilon-\epsilon_\theta(x_t,t)\|^2 \right] }
$$

(lựa chọn hệ số weighting thích hợp giữa các timestep).

Như vậy, predict Gaussian noise bằng MSE thực chất là một cách học score của noisy data distribution.

Một chi tiết quan trọng: model tối ưu không thể biết chính xác noise ngẫu nhiên của một training sample chỉ từ $x_t$. Nghiệm MSE lý tưởng là:

$$
\epsilon_\theta^*(x_t,t)=\mathbb E[\epsilon|x_t]
$$

Điều này giải thích tại sao score được học đúng ở mức phân phối, dù mỗi training example sử dụng một noise target cụ thể.

## 4. Từ score function đến reverse step $x_{t-1}$

Bây giờ ta đã có:

$$
s_\theta(x_t,t)\approx\nabla_{x_t}\log q_t(x_t)
$$

Vậy làm sao dùng score để sinh ảnh?

Quay lại forward process trong DDPM:

$$
q(x_t|x_{t-1})= \mathcal N(\sqrt{\alpha_t}x_{t-1},\beta_t I)
$$

với:

$$
\alpha_t=1-\beta_t
$$

Ta muốn đảo ngược:

$$
q(x_{t-1}|x_t)
$$

Áp dụng cùng identity vừa chứng minh, nhưng lần này cho một forward step:

$$
\nabla_{x_t}\log q_t(x_t) = -\frac{x_t-\sqrt{\alpha_t}\mathbb E[x_{t-1}|x_t]}{\beta_t}
$$

Biến đổi:

$$
\beta_t\nabla_{x_t}\log q_t(x_t) = -x_t+\sqrt{\alpha_t}\mathbb E[x_{t-1}|x_t]
$$

Suy ra:

$$
\boxed{ \mathbb E[x_{t-1}|x_t] = \frac{1}{\sqrt{\alpha_t}} \left( x_t+\beta_t\nabla_{x_t}\log q_t(x_t) \right) }
$$

Đây là kết nối trực tiếp giữa score function và mean của reverse step.

Nhưng ta đã học được:

$$
\nabla_{x_t}\log q_t(x_t) \approx -\frac{\epsilon_\theta(x_t,t)} {\sqrt{1-\bar\alpha_t}}
$$

Thay vào công thức trên:

$$
\boxed{ \mu_\theta(x_t,t)= \frac{1}{\sqrt{\alpha_t}} \left( x_t- \frac{\beta_t}{\sqrt{1-\bar\alpha_t}} \epsilon_\theta(x_t,t) \right) }
$$

Đây chính xác là Eq. (11) trong paper DDPM (2020).

Lưu ý: Biểu thức kỳ vọng ở trên là chính xác. Nhưng reverse conditional đầy đủ $q(x_{t-1}|x_t)$ không nhất thiết là Gaussian. DDPM mô hình hóa nó bằng Gaussian, một lựa chọn hợp lý khi mỗi forward step đủ nhỏ.

### Reverse sampling thực tế

DDPM định nghĩa:

$$
p_\theta(x_{t-1}|x_t) = \mathcal N(\mu_\theta(x_t,t),\sigma_t^2I)
$$

Vì vậy:

$$
\boxed{ x_{t-1}=\mu_\theta(x_t,t)+\sigma_tz }
$$

với $z\sim\mathcal N(0,I)$ cho $t>1$, và $z=0$ tại bước cuối theo Algorithm 2 của DDPM.

Có hai loại noise cần phân biệt:

- $\epsilon_\theta(x_t,t)$: noise model dự đoán, dùng để xác định reverse mean.
- $z$: noise lấy mẫu mới, dùng để tạo stochastic reverse transition.

Model không đơn giản lấy $\epsilon_\theta$ trừ thẳng khỏi $x_t$. Nó dùng noise prediction để tính mean của phân phối $p_\theta(x_{t-1}|x_t)$, rồi sample từ phân phối đó.

## 5. Vậy paper DDPM gốc thực sự suy ra MSE noise như thế nào?

Đây là con đường likelihood-based mà Ho et al. thực sự trình bày.

Bắt đầu từ mô hình sinh:

$$
p_\theta(x_0)= \int p_\theta(x_{0:T})\,dx_{1:T}
$$

Objective là giảm negative log-likelihood:

$$
\mathbb E_{p_{\text{data}}} [-\log p_\theta(x_0)]
$$

Tuy nhiên việc marginalize toàn bộ latent trajectory khó tính. Vì vậy paper sử dụng variational upper bound cho negative log-likelihood.

Trong Eq. (5), phần loss ở mỗi reverse step là:

$$
L_{t-1}= D_{\mathrm{KL}}\left( q(x_{t-1}|x_t,x_0) \| p_\theta(x_{t-1}|x_t) \right)
$$

Forward posterior khi biết $x_0$ là Gaussian có closed-form mean $\tilde\mu_t$.

Giả sử reverse variance được cố định ở $\sigma_t^2I$. KL giữa hai Gaussian dẫn tới:

$$
L_{t-1} = \mathbb E\left[ \frac{1}{2\sigma_t^2} \|\tilde\mu_t-\mu_\theta(x_t,t)\|^2 \right]+C
$$

Tiếp theo, paper chọn noise parameterization cho $\mu_\theta$, chính là công thức ta vừa suy ra trong Section 4.

Thay vào loss:

$$
\boxed{ L_{t-1} = \mathbb E\left[ \frac{\beta_t^2} {2\sigma_t^2\alpha_t(1-\bar\alpha_t)} \|\epsilon-\epsilon_\theta(x_t,t)\|^2 \right]+C }
$$

Đây là Eq. (12) của DDPM.

Cuối cùng, tác giả bỏ hệ số weighting phụ thuộc vào timestep và dùng simplified objective:

$$
\boxed{ L_{\mathrm{simple}}= \mathbb E_{t,x_0,\epsilon} \left[ \left\| \epsilon- \epsilon_\theta( \sqrt{\bar\alpha_t}x_0+ \sqrt{1-\bar\alpha_t}\epsilon,t ) \right\|^2 \right] }
$$

Đây là Eq. (14), trang 5 của paper. Nó không còn là variational bound gốc với đúng các hệ số KL, mà là một weighted variant cho kết quả sample tốt hơn trong thực nghiệm của tác giả.

Như vậy, có hai con đường gặp nhau tại cùng một objective:

Score-based view

Score Matching

Gaussian Denoising

Score / Noise Identity

DDPM likelihood view

Variational Bound

Gaussian KL

Reverse Mean Parameterization

Noise Prediction MSE

$\mathbb E\|\epsilon-\epsilon_\theta(x_t,t)\|^2$

## 6. Tại sao cần nhiều bước?

Score mà model học là:

$$
s_\theta(x_t,t)\approx\nabla\log q_t(x_t)
$$

Nó là score của phân phối tại timestep $t$, không phải chỉ riêng $p_{\text{data}}$.

Mỗi timestep có một noisy distribution khác nhau. Khi sampling, ta đi từ:

$$
q_T\approx\mathcal N(0,I)
$$

qua các reverse transitions để tiến dần về:

$$
q_0=p_{\text{data}}
$$

Khi $\beta_t$ nhỏ, mỗi transition dễ được xấp xỉ bằng một Gaussian hơn. Nhiều bước nhỏ giúp xây dựng một quá trình sinh phức tạp từ các chuyển tiếp đơn giản.

Quan trọng: Trong training, DDPM không cần tuần tự chạy U-Net qua toàn bộ timestep. Model lấy ngẫu nhiên $t$, tạo $x_t$ trực tiếp, rồi học predict noise tại timestep đó. Chỉ trong inference mới lặp các reverse steps.

## Key things to remember

1. Objective: Học một generative process có phân phối cuối $p_\theta(x_0)$ gần $p_{\text{data}}(x)$.
2. Score: Thay vì nhất thiết phải tính density, ta có thể học vector field $\nabla\log q_t(x_t)$.
3. Gaussian noise: Giúp tạo training target tính được bằng $-\epsilon/\sqrt{1-\bar\alpha_t}$.
4. Noise prediction: Là cách parameterize score estimation bằng MSE.
5. Reverse sampling: Noise prediction được chuyển thành reverse mean $\mu_\theta$, rồi dùng để sample $x_{t-1}$.

Kết nối toán học quan trọng nhất là:

$$
\boxed{ \underbrace{\nabla\log q_t(x_t)}_{\text{Score}} = -\frac{\underbrace{\mathbb E[\epsilon|x_t]}_{\text{Optimal noise prediction}}} {\sqrt{1-\bar\alpha_t}} }
$$

Và khi thay score vào reverse mean, ta thu được sampling equation của DDPM.
