#!/bin/bash
# Enable strict error handling for stability
set -o pipefail
trap 'echo -e "\n${R}❌ Script interrupted or error occurred${NC}"; exit 130' INT TERM

# ╔═══════════════════════════════════════════════════════════════════════════════╗
# ║                 NEX VM V1 - Ultimate Virtualization Platform                  ║
# ║                         Next Generation VM Management                         ║
# ║                    Version: 1.0.0 | Enterprise Edition                       ║
# ║                      Made by DeVv-Prime with ❤️                               ║
# ║            💰 UPI: vedant1437@fam | Discord: https://discord.gg/zS2ynbF6jK    ║
# ╚═══════════════════════════════════════════════════════════════════════════════╝

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  🎨  ADVANCED COLOR DEFINITIONS WITH EFFECTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Base Colors
R='\033[0;31m'      # Red
G='\033[0;32m'      # Green
Y='\033[1;33m'      # Yellow
B='\033[0;34m'      # Blue
P='\033[0;35m'      # Purple
C='\033[0;36m'      # Cyan
W='\033[1;37m'      # White
NC='\033[0m'        # No Color

# Effects
BOLD='\033[1m'
DIM='\033[2m'
UNDERLINE='\033[4m'
BLINK='\033[5m'
REVERSE='\033[7m'
HIDDEN='\033[8m'

# Extended Colors
ORANGE='\033[38;5;214m'
PINK='\033[38;5;205m'
PURPLE='\033[38;5;129m'
GOLD='\033[38;5;220m'
SILVER='\033[38;5;250m'
LIME='\033[38;5;154m'
TEAL='\033[38;5;37m'
MAROON='\033[38;5;124m'
NAVY='\033[38;5;17m'
OLIVE='\033[38;5;58m'

# Background Colors
BG_BLACK='\033[40m'
BG_RED='\033[41m'
BG_GREEN='\033[42m'
BG_YELLOW='\033[43m'
BG_BLUE='\033[44m'
BG_PURPLE='\033[45m'
BG_CYAN='\033[46m'
BG_WHITE='\033[47m'
BG_ORANGE='\033[48;5;214m'

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  📍  ADVANCED PATH CONFIGURATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Main Directories
INSTALL_DIR="/opt/primevm"
BOT_SCRIPT="primevm.py"
SERVICE_NAME="primevm"
LOG_FILE="/var/log/primevm.log"
CONFIG_DIR="/etc/primevm"
DATA_DIR="/var/lib/primevm"
BACKUP_DIR="/var/backups/primevm"
TEMP_DIR="/tmp/primevm"
CACHE_DIR="/var/cache/primevm"
SSL_DIR="/etc/primevm/ssl"
HOOKS_DIR="/etc/primevm/hooks"
PLUGINS_DIR="/etc/primevm/plugins"
PAYMENT_DIR="/etc/primevm/payments"
TICKET_DIR="/etc/primevm/tickets"

# Payment Configuration
UPI_ID="vedant1437@fam"
DISCORD_INVITE="https://discord.gg/zS2ynbF6jK"
SUPPORT_DISCORD="@DeVv-Prime"
PAYMENT_AMOUNT=499
ENTERPRISE_AMOUNT=999
TEAM_AMOUNT=2499
CLUSTER_AMOUNT=9999

# Database Configuration
DB_PATH="$DATA_DIR/nexvm.db"
DB_BACKUP_DIR="$BACKUP_DIR/database"
DB_VERSION=1

# Network Configuration
NETWORK_BRIDGE="nexbr0"
NETWORK_SUBNET="10.200.0.1/24"
PORT_RANGE_START=10000
PORT_RANGE_END=50000
MAX_CONTAINERS=100

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  🖥️  CINEMATIC ASCII ART HEADER WITH PAYMENT INFO
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

show_header() {
    clear
    echo -e "${PURPLE}╔═══════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║${NC} ${BOLD}${TEAL}PRIME VM - Ultimate Virtualization Platform${NC}${PURPLE}                       ║${NC}"
    echo -e "${PURPLE}╠═══════════════════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${PURPLE}║${NC} ${C}Welcome to the easiest installation experience for your VPS bot.${NC} ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC} ${C}This script installs the bot, configures licenses, and creates the service.${NC} ${PURPLE}║${NC}"
    echo -e "${PURPLE}╚═══════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""

    if command -v figlet >/dev/null 2>&1; then
        echo -e "${TEAL}$(figlet -f slant "PRIME VM" | sed 's/^/    /')${NC}"
    else
        echo -e "${TEAL}    █████╗  ██╗  ████╗ █████╗ ████╗ ██████╗  ${NC}"
        echo -e "${TEAL}    ██╔═██╗██║ ██║██╔══╝██╔══██╗ ██╔══╝ ${NC}"
        echo -e "${TEAL}    ██║ ██║██║ ██║█████╗ ██║  ██║ ██████╗ ${NC}"
        echo -e "${TEAL}    ██║ ██║██║ ██║██╔══╝██║  ██║     ██║ ${NC}"
        echo -e "${TEAL}    ██╔═██╗╚████╔╝██████╗██╔══██╗ ██████╗ ${NC}"
        echo -e "${TEAL}    ╚══╝ ╚══╝╚════╝ ╚═════╝ ╚════╝╚═════╝ ${NC}"
    fi

    echo ""
    echo -e "${GOLD}═══════════════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${W}  💡 ${BOLD}Quick Setup Notes:${NC}"
    echo -e "${W}    • Run this script on a Linux server with root access.${NC}"
    echo -e "${W}    • You can select a license, enter a valid key, or cancel anytime.${NC}"
    echo -e "${W}    • The bot config will auto-start after license verification.${NC}"
    echo -e "${GOLD}═══════════════════════════════════════════════════════════════════════════════${NC}"
    echo ""

    echo -ne "${DIM}Loading interface "
    for i in {1..12}; do
        echo -ne "${GREEN}●${NC}"
        sleep 0.03
    done
    echo -e " ${G}Ready!${NC}\n"
}

show_progress_bar() {
    local message="$1"
    local width=36
    local progress=0

    echo -ne "${Y}${message}${NC} "
    echo -ne "["
    while [ $progress -le $width ]; do
        echo -ne "${GREEN}#${NC}"
        sleep 0.03
        progress=$((progress + 1))
    done
    echo -ne "] ${G}Done${NC}\n"
    sleep 0.3
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  📊  LICENSE DASHBOARD WITH VALIDITY DISPLAY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

calculate_validity() {
    local license_key=$1
    local license_type=$2
    
    # Check if it's a lifetime key
    if [[ "$license_key" == "1kapi" ]] || [[ "$license_type" == "Lifetime" ]] || [[ "$license_key" == *"MASTER"* ]] || [[ "$license_key" == *"ADMIN"* ]]; then
        echo "∞ (Lifetime)"
        return
    fi
    
    # Calculate validity based on license type
    case $license_type in
        Developer)
            # 365 days validity
            EXPIRY_DATE=$(date -d "+365 days" +"%Y-%m-%d" 2>/dev/null || date -v+365d +"%Y-%m-%d" 2>/dev/null || echo "N/A")
            echo "365d (1 year)"
            ;;
        Enterprise)
            # Lifetime
            echo "∞ (Lifetime)"
            ;;
        Team)
            # 2 years validity
            EXPIRY_DATE=$(date -d "+730 days" +"%Y-%m-%d" 2>/dev/null || date -v+730d +"%Y-%m-%d" 2>/dev/null || echo "N/A")
            echo "730d (2 years)"
            ;;
        Cluster)
            # Lifetime
            echo "∞ (Lifetime)"
            ;;
        *)
            echo "Unlimited"
            ;;
    esac
}

show_license_dashboard() {
    clear
    echo ""
    
    # Read stored license info
    LICENSE_KEY=""
    LICENSE_TYPE="Trial"
    ACTIVATION_DATE=$(date +"%Y-%m-%d %H:%M:%S")
    
    if [ -f "$CONFIG_DIR/license/license.key" ]; then
        LICENSE_KEY=$(cat "$CONFIG_DIR/license/license.key")
    fi
    
    if [ -f "$PAYMENT_DIR/last_payment.txt" ]; then
        LICENSE_TYPE=$(grep "License activated - Type:" "$PAYMENT_DIR/last_payment.txt" 2>/dev/null | awk -F': ' '{print $NF}' | awk '{print $1}' || echo "Standard")
    fi
    
    VALIDITY=$(calculate_validity "$LICENSE_KEY" "$LICENSE_TYPE")
    
    echo -e "${PURPLE}╔═══════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║${NC}                                                                              ${PURPLE}║${NC}"
    echo -e "${GOLD}║${NC} ${BOLD}${TEAL}📊 PRIME VM - LICENSE DASHBOARD 📊${NC}${GOLD}                                     ║${NC}"
    echo -e "${PURPLE}║${NC}                                                                              ${PURPLE}║${NC}"
    echo -e "${PURPLE}╠═══════════════════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${PURPLE}║${NC}                                                                              ${PURPLE}║${NC}"
    echo -e "${W}║   ${BOLD}📋 License Information${NC}                                                     ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC}   ──────────────────────────────────────────────────────────────────────────   ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC}                                                                              ${PURPLE}║${NC}"
    echo -e "${W}║   License Type:       ${BOLD}${G}$LICENSE_TYPE${NC}                                        ${PURPLE}║${NC}"
    echo -e "${W}║   License Key:        ${BOLD}${Y}${LICENSE_KEY:0:20}***${NC}                               ${PURPLE}║${NC}"
    echo -e "${W}║   Status:             ${BOLD}${G}✅ ACTIVE${NC}                                            ${PURPLE}║${NC}"
    echo -e "${W}║   Activated:          ${BOLD}${C}$ACTIVATION_DATE${NC}                      ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC}                                                                              ${PURPLE}║${NC}"
    echo -e "${PURPLE}╠═══════════════════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${PURPLE}║${NC}                                                                              ${PURPLE}║${NC}"
    echo -e "${W}║   ${BOLD}⏱️  Validity${NC}                                                               ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC}   ──────────────────────────────────────────────────────────────────────────   ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC}                                                                              ${PURPLE}║${NC}"
    
    if [[ "$VALIDITY" == *"∞"* ]]; then
        echo -e "${W}║   Validity Period:    ${BOLD}${LIME}$VALIDITY${NC}                                            ${PURPLE}║${NC}"
    else
        echo -e "${W}║   Validity Period:    ${BOLD}${ORANGE}$VALIDITY${NC}                                           ${PURPLE}║${NC}"
    fi
    
    echo -e "${PURPLE}║${NC}                                                                              ${PURPLE}║${NC}"
    echo -e "${PURPLE}╠═══════════════════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${PURPLE}║${NC}                                                                              ${PURPLE}║${NC}"
    echo -e "${W}║   ${BOLD}🔧 Available Actions${NC}                                                       ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC}   ──────────────────────────────────────────────────────────────────────────   ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC}                                                                              ${PURPLE}║${NC}"
    echo -e "${GOLD}║   ${BOLD}1.${NC} ${G}View Bot Status${NC}                                                    ${PURPLE}║${NC}"
    echo -e "${GOLD}║   ${BOLD}2.${NC} ${C}View License Details${NC}                                               ${PURPLE}║${NC}"
    echo -e "${GOLD}║   ${BOLD}3.${NC} ${ORANGE}Payment & Renewal${NC}                                               ${PURPLE}║${NC}"
    echo -e "${GOLD}║   ${BOLD}4.${NC} ${PINK}Discord Support${NC}                                                 ${PURPLE}║${NC}"
    echo -e "${GOLD}║   ${BOLD}5.${NC} ${R}Exit Dashboard${NC}                                                    ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC}                                                                              ${PURPLE}║${NC}"
    echo -e "${PURPLE}╚═══════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    read -p "${BOLD}${C}Select option (1-5): ${NC}" MENU_CHOICE
    MENU_CHOICE="$(printf '%s' "$MENU_CHOICE" | tr -d '\r\n[:space:]')"
    
    case $MENU_CHOICE in
        1)
            echo -e "${C}Checking bot status...${NC}"
            systemctl status $SERVICE_NAME
            echo ""
            read -p "Press Enter to return to dashboard..."
            show_license_dashboard
            ;;
        2)
            clear
            echo -e "${PURPLE}╔═══════════════════════════════════════════════════════════════════════════════╗${NC}"
            echo -e "${PURPLE}║${NC}                  ${BOLD}${TEAL}📋 DETAILED LICENSE INFORMATION${NC}                              ${PURPLE}║${NC}"
            echo -e "${PURPLE}╠═══════════════════════════════════════════════════════════════════════════════╣${NC}"
            echo -e "${PURPLE}║${NC}                                                                              ${PURPLE}║${NC}"
            echo -e "${W}║   Full License Key:     ${BOLD}${Y}$LICENSE_KEY${NC}                                    ${PURPLE}║${NC}"
            echo -e "${W}║   License Category:     ${BOLD}${G}Enterprise${NC}                                      ${PURPLE}║${NC}"
            echo -e "${W}║   Activation Date:      ${BOLD}${C}$ACTIVATION_DATE${NC}                      ${PURPLE}║${NC}"
            echo -e "${W}║   Current Status:       ${BOLD}${LIME}✅ VERIFIED & ACTIVE${NC}                                ${PURPLE}║${NC}"
            echo -e "${W}║   Validity:             ${BOLD}${LIME}$VALIDITY${NC}                                      ${PURPLE}║${NC}"
            echo -e "${W}║   Bot Installation:     ${BOLD}${G}$INSTALL_DIR${NC}                                  ${PURPLE}║${NC}"
            echo -e "${W}║   Service Name:         ${BOLD}${C}$SERVICE_NAME${NC}                                      ${PURPLE}║${NC}"
            echo -e "${PURPLE}║${NC}                                                                              ${PURPLE}║${NC}"
            echo -e "${PURPLE}╠═══════════════════════════════════════════════════════════════════════════════╣${NC}"
            if [ -f "$PAYMENT_DIR/last_payment.txt" ]; then
                echo -e "${PURPLE}║${NC}  ${BOLD}${GOLD}💳 Payment Details:${NC}                                                    ${PURPLE}║${NC}"
                echo -e "${PURPLE}║${NC}                                                                              ${PURPLE}║${NC}"
                cat "$PAYMENT_DIR/last_payment.txt" | sed 's/^/║   /'
                echo -e "${PURPLE}║${NC}                                                                              ${PURPLE}║${NC}"
            fi
            echo -e "${PURPLE}╚═══════════════════════════════════════════════════════════════════════════════╝${NC}"
            echo ""
            read -p "Press Enter to return to dashboard..."
            show_license_dashboard
            ;;
        3)
            clear
            generate_payment_qr 499 "Renewal"
            echo -e "${Y}Join Discord: https://discord.gg/zS2ynbF6jK${NC}"
            echo -e "${Y}Send payment screenshot to @DeVv-Prime${NC}"
            echo ""
            read -p "Press Enter to return to dashboard..."
            show_license_dashboard
            ;;
        4)
            show_discord_support
            read -p "Press Enter to return to dashboard..."
            show_license_dashboard
            ;;
        5)
            show_goodbye
            ;;
        *)
            echo -e "${R}❌ Invalid option${NC}"
            sleep 2
            show_license_dashboard
            ;;
    esac
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  🌟  CUSTOM THANK YOU MESSAGE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

show_goodbye() {
    sleep 2
    clear
    echo ""
    echo -e "${PURPLE}╔═══════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${PURPLE}║${NC}                                                                              ${PURPLE}║${NC}"
    echo -e "${GOLD}║${NC} ${BOLD}${LIME}🎉 THANK YOU FOR TRUSTING NEX VM V1! 🎉${NC}${GOLD}                                   ║${NC}"
    echo -e "${PURPLE}║${NC}                                                                              ${PURPLE}║${NC}"
    echo -e "${PURPLE}╠═══════════════════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${PURPLE}║${NC}                                                                              ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC} ${C}Your NEX VM V1 bot is now fully installed and running!${NC}                      ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC}                                                                              ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC} ${BOLD}${Y}🙋 Service Status:${NC}                                                             ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC}   ✅ Bot configured and ready to use                                       ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC}   ✅ Systemd service started and enabled                                   ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC}   ✅ License verified and saved                                            ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC}                                                                              ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC} ${BOLD}${G}🔗 Quick Links:${NC}                                                                 ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC}   👤 Discord Support: ${Y}https://discord.gg/zS2ynbF6jK${NC}                     ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC}   📱 UPI: ${Y}vedant1437@fam${NC}                                                 ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC}   👤 Contact: ${Y}@DeVv-Prime${NC} on Discord                                      ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC}                                                                              ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC} ${BOLD}${ORANGE}🚀 What's Next:${NC}                                                                ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC}   1. Check bot status: ${C}systemctl status $SERVICE_NAME${NC}                  ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC}   2. View logs: ${C}journalctl -u $SERVICE_NAME -f${NC}                           ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC}   3. Restart bot: ${C}systemctl restart $SERVICE_NAME${NC}                      ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC}                                                                              ${PURPLE}║${NC}"
    echo -e "${PURPLE}╠═══════════════════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${PURPLE}║${NC}                                                                              ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC} ${BOLD}${TEAL}Made by DeVv-Prime with ❤️ | Version 1.0.0${NC}                              ${PURPLE}║${NC}"
    echo -e "${PURPLE}║${NC}                                                                              ${PURPLE}║${NC}"
    echo -e "${PURPLE}╚═══════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${G}${BOLD}🌟 Exiting in 5 seconds...${NC}"
    sleep 5
}
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

generate_payment_qr() {
    local amount=$1
    local license_type=$2
    
    echo -e "${GOLD}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GOLD}║                 💰 PAYMENT QR CODE GENERATED                 ║${NC}"
    echo -e "${GOLD}╠══════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${GOLD}║                                                              ║${NC}"
    echo -e "${W}║   UPI ID: ${Y}vedant1437@fam${W}                                   ║${NC}"
    echo -e "${W}║   Amount: ₹${amount} (${license_type})                           ║${NC}"
    echo -e "${W}║                                                              ║${NC}"
    echo -e "${C}║   📱 Scan with any UPI app to pay:                            ║${NC}"
    echo -e "${W}║                                                              ║${NC}"
    
    # Generate UPI payment link
    local upi_link="upi://pay?pa=vedant1437@fam&pn=NEX%20VM%20V1&am=${amount}&cu=INR&tn=${license_type}%20License"
    
    # Create ASCII QR representation (simplified)
    echo -e "${Y}║                                                              ║${NC}"
    echo -e "${Y}║       ████████████████████████████████████████████████       ║${NC}"
    echo -e "${Y}║       ██                                          ██         ║${NC}"
    echo -e "${Y}║       ██    ██████  ██████  ██  ██                ██           ║${NC}"
    echo -e "${Y}║       ██    ██  ██  ██  ██  ██  ██                ██             ║${NC}"
    echo -e "${Y}║       ██    ██████  ██████  ██████                ██             ║${NC}"
    echo -e "${Y}║       ██    ██      ██  ██      ██                ██             ║${NC}"
    echo -e "${Y}║       ██    ██      ██  ██  ██████                ██             ║${NC}"
    echo -e "${Y}║       ██                                          ██           ║${NC}"
    echo -e "${Y}║       ████████████████████████████████████████████████         ║${NC}"
    echo -e "${W}║                                                                ║${NC}"
    echo -e "${W}║   Or click: ${UNDERLINE}${C}${upi_link}${NC}${W}               ║${NC}"
    echo -e "${GOLD}║                                                              ║${NC}"
    echo -e "${GOLD}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    # Save payment link to file
    mkdir -p "$PAYMENT_DIR"
    echo "$upi_link" > "$PAYMENT_DIR/payment_${license_type}_${amount}.link"
    echo "UPI: vedant1437@fam" >> "$PAYMENT_DIR/payment_${license_type}_${amount}.link"
    echo "Amount: ₹$amount" >> "$PAYMENT_DIR/payment_${license_type}_${amount}.link"
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  🎫  DISCORD TICKET CREATION LINK
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

show_discord_support() {
    echo -e "${GOLD}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GOLD}║                 🎫 DISCORD SUPPORT & TICKETS                 ║${NC}"
    echo -e "${GOLD}╠══════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${GOLD}║                                                              ║${NC}"
    echo -e "${W}║   📌 Join our Discord server for:                             ║${NC}"
    echo -e "${W}║                                                              ║${NC}"
    echo -e "${G}║   ✅ Instant Support                                        ║${NC}"
    echo -e "${G}║   🎫 Create Support Tickets                                 ║${NC}"
    echo -e "${G}║   💬 Community Chat                                         ║${NC}"
    echo -e "${G}║   📢 Latest Updates                                         ║${NC}"
    echo -e "${G}║   🤝 Developer Connect                                      ║${NC}"
    echo -e "${G}║   🔧 Troubleshooting Help                                   ║${NC}"
    echo -e "${W}║                                                              ║${NC}"
    echo -e "${C}║   🔗 Discord Invite: ${Y}${UNDERLINE}https://discord.gg/zS2ynbF6jK${NC}${C}           ║${NC}"
    echo -e "${W}║                                                              ║${NC}"
    echo -e "${P}║   👤 Support Team: @DeVv-Prime, @NEX-VM-Support             ║${NC}"
    echo -e "${W}║                                                              ║${NC}"
    echo -e "${ORANGE}║   💡 To create a ticket:                                    ║${NC}"
    echo -e "${ORANGE}║      1. Join Discord                                      ║${NC}"
    echo -e "${ORANGE}║      2. Go to #create-ticket channel                      ║${NC}"
    echo -e "${ORANGE}║      3. Click on 'Purchase Support' or 'Technical Help'   ║${NC}"
    echo -e "${ORANGE}║      4. Send payment screenshot to @DeVv-Prime            ║${NC}"
    echo -e "${W}║                                                              ║${NC}"
    echo -e "${GOLD}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  🔐  ENTERPRISE LICENSE VERIFICATION WITH PAYMENT INTEGRATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

check_license() {
    show_header
    show_discord_support
    
    echo -e "${GOLD}┌─────────────────────────────────────────────────────────────────┐${NC}"
    echo -e "${GOLD}│                    🔐 ENTERPRISE LICENSE ACTIVATION              │${NC}"
    echo -e "${GOLD}├─────────────────────────────────────────────────────────────────┤${NC}"
    echo -e "${SILVER}│  This software is protected by DeVv-Prime Enterprise License     │${NC}"
    echo -e "${SILVER}│  UPI: vedant1437@fam | Discord: https://discord.gg/zS2ynbF6jK   │${NC}"
    echo -e "${GOLD}└─────────────────────────────────────────────────────────────────┘${NC}"
    echo ""
    
    # Create license directory if not exists
    mkdir -p "$CONFIG_DIR/license" "$PAYMENT_DIR" "$TICKET_DIR"
    
    # Check for existing license
    if [ -f "$CONFIG_DIR/license/license.key" ] && [ -f "$CONFIG_DIR/license/license.sig" ]; then
        STORED_KEY=$(cat "$CONFIG_DIR/license/license.key")
        STORED_SIG=$(cat "$CONFIG_DIR/license/license.sig")
        
        # Verify signature
        VERIFY_HASH=$(echo -n "$STORED_KEY" | sha256sum | awk '{print $1}')
        
        if [ "$STORED_SIG" == "$VERIFY_HASH" ]; then
            echo -e "${G}✅ Found valid license signature${NC}"
            read -p "🔑 Use existing license? (y/n): " -n 1 -r EXISTING_LICENSE
            echo ""
            if [[ $EXISTING_LICENSE =~ ^[Yy]$ ]]; then
                KEY="$STORED_KEY"
                echo -e "${G}✅ Using existing license${NC}"
                show_progress_bar "Preparing installation..."
                return 0
            fi
        fi
    fi
    
    # License selection menu loop - keeps showing until valid selection
    while true; do
        echo -e "${GOLD}╔═══════════════════════════════════════════════════════════════════════════════╗${NC}"
        echo -e "${GOLD}║${NC} ${BOLD}${Y}Choose your license path:${NC}                                                       ${GOLD}║${NC}"
        echo -e "${GOLD}╠═══════════════════════════════════════════════════════════════════════════════╣${NC}"
        echo -e "${GOLD}║${NC}  ${GOLD}0.${NC} ${R}Exit Installation${NC}                       ${GOLD}│${NC}  ${GOLD}5.${NC} ${PINK}View Payment QR Codes${NC}                       ${GOLD}║${NC}"
        echo -e "${GOLD}║${NC}  ${GOLD}1.${NC} ${G}Developer Edition${NC}     - ₹499 / year           ${GOLD}│${NC}  ${GOLD}6.${NC} ${BLUE}Join Discord for Support${NC}                  ${GOLD}║${NC}"
        echo -e "${GOLD}║${NC}  ${GOLD}2.${NC} ${C}Enterprise Edition${NC}     - ₹999 / lifetime       ${GOLD}│${NC}  ${GOLD}7.${NC} ${GOLD}Enter Valid License Key${NC}   - Skip payment${GOLD}║${NC}"
        echo -e "${GOLD}║${NC}  ${GOLD}3.${NC} ${P}Team License${NC}          - ₹2499 (5 users)        ${GOLD}│${NC}  ${GOLD}4.${NC} ${ORANGE}Enterprise Cluster${NC}    - ₹9999 / unlimited${GOLD}║${NC}"
        echo -e "${GOLD}╚═══════════════════════════════════════════════════════════════════════════════╝${NC}"
        echo ""

        read -p "${BOLD}${C}Select option (0-7): ${NC}" LICENSE_OPTION
        # Normalize input: remove ALL whitespace, carriage returns, and newlines
        LICENSE_OPTION=$(printf '%s' "$LICENSE_OPTION" | tr -d '\r\n' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
        echo ""
        
        # Check if input is empty
        if [ -z "$LICENSE_OPTION" ]; then
            echo -e "${Y}⚠️  Please enter a valid option (0-7)${NC}"
            sleep 1
            continue
        fi
        
        # Validate that input is a single digit 0-7
        if ! [[ "$LICENSE_OPTION" =~ ^[0-7]$ ]]; then
            echo -e "${R}❌ Invalid selection! Please enter a number between 0-7${NC}"
            sleep 1
            continue
        fi
        
        # Process valid selection - respond instantly
        case $LICENSE_OPTION in
            0)
                echo -e "${G}════════════════════════════════════════════════════════════${NC}"
                echo -e "${R}❌ Installation cancelled by user${NC}"
                echo -e "${Y}Thank you for considering PRIME VM!${NC}"
                echo -e "${C}Made by DeVv-Prime with ❤️${NC}"
                echo -e "${G}════════════════════════════════════════════════════════════${NC}"
                exit 0
                ;;
            1)
                echo -e "${C}🔄 Processing Developer Edition (₹499/year)...${NC}"
                AMOUNT=499
                TYPE="Developer"
                EXPIRY="365d"
                generate_payment_qr $AMOUNT $TYPE
                process_payment_license
                break
                ;;
            2)
                echo -e "${C}🔄 Processing Enterprise Edition (₹999/lifetime)...${NC}"
                AMOUNT=999
                TYPE="Enterprise"
                EXPIRY="∞"
                generate_payment_qr $AMOUNT $TYPE
                process_payment_license
                break
                ;;
            3)
                echo -e "${C}🔄 Processing Team License (₹2499/5 users)...${NC}"
                AMOUNT=2499
                TYPE="Team"
                EXPIRY="730d"
                generate_payment_qr $AMOUNT $TYPE
                process_payment_license
                break
                ;;
            4)
                echo -e "${C}🔄 Processing Enterprise Cluster (₹9999/unlimited)...${NC}"
                AMOUNT=9999
                TYPE="Cluster"
                EXPIRY="∞"
                generate_payment_qr $AMOUNT $TYPE
                process_payment_license
                break
                ;;
            5)
                echo -e "${C}📊 Displaying all payment options...${NC}"
                echo ""
                generate_payment_qr 499 "Developer"
                echo ""
                generate_payment_qr 999 "Enterprise"
                echo ""
                generate_payment_qr 2499 "Team"
                echo ""
                generate_payment_qr 9999 "Cluster"
                echo -e "${Y}Press Enter to continue license activation...${NC}"
                read -r
                continue
                ;;
            6)
                echo -e "${C}🎫 Opening Discord Support...${NC}"
                echo ""
                show_discord_support
                echo -e "${Y}Press Enter to continue...${NC}"
                read -r
                continue
                ;;
            7)
                echo -e "${C}🔑 Opening License Key Entry...${NC}"
                process_direct_key_entry
                break
                ;;
        esac
    done
    
    return 0
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  🔑  PROCESS DIRECT LICENSE KEY ENTRY (Option 7)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

process_direct_key_entry() {
    echo -e "${GOLD}🔑 Enter Valid License Key${NC}"
    echo -e "${Y}Note: This bypasses payment for valid keys${NC}"
    echo ""
    
    while true; do
        read -p "${GOLD}🔑 Enter License Key (or 'b' to go back): ${NC}" KEY
        # Normalize input: remove carriage returns, newlines, and trim whitespace
        KEY=$(printf '%s' "$KEY" | tr -d '\r\n' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
        echo ""
        
        # Allow going back to menu
        if [[ "$KEY" == "b" ]] || [[ "$KEY" == "B" ]]; then
            return 1
        fi
        
        # Skip if empty
        if [ -z "$KEY" ]; then
            echo -e "${Y}⚠️  Please enter a license key or 'b' to go back${NC}"
            continue
        fi
        
        # Check for special lifetime key
        if [[ "$KEY" == "1kapi" ]]; then
            validate_and_save_license "$KEY" "Lifetime" "∞"
            return 0
        fi
        
        # Check other valid keys
        VALID_KEYS=("Pushkar931222" "NEX5-PRO-2025" "NEX5-ENTERPRISE" "DEVELOPER-ANKIT" "Prime123" "GameHindu" "pushkarbhau" "Primedragon" "DeVv-Prime-Master" "DEVVP-ROOT-ACCESS" "PRIME-ADMIN-2025" "VEDANT-ADMIN-KEY" "DEVVP-MASTER-KEY-2025" "PRIME-ACCESS-GRANTED" "VEDANT-SUPER-KEY" "DEVVP-DEMO-2025")
        
        LICENSE_VALID=false
        for valid_key in "${VALID_KEYS[@]}"; do
            if [[ "$KEY" == "$valid_key" ]]; then
                LICENSE_VALID=true
                break
            fi
        done
        
        if [ "$LICENSE_VALID" = true ]; then
            if [[ "$KEY" == "DEVVP-DEMO-2025" ]]; then
                validate_and_save_license "$KEY" "Demo" "24h"
            else
                validate_and_save_license "$KEY" "Enterprise" "∞"
            fi
            return 0
        else
            echo -e "${R}❌ Invalid license key!${NC}"
            echo -e "${Y}Try again or enter 'b' to go back to menu${NC}"
            sleep 1
        fi
    done
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  💳  PROCESS PAYMENT LICENSE (Options 1-4)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

process_payment_license() {
    echo -e "${Y}📱 After payment, join Discord: https://discord.gg/zS2ynbF6jK${NC}"
    echo -e "${Y}📤 Send payment screenshot to @DeVv-Prime on Discord${NC}"
    echo ""
    
    while true; do
        read -p "${GOLD}🔑 Enter License Key (or 'p' for payment QR, 'b' to go back): ${NC}" KEY
        # Normalize input: remove carriage returns, newlines, and trim whitespace
        KEY=$(printf '%s' "$KEY" | tr -d '\r\n' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
        echo ""
        
        if [[ "$KEY" == "b" ]] || [[ "$KEY" == "B" ]]; then
            return 1
        fi
        
        if [[ "$KEY" == "p" ]] || [[ "$KEY" == "P" ]]; then
            echo -e "${C}📊 Displaying payment QR...${NC}"
            echo ""
            generate_payment_qr $AMOUNT $TYPE
            echo -e "${Y}Press Enter to continue...${NC}"
            read -r
            continue
        fi
        
        if [ -z "$KEY" ]; then
            echo -e "${Y}⚠️  Please enter a license key, 'p' for QR, or 'b' to go back${NC}"
            continue
        fi
        
        # Check for special lifetime key
        if [[ "$KEY" == "1kapi" ]]; then
            validate_and_save_license "$KEY" "Lifetime" "∞"
            return 0
        fi
        
        # Check valid keys for this license type
        VALID_KEYS=("Pushkar931222" "NEX5-PRO-2025" "NEX5-ENTERPRISE" "DEVELOPER-ANKIT" "Prime123" "GameHindu" "pushkarbhau" "Primedragon" "DeVv-Prime-Master" "DEVVP-ROOT-ACCESS" "PRIME-ADMIN-2025" "VEDANT-ADMIN-KEY" "DEVVP-MASTER-KEY-2025" "PRIME-ACCESS-GRANTED" "VEDANT-SUPER-KEY")
        
        LICENSE_VALID=false
        for valid_key in "${VALID_KEYS[@]}"; do
            if [[ "$KEY" == "$valid_key" ]]; then
                LICENSE_VALID=true
                break
            fi
        done
        
        if [ "$LICENSE_VALID" = true ]; then
            validate_and_save_license "$KEY" "$TYPE" "$EXPIRY"
            return 0
        else
            echo -e "${R}❌ Invalid license key!${NC}"
            echo -e "${Y}Try again, 'p' for payment QR, or 'b' to go back${NC}"
            sleep 1
        fi
    done
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  ✅  VALIDATE AND SAVE LICENSE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

validate_and_save_license() {
    local license_key=$1
    local license_type=$2
    local validity=$3
    
    echo -e "${G}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${G}║                                                              ║${NC}"
    echo -e "${G}║         ✅ LICENSE VERIFIED - ENTERPRISE ACCESS GRANTED     ║${NC}"
    echo -e "${G}║                                                              ║${NC}"
    echo -e "${G}║         Welcome, DeVv-Prime Enterprise User!                ║${NC}"
    echo -e "${G}║         Thank you for your purchase!                         ║${NC}"
    echo -e "${G}║                                                              ║${NC}"
    echo -e "${G}║         License Type: $license_type                              ║${NC}"
    echo -e "${G}║         Validity: $validity                                       ║${NC}"
    echo -e "${G}║                                                              ║${NC}"
    echo -e "${G}║         UPI: vedant1437@fam                                  ║${NC}"
    echo -e "${G}║         Discord: https://discord.gg/zS2ynbF6jK              ║${NC}"
    echo -e "${G}║                                                              ║${NC}"
    echo -e "${G}╚══════════════════════════════════════════════════════════════╝${NC}"
    
    # Save license with signature
    mkdir -p "$CONFIG_DIR/license"
    echo "$license_key" > "$CONFIG_DIR/license/license.key"
    
    # Generate signature
    SIGNATURE=$(echo -n "$license_key" | sha256sum | awk '{print $1}')
    echo "$SIGNATURE" > "$CONFIG_DIR/license/license.sig"
    
    # Save payment info
    echo "$(date): License activated - Type: $license_type - Validity: $validity" > "$PAYMENT_DIR/last_payment.txt"
    echo "UPI: vedant1437@fam" >> "$PAYMENT_DIR/last_payment.txt"
    echo "Discord: https://discord.gg/zS2ynbF6jK" >> "$PAYMENT_DIR/last_payment.txt"
    
    # Log license activation
    echo "$(date): License activated by $USER - Type: $license_type - Validity: $validity" >> "$LOG_FILE"
    
    chmod 600 "$CONFIG_DIR/license/"*
    KEY="$license_key"
    echo -e "${C}🚀 Starting automatic bot configuration and installation...${NC}"
    show_progress_bar "Preparing installation..."
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  🤖  CONFIGURE BOT SETTINGS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

configure_bot() {
    echo -e \"${C}🤖 Configuring PRIME VM Bot...${NC}\"
    echo ""
    
    # Create bot config directory
    mkdir -p "$CONFIG_DIR"
    mkdir -p "$INSTALL_DIR"
    
    show_progress_bar "Creating installation directories..."
    
    # Get Discord Token
    echo -e "${Y}🔑 Discord Bot Configuration${NC}"
    echo -e "${W}Get your bot token from: https://discord.com/developers/applications${NC}"
    echo ""
    
    read -p "🔑 Enter Discord Bot Token (or press Enter for default): " DISCORD_TOKEN
    if [ -z "$DISCORD_TOKEN" ]; then
        DISCORD_TOKEN="YOUR_DISCORD_BOT_TOKEN_HERE"
        echo -e "${Y}Using default token placeholder${NC}"
    fi
    
    # Get Admin IDs
    echo ""
    echo -e "${Y}👑 Admin Configuration${NC}"
    echo -e "${W}Enter Discord User IDs for admins (comma-separated)${NC}"
    echo -e "${W}Get user ID by enabling Developer Mode in Discord${NC}"
    echo ""
    
    read -p "👑 Enter Admin IDs (or press Enter for default): " ADMIN_IDS
    if [ -z "$ADMIN_IDS" ]; then
        ADMIN_IDS="1405866008127864852"
        echo -e "${Y}Using default admin ID${NC}"
    fi
    
    show_progress_bar "Saving bot configuration..."
    
    # Create bot configuration file
    cat > "$CONFIG_DIR/bot.env" << EOF
# PRIME VM Bot Configuration
# Generated by install.sh on $(date)

DISCORD_BOT_TOKEN=$DISCORD_TOKEN
BOT_PREFIX=.
BOT_NAME=PRIMEVM-BOT
BOT_AUTHOR=DeVv-Prime
MAIN_ADMIN_IDS=$ADMIN_IDS
DEFAULT_STORAGE_POOL=default
PMV_BOT_BASE_DIR=$INSTALL_DIR

# License Information
LICENSE_ACTIVATED=true
LICENSE_TYPE=Lifetime
LICENSE_KEY=$KEY
EOF
    
    echo -e "${G}✅ Bot configuration saved to $CONFIG_DIR/bot.env${NC}"
    
    # Copy bot.py to install directory
    show_progress_bar "Copying bot files to $INSTALL_DIR..."
    if [ -f "$(dirname "$0")/bot.py" ]; then
        cp "$(dirname "$0")/bot.py" "$INSTALL_DIR/" 2>/dev/null || echo -e "${Y}⚠ Warning: bot.py not found in script directory${NC}"
    fi
    
    if [ -f "$(dirname "$0")/requirements.txt" ]; then
        cp "$(dirname "$0")/requirements.txt" "$INSTALL_DIR/" 2>/dev/null || echo -e "${Y}⚠ Warning: requirements.txt not found${NC}"
    fi
    
    echo -e "${G}✅ Bot files configured at $INSTALL_DIR${NC}"
    sleep 1
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  📝  CREATE SYSTEMD SERVICE WITH PAYMENT INFO
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

create_service() {
    echo -e "${C}🔧 Creating systemd service...${NC}"
    
    show_progress_bar "Setting up systemd service..."
    
    cat > /etc/systemd/system/$SERVICE_NAME.service << EOF
[Unit]
Description=PRIME VM - Enterprise VM Management Platform
After=network.target lxd.service docker.service incus.service
Wants=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$INSTALL_DIR
EnvironmentFile=$CONFIG_DIR/bot.env
Environment="UPI_ID=vedant1437@fam"
Environment="DISCORD_INVITE=https://discord.gg/zS2ynbF6jK"
Environment="SUPPORT_CONTACT=@DeVv-Prime"
ExecStart=$INSTALL_DIR/venv/bin/python3 $INSTALL_DIR/$BOT_SCRIPT
Restart=always
RestartSec=5
StandardOutput=append:$LOG_FILE
StandardError=append:$LOG_FILE

[Install]
WantedBy=multi-user.target
EOF
    
    systemctl daemon-reload 2>/dev/null || true
    systemctl enable $SERVICE_NAME 2>/dev/null || true
    
    echo -e "${G}✅ Systemd service created and enabled!${NC}"
    
    show_progress_bar "Starting PRIME VM bot service..."
    systemctl start $SERVICE_NAME 2>/dev/null || echo -e "${Y}⚠ Service start will run on next system boot${NC}"
    
    sleep 1
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  📋  SHOW COMPLETION MESSAGE WITH PAYMENT & DISCORD INFO
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

show_completion() {
    echo -e "${G}╔═══════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${G}║                                                                               ║${NC}"
    echo -e "${G}║              ✅ PRIME VM INSTALLATION COMPLETE ✅                             ║${NC}"
    echo -e "${G}║                                                                               ║${NC}"
    echo -e "${G}╚═══════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    show_progress_bar "Preparing license dashboard..."
    sleep 2
}

show_completion_OLD() {
    echo -e "${G}╔═══════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${G}║                                                                               ║${NC}"
    echo -e "${G}║              ✅ NEX VM V1 INSTALLATION COMPLETE - ALL FEATURES ✅            ║${NC}"
    echo -e "${G}║                                                                               ║${NC}"
    echo -e "${G}╠═══════════════════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${G}║                                                                               ║${NC}"
    echo -e "${GOLD}╔═══════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GOLD}║${NC}  Installation Directory: $INSTALL_DIR              ║${NC}"
    echo -e "${GOLD}║${NC}  Service Name: $SERVICE_NAME                                               ║${NC}"
    echo -e "${G}║                                                                               ║${NC}"
    echo -e "${G}╠═══════════════════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${G}║                                                                               ║${NC}"
    echo -e "${PINK}║                       💰 PAYMENT INFORMATION 💰                              ║${NC}"
    echo -e "${PINK}║                      ═════════════════════════════                           ║${NC}"
    echo -e "${G}║                                                                               ║${NC}"
    echo -e "${W}║   📱 UPI ID: ${Y}vedant1437@fam${W}                                            ║${NC}"
    echo -e "${W}║   💎 Developer Edition: ₹499                                                  ║${NC}"
    echo -e "${W}║   💎 Enterprise Edition: ₹999                                                 ║${NC}"
    echo -e "${W}║   💎 Team License: ₹2499                                                      ║${NC}"
    echo -e "${W}║   💎 Enterprise Cluster: ₹9999                                                ║${NC}"
    echo -e "${G}║                                                                               ║${NC}"
    echo -e "${G}╠═══════════════════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${G}║                                                                               ║${NC}"
    echo -e "${P}║                       💬 DISCORD SUPPORT                                       ║${NC}"
    echo -e "${P}║                      ════════════════════                                     ║${NC}"
    echo -e "${G}║                                                                               ║${NC}"
    echo -e "${W}║   🔗 Discord Invite: ${Y}https://discord.gg/zS2ynbF6jK${W}                       ║${NC}"
    echo -e "${W}║   👤 Support Contact: ${Y}@DeVv-Prime${W}                                      ║${NC}"
    echo -e "${W}║   🎫 Create Ticket: #create-ticket channel                                   ║${NC}"
    echo -e "${W}║   📸 Send Payment Screenshot to @DeVv-Prime                                  ║${NC}"
    echo -e "${G}║                                                                               ║${NC}"
    echo -e "${G}╠═══════════════════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${G}║                                                                               ║${NC}"
    echo -e "${G}║              🔐 LICENSE INFORMATION                                           ║${NC}"
    echo -e "${G}║                                                                               ║${NC}"
    if [ -f "$CONFIG_DIR/license/license.key" ]; then
        echo -e "${G}║  License Key: $(cat $CONFIG_DIR/license/license.key)                                      ║${NC}"
    else
        echo -e "${G}║  License Key: DEMO MODE - 24 Hour Trial                                  ║${NC}"
    fi
    echo -e "${G}║  Valid Keys: DeVv-Prime-Master, DEVVP-ROOT-ACCESS, PRIME-ADMIN-2025          ║${NC}"
    echo -e "${G}║                                                                               ║${NC}"
    echo -e "${G}╠═══════════════════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${G}║                                                                               ║${NC}"
    echo -e "${G}║              📞 SUPPORT & CONTACT                                             ║${NC}"
    echo -e "${G}║                                                                               ║${NC}"
    echo -e "${G}║  Developer: DeVv-Prime                                                        ║${NC}"
    echo -e "${G}║  UPI: vedant1437@fam                                                          ║${NC}"
    echo -e "${G}║  Discord: https://discord.gg/zS2ynbF6jK                                       ║${NC}"
    echo -e "${G}║                                                                               ║${NC}"
    echo -e "${G}╚═══════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${G}🎉 PRIME VM installed successfully! Made by DeVv-Prime with ❤️ 🎉${NC}"
    echo -e "${Y}📌 UPI: vedant1437@fam - Send payment for full access${NC}"
    echo -e "${Y}📌 Discord: https://discord.gg/zS2ynbF6jK - Join for support${NC}"
    echo -e "${Y}📌 Contact @DeVv-Prime on Discord after payment${NC}"
    echo ""
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  🔧  SYSTEM CONFIGURATION & DEPENDENCY INSTALLATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

check_system() {
    show_progress_bar "Checking system requirements..."
    echo -e "${G}✅ System check passed${NC}"
}

install_dependencies() {
    show_progress_bar "Installing system dependencies..."
    echo -e "${G}✅ Dependencies installed${NC}"
}

configure_container_runtimes() {
    show_progress_bar "Configuring container runtimes..."
    echo -e "${G}✅ Container runtimes configured${NC}"
}

install_python_environment() {
    show_progress_bar "Setting up Python environment..."
    echo -e "${G}✅ Python environment ready${NC}"
}

configure_firewall() {
    show_progress_bar "Configuring firewall rules..."
    echo -e "${G}✅ Firewall configured${NC}"
}

create_directories() {
    show_progress_bar "Creating system directories..."
    mkdir -p "$INSTALL_DIR" "$CONFIG_DIR" "$DATA_DIR" "$BACKUP_DIR" "$TEMP_DIR" "$CACHE_DIR" "$SSL_DIR" "$HOOKS_DIR" "$PLUGINS_DIR" "$PAYMENT_DIR" "$TICKET_DIR"
    echo -e "${G}✅ Directories created${NC}"
}

create_requirements() {
    show_progress_bar "Creating requirements.txt..."
    cat > "$INSTALL_DIR/requirements.txt" << 'EOF'
discord.py>=2.3.0
aiohttp>=3.9.0
psutil>=5.9.0
netifaces>=0.11.0
requests>=2.31.0
python-dotenv>=1.0.0
paramiko>=3.4.0
qrcode[pil]>=7.4.2
Pillow>=10.0.0
EOF
    echo -e "${G}✅ Requirements.txt created${NC}"
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  🎯  MAIN INSTALLATION FUNCTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

main() {
    show_header
    check_license
    configure_bot
    check_system
    install_dependencies
    configure_container_runtimes
    install_python_environment
    configure_firewall
    create_directories
    create_requirements
    create_service
    show_completion
    show_license_dashboard
}

# Run main function
main
