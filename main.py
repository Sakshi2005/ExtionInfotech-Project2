from flask import Flask, request, jsonify
import os
from cryptography.x509 import Name, NameAttribute
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import datetime
import cryptography.x509 as x509

# Function to generate self-signed certificate
def generate_self_signed_cert(cert_file="cert.pem", key_file="key.pem"):
    # Generate RSA private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    
    # Generate public key
    public_key = private_key.public_key()

    # Create a self-signed certificate
    subject = issuer = Name([NameAttribute(NameOID.COUNTRY_NAME, u"US"),
                             NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
                             NameAttribute(NameOID.LOCALITY_NAME, u"San Francisco"),
                             NameAttribute(NameOID.ORGANIZATION_NAME, u"My Organization"),
                             NameAttribute(NameOID.COMMON_NAME, u"localhost")])

    cert = x509.CertificateBuilder().subject_name(subject) \
        .issuer_name(issuer) \
        .public_key(public_key) \
        .serial_number(x509.random_serial_number()) \
        .not_valid_before(datetime.datetime.utcnow()) \
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365)) \
        .add_extension(
            x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
            critical=False,
        ) \
        .sign(private_key, hashes.SHA256())

    # Write private key to file
    with open(key_file, "wb") as key:
        key.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # Write certificate to file
    with open(cert_file, "wb") as cert_out:
        cert_out.write(cert.public_bytes(serialization.Encoding.PEM))

    print(f"Self-signed certificate generated: {cert_file}, {key_file}")

# Flask application setup
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Quantum Model Training API!"})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    # Add your prediction logic here (e.g., load the model and predict)
    prediction = {"result": "This is a dummy prediction!"}
    return jsonify(prediction)

if __name__ == "__main__":
    # Generate certificates if they don't exist
    if not os.path.exists("cert.pem") or not os.path.exists("key.pem"):
        generate_self_signed_cert()

    # Running the Flask app with SSL context
    app.run(ssl_context=('cert.pem', 'key.pem'), host='0.0.0.0', port=5000)
