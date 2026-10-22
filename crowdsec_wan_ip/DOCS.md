# CrowdSec WAN IP Updater

Add-on para Home Assistant que detecta periódicamente cambios en tu IP pública (WAN) y notifica a tu VPS para actualizar de forma inmediata la lista blanca de CrowdSec, previniendo baneos accidentales.

## Modos de funcionamiento

### 1. Modo SSH (Recomendado con comando forzado)

Ejecuta el script de actualización en el VPS mediante SSH autenticado con clave privada restringida en `authorized_keys` con `command="/usr/local/bin/update-crowdsec-whitelist"`.

1. Coloca tu clave privada en Home Assistant (ej. `/config/crowdsec_wan_ip_ssh_key`) con permisos adecuados.
2. Configura en las opciones del add-on:
   - `update_mode`: `ssh`
   - `ssh_host`: `<IP_O_DOMINIO_DEL_VPS>`
   - `ssh_port`: `22`
   - `ssh_user`: `root` (o el usuario con la clave restringida)
   - `ssh_key_path`: `/config/crowdsec_wan_ip_ssh_key`
   - `ssh_command`: `update-crowdsec-whitelist`

### 2. Modo Webhook

Envía una petición HTTP `POST` JSON al endpoint configurado en el VPS con el formato:

```json
{
  "old_ip": "203.0.113.10",
  "new_ip": "198.51.100.5",
  "timestamp": "2026-10-22T20:00:00+00:00"
}
```

## Opciones de configuración

| Opción | Descripción | Por defecto |
|--------|-------------|-------------|
| `check_interval_minutes` | Frecuencia de comprobación en minutos (1-1440) | `5` |
| `resolver_urls` | Lista de servicios para resolver la IP pública | ipify, ifconfig.me, icanhazip.com |
| `update_mode` | `ssh` o `webhook` | `ssh` |
| `notify_on_initial_run` | Enviar la IP en el primer arranque | `true` |
| `ssh_host` | Host / IP del servidor VPS | `""` |
| `ssh_port` | Puerto SSH | `22` |
| `ssh_user` | Usuario SSH | `root` |
| `ssh_key_path` | Ruta a la clave privada dentro de HA | `/config/crowdsec_wan_ip_ssh_key` |
| `ssh_command` | Comando remoto a ejecutar | `update-crowdsec-whitelist` |
| `webhook_url` | URL del webhook remoto (modo webhook) | `""` |
| `webhook_token` | Token Bearer para autenticación (opcional) | `""` |
