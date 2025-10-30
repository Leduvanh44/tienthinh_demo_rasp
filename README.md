Tổng quan dây chuyền cần giám sát: 
Dây chuyền sản xuất dây đồng tráng men bao gồm bốn hệ thống chính, mỗi hệ thống đảm nhiệm một vai trò quan trọng nhằm đảm bảo chất lượng và hiệu suất sản xuất tối ưu. Cụ thể, các hệ thống đó bao gồm: hệ thống đo đường kính dây, hệ thống gia nhiệt và tráng men, hệ thống soi lỗ kim, và hệ thống cuộn dây tự động.
Hệ thống đo đường kính dây là bước đầu tiên trong quy trình. Mục tiêu của hệ thống này là kiểm tra và giám sát đường kính của dây đồng trong suốt quá trình kéo dây. Bằng cách sử dụng các thiết bị đo chuyên dụng (có thể hỗ trợ tối đa đến 32 line đo đồng thời), hệ thống giúp xác định xem đường kính dây có nằm trong giới hạn sai số cho phép hay không. Việc kiểm soát đường kính dây ngay từ đầu không chỉ giúp đảm bảo chất lượng sản phẩm mà còn giúp giảm thiểu hao hụt nguyên vật liệu và thời gian phải điều chỉnh lại thiết bị. Dữ liệu từ máy đo đường kính sẽ được truyền tới màn hình HMI để hiển thị và ghi nhận, giúp người vận hành dễ dàng theo dõi và điều chỉnh khi cần thiết.
Tiếp theo là hệ thống gia nhiệt và tráng men, đóng vai trò then chốt trong việc tạo ra lớp cách điện hoàn hảo cho dây đồng. Hệ thống này bao gồm bốn bộ điều khiển nhiệt điện trở để gia nhiệt dây đồng trước khi tráng men, đảm bảo nhiệt độ phù hợp giúp lớp men bám chắc và đều trên bề mặt dây. Bên cạnh đó, còn có một bộ điều khiển nhiệt độ riêng biệt dùng để theo dõi nhiệt độ tổng thể trong khu vực gia nhiệt, từ đó đảm bảo tính ổn định và an toàn trong suốt quá trình vận hành. Ngoài ra, năm biến tần cũng được tích hợp để điều khiển tốc độ của các quạt làm mát và các động cơ kéo dây, nhằm tối ưu hóa hiệu quả truyền nhiệt và điều chỉnh tốc độ phù hợp với từng công đoạn.
Sau khi dây đã được tráng men, hệ thống soi lỗ kim sẽ tiếp tục kiểm tra lớp cách điện nhằm phát hiện những lỗi vi mô như các lỗ kim nhỏ li ti mà mắt thường không thể nhận biết được. Những lỗ kim này, nếu không được phát hiện kịp thời, có thể dẫn đến hiện tượng chập điện hoặc phóng điện trong quá trình sử dụng sản phẩm thực tế, gây ảnh hưởng nghiêm trọng đến độ an toàn và độ bền của thiết bị điện. Hệ thống soi lỗ kim bao gồm một máy soi chuyên dụng được kết nối với máy tính điều khiển, nơi chạy phần mềm giám sát và xử lý tín hiệu. Hệ thống này hoạt động với độ chính xác cao, cho phép đánh giá chất lượng lớp cách điện một cách chi tiết và đáng tin cậy.
Cuối cùng, dây đồng sau khi đã được kiểm tra kỹ lưỡng sẽ được đưa đến hệ thống cuộn dây tự động. Tại đây, dây được cuộn lại thành các cuộn gọn gàng và đồng đều, sẵn sàng cho khâu đóng gói và vận chuyển. Hệ thống cuộn dây được thiết kế để hoạt động liên tục và đồng bộ với các hệ thống phía trước, giúp đảm bảo không bị gián đoạn trong chuỗi sản xuất.
Toàn bộ dây chuyền được giám sát và điều khiển thông qua các thiết bị đo lường, giao tiếp HMI và phần mềm chuyên dụng, giúp nâng cao khả năng quản lý dữ liệu, phát hiện sớm lỗi kỹ thuật, đồng thời tạo điều kiện thuận lợi cho việc phân tích và tối ưu hóa quy trình vận hành. Nhờ sự kết hợp chặt chẽ giữa các hệ thống, dây chuyền không chỉ đảm bảo chất lượng sản phẩm đầu ra mà còn nâng cao hiệu suất sản xuất, giảm thiểu rủi ro và chi phí bảo trì. Các thành phần cần theo dõi dữ liệu như sau:
Hệ thống đo đường kính dây:
-	Máy đo đường kính dây (tối đa 32 line).
-	HMI truyền thông với máy đo đường kính dây. 
Hệ thống gia nhiệt và tráng men:
-	5 bộ điều khiển nhiệt độ gồm 4 bộ điều khiển nhiệt điện trở nhằm gia nhiệt dây đồng và 1 bộ để theo dõi nhiệt độ.
-	5 biến tần điều khiển các quạt và động cơ.  
Hệ thống máy soi lỗ kim:
-	Máy soi lỗ kim
-	Máy tính chạy phần mềm điều khiển hệ thống soi lỗ kim.
  Hình ảnh
Sơ đồ nguyên lý; 
  Hệ thống gồm một bộ thu thập dữ liệu và các thiết bị cần giám sát. Bộ thu thập dữ liệu sử dụng Raspberry Pi 3 B+ đóng vai trò là thiết bị trung tâm để thu thập dữ liệu từ các thiết bị công nghiệp. Pi kết nối với các thiết bị sử dụng giao tiếp RS-485 thông qua các cổng chuyển đổi, đồng thời liên kết với các thiết bị HMI và PC thông qua switch Ethernet.
Raspberry Pi sử dụng giao thức MQTT – một giao thức nhẹ, hiệu quả cao cho IoT – để truyền dữ liệu thu thập được tới MQTT Broker, từ đó đưa về server để phân tích và hiển thị trên giao diện người dùng. Hệ thống MQTT giúp đảm bảo dữ liệu được cập nhật liên tục, thời gian thực, trong khi vẫn giảm thiểu độ trễ và băng thông sử dụng.
Server tiếp nhận dữ liệu từ MQTT Broker thông qua thư viện MQTTnet, lưu trữ vào cơ sở dữ liệu và cung cấp các API để hiển thị thông tin trên giao diện người dùng. Người quản lý có thể truy cập hệ thống từ xa để giám sát, cảnh báo và trích xuất báo cáo mọi lúc mọi nơi thông qua trình duyệt web trên máy tính hoặc điện thoại.
Cơ chế thu thập và xử lý dữ liệu
Trong hệ thống giám sát và truyền thông được nghiên cứu, quá trình thu thập và xử lý dữ liệu được thực hiện thông qua bốn luồng chính: Modbus RTU, Modbus TCP (Ethernet), PC-Ethernet và MQTT. Mỗi luồng đảm nhiệm một vai trò riêng biệt trong chu trình thu thập, đồng bộ hóa, phân tích và truyền tải dữ liệu, tạo nên một hệ thống hoạt động nhịp nhàng và hiệu quả. Để đảm bảo tính nhất quán và an toàn trong quá trình truy cập dữ liệu đa luồng, tất cả dữ liệu trung gian được lưu trữ và chia sẻ thông qua cơ chế khóa luồng (ThreadingLock), giúp ngăn chặn các xung đột không mong muốn trong quá trình đọc/ghi dữ liệu.
•	Modbus RTU và Modbus Ethernet
Hai luồng này đóng vai trò quan trọng trong việc thu thập dữ liệu trực tiếp từ các thiết bị hiện trường như bộ điều khiển lập trình (PLC), cảm biến, hoặc các thiết bị đo lường khác, thông qua giao thức Modbus – một giao thức phổ biến trong lĩnh vực công nghiệp. Cụ thể:
Modbus RTU: Sử dụng phương thức giao tiếp nối tiếp (serial communication) qua chuẩn RS-485, phù hợp với các hệ thống yêu cầu truyền tải dữ liệu ổn định ở khoảng cách xa. Sau khi thiết lập kết nối với thiết bị, hệ thống sẽ truy vấn các thanh ghi (register) để thu thập các giá trị giám sát, bao gồm điểm đặt (setpoint), giá trị hiện tại, cảnh báo (alarm), ngưỡng tối thiểu/tối đa (min/max threshold), và các thông số liên quan khác.
Modbus Ethernet: Hoạt động trên nền giao thức TCP/IP, cho phép truyền tải dữ liệu nhanh chóng và linh hoạt qua mạng Ethernet, thường được áp dụng trong các hệ thống hiện đại có cơ sở hạ tầng mạng phát triển. Tương tự như Modbus RTU, sau khi kết nối thành công, luồng này cũng truy vấn các thanh ghi để lấy dữ liệu từ thiết bị.
Hệ thống được thiết kế với khả năng xử lý lỗi linh hoạt, đảm bảo tính ổn định trong các tình huống bất thường:
•	Lỗi Timeout: Nếu thiết bị không phản hồi trong khoảng thời gian quy định, hệ thống sẽ gán giá trị -1 cho các biến tương ứng, đồng thời ghi nhận sự cố để xử lý sau.
•	Lỗi từ thiết bị: Trong trường hợp thiết bị phản hồi nhưng trả về mã lỗi Modbus, hệ thống sẽ ghi lại lỗi dưới dạng E{mã lỗi} vào nhật ký, giúp người vận hành dễ dàng tra cứu và khắc phục.
•	Không có lỗi: Nếu dữ liệu được thu thập thành công, hệ thống sẽ sử dụng các giá trị này để tính toán trạng thái hoạt động hoặc hiệu suất của thiết bị, sau đó lưu trữ dữ liệu vào cơ chế ThreadingLock để đồng bộ hóa với các luồng khác.
•	PC-Ethernet
Luồng PC-Ethernet chịu trách nhiệm truy vấn dữ liệu từ cơ sở dữ liệu SQL của các phần mềm bên thứ ba. Đây là một luồng quan trọng trong việc tích hợp dữ liệu từ các hệ thống bên ngoài vào hệ thống giám sát tổng thể.
Quy trình hoạt động của luồng này bao gồm:
•	Thiết lập kết nối với cơ sở dữ liệu SQL của phần mềm bên thứ ba. Trong một số trường hợp, cơ sở dữ liệu này được lưu trữ dưới dạng file .db và excel trên PC chứa phần mềm bên thứ ba. Khi đó, luồng PC-Ethernet sử dụng giao thức SMB (Server Message Block) để kết nối tới thư mục chia sẻ và truy xuất trực tiếp file cơ sở dữ liệu từ xa. Việc thiết lập bao gồm xác thực tài khoản truy cập (username/password), ánh xạ ổ đĩa tới đường dẫn /mnt/pcshare trên máy tính nhúng. 
•	Truy vấn các giá trị giám sát cần thiết thông qua truy vấn SQL trực tiếp lên file .db sau khi kết nối SMB được thiết lập thành công.
•	Đồng bộ hóa và lưu trữ dữ liệu vào ThreadingLock để đảm bảo dữ liệu từ PC-Ethernet được tích hợp liền mạch với các luồng dữ liệu khác trong hệ thống.
Luồng này cũng được trang bị các cơ chế xử lý lỗi để đảm bảo tính liên tục, chẳng hạn như ghi nhận và xử lý các trường hợp mất kết nối SMB, lỗi xác thực, hoặc lỗi truy vấn SQL. Các biện pháp này góp phần giảm thiểu nguy cơ gián đoạn trong quá trình giám sát và đảm bảo hệ thống vận hành ổn định trong môi trường công nghiệp.
•	MQTT
Luồng MQTT đóng vai trò quan trọng trong việc truyền tải dữ liệu đã xử lý đến các nền tảng đám mây hoặc hệ thống giám sát trung tâm, đảm bảo thông tin được cập nhật liên tục và có thể truy cập từ xa. Quy trình hoạt động của luồng này như sau:
•	Dữ liệu từ ThreadingLock được xử lý và đóng gói dưới định dạng JSON – một định dạng nhẹ và phổ biến, phù hợp cho việc truyền tải dữ liệu qua mạng.
•	Hệ thống sử dụng giao thức MQTT (Message Queuing Telemetry Transport), một giao thức truyền thông nhẹ, lý tưởng cho các ứng dụng IoT và giám sát từ xa.
•	Dữ liệu JSON được xuất bản (publish) lên các chủ đề (topic) trên MQTT broker để các hệ thống khác có thể truy cập.
Để đảm bảo tính ổn định trong quá trình truyền tải, hệ thống áp dụng cơ chế thử lại (retry mechanism):
•	Nếu kết nối với MQTT broker không thành công, hệ thống sẽ thử lại tối đa 5 lần.
•	Nếu việc xuất bản dữ liệu lên topic thất bại, hệ thống sẽ thử lại tối đa 3 lần.
•	Trong trường hợp thất bại hoàn toàn, một bản sao của dữ liệu JSON cùng với trạng thái của nó sẽ được lưu trữ cục bộ, giúp ngăn chặn việc mất dữ liệu và đảm bảo tính toàn vẹn của thông tin.
Tất cả các luồng trong hệ thống đều sử dụng cơ chế ThreadingLock để đồng bộ hóa việc truy cập dữ liệu đa luồng, tránh các xung đột có thể xảy ra trong quá trình đọc/ghi dữ liệu. Điều này đặc biệt quan trọng trong một hệ thống phức tạp với nhiều luồng hoạt động đồng thời, giúp đảm bảo rằng dữ liệu luôn được xử lý một cách nhất quán và chính xác.
Bên cạnh đó, hệ thống được trang bị các cơ chế xử lý lỗi toàn diện tại từng luồng, cho phép:
•	Phát hiện và ghi nhận các lỗi kết nối, chẳng hạn như mất kết nối với thiết bị hoặc cơ sở dữ liệu.
•	Xử lý các lỗi phản hồi từ giao thức Modbus, đảm bảo hệ thống không bị gián đoạn bởi các sự cố từ thiết bị.
•	Quản lý các lỗi ứng dụng, giúp tăng cường độ tin cậy và khả năng phục hồi của hệ thống giám sát.
Sơ đồ biểu diễn cơ thế thu thập dữ liệu của Raspberry Pi (các luồng chính).
Chi tiết giao diện phâhnf mềm ở đười link github sau: https://github.com/Leduvanh44/tienthinh_demo.git
