from alipay import AliPay

alipay_public_key_string="""-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvIpEqSdDNQiW3qIgwoAqIOxuEEKBYK4dioMkWUj7WWMP4Wozlmxlzvt9Xtq77GwcSD7FCJZPqqqvT+vmRtpmVvUvDRk7fOfFMQHNShOBBIQuWBIUL+rjQ+VJXPbYgu+6yJVS4xd+sqHZsPw2/DI5xinHMsUdPdi3kyyYR8qI9vEdjKBM9aC1FcjF1yG7fnE/z5z4okHSzM99lq+zTphOeWepu3ilrV/Dqm6J4Grm4NoGkXjkGRe/yVgiUx84Fv2Dk2Jyy8P53PrUK5Jll4fcf/4ENlQ5czdbqjva12IyDqCPHg9RwhbzpKHKYfK8nvz+oTQawrIg4abqH1ai3pLWVwIDAQAB
-----END PUBLIC KEY-----"""

alipay_private_key_string="""-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAvIpEqSdDNQiW3qIgwoAqIOxuEEKBYK4dioMkWUj7WWMP4Wozlmxlzvt9Xtq77GwcSD7FCJZPqqqvT+vmRtpmVvUvDRk7fOfFMQHNShOBBIQuWBIUL+rjQ+VJXPbYgu+6yJVS4xd+sqHZsPw2/DI5xinHMsUdPdi3kyyYR8qI9vEdjKBM9aC1FcjF1yG7fnE/z5z4okHSzM99lq+zTphOeWepu3ilrV/Dqm6J4Grm4NoGkXjkGRe/yVgiUx84Fv2Dk2Jyy8P53PrUK5Jll4fcf/4ENlQ5czdbqjva12IyDqCPHg9RwhbzpKHKYfK8nvz+oTQawrIg4abqH1ai3pLWVwIDAQABAoIBAQCCw6tnXpHgYHqzIuNxww51E0YrBNVSxrA6d0ZonpOlpW1IPC5XcAsUiZykgzS/fyQGf3KMyCOtDQDWf5iRH7zHJvphLVTzBpTfro5BiFF9Xmf+MVvK+DBz0L0XOyVjev2jTN3WH1+CaXrgo61HMVacuDEuZ0Qmtv5rlwxvDmv8SIHIbz2+L2F0Hc9mE6QnXph5LEA3ZmyI/Gyc6NVoWNM7Tdx5Gkh/dIoobnwX9Psc+afjiGBUw1BKJWCx3UPHFt6nW6m4N3sYYbumlN9Q1L0emrBvRa5MYTZYx8pxiNn9N2Mdsn1X68KDsY8o6Wi1YhOQsAilnM00sL2RKii5SlKBAoGBAOaauZb+HTqkSR2wYzJOZQWRCLcrBYlgpKzLMGJczHUOv/ka164m0PGNt/7buYoHknNbSOB4vQ5VyP5kJroHdXBzBDJL1D39MeBeboZ9DdmEb7jH2k3+mGl/ii4sFzdkxNLYJ2sU52tZydC+vPgiJ94J93fekDEbU+UFBrfeuFx3AoGBANFNpzD8Vu5AtOHywSL4oqCL7+d3oEpILEVcJKkf8bL7j94YaEbZYJKIK1aAoETbPDdHQzKgDVkCKjtECaNxwEujJ32tCuVFSAufijqxm3GiSeSZ+knK1t5JHiFEmgt4HpMvyQrx2HsPYT8RJ/LVx+6BkSHfrNGcueTR/3s9Yi0hAoGAB9qNJ49P/4dI1jIDrtrspdviqBpW/e7ErP3ej/sJG5N9BkbbwZqg0xk4gv2IvCK14ifhu4NhLPPO/Jr8lqlaXpIMOopKmDHfWPzeVsY7ioTwKSLlVHKvTiiB1EC8Ka7M5UFnVkZH+2f7b5iPZwQCx5UfUH3L+2Aq40ngiLKVJNECgYAVgMHVgYc40QMEV5lKC3tBvT63bA3Ws9WAhrfpfDOrrLaaHa3Q4ZJPW5gAOhS9HjzwfOzFbbYRV+yYzCOlXBFic++htL5y0YxWTVy5LPgIU6D90GfrXuB2U9K5nj+pP/z8KCOicThJZEocXZnaE+aHdV5AuacandxnSr/RnHvSoQKBgQDgnrk+CvzfNnX/e23dNzY5bbZBlWo7o+wL+/VGa1CHDx08QO+cYviSqqg0oAizNj+3rvEnetXelV7fqck9FC+3mo1mg99G9WBq8Q0aAHRcH0DS+fzO051nogOaKlCqBOoPx7LlavpzW+iRsWhpVADA2SslDT2wI8r1ZR/zyGSnjA==
-----END RSA PRIVATE KEY-----"""

alipay=AliPay(
    appid="2016101200667731",
    app_notify_url=None,
    app_private_key_string=alipay_private_key_string,
    alipay_public_key_string=alipay_public_key_string,
    sign_type="RSA2"
)

order_string=alipay.api_alipay_trade_page_pay(
    out_trade_no='1000000001',
    total_amount=str(10001),
    subject="py交易",
    return_url=None,
    notify_url=None
)

result="https://openapi.alipaydev.com/gateway.do?"+order_string
print(result)