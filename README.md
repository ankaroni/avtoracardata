# Avtora Car Data

Bulgaristan odaklı araç katalog veri katmanı.

Kaynak katalog: gor3a/vehicle-makes-models (ODbL 1.0). Bu repo ham veriyi olduğu gibi kullanmak yerine Vtora için normalize eder.

## Üretilen dosyalar
- `dist/makes-models.csv` — marka/model + üretim yılları
- `dist/engines.csv` — motor/teknik kayıtlar, canonical English terimler
- `dist/bulgaria-makes.csv` — Bulgaristan pazar önceliğine göre marka listesi
- `dist/catalog.json` — uygulama dropdownları için Make → Model yapısı
- `data/taxonomy.json` — Vtora'nın sabit filtre sözlüğü

## Bulgaristan yaklaşımı
Mobile.bg'deki güncel ilan dağılımı referans alınarak Mercedes-Benz, BMW, Audi, Volkswagen, Toyota, Hyundai, Peugeot, Opel, Kia, Ford vb. markalar önceliklendirilir. Kaynak katalogdaki diğer markalar silinmez; `market_priority` ile ayrılır.

## Canonical değerler
UI/database tarafında Almanca kaynak terimler tutulmaz. Yakıt, kasa, çekiş ve şanzıman değerleri normalize edilir.

## Güncelleme
GitHub Actions workflow'u upstream CSV verisini indirir, normalize eder ve `dist/` altına commit eder. Manuel çalıştırılabilir veya haftalık çalışır.

## Lisans
Kaynak araç verisi ODbL 1.0 kapsamındadır. Kaynak: https://github.com/gor3a/vehicle-makes-models
Bu repository'deki dönüştürülmüş veri için upstream attribution/share-alike koşullarını koruyun.
