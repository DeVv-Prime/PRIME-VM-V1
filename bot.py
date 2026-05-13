{
  "bot_config": {
    "version": "5.0.0",
    "name": "NEXVM-V1",
    "prefix": ".",
    "author": "DeVv-Prime",
    "main_admin_ids": [1405866008127864852]
  },
  
  "discord_config": {
    "token": "discordbot",
    "status": "online",
    "activity_type": "watching",
    "activity_name": ".help | NEXVM-V1 | DeVv-Prime"
  },
  
  "server_config": {
    "storage_pool": "default",
    "backup_path": "/opt/nexvm-v1/backups",
    "logs_path": "/opt/nexvm-v1/logs",
    "data_path": "/opt/nexvm-v1/data"
  },
  
  "database_config": {
    "type": "sqlite",
    "path": "/opt/nexvm-v1/data/nexvm.db"
  },
  
  "vps_config": {
    "default_ram": 2,
    "default_cpu": 1,
    "default_disk": 20,
    "enable_nesting": true
  },
  
  "free_vps_plans": {
    "enabled": true,
    "plans": [
      {"name": "🥉 Bronze", "invites": 5, "ram": 2, "cpu": 1, "disk": 20},
      {"name": "🥈 Silver", "invites": 10, "ram": 4, "cpu": 2, "disk": 40},
      {"name": "🥇 Gold", "invites": 15, "ram": 8, "cpu": 4, "disk": 80}
    ]
  },
  
  "port_forwarding": {
    "enabled": true,
    "default_quota": 5,
    "port_range_start": 20000,
    "port_range_end": 50000
  },
  
  "ipv4_management": {
    "enabled": true,
    "price_inr": 50,
    "default_upi_id": "vedant1437@fam"
  },
  
  "ai_config": {
    "enabled": true,
    "api_key": "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",
    "model": "llama-3.3-70b-versatile"
  },
  
  "node_management": {
    "enabled": true,
    "main_node": "local",
    "config_file": "/opt/nexvm-v1/nodes.json"
  },
  
  "security_config": {
    "require_license": true,
    "license_keys": [
      "DeVv-Prime-Master", 
      "DEVVP-ROOT-ACCESS", 
      "PRIME-ADMIN-2025",
      "VEDANT-SUPER-KEY",
      "NEXVM-ENTERPRISE",
      "NEXVM-DEVELOPER",
      "NEXVM-TEAM",
      "NEXVM-CLUSTER"
    ],
    "upi_id": "vedant1437@fam",
    "discord_invite": "https://discord.gg/zS2ynbF6jK",
    "support_contact": "@DeVv-Prime"
  },
  
  "payment_config": {
    "enabled": true,
    "upi_id": "vedant1437@fam",
    "prices": {
      "developer": 499,
      "enterprise": 999,
      "team": 2499,
      "cluster": 9999
    },
    "currency": "INR",
    "payment_notes": "Send payment screenshot to @DeVv-Prime on Discord"
  },
  
  "support_config": {
    "discord_invite": "https://discord.gg/zS2ynbF6jK",
    "support_server": "NEXVM Support",
    "ticket_channel": "#create-ticket",
    "support_contacts": ["@DeVv-Prime", "@NEXVM-Support"],
    "faq_channel": "#faq",
    "announcements_channel": "#announcements"
  },
  
  "features": {
    "free_vps": true,
    "port_forwarding": true,
    "ipv4_sales": true,
    "ai_chat": true,
    "node_management": true,
    "panel_installation": true,
    "ssh_access": true,
    "console_commands": true,
    "upi_payments": true,
    "invite_system": true,
    "discord_tickets": true,
    "payment_qr": true,
    "license_verification": true
  },
  
  "embeds": {
    "thumbnail_url": "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg",
    "footer_text": "NEXVM-V1 | Made by DeVv-Prime with ❤️",
    "footer_icon": "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg"
  },
  
  "license_info": {
    "version": "1.0.0",
    "release_date": "March 2025",
    "developer": "DeVv-Prime",
    "website": "https://discord.gg/zS2ynbF6jK",
    "github": "https://github.com/DeVv-Prime/NexVM",
    "copyright": "© 2025 DeVv-Prime. All rights reserved."
  }
}
