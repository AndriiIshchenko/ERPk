"""
Seed 200 tech products (computers & peripherals, Alza-style).
Usage:
    docker compose exec backend python -m scripts.seed_products
    DATABASE_URL=postgresql+asyncpg://erpk:erpk@localhost:5432/orders_db python -m scripts.seed_products
"""

import asyncio
import os
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.models.product import Product

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+asyncpg://erpk:erpk@localhost:5432/orders_db"
)

PRODUCTS = [
    # ── Laptops (45) ──────────────────────────────────────────────────────────
    (
        "Lenovo ThinkPad X1 Carbon Gen 11",
        '14" FHD IPS, Core i7-1365U, 16 GB, 512 GB SSD, W11 Pro',
        Decimal("1549.99"),
    ),
    (
        "Lenovo ThinkPad E16 Gen 1",
        '16" FHD IPS, Core i5-1335U, 16 GB, 512 GB SSD',
        Decimal("899.99"),
    ),
    (
        "Lenovo IdeaPad Slim 5",
        '15.6" FHD, Core i5-12450H, 16 GB, 512 GB SSD',
        Decimal("649.99"),
    ),
    (
        "Dell XPS 13 9340",
        '13.4" FHD+ IPS, Core Ultra 7-155H, 16 GB, 1 TB SSD',
        Decimal("1699.99"),
    ),
    (
        "Dell Inspiron 15 3530",
        '15.6" FHD, Core i5-1335U, 8 GB, 512 GB SSD',
        Decimal("549.99"),
    ),
    (
        "Dell Latitude 5540",
        '15.6" FHD IPS, Core i7-1355U, 16 GB, 512 GB SSD, W11 Pro',
        Decimal("1199.99"),
    ),
    (
        "HP EliteBook 840 G10",
        '14" WUXGA IPS, Core i7-1355U, 16 GB, 512 GB SSD, W11 Pro',
        Decimal("1399.99"),
    ),
    (
        "HP ProBook 450 G10",
        '15.6" FHD IPS, Core i5-1335U, 16 GB, 512 GB SSD',
        Decimal("849.99"),
    ),
    (
        "HP Pavilion 15-eh3",
        '15.6" FHD IPS, Ryzen 5 7530U, 16 GB, 512 GB SSD',
        Decimal("699.99"),
    ),
    (
        "Apple MacBook Air 13 M3",
        '13.6" Liquid Retina, Apple M3, 8 GB, 256 GB SSD',
        Decimal("1299.99"),
    ),
    (
        "Apple MacBook Pro 14 M3 Pro",
        '14.2" Liquid Retina XDR, M3 Pro 12-core, 18 GB, 512 GB SSD',
        Decimal("2099.99"),
    ),
    (
        "Apple MacBook Air 15 M3",
        '15.3" Liquid Retina, Apple M3, 16 GB, 512 GB SSD',
        Decimal("1549.99"),
    ),
    (
        "ASUS ZenBook 14 OLED",
        '14" 2.8K OLED, Core Ultra 5-125H, 16 GB, 512 GB SSD',
        Decimal("1099.99"),
    ),
    (
        "ASUS VivoBook 15 X1504",
        '15.6" FHD, Core i5-1235U, 16 GB, 512 GB SSD',
        Decimal("599.99"),
    ),
    (
        "ASUS ROG Zephyrus G14 2024",
        '14" QHD 165 Hz, Ryzen 9 8945HS, 16 GB, 1 TB SSD, RTX 4060',
        Decimal("1699.99"),
    ),
    (
        "ASUS TUF Gaming A15",
        '15.6" FHD 144 Hz, Ryzen 7 7735HS, 16 GB, 512 GB SSD, RTX 4060',
        Decimal("1099.99"),
    ),
    (
        "Acer Swift Go 14",
        '14" 2.8K OLED, Core Ultra 7-155U, 16 GB, 1 TB SSD',
        Decimal("1049.99"),
    ),
    (
        "Acer Aspire 5 A515-58M",
        '15.6" FHD IPS, Core i5-1335U, 16 GB, 512 GB SSD',
        Decimal("649.99"),
    ),
    (
        "Acer Nitro 16",
        '16" QHD 165 Hz, Ryzen 7 7745HX, 16 GB, 512 GB SSD, RTX 4060',
        Decimal("1149.99"),
    ),
    (
        "MSI Modern 14",
        '14" FHD IPS, Core Ultra 5-125U, 16 GB, 512 GB SSD',
        Decimal("799.99"),
    ),
    (
        "MSI Stealth 16 AI Studio",
        '16" QHD+ 240 Hz Mini-LED, Core Ultra 9-185H, 32 GB, 2 TB SSD, RTX 4080',
        Decimal("3499.99"),
    ),
    (
        "MSI Katana 15",
        '15.6" FHD 144 Hz, Core i7-12650H, 16 GB, 512 GB SSD, RTX 4060',
        Decimal("1099.99"),
    ),
    (
        "Samsung Galaxy Book4 Pro 360",
        '16" 3K AMOLED Touch, Core Ultra 7-155H, 16 GB, 512 GB SSD',
        Decimal("1799.99"),
    ),
    (
        "Microsoft Surface Laptop 6",
        '13.5" PixelSense, Core Ultra 5-135H, 16 GB, 256 GB SSD',
        Decimal("1299.99"),
    ),
    (
        "Huawei MateBook D16 2024",
        '16" FHD IPS, Core i7-13700H, 16 GB, 1 TB SSD',
        Decimal("999.99"),
    ),
    (
        "LG gram 16",
        '16" WQXGA IPS, Core Ultra 7-155H, 16 GB, 512 GB SSD',
        Decimal("1349.99"),
    ),
    (
        "Razer Blade 16 2024",
        '16" QHD+ 240 Hz OLED, Core Ultra 9-185H, 32 GB, 2 TB SSD, RTX 4090',
        Decimal("4499.99"),
    ),
    (
        "Gigabyte AORUS 16X",
        '16" QHD 165 Hz, Core i9-14900HX, 32 GB, 1 TB SSD, RTX 4070',
        Decimal("1999.99"),
    ),
    (
        "Toshiba Dynabook Satellite Pro",
        '15.6" FHD, Core i7-1355U, 16 GB, 512 GB SSD, W11 Pro',
        Decimal("1149.99"),
    ),
    (
        "Fujitsu LifeBook U7613",
        '13.3" FHD IPS, Core i7-1355U, 16 GB, 512 GB SSD, W11 Pro',
        Decimal("1499.99"),
    ),
    (
        "Lenovo Legion 5i Gen 9",
        '16" WQXGA 165 Hz, Core i7-14650HX, 32 GB, 1 TB SSD, RTX 4070',
        Decimal("1649.99"),
    ),
    (
        "HP OMEN 16",
        '16.1" QHD 165 Hz, Core i7-13700HX, 16 GB, 1 TB SSD, RTX 4070',
        Decimal("1549.99"),
    ),
    (
        "Dell G15 Gaming",
        '15.6" FHD 165 Hz, Core i7-13650HX, 16 GB, 512 GB SSD, RTX 4060',
        Decimal("1149.99"),
    ),
    (
        "ASUS ProArt Studiobook 16",
        '16" 4K OLED Touch, Core Ultra 9-185H, 64 GB, 2 TB SSD, RTX 4070',
        Decimal("3299.99"),
    ),
    (
        "Acer Predator Helios 18",
        '18" QHD 250 Hz, Core i9-14900HX, 32 GB, 2 TB SSD, RTX 4090',
        Decimal("3999.99"),
    ),
    (
        "Lenovo Yoga 9i Gen 9",
        '14" 2.8K OLED Touch, Core Ultra 7-155H, 32 GB, 1 TB SSD',
        Decimal("1799.99"),
    ),
    (
        "HP Spectre x360 14",
        '14" 2.8K OLED Touch, Core Ultra 7-155U, 32 GB, 2 TB SSD',
        Decimal("1999.99"),
    ),
    (
        "Dell XPS 15 9530",
        '15.6" OLED Touch, Core i9-13900H, 32 GB, 1 TB SSD, RTX 4060',
        Decimal("2499.99"),
    ),
    (
        "ASUS Zenbook Pro 16X OLED",
        '16" 4K OLED Touch, Core i9-13980HX, 32 GB, 1 TB SSD, RTX 4070',
        Decimal("2999.99"),
    ),
    (
        "Microsoft Surface Pro 10",
        '13" PixelSense Flow, Core Ultra 5-135U, 16 GB, 256 GB SSD',
        Decimal("1399.99"),
    ),
    (
        "Lenovo ThinkPad T14s Gen 5",
        '14" WUXGA IPS, Core Ultra 7-155U, 32 GB, 1 TB SSD, W11 Pro',
        Decimal("1449.99"),
    ),
    (
        "HP ZBook Firefly G10",
        '14" WUXGA IPS, Core i7-1355U, 32 GB, 1 TB SSD, W11 Pro',
        Decimal("1799.99"),
    ),
    (
        "ASUS ExpertBook B9403",
        '14" 2.8K OLED, Core Ultra 7-155U, 32 GB, 1 TB SSD',
        Decimal("1999.99"),
    ),
    (
        "Acer Chromebook Spin 714",
        '14" 2K IPS Touch, Core i5-1235U, 8 GB, 256 GB SSD, ChromeOS',
        Decimal("649.99"),
    ),
    (
        "Samsung Galaxy Book4 360",
        '15.6" FHD AMOLED Touch, Core i7-1355U, 16 GB, 512 GB SSD',
        Decimal("1299.99"),
    ),
    # ── Desktop PCs (20) ──────────────────────────────────────────────────────
    (
        "Lenovo ThinkCentre M70q Gen 5",
        "Mini PC, Core i5-14400T, 16 GB, 512 GB SSD, W11 Pro",
        Decimal("799.99"),
    ),
    (
        "Dell OptiPlex 7010 Micro",
        "Micro PC, Core i5-13500T, 16 GB, 512 GB SSD, W11 Pro",
        Decimal("849.99"),
    ),
    (
        "HP EliteDesk 800 G9 Mini",
        "Mini PC, Core i7-13700T, 32 GB, 1 TB SSD, W11 Pro",
        Decimal("1099.99"),
    ),
    (
        "Apple Mac mini M4",
        "Apple M4, 16 GB, 256 GB SSD, macOS Sequoia",
        Decimal("699.99"),
    ),
    (
        "Apple Mac Studio M4 Max",
        "Apple M4 Max 16-core, 64 GB, 512 GB SSD, macOS",
        Decimal("2499.99"),
    ),
    (
        "ASUS NUC 14 Pro",
        "Mini PC, Core Ultra 7-155H, 32 GB, 1 TB SSD, W11 Pro",
        Decimal("999.99"),
    ),
    ("Intel NUC 14 Essential", "Mini PC, N200, 8 GB, 256 GB SSD", Decimal("299.99")),
    (
        "Lenovo Legion Tower 7i Gen 8",
        "Core i9-13900K, 32 GB, 2 TB SSD, RTX 4090, W11",
        Decimal("3499.99"),
    ),
    (
        "Dell XPS 8960 Tower",
        "Core i7-13700K, 32 GB, 1 TB SSD + 2 TB HDD, RTX 4060 Ti",
        Decimal("1799.99"),
    ),
    (
        "HP Pavilion Gaming TG01",
        "Core i7-13700F, 16 GB, 512 GB SSD, RTX 4060, W11",
        Decimal("1099.99"),
    ),
    (
        "ASUS ROG Strix GT15",
        "Core i9-13900KF, 32 GB, 1 TB NVMe, RTX 4080, W11",
        Decimal("2999.99"),
    ),
    (
        "Acer Aspire TC-1780",
        "Core i7-13700, 16 GB, 512 GB SSD + 1 TB HDD, W11",
        Decimal("849.99"),
    ),
    (
        "MSI Infinite RS 13NUF",
        "Core i9-13900K, 32 GB, 2 TB NVMe, RTX 4080, W11",
        Decimal("3199.99"),
    ),
    (
        "Lenovo IdeaCentre 5 Tower",
        "Ryzen 5 7600, 16 GB, 512 GB SSD, RX 6600, W11",
        Decimal("899.99"),
    ),
    (
        "HP OMEN GT22-0",
        "Core i9-14900K, 64 GB, 2 TB NVMe, RTX 4090, W11",
        Decimal("4499.99"),
    ),
    (
        "Custom Gaming PC Starter",
        "Ryzen 5 7600X, 16 GB DDR5, 1 TB NVMe, RTX 4060, W11",
        Decimal("1199.99"),
    ),
    (
        "Custom Gaming PC Pro",
        "Ryzen 7 7800X3D, 32 GB DDR5, 2 TB NVMe, RTX 4070 Super, W11",
        Decimal("1999.99"),
    ),
    (
        "Custom Workstation Basic",
        "Core i9-14900K, 64 GB ECC, 4 TB NVMe RAID, W11 Pro",
        Decimal("3499.99"),
    ),
    (
        "Raspberry Pi 5 8 GB Kit",
        "BCM2712 2.4 GHz, 8 GB LPDDR4X, official PSU + case",
        Decimal("109.99"),
    ),
    (
        "Minisforum UM790 Pro",
        "Mini PC, Ryzen 9 7940HS, 32 GB DDR5, 1 TB NVMe, W11",
        Decimal("649.99"),
    ),
    # ── Monitors (30) ─────────────────────────────────────────────────────────
    (
        "LG 27GP850-B",
        '27" QHD IPS 165 Hz, 1 ms, HDR400, FreeSync/G-Sync',
        Decimal("349.99"),
    ),
    (
        "Samsung Odyssey G7 32",
        '32" QHD VA 240 Hz, 1 ms, HDR600, G-Sync Compatible',
        Decimal("549.99"),
    ),
    (
        "Dell U2723QE",
        '27" 4K IPS 60 Hz, USB-C 90 W, RJ-45, factory calibrated',
        Decimal("649.99"),
    ),
    (
        "ASUS ProArt PA279CRV",
        '27" 4K IPS 60 Hz, USB-C 96 W, 99% DCI-P3, factory calibrated',
        Decimal("699.99"),
    ),
    (
        "BenQ MOBIUZ EX2710U",
        '27" 4K IPS 144 Hz, HDMI 2.1, FreeSync Premium Pro',
        Decimal("549.99"),
    ),
    (
        "LG 34WP85C-B",
        '34" WQHD IPS Curved 160 Hz, USB-C 96 W, FreeSync',
        Decimal("799.99"),
    ),
    (
        "Samsung Odyssey OLED G9 49",
        '49" DQHD OLED 240 Hz, 0.03 ms, HDR True Black 400',
        Decimal("1799.99"),
    ),
    (
        "Philips 279M1RV",
        '27" 4K Nano IPS 144 Hz, HDMI 2.1, Ambiglow',
        Decimal("449.99"),
    ),
    (
        "Acer Predator X34 X",
        '34" WQHD IPS 180 Hz, HDMI 2.0, G-Sync, HDR400',
        Decimal("899.99"),
    ),
    (
        "ASUS ROG Swift OLED PG32UCDM",
        '32" 4K OLED 240 Hz, 0.03 ms, G-Sync Ultimate',
        Decimal("1299.99"),
    ),
    (
        "MSI MPG 321URX QD-OLED",
        '32" 4K QD-OLED 240 Hz, HDR True Black 400, HDMI 2.1',
        Decimal("1099.99"),
    ),
    (
        "Lenovo ThinkVision P32p-20",
        '32" 4K IPS 60 Hz, USB-C 135 W, factory calibrated',
        Decimal("799.99"),
    ),
    ("HP Z32k G3", '32" 4K IPS 60 Hz, USB-C 100 W, RJ-45', Decimal("699.99")),
    ("LG 27UK850-W", '27" 4K IPS 60 Hz, USB-C 60 W, HDR400', Decimal("399.99")),
    ("AOC 24G2SPU", '24" FHD IPS 165 Hz, 1 ms, FreeSync Premium', Decimal("199.99")),
    ("ViewSonic VX3276-4K-MHD", '32" 4K IPS 60 Hz, 4 ms, HDR400', Decimal("349.99")),
    (
        "Samsung Smart Monitor M8 32",
        '32" 4K VA 60 Hz, Smart TV apps, Webcam, USB-C 65 W',
        Decimal("699.99"),
    ),
    (
        "Dell S3222DGM",
        '32" QHD VA Curved 165 Hz, 1 ms, FreeSync Premium',
        Decimal("349.99"),
    ),
    (
        "ASUS TUF Gaming VG27AQ",
        '27" QHD IPS 165 Hz, 1 ms, HDR400, G-Sync Compatible',
        Decimal("329.99"),
    ),
    (
        "Gigabyte M27Q X",
        '27" QHD IPS 240 Hz, KVM switch, USB-C 18 W',
        Decimal("399.99"),
    ),
    (
        "LG 45GR95QE-B",
        '45" WQHD OLED Curved 240 Hz, 0.03 ms, G-Sync Compatible',
        Decimal("1199.99"),
    ),
    (
        "Alienware AW3225QF",
        '32" 4K OLED 240 Hz, 0.1 ms, G-Sync Compatible',
        Decimal("1399.99"),
    ),
    ("HP 24mh FHD", '24" FHD IPS 75 Hz, built-in speakers, VESA', Decimal("159.99")),
    ("BenQ EW2880U", '28" 4K IPS 60 Hz, USB-C 65 W, HDR400', Decimal("449.99")),
    (
        "Philips 246E9QDSB",
        '24" FHD IPS 75 Hz, Flicker-Free, Low Blue Light',
        Decimal("139.99"),
    ),
    (
        "AOC Q27G3XMN",
        '27" QHD Mini-LED 180 Hz, HDR1000, FreeSync Premium Pro',
        Decimal("499.99"),
    ),
    (
        "ASUS ProArt Display PA16DC",
        '15.6" 4K IPS Portable, USB-C, 99% DCI-P3',
        Decimal("699.99"),
    ),
    ("Arzopa Z1FC Portable", '13.3" FHD IPS 60 Hz, 1.1 kg, USB-C', Decimal("119.99")),
    (
        "Samsung Odyssey Ark 55",
        '55" 4K VA Curved 165 Hz, 1 ms, HDR10+, Multi-View',
        Decimal("2999.99"),
    ),
    (
        "LG DualUp 28MQ780-B",
        '27.6" SDQHD IPS 60 Hz, USB-C 96 W, vertical dual-screen',
        Decimal("599.99"),
    ),
    # ── Keyboards (20) ────────────────────────────────────────────────────────
    (
        "Logitech MX Keys S",
        "Wireless, backlit, scissor switches, multi-device, USB-C",
        Decimal("109.99"),
    ),
    (
        "Logitech G915 TKL",
        "Wireless TKL, low-profile GL Linear, RGB, 40 h battery",
        Decimal("219.99"),
    ),
    (
        "Keychron Q1 Pro",
        "75% wireless, hot-swap, Gateron G Pro Red, aluminium",
        Decimal("199.99"),
    ),
    (
        "Keychron K8 Pro",
        "TKL wireless, hot-swap, Gateron G Pro Brown, RGB",
        Decimal("109.99"),
    ),
    (
        "ASUS ROG Strix Flare II",
        "Full-size, Cherry MX Red, RGB, USB passthrough, detachable wrist rest",
        Decimal("149.99"),
    ),
    (
        "Razer BlackWidow V4 Pro",
        "Full-size wireless, Razer Green, Chroma RGB, media wheel",
        Decimal("229.99"),
    ),
    (
        "SteelSeries Apex Pro TKL",
        "TKL, adjustable OmniPoint 2.0, OLED display, PBT keycaps",
        Decimal("239.99"),
    ),
    (
        "Corsair K100 RGB",
        "Full-size, Cherry MX Speed, iCUE, axial scroll wheel",
        Decimal("229.99"),
    ),
    (
        "Das Keyboard 6 Professional",
        "Full-size, Cherry MX Blue, anodised aluminium, Omnitype",
        Decimal("199.99"),
    ),
    (
        "Ducky One 3 TKL",
        "TKL, hot-swap, Cherry MX Brown, double-shot PBT",
        Decimal("119.99"),
    ),
    (
        "GMMK Pro 75%",
        "75%, hot-swap Gateron Yellow, aluminium, knob, RGB",
        Decimal("169.99"),
    ),
    (
        "NuPhy Air75 V2",
        "75% wireless BT5.0, low-profile Gateron Red, RGB, 3000 mAh",
        Decimal("129.99"),
    ),
    (
        "Logitech MX Mechanical Mini",
        "Compact wireless, tactile quiet switches, backlit, metal",
        Decimal("129.99"),
    ),
    (
        "Microsoft Designer Compact",
        "Compact wireless BT, quiet keys, portrait number pad, USB-C",
        Decimal("69.99"),
    ),
    (
        "Apple Magic Keyboard Touch ID",
        "Wireless, scissor, Touch ID, USB-C, compact",
        Decimal("109.99"),
    ),
    (
        "Cherry MX Board 3.0S",
        "Full-size, Cherry MX Silent Red, aluminium top plate",
        Decimal("89.99"),
    ),
    (
        "HyperX Alloy Origins 65",
        "65% compact, HyperX Linear Red, RGB, detachable USB-C",
        Decimal("89.99"),
    ),
    (
        "Razer DeathStalker V2 Pro",
        "Full-size wireless, low-profile Linear Red, Chroma RGB, 50 h",
        Decimal("189.99"),
    ),
    (
        "Wooting 60HE",
        "60% analogue hall-effect, hot-swap, per-key actuation",
        Decimal("174.99"),
    ),
    (
        "HHKB Professional Hybrid Type-S",
        "60%, Topre 45 g silent, dual-mode BT/USB, PFU Limited",
        Decimal("349.99"),
    ),
    # ── Mice (20) ─────────────────────────────────────────────────────────────
    (
        "Logitech MX Master 3S",
        "Wireless BT, 8000 DPI, MagSpeed scroll, USB-C, 7 buttons",
        Decimal("99.99"),
    ),
    (
        "Logitech G Pro X Superlight 2",
        "Wireless, 32000 DPI Hero 2, 60 g, HERO sensor",
        Decimal("159.99"),
    ),
    (
        "Razer DeathAdder V3 HyperSpeed",
        "Wireless, Focus Pro 26K, 59 g, optical switches",
        Decimal("99.99"),
    ),
    (
        "SteelSeries Aerox 5 Wireless",
        "Wireless, 18000 DPI, 74 g, honeycomb, 9 buttons",
        Decimal("129.99"),
    ),
    (
        "Corsair M75 Air",
        "Wireless, 26000 DPI Marksman V2, 60 g, optical switches",
        Decimal("119.99"),
    ),
    (
        "Zowie EC2-CW",
        "Wireless, 3200 DPI, 77 g, plug-and-play, no software",
        Decimal("139.99"),
    ),
    ("Pulsar X2 Mini", "Wireless, 26000 DPI, 52 g, 1000 Hz polling", Decimal("94.99")),
    (
        "Endgame Gear XM2we",
        "Wireless, 26000 DPI, 63 g, BAMF 2.0 sensor",
        Decimal("89.99"),
    ),
    (
        "Asus ROG Gladius III AimPoint",
        "Wireless, 36000 DPI AimPoint, hot-swap switches, 79 g",
        Decimal("129.99"),
    ),
    (
        "Razer Naga V2 HyperSpeed",
        "Wireless MMO, 30000 DPI Focus Pro, 19 buttons, 100 g",
        Decimal("129.99"),
    ),
    (
        "Microsoft Arc Mouse",
        "Wireless BT, 1800 DPI, ultra-flat, Arc bend to on/off",
        Decimal("79.99"),
    ),
    (
        "Apple Magic Mouse",
        "Wireless BT, Multi-Touch surface, USB-C charging, 99 g",
        Decimal("79.99"),
    ),
    (
        "Logitech MX Anywhere 3S",
        "Wireless BT, 8000 DPI, MagSpeed scroll, compact travel",
        Decimal("59.99"),
    ),
    (
        "Glorious Model O 2 Wireless",
        "Wireless, 26000 DPI, 59 g, honeycomb, 69 h battery",
        Decimal("89.99"),
    ),
    (
        "LAMZU Atlantis Mini Pro V2",
        "Wireless, PAW3395, 48 g, optical switches, 1000 Hz",
        Decimal("79.99"),
    ),
    (
        "Logitech G502 X Plus",
        "Wireless, 25600 DPI Hero, 89 g, 13 buttons, LIGHTFORCE switches",
        Decimal("149.99"),
    ),
    (
        "HyperX Pulsefire Haste 2 Wireless",
        "Wireless, 26000 DPI, 61 g, honeycomb shell",
        Decimal("79.99"),
    ),
    (
        "Alienware Pro Wireless",
        "Wireless, 26000 DPI, 80 g, CHERRY optical, 35 h",
        Decimal("99.99"),
    ),
    (
        "Roccat Kone Pro Air",
        "Wireless, 19000 DPI, 75 g, Titan optical switch",
        Decimal("99.99"),
    ),
    (
        "Xiaomi Wireless Mouse 2",
        "Wireless 2.4 GHz, 1200 DPI, 98 g, 18-month battery",
        Decimal("19.99"),
    ),
    # ── Storage (20) ──────────────────────────────────────────────────────────
    (
        "Samsung 990 Pro 2 TB NVMe",
        "PCIe 4.0 M.2, 7450/6900 MB/s, MLC, 5-year warranty",
        Decimal("139.99"),
    ),
    (
        "WD Black SN850X 2 TB",
        "PCIe 4.0 M.2, 7300/6600 MB/s, 5-year warranty",
        Decimal("129.99"),
    ),
    (
        "Crucial T705 2 TB NVMe",
        "PCIe 5.0 M.2, 14500/12700 MB/s, 5-year warranty",
        Decimal("199.99"),
    ),
    (
        "Seagate FireCuda 530 4 TB",
        "PCIe 4.0 M.2, 7300/6900 MB/s, 5-year warranty",
        Decimal("299.99"),
    ),
    (
        "Kingston NV3 1 TB NVMe",
        "PCIe 4.0 M.2, 6000/4000 MB/s, budget NVMe",
        Decimal("59.99"),
    ),
    (
        "Samsung 870 EVO 2 TB SATA",
        '2.5" SATA 6 Gb/s, 560/530 MB/s, MLC V-NAND',
        Decimal("149.99"),
    ),
    (
        "Crucial MX500 1 TB SATA",
        '2.5" SATA 6 Gb/s, 560/510 MB/s, 5-year warranty',
        Decimal("79.99"),
    ),
    (
        "WD Blue 2 TB HDD",
        '3.5" SATA 5400 rpm, 256 MB cache, 2-year warranty',
        Decimal("59.99"),
    ),
    (
        "Seagate BarraCuda 4 TB HDD",
        '3.5" SATA 5400 rpm, 256 MB cache',
        Decimal("79.99"),
    ),
    (
        "WD Red Plus 8 TB NAS HDD",
        '3.5" SATA 5640 rpm, CMR, 3-year warranty',
        Decimal("179.99"),
    ),
    (
        "Samsung T7 Shield 2 TB External",
        "USB 3.2 Gen 2, IP65, 1050/1000 MB/s, 3-year warranty",
        Decimal("149.99"),
    ),
    (
        "WD My Passport 5 TB External",
        'USB 3.0, hardware AES-256, compact 2.5"',
        Decimal("119.99"),
    ),
    (
        "Seagate Expansion 8 TB External",
        'USB 3.0, 3.5", plug-and-play',
        Decimal("149.99"),
    ),
    (
        "SanDisk Extreme Pro Portable 4 TB",
        "USB 3.2 Gen 2, 2000/1800 MB/s, IP55",
        Decimal("299.99"),
    ),
    (
        "Synology DS923+ NAS",
        "4-bay, Ryzen R1600, 4 GB ECC, 2x M.2 NVMe, 2x 2.5 GbE",
        Decimal("599.99"),
    ),
    ("QNAP TS-464 NAS", "4-bay, N5105, 8 GB, 2x M.2 NVMe, 2.5 GbE", Decimal("499.99")),
    (
        "Lexar NM800 Pro 1 TB NVMe",
        "PCIe 4.0 M.2, 7500/6300 MB/s, heatsink included",
        Decimal("79.99"),
    ),
    (
        "Transcend JetFlash 930C 256 GB",
        "USB 3.2 Gen 1 / USB-C dual, 100/85 MB/s",
        Decimal("29.99"),
    ),
    (
        "Samsung 980 Pro 1 TB NVMe",
        "PCIe 4.0 M.2, 7000/5100 MB/s, V-NAND MLC",
        Decimal("79.99"),
    ),
    (
        "PNY XLR8 CS3140 2 TB NVMe",
        "PCIe 4.0 M.2, 7500/6850 MB/s, heatsink",
        Decimal("119.99"),
    ),
    # ── RAM (15) ──────────────────────────────────────────────────────────────
    (
        "Kingston FURY Beast 32 GB DDR5-5600",
        "2x 16 GB, CL40, XMP 3.0, black heatspreader",
        Decimal("79.99"),
    ),
    (
        "Corsair Vengeance 64 GB DDR5-6000",
        "2x 32 GB, CL30, XMP 3.0, AMD EXPO, black",
        Decimal("159.99"),
    ),
    (
        "G.Skill Trident Z5 RGB 32 GB DDR5-7200",
        "2x 16 GB, CL34, XMP 3.0, RGB",
        Decimal("129.99"),
    ),
    (
        "Crucial Pro 32 GB DDR5-5600",
        "2x 16 GB, CL46, plug-and-play, JEDEC",
        Decimal("69.99"),
    ),
    (
        "Team T-Force Vulcan 64 GB DDR5-6400",
        "2x 32 GB, CL32, AMD EXPO, XMP 3.0",
        Decimal("139.99"),
    ),
    (
        "Kingston FURY Beast 32 GB DDR4-3200",
        "2x 16 GB, CL16, XMP 2.0, aluminium heatspreader",
        Decimal("59.99"),
    ),
    (
        "Corsair Vengeance LPX 16 GB DDR4-3200",
        "2x 8 GB, CL16, XMP 2.0, low-profile",
        Decimal("39.99"),
    ),
    (
        "G.Skill Ripjaws V 32 GB DDR4-3600",
        "2x 16 GB, CL16, XMP 2.0, red heatspreader",
        Decimal("69.99"),
    ),
    (
        "Crucial 32 GB DDR4-3200",
        "2x 16 GB, CL22, JEDEC, Micron cells",
        Decimal("49.99"),
    ),
    (
        "Samsung SO-DIMM 16 GB DDR4-3200",
        "1x 16 GB laptop RAM, 1.2 V, bulk",
        Decimal("29.99"),
    ),
    (
        "Crucial SO-DIMM 32 GB DDR5-4800",
        "2x 16 GB laptop RAM, CL40, JEDEC",
        Decimal("69.99"),
    ),
    (
        "Kingston FURY Impact 32 GB DDR5-5600",
        "2x 16 GB SO-DIMM, CL40, XMP 3.0, laptop",
        Decimal("79.99"),
    ),
    (
        "G.Skill Trident Z5 RGB 96 GB DDR5-6800",
        "2x 48 GB, CL34, XMP 3.0, RGB, extreme capacity",
        Decimal("249.99"),
    ),
    (
        "Corsair Dominator Titanium RGB 64 GB DDR5-7200",
        "2x 32 GB, CL34, RGB, DHX cooling",
        Decimal("299.99"),
    ),
    (
        "TeamGroup T-Force Cardea A440 Pro 2 TB",
        "PCIe 4.0 M.2, 7400/7000 MB/s, DRAM cache",
        Decimal("129.99"),
    ),
    # ── Graphics Cards (15) ───────────────────────────────────────────────────
    (
        "NVIDIA GeForce RTX 4060 8 GB",
        "ASUS Dual OC, GDDR6, HDMI 2.1a, 3x DP 1.4a, 115 W",
        Decimal("329.99"),
    ),
    (
        "NVIDIA GeForce RTX 4070 12 GB",
        "MSI Ventus 3X OC, GDDR6X, 200 W, DLSS 3",
        Decimal("599.99"),
    ),
    (
        "NVIDIA GeForce RTX 4070 Super 12 GB",
        "Gigabyte Gaming OC, GDDR6X, 220 W, DLSS 3",
        Decimal("649.99"),
    ),
    (
        "NVIDIA GeForce RTX 4070 Ti Super 16 GB",
        "ASUS TUF OC, GDDR6X, 285 W, DLSS 3.5",
        Decimal("829.99"),
    ),
    (
        "NVIDIA GeForce RTX 4080 Super 16 GB",
        "MSI Suprim X, GDDR6X, 320 W, DLSS 3.5",
        Decimal("1049.99"),
    ),
    (
        "NVIDIA GeForce RTX 4090 24 GB",
        "ASUS ROG Strix OC, GDDR6X, 450 W, DLSS 3.5",
        Decimal("1899.99"),
    ),
    (
        "AMD Radeon RX 7600 8 GB",
        "PowerColor Fighter, GDDR6, 165 W, FSR 3.0",
        Decimal("269.99"),
    ),
    (
        "AMD Radeon RX 7700 XT 12 GB",
        "XFX Speedster QICK 319, GDDR6, 245 W, FSR 3.0",
        Decimal("399.99"),
    ),
    (
        "AMD Radeon RX 7800 XT 16 GB",
        "Sapphire Pulse, GDDR6, 263 W, FSR 3.0",
        Decimal("479.99"),
    ),
    (
        "AMD Radeon RX 7900 GRE 16 GB",
        "MSI Gaming X Trio, GDDR6, 260 W, FSR 3.0",
        Decimal("549.99"),
    ),
    (
        "AMD Radeon RX 7900 XT 20 GB",
        "ASUS TUF OC, GDDR6, 315 W, FSR 3.0",
        Decimal("799.99"),
    ),
    (
        "AMD Radeon RX 7900 XTX 24 GB",
        "Sapphire Nitro+, GDDR6, 355 W, FSR 3.0",
        Decimal("999.99"),
    ),
    (
        "Intel Arc A770 16 GB",
        "ASRock Challenger OC, GDDR6, 225 W, XeSS",
        Decimal("329.99"),
    ),
    (
        "NVIDIA RTX 4000 SFF Ada 20 GB",
        "Professional workstation, GDDR6, 70 W, low-profile",
        Decimal("1299.99"),
    ),
    (
        "AMD Radeon Pro W7900 48 GB",
        "Workstation, GDDR6, ECC, 295 W, 6x mDP",
        Decimal("3999.99"),
    ),
    # ── Networking (15) ───────────────────────────────────────────────────────
    (
        "TP-Link Archer BE800 WiFi 7 Router",
        "Tri-band, 19000 Mbps, 2.5 GbE WAN+LAN, 4x GbE",
        Decimal("349.99"),
    ),
    (
        "ASUS RT-AXE7800 WiFi 6E Router",
        "Tri-band 6E, 7800 Mbps, 2.5 GbE, AiMesh",
        Decimal("299.99"),
    ),
    (
        "Netgear Orbi 960 Mesh WiFi 6E",
        "Tri-band 6E, 2-pack, 10 GbE, 10000 Mbps",
        Decimal("899.99"),
    ),
    (
        "TP-Link Deco XE75 Pro Mesh 3-pack",
        "WiFi 6E, 11000 Mbps, 2.5 GbE, AI roaming",
        Decimal("399.99"),
    ),
    (
        "Ubiquiti UniFi Dream Machine Pro",
        "Rack 1U, 10 GbE SFP+, 4x GbE, UniFi controller",
        Decimal("499.99"),
    ),
    (
        "Ubiquiti UniFi AP U6 Pro",
        "WiFi 6 4x4, 5.3 Gbps, 300+ clients, PoE",
        Decimal("179.99"),
    ),
    (
        "TP-Link TL-SG108E 8-port Switch",
        "8x GbE, smart managed, VLAN, QoS, metal",
        Decimal("39.99"),
    ),
    (
        "Netgear GS308E 8-port Switch",
        "8x GbE, smart managed, VLAN, QoS",
        Decimal("49.99"),
    ),
    (
        "ASUS ZenWiFi Pro ET12 3-pack",
        "WiFi 6E, 10 Gbps backhaul, 11000 Mbps, 2.5 GbE",
        Decimal("699.99"),
    ),
    (
        "TP-Link Archer TX3000E WiFi 6 PCIe",
        "AX3000, PCIe adapter, Bluetooth 5.0, heat sink",
        Decimal("49.99"),
    ),
    (
        "Intel AX210 WiFi 6E M.2 Card",
        "AX5400, 6 GHz, Bluetooth 5.3, M.2 2230",
        Decimal("29.99"),
    ),
    (
        "Netgear Nighthawk RAXE500 WiFi 6E",
        "Tri-band 6E, 10.8 Gbps, 6x GbE + 2.5 GbE WAN",
        Decimal("399.99"),
    ),
    (
        "Synology RT6600ax Router",
        "Quad-band WiFi 6, 6600 Mbps, 2.5 GbE, VPN, SRM",
        Decimal("399.99"),
    ),
    (
        "MikroTik RB5009UG+S+IN",
        "8x GbE, 1x SFP+, 2.5 GbE, RouterOS, rack/desktop",
        Decimal("199.99"),
    ),
    (
        "D-Link DGS-1100-08P PoE Switch",
        "8x GbE PoE+, 65 W budget, smart managed",
        Decimal("79.99"),
    ),
    # ── Webcams & Audio (15) ──────────────────────────────────────────────────
    (
        "Logitech Brio 4K Pro",
        "4K 60 fps, HDR, Windows Hello, USB-C, 90° FOV",
        Decimal("199.99"),
    ),
    (
        "Logitech MX Brio 705 for Business",
        "4K 30 fps, AI framing, 90° FOV, USB-C, USB-A",
        Decimal("249.99"),
    ),
    (
        "Elgato Facecam Pro",
        "4K 60 fps, Sony sensor, USB-C, no compression, OBS integration",
        Decimal("299.99"),
    ),
    (
        "Razer Kiyo Pro Ultra",
        "4K 30 fps / 1080p 60 fps, Sony Starvis 2, USB-C",
        Decimal("279.99"),
    ),
    (
        "Microsoft Modern Webcam",
        "1080p 30 fps, 78° FOV, privacy shutter, Windows Hello",
        Decimal("69.99"),
    ),
    (
        "Insta360 Link 2",
        '4K 30 fps, AI tracking, gesture control, 1/1.5" Sony sensor',
        Decimal("249.99"),
    ),
    (
        "Sony WH-1000XM5 Headphones",
        "Wireless BT 5.2, ANC, 30 h, USB-C, foldable",
        Decimal("299.99"),
    ),
    (
        "Apple AirPods Pro 2 USB-C",
        "ANC, Transparency, Personalized Spatial Audio, USB-C case",
        Decimal("249.99"),
    ),
    (
        "Bose QuietComfort 45",
        "Wireless BT, ANC, 24 h, dual microphone",
        Decimal("279.99"),
    ),
    (
        "Jabra Evolve2 85 MS Wireless",
        "ANC, 40 h, Jabra Link 380c USB-C, Microsoft Teams",
        Decimal("449.99"),
    ),
    (
        "Elgato Wave:3",
        "USB-C condenser, cardioid, Clipguard, Wave Link software",
        Decimal("149.99"),
    ),
    (
        "Blue Yeti X",
        "USB condenser, 4 polar patterns, LED meter, Blue VO!CE",
        Decimal("139.99"),
    ),
    (
        "HyperX QuadCast S",
        "USB condenser, RGB, anti-vibration mount, 4 polar patterns",
        Decimal("149.99"),
    ),
    (
        "Rode NT-USB+",
        "USB-C condenser, 32-bit float, headphone monitoring, DSP",
        Decimal("189.99"),
    ),
    (
        "Samsung Galaxy Buds3 Pro",
        "ANC, 360 Audio, Intelligent ANC, 6 + 18 h",
        Decimal("229.99"),
    ),
]


async def seed():
    engine = create_async_engine(DATABASE_URL, echo=False)
    session_factory = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with session_factory() as session:
        for name, description, price in PRODUCTS:
            product = Product(name=name, description=description, price=price)
            session.add(product)
        await session.commit()

    await engine.dispose()
    print(f"✓ Seeded {len(PRODUCTS)} products.")


if __name__ == "__main__":
    asyncio.run(seed())
