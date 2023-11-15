# Hand-Sign

**THUẬT TOÁN SỬ DỤNG**
**1.2 Thuật toán phát hiện vùng bàn tay người theo thời gian thực để dịch ngôn ngữ ký hiệu **
1.2.1 Để phát hiện vùng bàn tay, ở đây ta tiến hành phân vùng ảnh chiều sâu Depth image xung quanh tâm bàn tay để xác định đối tượng theo các bước: 
Bước 1: Xác định thô vùng bàn tay, sử dụng đáng giá về tương quan khoảng cách
	Hand Ix,y = (x-x0)2+(y-y0)2 ^ (depth Ix,y-depth Ix0,y0)
Bước 2: Sử dụng OpenCV và Tensorflow để xử lí hình ảnh.
1.2.2 Chương trình này sử dụng màu sắc để phát hiện bàn tay. Do bàn tay có nhiều màu nhiều chương trình sẽ lấy nhiều màu ở những vị trí khác nhau: lòng bàn tay, ngón tay,… rồi ghép lại thành 1 hình. Để sử dụng bạn giơ bàn tay che lên tất cả các ô vuông, chương trình sẽ lấy màu từ các ô vuông đó.
Đây là ví dụ minh hoạ khi chỉ lấy 1 màu để detect màu, bàn tay sẽ rất loang lổ

![image](https://github.com/thanthienhai/Hand-Sign/assets/50171638/6f4dee84-9de2-4f99-b8ba-858b6ba0345f)

Để tiến hành nhận cử chỉ của bàn tay , trước hết cần tiến hành trích chọn đặc trưng vùng thu được ở phần phát hiện đối tượng . Các nghiên cứu trước đây cho thấy , có thể sử dụng các kỹ thuật phân tích hình dạng đối tượng như : sử dụng các dạng moment  , sử dụng bộ lọc Gabor và trích chọn PCA ( Principal Component Analysis ) , LDA ( Linear Discriminant Analysis ) hoặc sử dụng đơn thuần các kỹ thuật trích chọn đặc trưng dựa trên phân bổ mức xám  ... tuy nhiên , qua khảo sát cho thấy nếu chỉ sử dụng các đặc trưng về đường bao thì cơ bản chỉ nhận được một số cử chỉ có hình dạng tương đối tường minh . Khi kích thước bàn tay thu được nhỏ , các kẽ tay sẽ khó phân biệt , lúc này cần bổ sung thêm một số đặc trưng dạng thống kê . Vì vậy , trong nghiên cứu này sử dụng kỹ thuật xấp xỉ đa giác cho vùng đường bao và tìm bao lồi nhỏ nhất chứa vùng bàn tay , tiếp đó trích chọn các đặc trưng theo đa giác , sau đó sử dụng một dạng đặc trưng thống kế dựa trên mức độ tự tương quan về cường độ sáng và có khả năng bất biến với một số phép biến đổi hình học như xoay , tịnh tiến , co giãn . Trước hết , để phân biệt các ngón tay , ta tiến hành phân tích độ sâu các kẽ tay , đồng thời loại bỏ các kế không phù hợp về độ sâu  . Trong đó , các thao tác về xấp xỉ da giác và tìm bao lồi được nhóm tác giả sử dụng thuật toán Douglas Peucker tích hợp sẵn trong bộ thư viện OpenCV
Vùng bàn tay sau khi được chuẩn hóa kích thước thì các đặc trưng hình dạng cho bàn tay được xác định gồm các thành phần sau : f1 số lượng kẽ tay , f2 độ sâu trung bình của các kẽ tay ; f3 diện tích vùng bàn tay , f4 giá trị của tâm bàn tay ; f5 khoảng cách trung bình giữa hai kẽ tay liên tiếp ; f6 khoảng cách xa nhất giữa hai kẽ tay ; f7 số đỉnh bao lồi , f8 độ dài cạnh lớn nhất của bao lồi , f9 độ dài cạnh nhỏ nhất của bao lồi ; f10 tỷ lệ giữa chiều rộng và chiều cao của hình chữ nhật chứa vùng bàn tay . Tiếp đó , để cải thiện chất lượng nhận dạng , đặc biệt để có thể nhận dạng tốt khi bàn tay xuất hiện ở các hướng xoay khác nhau , ta bổ sung thêm đặc trưng mức độ tự tương quan HLAC ( Higher Order Local Autocorrelation ) , theo các nghiên cứu HLAC cũng có khả năng bất biến với các phép co dãn và xoay đối tượng , hơn nữa còn cho phép có thể mở rộng hơn nữa số lượng cử chỉ có thể nhận dạng .

**KẾT QUẢ CỦA THỬ NGHIỆM**
3.1 Thông tin dữ liệu huấn luyện 
![image](https://github.com/thanthienhai/Hand-Sign/assets/50171638/f0ac470d-0c0d-4f6b-9e7f-8bf67ec8cecf)

3.2 Kết quả thử nghiệm nhận dạng cử chỉ tay 
![image](https://github.com/thanthienhai/Hand-Sign/assets/50171638/e3140557-c924-4200-a7a0-ed4f7dbb25e3)

3.3 Đánh giá 
Kết quả thu được đạt xấp xỉ 86 % so với thực tế. Xong do những vấn đề khách quan như khoảng cách, ánh sáng, chất lượng camera, … ở một số trường hợp không thể nhận dạng được. 
