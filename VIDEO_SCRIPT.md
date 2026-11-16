# 🎬 KỊCH BẢN QUAY VIDEO DEMO (BẢN SIÊU DỄ ĐỌC CÓ PHIÊN ÂM)
**Môn học:** Tư duy tính toán (Computational Thinking) - HCMUS  
**Bài tập:** Practice 03 — Sign-In Travel Assistant with RAG Chat  
**MSSV:** 25127344  
**Thành phố:** Hà Nội, Việt Nam  
**Thời lượng dự kiến:** ~3 phút (Tối đa 5 phút)

---

> 💡 **MẸO QUAY NHANH & TỰ TIN:**
> 1. Mỗi câu tiếng Anh đều có **dòng phiên âm tiếng Việt ngay bên dưới**, bạn chỉ cần nhìn vào dòng chữ nghiêng là đọc chuẩn, không lo bị vấp.
> 2. Mở sẵn file Notepad để copy sẵn 2 câu hỏi test dán vào cho nhanh:
>    - Câu 1: `When is the Ho Chi Minh Mausoleum open for visitors?`
>    - Câu 2: `What time does the Eiffel Tower open in Paris?`
> 3. Tốc độ đọc cứ bình tĩnh, chậm rãi, vừa nói vừa rê chuột.

---

## 📌 PHẦN 1: DEMO TRÊN WEB (Thời gian: ~1.5 phút)

### Bước 1: Giới thiệu & Đăng nhập
* **Thao tác màn hình:** Mở sẵn trang web `http://localhost:8501`, điền sẵn Email (`student25127344@gmail.com`) và Password.
* **Tiếng Anh:**
  > *"Hello instructors. My name is student 25127344. Today, I present Practice 03: Sign-In Travel Assistant with RAG Chat for Hanoi city."*
* **Phiên âm đọc:**
  > *(Hê-lô in-strắc-tơ-x. Mai nem i-x sờ-tiu-đần tu-fai-v-uăn-tu-se-vừn-thờ-ri-fo-fo. Tu-đây, ai pri-xen Prắc-tít du-ro-thờ-ri: Sai-in Tra-vồ Ớ-sít-từn uých Rát Chát fo Hà Nội si-ti.)*

* *(Bấm chuột vào nút **Sign In** để vào giao diện chính)*

* **Tiếng Anh:**
  > *"First, I sign in with Firebase Authentication. Only authenticated users can access the chat."*
* **Phiên âm đọc:**
  > *(Phớt-x-t, ai sai-in uých Phai-ơ-bây-x Ọt-then-ti-kây-sần. Ôn-li ọt-then-ti-kay-tịt du-sơ-x kèn ác-xét đơ chát.)*

---

### Bước 2: Hỏi câu có trong cẩm nang (Answerable Question)
* **Thao tác màn hình:** Copy câu này dán vào ô chat rồi ấn Enter:  
  `When is the Ho Chi Minh Mausoleum open for visitors?`
* *(Chờ bot trả lời xong, bấm mở thanh **`🔍 Retrieved Sources & Similarity Scores`** ở ngay dưới câu trả lời)*

* **Tiếng Anh:**
  > *"Next, I ask an answerable question about Ho Chi Minh Mausoleum. The assistant answers correctly and cites entry G03. Here, we can see the retrieved sources and similarity scores."*
* **Phiên âm đọc:**
  > *(Nếch-s-t, ai át-x-k ừn an-sơ-rơ-bồ quét-x-sần ơ-bao Hồ Chí Minh Mô-sô-li-ừm. Đi ớ-sít-từn an-sơ-x cơ-rếch-li èn sai-x en-tri G-di-ro-thờ-ri. Hi-ơ, uy kèn xi đơ ri-tri-v-đ sơ-xịt èn xi-mi-le-ri-ti sờ-co-x.)*

---

### Bước 3: Hỏi câu ngoài cẩm nang (Out-of-guide Question)
* **Thao tác màn hình:** Copy câu này dán vào ô chat rồi ấn Enter:  
  `What time does the Eiffel Tower open in Paris?`
* *(Chờ bot hiện câu: "I don't know based on the provided travel guide.")*

* **Tiếng Anh:**
  > *"Now, I ask an out-of-guide question about the Eiffel Tower. The assistant strictly says 'I don't know based on the provided travel guide' to prevent hallucination."*
* **Phiên âm đọc:**
  > *(Nao, ai át-x-k ừn ao-ộp-gai quét-x-sần ơ-bao đi Ai-phơn Tao-uơ. Đi ớ-sít-từn sờ-trích-li sây: 'Ai đơn-t nô bây-x-t on đơ prơ-vai-địt tra-vồ gai' tu pri-ven ha-lu-xi-nây-sần.)*

---

### Bước 4: Đăng xuất (Sign out)
* **Thao tác màn hình:** Bấm vào nút đỏ **`🚪 Sign Out`** ở thanh menu bên trái.

* **Tiếng Anh:**
  > *"Finally, I click Sign Out. The session is closed and chat history is completely cleared."*
* **Phiên âm đọc:**
  > *(Phai-nờ-li, ai cờ-líc Sai-ao-t. Đơ se-sần i-x cờ-lô-x-t èn chát hít-xtơ-ri i-x com-lít-li cli-ơ-đ.)*

---

## 📌 PHẦN 2: TƯ DUY TÍNH TOÁN (Thời gian: ~1.5 phút)
*(Chuyển màn hình sang file **`README.md`**, từ từ cuộn chuột theo 4 mục)*

### 1. Abstraction (Trừu tượng hóa)
* **Thao tác:** Cuộn chuột đến mục **5.1. Abstraction**.
* **Tiếng Anh:**
  > *"For Abstraction: The inputs are user query and credentials. The output is the verified answer with citation. In the guide, we keep ID, title, category, tags, verified text, and source."*
* **Phiên âm đọc:**
  > *(Fo Áp-x-trắc-sần: Đi in-pụt-x a du-sơ cue-ri èn cơ-re-đen-sồ-x. Đi ao-pụt i-x đơ ve-ri-phai-đ an-sơ uých sai-tay-sần. In đơ gai, uy kíp Ai-Đi, tai-tồ, ca-tê-gô-ri, tác-x, ve-ri-phai-đ tếch-x-t, èn sơ-x.)*

---

### 2. Decomposition (Phân rã)
* **Thao tác:** Cuộn chuột đến sơ đồ 7 khối ở mục **5.2. Decomposition**.
* **Tiếng Anh:**
  > *"For Decomposition: The system is split into seven steps: Authentication, Guide Embedding, Query Embedding, Cosine Retrieval, Context Building, Qwen3 generation, and UI Display."*
* **Phiên âm đọc:**
  > *(Fo Đi-com-pơ-di-sần: Đơ sít-x-từm i-x sờ-pơ-lít in-tu se-vừn sờ-tép-x: Ọt-then-ti-kây-sần, Gai Em-bét-đinh, Cue-ri Em-bét-đinh, Cô-sai-n Ri-tri-vồ, Con-tếch-x-t Bưu-đinh, Qwen-thờ-ri dze-nơ-ray-sần, èn Du-Ai Đít-x-pơ-lay.)*

---

### 3. Pattern Recognition (Nhận diện mẫu)
* **Thao tác:** Cuộn chuột đến mục **5.3. Pattern Recognition**.
* **Tiếng Anh:**
  > *"For Pattern Recognition: We reused Firebase auth and Ollama REST calls. The Filter-Score-TopK pattern is used here for cosine retrieval and will be reused for travel recommendation."*
* **Phiên âm đọc:**
  > *(Fo Pát-tơn Re-cốc-ni-sần: Uy ri-du-x-t Phai-ơ-bây-x ọt èn Ô-la-ma Rét-x-t co-x. Đơ Phiu-tơ-Sờ-co-Top-K pát-tơn i-x du-x-t hi-ơ fo cô-sai-n ri-tri-vồ èn uých bi ri-du-x-t fo tra-vồ re-cô-men-đây-sần.)*

---

### 4. Algorithm Design (Thiết kế thuật toán)
* **Thao tác:** Cuộn chuột đến đoạn mã giả ở mục **5.4. Algorithm Design**.
* **Tiếng Anh:**
  > *"For Algorithm Design: We select Top 3 with cosine similarity. We use two layers: score below 0.35 is rejected instantly, and unknown items are rejected by prompt constraint."*
* **Phiên âm đọc:**
  > *(Fo An-gô-ri-đừm Đi-zai: Uy si-lếch Top Thờ-ri uých cô-sai-n xi-mi-le-ri-ti. Uy du-x tu lay-ơ-x: sờ-co bi-lô di-ro-poynt-thờ-ri-fai-v i-x ri-dếch-tịt in-xtừn-t-li, èn ân-nôn ai-tầm-x a ri-dếch-tịt bai prọm-p-t cơn-sờ-tren-t.)*

---

## 📌 PHẦN 3: KẾT QUẢ & KẾT THÚC (~30 giây)

### Test Results (Kết quả kiểm thử)
* **Thao tác:** Cuộn chuột lên bảng **4. Test Table**.
* **Tiếng Anh:**
  > *"In our test table, all six queries passed. A successful case is Question 1 with score 0.6489. An unlisted case is Question 6, which correctly returned 'I don't know'."*
* **Phiên âm đọc:**
  > *(In ao-uơ test tay-bồ, ô-l sít-x cue-ri-x pát-x-t. Ờ sắc-xét-x-phun cây-x i-x Quét-x-sần Uăn uých sờ-co di-ro-poynt-síc-fo-ết-nai. Ừn ơn-lít-x-tịt cây-x i-x Quét-x-sần Síc-x, uých cơ-rếch-li ri-tơn-d 'Ai đơn-t nô'.)*

---

### Lời kết
* **Tiếng Anh:**
  > *"Thank you for watching!"*
* **Phiên âm đọc:**
  > *(Thanh-kiu fo uót-chinh!)*

---

## 📱 BẢN TÓM TẮT DỊCH NGHĨA TIẾNG VIỆT
1. **Chào & Đăng nhập:** Chào thầy cô, em là sinh viên 25127344. Hôm nay em trình bày Lab 03 cho TP Hà Nội. Đầu tiên em đăng nhập bằng Firebase. Chỉ người dùng đã xác thực mới vào được bot.
2. **Hỏi câu có trong bài:** Tiếp theo, em hỏi câu về Lăng Bác. Bot trả lời chính xác và trích dẫn mã G03. Khung bên dưới hiển thị nguồn và điểm tương đồng cosine.
3. **Hỏi câu ngoài bài:** Bây giờ em hỏi về tháp Eiffel. Bot từ chối trả lời bằng câu "I don't know..." để chống bịa đặt (hallucination).
4. **Đăng xuất:** Cuối cùng em đăng xuất, phiên kết thúc và lịch sử trò chuyện được xóa hoàn toàn.
5. **Trừu tượng hóa:** Input là câu hỏi và tài khoản; Output là câu trả lời có trích dẫn. Giữ lại các trường quan trọng trong cẩm nang.
6. **Phân rã:** Hệ thống chia làm 7 bước từ đăng nhập, nhúng, truy xuất, đến sinh văn bản.
7. **Nhận diện mẫu:** Tái sử dụng Firebase, Ollama và mô hình Lọc - Chấm điểm - Chọn Top K.
8. **Thuật toán:** Lấy Top 3, hàng rào 2 lớp (điểm < 0.35 từ chối ngay, không có dữ liệu thì prompt từ chối).
9. **Kết quả:** Cả 6 câu hỏi đều đạt, câu 1 đạt điểm 0.6489, câu 6 từ chối chính xác.
10. **Lời kết:** Cảm ơn thầy cô đã theo dõi!
