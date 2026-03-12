FROM php:8.2-apache

# ── ติดตั้ง dependencies สำหรับ OCI8 ──────────────────────────────
RUN apt-get update && apt-get install -y \
    wget unzip libaio1t64 \
    && rm -rf /var/lib/apt/lists/* \
    && ln -sf /usr/lib/x86_64-linux-gnu/libaio.so.1t64 /usr/lib/x86_64-linux-gnu/libaio.so.1

# ── ดาวน์โหลด Oracle Instant Client (Basic + SDK) ─────────────────
RUN mkdir -p /opt/oracle && cd /opt/oracle \
    && wget -q https://download.oracle.com/otn_software/linux/instantclient/2113000/instantclient-basic-linux.x64-21.13.0.0.0dbru.zip \
    && wget -q https://download.oracle.com/otn_software/linux/instantclient/2113000/instantclient-sdk-linux.x64-21.13.0.0.0dbru.zip \
    && unzip -q instantclient-basic-linux.x64-21.13.0.0.0dbru.zip \
    && unzip -q instantclient-sdk-linux.x64-21.13.0.0.0dbru.zip \
    && rm -f *.zip

# ── ตั้งค่า LD path สำหรับ OCI libs ──────────────────────────────
RUN IC_DIR=$(ls -d /opt/oracle/instantclient_*) \
    && echo "$IC_DIR" > /etc/ld.so.conf.d/oracle-instantclient.conf \
    && ldconfig

# ── ติดตั้ง PHP OCI8 extension ────────────────────────────────────
RUN IC_DIR=$(ls -d /opt/oracle/instantclient_*) \
    && echo "instantclient,$IC_DIR" | pecl install oci8 \
    && docker-php-ext-enable oci8

# ── เปิด mod_rewrite ───────────────────────────────────────────────
RUN a2enmod rewrite

# ── Copy source code เข้า container ──────────────────────────────
COPY www/ /var/www/html/

# ── สิทธิ์ไฟล์ ────────────────────────────────────────────────────
RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html

EXPOSE 80
