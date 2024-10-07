const textAreaData = document.getElementById('qr-code-text');
const qrCodeImage = document.getElementById('qr-code-image');
const qrCodeColor = document.getElementById('qr-code-color');
const qrCodeWidth = document.getElementById('qr-code-width');
const qrCodeHeight = document.getElementById('qr-code-height');
const qrCodeBackgroundColor = document.getElementById('qr-code-background-color');
const qrCodeColorCornerSquare = document.getElementById('qr-code-color-corner-square');

const downloadSVG = document.getElementById('generate-qr-code-svg');
const downloadPNG = document.getElementById('generate-qr-code-png');

const data = textAreaData.value;
const color = qrCodeColor.value;
const width = qrCodeWidth.value;
const height = qrCodeHeight.value;
const cornerSquareColor = qrCodeColorCornerSquare.value;
const backgroundColor = qrCodeBackgroundColor.value;

const qrCode = new QRCodeStyling({
    width: height,
    height: width,
    type: "svg",
    data: data,
    dotsOptions: {
        color: color,
        type: "rounded"
    },
    backgroundOptions: {
        color: backgroundColor,
    },
    imageOptions: {
        margin: 20,
    }
});

qrCode.append(document.getElementById("qr-display"));

const events = [
    { element: textAreaData, event: 'input', property: 'data' },
    { element: qrCodeWidth, event: 'input', property: 'width' },
    { element: qrCodeHeight, event: 'input', property: 'height' },
    { element: qrCodeColor, event: 'input', property: 'dotsOptions.color' },
    { element: qrCodeImage, event: 'input', property: 'image', isFile: true },
    { element: qrCodeBackgroundColor, event: 'input', property: 'backgroundOptions.color' },
    { element: qrCodeColorCornerSquare, event: 'input', property: 'cornersSquareOptions.color' },
];

function updateQRCode(property, value) {
    const updateData = {};
    const keys = property.split('.');
    if (keys.length > 1) {
        updateData[keys[0]] = { [keys[1]]: value };
    } else {
        updateData[property] = value;
    }
    qrCode.update(updateData);
}

events.forEach(({ element, event, property, isFile }) => {
    element.addEventListener(event, () => {
        if (isFile) {
            const reader = new FileReader();
            reader.onload = function(e) {
                updateQRCode(property, e.target.result);
            }
            reader.readAsDataURL(element.files[0]);
        } else {
            updateQRCode(property, element.value);
        }
    });
});

downloadSVG.addEventListener('click', () => {
    qrCode.download({ extension: "svg" });
});

downloadPNG.addEventListener('click', () => {
    qrCode.download({ extension: "png" });
});

document.getElementById('create-payment-qr-code').addEventListener('click', function() {
    const form = document.getElementById('payment-form');
    if (form.checkValidity()) {
        const iban = document.getElementById('iban').value;
        const name = document.getElementById('name').value;
        const bic = document.getElementById('bic').value;
        const amount = document.getElementById('amount').value;
        const communication = document.getElementById('communication').value;

        textAreaData.value = `BCD\n002\n1\nSCT\n${bic}\n${name}\n${iban}\nEUR${amount}\n\n\n${communication}\nGénéré par carpestudentem.be`;
        // Close the modal
        document.getElementById('payment-close-modal').click();
        textAreaData.dispatchEvent(new Event('input'));
    } else {
        form.reportValidity();
    }
});