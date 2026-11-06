
> Q1: Tại sao model dự đoán noise \(\epsilon\) thay vì trực tiếp dự đoán ảnh gốc \(x_0\)?
- Noise có phân phối đơn giản Normal distribution, trong khi X_0 có phân phối phức tạp -- Việc predict noise cung cấp một mục tiêu được chuẩn hóa và thuận tiện cho optimization, mặc dù bản thân việc dự đoán noise vẫn phụ thuộc vào cấu trúc dữ liệu.
- Score Matching: \[
\nabla_{x_t}\log q(x_t|x_0)
=
-\frac{\epsilon}{\sqrt{1-\bar\alpha_t}}
\]

Khi dự đoán noise model cũng sẽ học được thông tin về score (gradient của log-density)



> Q2: Tại sao phải khôi phục qua nhiều bước \(x_T \rightarrow x_{T-1}\rightarrow \cdots \rightarrow x_0\), thay vì sinh ảnh trong một bước?
Vấn đề: Từ một ảnh nhiễu thuần túy, có vô số ảnh chó hợp lệ có thể được sinh ra.

Nếu training model bằng MSE để predict trực tiếp \(x_0\) từ nhiễu thuần túy, nghiệm tối ưu là:
\[
f_\theta^*(x_T)=\mathbb E[x_0|x_T]
\]
Khi \(x_T\) gần như độc lập với \(x_0\):
\[
\mathbb E[x_0|x_T]\approx\mathbb E[x_0]
\]
Tức là model có xu hướng dự đoán ảnh trung bình của dataset, thay vì tạo ra một mẫu ảnh cụ thể.

Kết quả dễ bị mờ hoặc thiếu cấu trúc rõ ràng.

Còn làm từng bước thì sao?
DDPM học reverse transition:
\[
p_\theta(x_{t-1}|x_t)
\]
Mỗi bước chỉ cần thực hiện một thay đổi tương đối nhỏ đối với trạng thái hiện tại.

Quá trình reverse còn có thành phần stochastic, cho phép sinh các mẫu khác nhau từ phân phối dữ liệu.