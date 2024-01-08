RUN:
  Step1: python3 -m venv venv
  Step2: source venv/bin/activate
  Step3: pip3 install 'qrcode[pil]' matplotlib
  Step4: python3 generate_qr_code.py
