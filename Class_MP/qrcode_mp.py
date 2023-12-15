from qrcode.main import QRCode

qr = QRCode(version=3, box_size=20, border=2)

qr.add_data("00020101021243650016com.mercadolibre020130636d9a26148-00fc-48db-a090-51a9b19f9f465011000711111115204970053030325802AR5909Test Test6004CABA63047859")
qr.make(fit=True)

img = qr.make_image(fill_color=(0, 0, 0), back_color=(255, 255, 255))
img.save("Scan.png")
img.show()