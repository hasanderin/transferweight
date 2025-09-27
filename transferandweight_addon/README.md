# Transfer and Weight Management

Odoo 13 için geliştirilmiş ağırlık hesaplama ve araç yönetimi addon'u.

## Özellikler

### Ağırlık Hesaplama
- Satış siparişi satırlarında ürün ağırlığı × miktar hesaplaması
- Sipariş toplam ağırlık hesaplaması
- Otomatik ağırlık güncellemeleri

### Araç Yönetimi
- Araç tanımlama (isim, plaka, kapasite)
- Araç statü takibi (boşta, yolda, tamamlandı, bakım)
- Şoför bilgileri
- Kapasite kullanım oranı hesaplaması

### Sipariş-Araç Ataması
- Otomatik araç atama (kapasiteye göre)
- Manuel araç atama
- Kapasite kontrolü ve validasyonu
- Teslimat takibi

### Raporlama
- Ağırlık raporları
- Araç kullanım raporları
- Sipariş durumu raporları

## Kurulum

1. Addon'u Odoo addons dizinine kopyalayın
2. Odoo'yu yeniden başlatın
3. Apps menüsünden "Transfer and Weight Management" modülünü yükleyin

## Kullanım

### Araç Tanımlama
1. Transfer & Weight > Vehicle Management > Vehicles menüsüne gidin
2. Yeni araç oluşturun
3. Araç bilgilerini doldurun (isim, plaka, maksimum kapasite)
4. Şoför bilgilerini ekleyin

### Sipariş Ağırlık Hesaplama
1. Satış siparişi oluşturun
2. Ürünlerin ağırlık bilgileri otomatik olarak hesaplanır
3. Sipariş toplam ağırlığı otomatik olarak güncellenir

### Araç Atama
1. Onaylanmış siparişte "Assign Vehicle" butonuna tıklayın
2. Sistem uygun araçları otomatik olarak bulur
3. Araç seçin ve atayın
4. Kapasite kontrolü otomatik olarak yapılır

### Teslimat Takibi
1. Araç atanmış siparişte "Mark Delivered" butonuna tıklayın
2. Teslimat tarihi otomatik olarak kaydedilir
3. Araç statüsü güncellenir

## Teknik Detaylar

### Modeller
- `fleet.vehicle`: Araç yönetimi
- `sale.order`: Satış siparişi genişletmeleri
- `sale.order.line`: Sipariş satırı genişletmeleri

### Ana Alanlar
- `total_weight`: Sipariş toplam ağırlığı
- `vehicle_id`: Atanmış araç
- `max_capacity`: Araç maksimum kapasitesi
- `current_weight`: Araç mevcut ağırlığı
- `state`: Araç statüsü

### Validasyonlar
- Araç kapasitesi kontrolü
- Plaka benzersizlik kontrolü
- Statü geçiş kontrolleri

## Gereksinimler

- Odoo 13.0
- sale modülü
- stock modülü

## Lisans

Bu modül MIT lisansı altında lisanslanmıştır.
