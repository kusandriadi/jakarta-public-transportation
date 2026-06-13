---
name: jakarta-public-transportation
description: >
  Jakarta / Jabodetabek public transit router and reference. Knows every
  Transjakarta corridor & service category, all MRT Jakarta lines, LRT Jakarta &
  LRT Jabodebek lines, the full KRL Commuter + KA Bandara network with every
  station, and Whoosh high-speed rail Jakarta–Bandung (KCIC). Use whenever the
  user asks about routes, "naik apa dari A ke B", how to
  get somewhere in Jakarta, which corridor/line serves a place, transfers/
  interchange points between Transjakarta–MRT–LRT–KRL, getting to Bandung by
  kereta cepat/Whoosh, or anything about
  Transjakarta, busway, MRT, LRT, KRL/commuter line, KA Bandara, Whoosh. Triggers on
  /transit, /rute, and route questions in Indonesian or English.
---

# Jakarta Transit Router

Reference + routing helper for Jabodetabek public transport. **Always ground
answers in the `references/` docs below — do not improvise station names or
corridor numbers from memory.**

> Data captured **June 2026** from Transjakarta, MRT Jakarta, LRT Jakarta, KAI
> Commuter (KRL) sources. Networks change (new stations, renamed stops, schedule
> shifts). For live departures, fares, and service alerts, tell the user to check
> the official apps: **Tije** (Transjakarta), **MRT-J**, **KRL Access /
> C-Access** (KAI Commuter).

## Updating the data ("update skill")

When the user says **"update skill"**, "update jakarta-public-transportation", "scan ulang",
"refresh rute", or similar → re-scan all sources from scratch and regenerate the
reference files by following **`UPDATE.md`**. In short: run
`update/fetch-tj-routes.sh` (downloads all route-map images + KRL map), run the
saved OCR workflow `update/ocr-routes.workflow.js` over them, rebuild
`references/routes-haltes.md` with `update/build-routes-haltes.py`, then refresh
the KRL/MRT/LRT/corridor prose docs. Warn the user it takes a few minutes and
spends tokens (the OCR workflow). Full step-by-step is in `UPDATE.md`.

## The systems

| System | What it is | Reference |
|---|---|---|
| **Transjakarta** | BRT busway (14 corridors) + feeder/Mikrotrans/Royaltrans/Transjabodetabek/Wisata | `references/transjakarta.md` (corridors), `references/transjakarta-feeder.md` (route list), `references/routes-haltes.md` (**per-halte detail, 208 routes, both directions**) |
| **MRT Jakarta** | Subway/elevated metro (North–South line operating; East–West building) | `references/mrt-lrt.md` |
| **LRT Jakarta** | City light rail (Pegangsaan Dua–Velodrome) | `references/mrt-lrt.md` |
| **LRT Jabodebek** | Regional light rail (Cibubur & Bekasi lines via Dukuh Atas) | `references/mrt-lrt.md` |
| **KRL Commuter + KA Bandara** | Heavy-rail commuter network across Jabodetabek + airport train | `references/krl.md` |
| **Whoosh (KCIC)** | Kereta cepat Jakarta–Bandung (HSR, 4 stasiun: Halim/Karawang/Padalarang/Tegalluar) + integrasi tiap stasiun | `references/whoosh.md` |
| **Tarif / Fares** | Biaya tiap moda + skema tarif integrasi Jak Lingko (untuk pilih opsi **termurah**) | `references/fares.md` |
| **Jam operasional / Headway** | Jam buka-tutup & frekuensi tiap moda (untuk "masih keburu?" / "nunggu berapa lama?") | `references/hours.md` |

## How to answer a route question

1. **Identify endpoints.** Map the origin & destination to a station/area in the
   reference docs. Many place names map to a known stop (e.g. "Sudirman" → KRL
   Sudirman / MRT Dukuh Atas / LRT Dukuh Atas cluster).
2. **Pick the system(s) — optimalkan KEDUANYA: tercepat & termurah.** Rail
   (MRT/LRT/KRL) is faster over distance and unaffected by traffic; Transjakarta
   reaches far more neighborhoods. Prefer a single rail line if both endpoints sit
   on one. Otherwise chain via an **interchange** (see below). **Selalu timbang
   biaya** pakai `references/fares.md`: Mikrotrans (JAK) gratis, KRL termurah
   untuk jarak jauh, TJ Rp 3.500 flat, KA Bandara/Royaltrans/ojol mahal. Kalau
   **rute tercepat ≠ rute termurah**, kasih **dua opsi** dan beri label jelas
   (lihat aturan di bawah).
3. **Give the path:** which line/corridor, direction (toward which terminus),
   where to transfer, and final stop. Keep it concrete and ordered. For
   stop-level Transjakarta questions ("which halte do I get off at", "does route
   X stop near Y"), look up the route in `references/routes-haltes.md` — it has
   the full ordered halte list for both directions of all 208 routes.
   **Catatan cakupan:** `routes-haltes.md` lengkap untuk **semua BRT/koridor +
   pengumpan + Mikrotrans (JAK)**, tapi **hanya sebagian** Royaltrans/
   Transjabodetabek (kode B/D/P/S/T/SH — mis. S21, B25, T11) yang punya detail
   halte. Kalau kode regional tidak ada di `routes-haltes.md`, pakai
   `references/transjakarta-feeder.md` untuk asal–tujuannya, dan jangan klaim
   urutan halte yang tidak kamu punya.
4. **Note transfers & integration.** Call out where the user changes systems and
   whether it's a paid-area integration or a walk/skybridge.
5. **Sebut perkiraan biaya.** Pakai `references/fares.md` untuk kasih estimasi
   tarif tiap leg + total. Kalau lintas TJ+MRT+LRT, ingatkan **cap tarif
   integrasi Jak Lingko ≈ Rp 10.000**. Angka rupiah bisa berubah — kasih
   estimasi + caveat "cek app resmi (Tije/MRT-J/KRL Access) untuk tarif live".
   **Jam operasional & headway** ada di `references/hours.md` (MRT, LRT Jakarta,
   LRT Jabodebek, Transjakarta, JakLingko, Whoosh, KRL, KA Bandara) — pakai untuk
   "masih keburu kereta terakhir?" / "nunggu berapa lama?". Jam pasti per
   stasiun/lin tetap arahkan ke app resmi.

### ✅ CHECKLIST WAJIB SEBELUM KIRIM JAWABAN (MUST verify every item)

**Cakupan checklist ini:** rute **dalam Jabodetabek** (TJ/MRT/LRT/KRL). Untuk
pertanyaan **Whoosh / ke Bandung**, checklist ini TIDAK berlaku (jangan paksa MRT
atau cap Jak Lingko ke itinerary antar-kota) — ikuti `references/whoosh.md`. LRT
Jabodebek tetap relevan sebagai cara seamless mencapai Stasiun Halim.

Sebelum kirim jawaban rute, cek **SEMUA** item di bawah. Kalau ada yang lolos,
JANGAN kirim — perbaiki dulu:

- [ ] **Gak ada kata "angkot" tanpa kode rute.** Kalau mau suruh naik angkot,
      harus sebut kode Jak Lingko/feeder (contoh: "JAK 43C", "8E"). Kalau gak
      tahu kodenya, ganti opsi dengan ojol atau rute yang kamu tahu kodenya.
- [ ] **Gak ada kata "naik TJ" atau "Koridor X" tanpa kode spesifik.** Harus
      sebut kode rute exact (contoh: "13E", bukan "Koridor 13"). Cek
      `routes-haltes.md` untuk rute yang benar-benar lewat halte tujuan.
- [ ] **Gak muter.** Tujuan dekat dari stasiun/halte terakhir? Turun aja, ojol/
      jalan kaki. Gak usah tambah 2-3x transit.
- [ ] **MRT dipertimbangkan.** Kalau bisa masuk jaringan MRT via TJ/KRL, itu
      harus jadi salah satu opsi.
- [ ] **Setiap leg punya: kode rute + halte naik + arah + halte turun.**
      KRL juga harus sebut nama lin.
- [ ] **Biaya disebut & opsi termurah dipertimbangkan.** Ada perkiraan tarif tiap
      leg + total. Sudah cek `references/fares.md`? Kalau ada JAK (Mikrotrans,
      gratis) atau KRL (murah jarak jauh) yang relevan, itu harus muncul sebagai
      kandidat. Kalau **tercepat ≠ termurah**, kasih dua opsi berlabel.

Kalau ragu tentang rute tertentu, **cek `references/routes-haltes.md` dulu**
sebelum jawab. Jangan ngarang.

### Routing quality rules (MUST follow)

**Minimize unnecessary transfers.** Jangan suruh pengguna transit 2-3 kali kalau
destinasinya udah dekat dari stasiun/halte terakhir. Contoh: dari Tanah Abang ke
tempat yang dekat Tanah Abang (Gedung Sarana Jaya, Monas, dsb.) → cukup turun di
Tanah Abang terus jalan kaki/ojol, **jangan** disuruh transit lagi ke Manggarai
lalu Gondangdia. Selalu cek jarak dari stasiun terakhir ke tujuan sebelum
menambah leg tambahan.

**Transjakarta, angkot, feeder, Mikrotrans: selalu sebut kode rute spesifik.**
Jangan tulis "naik TJ", "Koridor 13", atau "angkot" saja. Dalam satu koridor bisa
ada beberapa rute (contoh: 13, 13B, 13E) yang **tujuannya beda** — cek
`references/routes-haltes.md` untuk rute mana yang benar-benar lewat halte
tujuan. Setiap leg WAJIB menyertakan:
- **Kode rute spesifik** (contoh: "13E", "6H", "JAK 43C", "S21") — bukan cuma "Koridor 13" atau "angkot"
- **Nama halte naik** (contoh: "Halte CBD Ciledug")
- **Jurusan/arah** (contoh: "arah Flyover Kuningan")
- **Nama halte turun** (contoh: "Halte Kuningan")

Contoh jawaban benar: "Naik **13E** (arah Flyover Kuningan) dari **Halte CBD Ciledug**
→ turun di **Halte Kuningan**".
Contoh jawaban salah: "Naik Koridor 13 → turun di Kuningan" (bisa 13, 13B, atau 13E — cuma 13E yang nyampe Kuningan).

**KRL: sebutkan nama lin.** Setiap leg KRL harus menyebutkan nama lin dan arah.
Contoh: "Naik **Lin Rangkasbitung** arah Tanah Abang → turun di Tanah Abang".

**Jangan sekali-kali suruh "naik angkot" tanpa kode rute.** Kata "angkot" itu
tidak spesifik — gak ada yang tahu angkot mana. Kalau ada Jak Lingko (JAK) atau
feeder/Mikrotrans yang melayani rute itu, sebut **kodenya** (contoh: "JAK 43C",
"6H", "8E"). Kalau memang gak ada rute Transjakarta/Jak Lingko yang melayani
area itu, sebutin opsi lain (ojek online, KRL, dll.) — jangan tulis "naik angkot"
sebagai solusi. Cek selalu `references/transjakarta-feeder.md` dan
`references/routes-haltes.md` untuk rute yang tersedia.

**Opsi jalan kaki/ojol setelah turun.** Kalau tujuan akhir dekat dari stasiun/
halte terakhir (~1-2 km), sebutkan jarak dan opsi (jalan kaki / ojol). Jangan
langsung tambah transit ke stasiun lain yang lebih "dekat" kalau jaraknya udah
reasonable dari stasiun sekarang.

**Selalu pertimbangkan kombinasi multi-moda.** Jangan cuma kasih opsi per sistem
(KRL doang, TJ doang). Kalau rute melibatkan interchange hub yang terintegrasi
dengan sistem lain, eksplorasi kombinasi:
- TJ → MRT (contoh: naik TJ Koridor 13 ke CSW, transit ke MRT ASEAN, turun
  Bundaran HI, lanjut TJ/ojol ke tujuan)
- KRL → MRT (contoh: KRL turun di Sudirman, jalan ke MRT Dukuh Atas)
- TJ → KRL → ojol (contoh: TJ ke halte dekat stasiun, KRL ke stasiun terdekat
  dengan tujuan, ojol terakhir)

Intinya: lihat peta interchange hub di bawah, dan gunakan kombinasi sistem yang
memberikan rute terbaik ke tujuan. Sedikit transit itu bagus. Kadang 1x transit
via MRT jauh lebih cepat dari 0x transit TJ yang kena macet. Jangan rigid satu
sistem doang.

**Optimalkan tercepat DAN termurah — kalau beda, kasih dua opsi.** Tujuan akhir
adalah rute **terbaik**, bukan cuma tercepat. Banyak kasus rute tercepat
(mis. MRT/ojol) beda dari rute termurah (mis. KRL + Mikrotrans gratis). Kalau
keduanya beda signifikan, **sajikan keduanya** dengan label jelas, contoh:

> **🚀 Tercepat (~35 mnt, ~Rp 14.000):** KRL Lin Bogor → Sudirman, jalan ke MRT
> Dukuh Atas → turun Bundaran HI, ojol ~1 km ke tujuan.
> **💸 Termurah (~50 mnt, ~Rp 3.500):** KRL Lin Bogor → Sudirman, lanjut TJ
> Koridor 1 dari Halte Dukuh Atas → turun Bundaran HI, jalan kaki ~600 m.

Kalau rute tercepat **sekaligus** termurah, cukup satu opsi (sebut saja itu yang
terbaik). Selalu sertakan **perkiraan biaya** dan **perkiraan waktu** tiap opsi.
Untuk biaya, pakai `references/fares.md` (Mikrotrans gratis, KRL murah jarak
jauh, TJ Rp 3.500 flat, cap tarif integrasi Jak Lingko ≈ Rp 10.000 untuk
TJ+MRT+LRT). Untuk hop pendek (~1-2 km) di ujung, tawarkan **jalan kaki**
(gratis) vs **ojol** (cepat tapi bayar) sebagai pilihan murah-vs-cepat.

**Opsi MRT harus selalu dipertimbangkan.** MRT adalah moda tercepat dan paling
nyaman di Jakarta. Kalau ada cara untuk masuk ke jaringan MRT (via TJ ke stasiun
MRT, via KRL ke Sudirman/Dukuh Atas, dll.), itu harus jadi salah satu opsi yang
disarankan. Contoh: dari Ciledug → naik TJ Koridor 13 ke CSW → transit ke MRT
ASEAN → turun Bundaran HI → ojol/TJ ke tujuan. Ini sering lebih cepat dari
TJ saja atau KRL saja.

## Key interchange hubs (where systems connect)

- **Dukuh Atas / Sudirman** — the super-hub: MRT (Dukuh Atas BNI) ↔ KRL
  (Sudirman) ↔ LRT Jabodebek (Dukuh Atas BNI) ↔ KA Bandara (BNI City) ↔
  Transjakarta. Connect almost any system here.
- **Bundaran HI** — MRT ↔ Transjakarta (Koridor 1).
- **CSW / ASEAN** — Transjakarta (Koridor 1, 13, 13B, 13E, dll.) ↔ MRT ASEAN via
  **jembatan/skybridge** langsung. Hub utama untuk masuk jaringan MRT dari selatan
  (Ciledug, Bintaro, Kebayoran).
- **Velbak** — Transjakarta Koridor 13 ↔ Koridor 8 (koneksi ke Kebayoran/Koridor 8)
  dan terhubung via **skywalk** langsung ke **Stasiun KRL Kebayoran** (jalan kaki).
  Titik transit penting untuk pindah dari Koridor 13 ke Koridor 8 atau ke KRL.
- **Lebak Bulus** — MRT southern terminus ↔ Transjakarta (Koridor 8).
- **Velodrome (Rawamangun)** — LRT Jakarta ↔ Transjakarta (skybridge).
- **Cawang** — LRT Jabodebek ↔ Transjakarta ↔ KRL Cawang (Bogor line, walk).
- **Kampung Rambutan** — LRT Jabodebek ↔ Transjakarta (Koridor 7).
- **Harjamukti / TMII / Cibubur** — LRT Jabodebek ↔ Transjakarta feeders.
- **JIS (Jakarta Int'l Stadium)** — KRL Tanjung Priok line ↔ Transjakarta Koridor 14.
- **Jakarta Kota** — KRL (Bogor & Tanjung Priok) ↔ Transjakarta (Koridor 1) hub.
- **Jatinegara** — KRL Cikarang line junction (two branches split here).

### Stasiun Transit Utama KRL (detail)

Stasiun-stasiun KRL berikut adalah titik transit penting. Saat menjawab pertanyaan
rute KRL, gunakan info ini untuk menentukan di mana pengguna harus pindah kereta.

#### Stasiun Manggarai
**Pusat transit terbesar KRL.** Melayani rute-rute berikut:
- **Arah Bogor** — Lin Bogor (Jakarta Kota ↔ Bogor/Nambo), stop di Manggarai
- **Arah Jakarta Kota** — Lin Bogor menuju Jakarta Kota via Gondangdia–Juanda
- **Arah Bekasi/Cikarang** — Lin Cikarang (loop via Jatinegara)
- **Arah Tanah Abang/Kampung Bandan** — Lin Cikarang loop (selatan) via Sudirman–Tanah Abang–Angke–Kampung Bandan
- **Kereta Bandara (KA Bandara)** — Manggarai ↔ Soekarno-Hatta via BNI City, Duri, Batu Ceper

 Hampir semua perjalanan KRL antar-linie bisa dilakukan dengan transit di Manggarai.

#### Stasiun Tanah Abang
**Pusat transit untuk rute berikut:**
- **Arah Manggarai** — Lin Cikarang loop (via Karet–Sudirman–Manggarai)
- **Arah Rangkasbitung** — Lin Rangkasbitung (terminus, arah Serpong–Tigaraksa–Rangkasbitung)
- **Arah Jatinegara** — Lin Cikarang loop (via Duri–Angke–Kampung Bandan atau via Manggarai–Matraman–Jatinegara)

 Transit penting untuk penumpang dari arah selatan (Serpong, Tangerang Selatan) yang mau ke Jakarta pusat atau Bekasi.

#### Stasiun Duri
**Stasiun transit untuk tujuan:**
- **Tangerang** — Lin Tangerang (Duri ↔ Tangerang, terminus)
- **Manggarai** — Lin Cikarang loop via Tanah Abang–Karet–Sudirman–Manggarai
- **Kereta Bandara (KA Bandara)** — Duri adalah stop KA Bandara antara BNI City dan Batu Ceper

 Alternatif transit KA Bandara selain Manggarai, lebih dekat dari arah Tangerang.

#### Stasiun Kampung Bandan
**Titik transit untuk:**
- **KRL Lin Tanjung Priok** — Jakarta Kota ↔ Tanjung Priok (arah Ancol, JIS, Pelabuhan Tanjung Priok)
- **KRL Lin Bogor** — arah Jakarta Kota (via Manggarai–Gondangdia–Juanda) dan arah Bogor
- **Lin Cikarang loop** — via Manggarai (selatan) atau via Pasar Senen (utara)

 Hub utara Jakarta, cocok untuk transit antara rute pelabuhan/Tanjung Priok dan rute Bogor/Bekasi.

#### Stasiun Sudirman
**Integrasi multi-modal:**
- **KRL Lin Cikarang** — stop di Sudirman (antara Manggarai dan Karet)
- **MRT Jakarta** — transit jalan kaki ke **Stasiun MRT Dukuh Atas BNI** (~5-10 menit)
- **LRT Jabodebek** — transit ke **Stasiun LRT Dukuh Atas BNI**
- **KA Bandara** — **BNI City** berada di area yang sama (stasiun KA Bandara dedicated)
- **Transjakarta** — Halte Sudirman di Koridor 1

 Hub terbaik untuk pindah dari KRL ke MRT atau LRT, dan untuk naik KA Bandara.

### Halte Transit Utama Transjakarta (detail)

Halte-halte Transjakarta berikut adalah titik transit penting. Saat menjawab
pertanyaan rute Transjakarta, gunakan info ini untuk menentukan di mana
pengguna harus pindah koridor atau moda transportasi.

#### Halte Harmoni
**Titik transit sentral Transjakarta.** Melayani:
- **Koridor 1** — Blok M ↔ Kota (utama, jalur Sudirman–Thamrin)
- **Koridor 2** — Pulo Gadung ↔ Harmoni (arah timur–barat via Jakarta)
- **Koridor 3** — Kalideres ↔ Harmoni (arah Tangerang–Jakarta pusat)
- **Berbagai rute langsung (Royaltrans, dll.)** — banyak rute non-koridor juga stop di sini

 Hub terbesar Transjakarta — hampir semua perjalanan antar-koridor yang melewati Jakarta pusat bisa transit di sini.

#### Halte CSW – ASEAN
**Terintegrasi langsung dengan Stasiun MRT ASEAN.** Melayani:
- **Koridor 13** — CBD Ciledug ↔ Tendean (arah selatan–pusat kota)
- **Koridor 1** — Blok M ↔ Kota (via Halte Sudirman, dsb.)
- **Transit ke MRT** — Stasiun MRT ASEAN terintegrasi langsung, tanpa perlu jalan jauh
- **Akses ke koridor lain** — transit ke koridor 1, 9, dan rute feeder sekitar Senayan/Kebayoran

 Titik integrasi Transjakarta ↔ MRT terbaik di area Senayan–Kuningan.

#### Halte Dukuh Atas (Stasiun Dukuh Atas)
**Pusat integrasi multi-modal terlengkap.** Menghubungkan:
- **Transjakarta** — Koridor 1 (dan rute lain yang melintasi Sudirman–Thamrin)
- **KRL Sudirman** — transit jalan kaki ke Stasiun KRL Sudirman
- **MRT Dukuh Atas BNI** — stasiun MRT terdekat
- **LRT Jabodebek Dukuh Atas BNI** — stasiun LRT terdekat
- **KA Bandara (BNI City)** — akses ke Soekarno-Hatta Airport

 Satu-satunya titik di Jakarta di mana semua 5 moda (Transjakarta, KRL, MRT, LRT, KA Bandara) bisa dijangkau dalam radius ~10 menit jalan kaki.

#### Halte Cawang BNN
**Menghubungkan Transjakarta dengan LRT Jabodebek.** Melayani:
- **Koridor 7** — Kampung Rambutan ↔ Kampung Melayu (arah timur)
- **Koridor 9** — Pinang Ranti ↔ Pluit (arah timur–barat via Cawang)
- **Stasiun LRT Cawang** — transit langsung ke LRT Jabodebek (lin Cibubur & Bekasi)
- **KRL Cawang** — Stasiun KRL Cawang di Lin Bogor (jarak jalan kaki)

 Hub penting untuk transit antara Transjakarta dan LRT di area timur Jakarta.

#### Halte Manggarai
**Terhubung langsung via skywalk dengan Stasiun KRL Manggarai.** Melayani:
- **Transjakarta** — halte di korridor yang melintasi area Manggarai
- **KRL Manggarai** — skywalk langsung ke stasiun KRL (hub terbesar KRL, lihat detail di atas)
- **Akses ke MRT/LRT** — via KRL ke Sudirman/Dukuh Atas, atau langsung ke moda lain

 Mempermudah perpindahan dari Transjakarta ke KRL tanpa harus ke Dukuh Atas — alternatif lebih dekat untuk penumpang dari arah selatan/timur.

### Stasiun Transit Utama LRT Jabodebek (detail)

Stasiun-stasiun LRT Jabodebek berikut adalah titik transit penting. Saat menjawab
pertanyaan rute LRT, gunakan info ini untuk menentukan di mana pengguna harus
pindah moda atau rute LRT.

#### Stasiun Cawang (Transit Internal LRT)
**Persimpangan rute LRT Jabodebek.**
- **Rute Dukuh Atas ↔ Jatimulya** — lin Bekasi (timur)
- **Rute Dukuh Atas ↔ Harjamukti** — lin Cibubur (selatan)
- Dua rute LRT bercabang di sini; penumpang harus transit di Cawang untuk ganti arah
- **Integrasi Transjakarta** — terhubung langsung dengan **Halte Transjakarta BNN** (Koridor 9, dll.)
- **Integrasi KRL** — terhubung dengan **Stasiun KRL Cawang** (Lin Bogor) melalui jembatan penyeberangan

 Titik percabangan utama LRT — semua perjalanan LRT melewati stasiun ini, dan di sinilah penumpang pindah antar-lin LRT.

#### Stasiun Dukuh Atas BNI (Koneksi Antar Moda)
**Hub multi-modal terlengkap di jaringan LRT.** Terintegrasi langsung dengan:
- **KRL Commuter Line** — Stasiun KRL Sudirman (jarak jalan kaki)
- **MRT Jakarta** — Stasiun MRT Dukuh Atas BNI
- **Kereta Bandara (KA Bandara)** — Stasiun BNI City (Railink)
- **Transjakarta** — Halte Dukuh Atas dan Halte Galunggung

 Stasiun terbaik untuk pindah dari LRT ke moda lain (KRL, MRT, KA Bandara, Transjakarta) — semuanya dalam jangkauan dekat.

#### Stasiun Halim
**Terhubung dengan Kereta Cepat Whoosh (integrasi seamless).**
- **Whoosh (KCIC)** — Stasiun Halim adalah stasiun awal kereta cepat Jakarta–Bandung
- Akses langsung ke Whoosh tujuan Bandung (stasiun: Karawang, Padalarang, Tegalluar)
- Transit LRT ↔ Whoosh **tanpa keluar kompleks** (tetap tap-out/tap-in, jalan kaki via concourse)
- Detail stasiun, jam, kelas/tarif Whoosh → `references/whoosh.md`

 Satu-satunya titik integrasi LRT Jabodebek dengan kereta cepat Whoosh.

#### Stasiun Cikoko
**Dekat dengan Stasiun KRL Cawang.**
- **KRL Cawang** — stasiun KRL di Lin Bogor, terletak dekat Stasiun LRT Cikoko
- Alternatif transit LRT ↔ KRL selain via Cawang atau Dukuh Atas
- Cocok untuk penumpang LRT yang mau lanjut ke arah Bogor/Depok atau Jakarta Kota via KRL

### Stasiun Transit Utama MRT Jakarta (detail)

Stasiun-stasiun MRT berikut adalah titik integrasi antar-moda penting. Saat menjawab
pertanyaan rute MRT, gunakan info ini untuk menentukan di mana pengguna harus
pindah ke moda lain (KRL, LRT, Transjakarta, KA Bandara, bus).

#### Stasiun Dukuh Atas BNI
**Hub multi-modal terlengkap di jaringan MRT.** Terintegrasi langsung dengan:
- **KRL Commuter Line** — Stasiun KRL Sudirman (jarak jalan kaki)
- **Kereta Bandara (KA Bandara)** — Stasiun BNI City
- **LRT Jabodebek** — Stasiun LRT Dukuh Atas BNI
- **Transjakarta** — Halte Dukuh Atas & Halte Galunggung

 Titik terbaik untuk pindah dari MRT ke moda lain — KRL, KA Bandara, LRT, dan Transjakarta semuanya dalam jangkauan.

#### Stasiun Bundaran HI Bank Jakarta
**Terintegrasi dengan Transjakarta.**
- **Transjakarta** — Halte Bundaran HI di **Koridor 1** (Blok M ↔ Kota)
- Akses langsung ke area Monas, Grand Indonesia, Plaza Indonesia
- Titik transit utama MRT ↔ Transjakarta di jalur Sudirman–Thamrin

#### Stasiun Blok M BCA
**Terintegrasi dengan Terminal Blok M dan Transjakarta.**
- **Terminal Blok M** — terminal bus antar-kota dan dalam kota
- **Transjakarta** — halte dan rute feeder di sekitar Blok M
- Akses ke area perbelanjaan Blok M, Melawai

#### Stasiun Lebak Bulus
**Terintegrasi dengan Terminal Bus Lebak Bulus dan Transjakarta.**
- **Terminal Lebak Bulus** — terminal bus antar-kota dan AKDP
- **Transjakarta** — **Koridor 8** (Lebak Bulus ↔ Harmoni) dan rute feeder
- Terminus selatan MRT — cocok untuk penumpang dari Ciputat, Pondok Indah, sekitarnya

#### Stasiun Istora Mandiri
**Terintegrasi dengan Transjakarta.**
- **Transjakarta** — Halte **Polda Metro Jaya** di Koridor 1
- Akses ke area Senayan (GBK, Senayan City, Plaza Senayan)
- Alternatif transit MRT ↔ Transjakarta selain Bundaran HI

## Quick line-picker

- Anywhere along **Jl. Sudirman–Thamrin (Blok M ↔ Kota / Bundaran HI)** → MRT or
  Transjakarta Koridor 1.
- **To/from Bogor, Depok, Bekasi, Cikarang, Tangerang, Serpong/Rangkasbitung** →
  KRL (`references/krl.md`).
- **To Soekarno-Hatta Airport** → KA Bandara from Manggarai/BNI City/Duri/Batu
  Ceper (or DAMRI/Transjabodetabek bus).
- **Cibubur / Bekasi corridor toward Dukuh Atas** → LRT Jabodebek.
- **Within Kelapa Gading ↔ Rawamangun** → LRT Jakarta.
- **To Bandung (kereta cepat / Whoosh)** → Whoosh from **Halim** (reach Halim via
  LRT Jabodebek, seamless) → **Padalarang** + free KA Feeder for central Bandung,
  or **Tegalluar** for Bandung Timur/Jatinangor. See `references/whoosh.md`.
