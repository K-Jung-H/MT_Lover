import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailSender:
    def __init__(self, username, password):
        # SMTP 서버 연결에 필요한 정보 초기화
        self.host = "smtp.gmail.com"        # SMTP 서버의 호스트 주소
        self.port = 587         # SMTP 서버의 포트 번호
        self.username = username # SMTP 서버 로그인 사용자 이름
        self.password = password # SMTP 서버 로그인 비밀번호

    def send_email(self, subject, sender, recipient, plain_text_message):
        """
        지정된 제목, 발신자, 수신자 및 텍스트 메시지를 포함하여 이메일을 전송합니다.
        """
        # 이메일 메시지 객체 생성
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject       # 이메일 제목 설정
        msg['From'] = sender           # 발신자 설정
        msg['To'] = recipient          # 수신자 설정

        # 이메일 본문 내용을 텍스트로 설정
        msg_part = MIMEText(plain_text_message, 'plain')

        # 메시지 객체에 본문 내용 첨부
        msg.attach(msg_part)

        # SMTP 서버에 연결하고 이메일 전송
        with smtplib.SMTP(self.host, self.port) as server:
            server.ehlo()              # 서버 연결 확인
            server.starttls()          # TLS(Transport Layer Security) 모드로 전환
            server.ehlo()              # TLS 모드 연결 확인
            server.login(self.username, self.password) # SMTP 서버 로그인
            server.sendmail(sender, recipient, msg.as_string()) # 이메일 전송

        print("Mail sending complete!")

# 사용 예시:
# email_sender = EmailSender(host="smtp.gmail.com", port=587, username="your_username", password="your_password")
# email_sender.send_email(
#     subject="Mountain Information",
#     sender="your_email@gmail.com",
#     recipient="recipient_email@gmail.com",
#     plain_text_message="Here is the mountain information you requested:\nMountain 1\nMountain 2"
# )


email_sender = EmailSender(username="jay81385136@gmail.com", password="vmkw shgc jzmw fkoz")
email_sender.send_email(
    subject="Mountain Information",
    sender="jay81385136@gmail.com",
    recipient="jay81385136@gmail.com",
    plain_text_message="줄바꿈 \n 알아서\n 해줘야 함"

)

#vmkw shgc jzmw fkoz

