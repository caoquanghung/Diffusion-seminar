# Deep Dive: Deep Unsupervised Learning using Nonequilibrium Thermodynamics (2015)

## 2. Forward diffusion process — Section 2.1

Let \(x^{(0)}\) be a training image. At each timestep \(t\), we gradually introduce Gaussian noise:

\[ \boxed{ q(x^{(t)}\mid x^{(t-1)}) = \mathcal N\left( \sqrt{1-\beta_t}\,x^{(t-1)},\beta_t I \right) } \]

Equivalently, using reparameterization:

\[ x^{(t)}=\sqrt{1-\beta_t}\,x^{(t-1)} +\sqrt{\beta_t}\,\epsilon_t \]

where \(\epsilon_t\sim\mathcal N(0,I)\).

There are two simultaneous operations:

- \(\sqrt{1-\beta_t}\): progressively attenuates the original signal.
    
- \(\sqrt{\beta_t}\): introduces additional random Gaussian noise.
    

The factor \(\sqrt{1-\beta_t}\) ensures the standard normal distribution is stationary under this transition: if \(x^{(t-1)}\sim\mathcal N(0,I)\), then \(x^{(t)}\sim\mathcal N(0,I)\).

### Why many small steps?

For sufficiently small diffusion rates \(\beta_t\), the reverse-time transition is also approximately Gaussian.

That is important because the authors can learn a relatively simple Gaussian distribution at each reverse step instead of representing an arbitrary complex conditional distribution.

At the end of a sufficiently long forward process:

\[ q(x^{(T)})\approx\mathcal N(0,I) \]

We now have a known distribution from which generation can begin.

## 3. Reverse diffusion process — Section 2.2

This is the most important part of the method.

The forward process is known, but the true reverse distribution

$$\[ q(x^{(t-1)}\mid x^{(t)}) \]$$

is generally unknown because it depends on the underlying data distribution.

Therefore, the paper introduces a learnable approximation:

$$\[ \boxed{ p_\theta(x^{(t-1)}\mid x^{(t)}) = \mathcal N\left( f_\mu(x^{(t)},t), f_\Sigma(x^{(t)},t) \right) } \]$$

Here, the network learns two functions.

|Function|Output|Role|
|---|---|---|
|\(f_\mu(x^{(t)},t)\)|Mean vector \(\mu_\theta\)|Where the next denoised sample should be centered|
|\(f_\Sigma(x^{(t)},t)\)|Covariance matrix \(\Sigma_\theta\)|How much uncertainty should remain|

The original paper does not train a network to directly predict Gaussian noise \(\epsilon\). It learns the parameters of the reverse Gaussian distribution.

### Why a Gaussian?

For sufficiently small diffusion steps, reversing a Gaussian diffusion can be well approximated by Gaussian transitions.

That makes the reverse distribution tractable:

\[ x^{(t-1)} = \mu_\theta(x^{(t)},t) + \Sigma_\theta(x^{(t)},t)^{1/2}\epsilon \]

with \(\epsilon\sim\mathcal N(0,I)\).

Notice that the standard deviation is the square root of the predicted covariance. For diagonal covariance, this is simply an element-wise square root.

### An important subtlety

The reverse model does not predict one deterministic image.

Instead, it predicts a distribution of possible previous states and then samples from it.

This is what makes the process generative rather than merely deterministic denoising.

arXiv+1

## 4. How do they obtain training targets?

The unknown unconditional reverse \(q(x^{(t-1)}\mid x^{(t)})\) is difficult to calculate.

But during training, we know the original image \(x^{(0)}\).

That lets us calculate:

\[ \boxed{ q(x^{(t-1)}\mid x^{(t)},x^{(0)}) } \]

This is the posterior of the forward process conditioned on the clean image.

### Step 1: Derive a closed-form noisy distribution

Define:

\[ \alpha_t=1-\beta_t,\qquad \bar\alpha_t=\prod_{s=1}^{t}\alpha_s \]

Repeated substitution into the forward process gives:

\[ q(x^{(t)}\mid x^{(0)}) = \mathcal N\left( \sqrt{\bar\alpha_t}x^{(0)}, (1-\bar\alpha_t)I \right) \]

Therefore, we can sample a noisy image directly:

\[ x^{(t)} = \sqrt{\bar\alpha_t}x^{(0)} + \sqrt{1-\bar\alpha_t}\epsilon \]

without explicitly executing every preceding diffusion step.

### Step 2: Compute the posterior

Using Bayes' rule and the Markov property:

\[ q(x^{(t-1)}\mid x^{(t)},x^{(0)}) \propto q(x^{(t)}\mid x^{(t-1)}) q(x^{(t-1)}\mid x^{(0)}) \]

The product of these two Gaussian densities gives another Gaussian:

\[ \boxed{ q(x^{(t-1)}\mid x^{(t)},x^{(0)}) = \mathcal N(\tilde\mu_t,\tilde\beta_t I) } \]

where

\[ \tilde\mu_t= \frac{\sqrt{\bar\alpha_{t-1}}\beta_t}{1-\bar\alpha_t}x^{(0)} + \frac{\sqrt{\alpha_t}(1-\bar\alpha_{t-1})}{1-\bar\alpha_t}x^{(t)} \]

and

\[ \tilde\beta_t= \frac{1-\bar\alpha_{t-1}}{1-\bar\alpha_t}\beta_t \]

These are closed-form Gaussian posterior parameters, expressed in the notation later popularized by DDPM.

The crucial idea: the model can learn to match a computable posterior, even though the unconditional reverse distribution is unknown.

## 5. Training objective — Section 2.4

The authors want to maximize the likelihood of training samples:

\[ \max_\theta\mathbb E_{q_{\text{data}}(x^{(0)})} [\log p_\theta(x^{(0)})] \]

However, computing \(p_\theta(x^{(0)})\) requires integrating over every intermediate latent variable:

\[ p_\theta(x^{(0)}) = \int p_\theta(x^{(0:T)})\,dx^{(1:T)} \]

That integral is generally intractable.

### Solution: Variational lower bound (ELBO)

They introduce the known forward distribution as an auxiliary distribution:

\[ \log p_\theta(x^{(0)}) = \log\mathbb E_{q(x^{(1:T)}\mid x^{(0)})} \left[ \frac{p_\theta(x^{(0:T)})} {q(x^{(1:T)}\mid x^{(0)})} \right] \]

Applying Jensen's inequality gives a tractable lower bound:

\[ \boxed{ \mathcal L_{\mathrm{ELBO}} = \mathbb E_q \left[ \log p_\theta(x^{(0:T)}) - \log q(x^{(1:T)}\mid x^{(0)}) \right] } \]

In the paper's particular formulation, this is rewritten as:

\[ \boxed{ K= -\sum_{t=2}^{T} \mathbb E_q \left[ D_{\mathrm{KL}}\left( q(x^{(t-1)}\mid x^{(t)},x^{(0)}) \parallel p_\theta(x^{(t-1)}\mid x^{(t)}) \right) \right]+C } \]

where

\[ C= H_q(X^{(T)}\mid X^{(0)}) - H_q(X^{(1)}\mid X^{(0)}) - H_p(X^{(T)}) \]

The authors handle the last reverse transition \(t=1\) specially, using the stationary forward kernel, which is why the KL sum begins at \(t=2\).

arXiv+1

### What is the KL actually optimizing?

Both distributions inside the KL are Gaussian:

\[ q=\mathcal N(\tilde\mu_t,\tilde\beta_t I) \]

\[ p_\theta=\mathcal N(\mu_\theta,\Sigma_\theta) \]

For diagonal \(\Sigma_\theta\), the KL is:

\[ D_{\mathrm{KL}}(q\parallel p_\theta) = \frac12\sum_i \left[ \log\frac{\sigma_{\theta,i}^2}{\tilde\beta_t} + \frac{\tilde\beta_t+(\tilde\mu_{t,i}-\mu_{\theta,i})^2} {\sigma_{\theta,i}^2} -1 \right] \]

The model therefore learns to match:

- The posterior mean, reducing denoising error.
    
- The posterior variance, representing appropriate uncertainty.
    

If the reverse variance is fixed, the mean-dependent part becomes a weighted MSE. But in this paper, both reverse mean and reverse covariance are learned.

## 6. How the neural network is implemented

The original 2015 architecture is quite different from the U-Net commonly used in modern DDPMs.

For image experiments, the authors use a combination of multi-scale convolution, pointwise convolution, and a time-dependent readout.

Noisy image \(x^{(t)}\)

Multi-scale convolution + dense pathway

Extract spatial and contextual features

1×1 convolutions + temporal readout

Convert features using timestep \(t\)

Mean \(\mu_\theta\)

Predicted image center

Variance \(\Sigma_\theta\)

Predicted uncertainty

Two interesting architectural details appear in Appendix D.

First: time-dependent readout. Instead of using modern sinusoidal timestep embeddings, the paper uses Gaussian-shaped temporal basis functions \(g_j(t)\) to combine per-pixel network outputs.

Second: structured mean and variance. The paper parameterizes the per-pixel variance with a sigmoid and constructs the reverse mean as a perturbation of the current image:

\[ \Sigma_{ii}=\operatorname{sigmoid} \left(z_i^\Sigma+\operatorname{logit}(\beta_t)\right) \]

\[ \mu_i=(x_i^{(t)}-z_i^\mu)(1-\Sigma_{ii})+z_i^\mu \]

This encourages each reverse transition to remain close to a small diffusion step.

For image experiments, the paper uses \(T=1000\) steps, except the bark dataset with \(T=500\).

arXiv+1

### Is the forward noise schedule fixed?

Not entirely. The paper explicitly states that for Gaussian diffusion:

- \(\beta_1\) is fixed to a small constant.
    
- \(\beta_2,\ldots,\beta_T\) are learned by maximizing the variational lower bound.
    
- The authors also report that a fixed schedule performed similarly in later experiments.
    

This is a notable distinction from the standard DDPM (2020) configuration.

arXiv+1

## 7. Sampling and conditional generation

Once training has finished, generating a new image requires no original image.

Start with:

\[ x^{(T)}\sim\mathcal N(0,I) \]

For \(t=T,T-1,\ldots,1\), use the learned reverse kernel to sample:

\[ x^{(t-1)} \sim p_\theta(x^{(t-1)}\mid x^{(t)}) \]

The final \(x^{(0)}\) is a generated sample.

The paper also proposes conditional sampling by multiplying the learned model distribution with an additional factor:

\[ \tilde p(x)\propto p_\theta(x)\,r(x) \]

This supports tasks such as image denoising and inpainting.

For a smooth factor \(r\), the authors derive an approximate adjustment to the reverse Gaussian mean:

\[ \boxed{ \tilde\mu_\theta \approx \mu_\theta+ \Sigma_\theta\nabla_x\log r(x)\big|_{x=\mu_\theta} } \]

Intuitively, the additional gradient pushes generated samples toward states satisfying the desired condition. This is an early foundation for later diffusion guidance ideas, although the procedures are not identical.

arXiv+1

## 8. Original DPM (2015) versus DDPM (2020)

|Aspect|DPM 2015|DDPM 2020|
|---|---|---|
|Forward process|Gaussian diffusion|Gaussian diffusion|
|Reverse distribution|Gaussian|Gaussian|
|Prediction target|Mean and covariance|Typically noise \(\epsilon\)|
|Reverse variance|Learned|Fixed in main experiments|
|\(\beta_t\) schedule|Mostly learned for Gaussian experiments|Fixed schedule|
|Architecture|MLP / multiscale CNN|U-Net|
|Training objective|Variational bound with Gaussian KL|Variational bound; simplified noise MSE|
|Conditioning|Distribution multiplication|Main paper focuses on unconditional generation|

The fundamental probabilistic framework was already established in 2015. DDPM significantly improved image generation through a different parameterization, training objective, and neural architecture.

arXiv+1

## Key things to remember

1. Forward process: progressively converts data into a simple noise distribution.
    
2. Reverse process: learns Gaussian mean and covariance for reconstructing data.
    
3. Training: maximizes a variational lower bound, chiefly by matching the known conditional forward posterior using KL divergence.
    
4. Generation: samples from a simple prior and repeatedly applies learned reverse transitions.
    
5. Original contribution: the probabilistic diffusion framework—not U-Net noise prediction or the simplified noise MSE.
    

The most valuable next question is why DDPM replaced direct Gaussian mean prediction with noise prediction, and how the original KL objective leads mathematically to the noise-prediction MSE. That is the bridge between this foundational paper and modern diffusion models.