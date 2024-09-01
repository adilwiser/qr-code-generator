from flask import Flask, render_template, request, send_from_directory
import qrcode
import os

app = Flask(__name__)

# Ensure the static/qrcodes directory exists
if not os.path.exists('static/qrcodes'):
    os.makedirs('static/qrcodes')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_qr_code():
    data = request.form.get('data')
    if data:
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')

        # Save the QR code image
        file_path = 'static/qrcodes/qr_code.png'
        img.save(file_path)

        return send_from_directory('static/qrcodes', 'qr_code.png')
    return 'No data provided', 400

if __name__ == '__main__':
    app.run(debug=True)
