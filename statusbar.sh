#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# STATUSBAR PANTHEON - Barre de statut système + daemons
# Usage: ./statusbar.sh          (one-shot)
#        ./statusbar.sh watch    (mise à jour continue)
#        ./statusbar.sh polybar  (format polybar)
#        ./statusbar.sh waybar   (format waybar JSON)
# ═══════════════════════════════════════════════════════════════════════════════

get_time() {
    date '+%H:%M'
}

get_date() {
    date '+%d/%m'
}

get_cpu() {
    top -bn1 | grep "Cpu(s)" | awk '{printf "%.0f%%", $2}'
}

get_temp() {
    if [ -f /sys/class/thermal/thermal_zone0/temp ]; then
        temp=$(cat /sys/class/thermal/thermal_zone0/temp)
        echo "$((temp / 1000))°C"
    else
        echo "N/A"
    fi
}

get_ram() {
    free | awk '/^Mem:/ {printf "%.0f%%", $3/$2*100}'
}

get_battery() {
    bat_path=$(ls -d /sys/class/power_supply/BAT* 2>/dev/null | head -1)
    if [ -n "$bat_path" ]; then
        capacity=$(cat "$bat_path/capacity" 2>/dev/null)
        status=$(cat "$bat_path/status" 2>/dev/null)
        if [ "$status" = "Charging" ]; then
            echo "⚡${capacity}%"
        elif [ "$status" = "Full" ]; then
            echo "⚡100%"
        else
            if [ "$capacity" -gt 80 ]; then
                echo "🔋${capacity}%"
            elif [ "$capacity" -gt 40 ]; then
                echo "🔋${capacity}%"
            elif [ "$capacity" -gt 20 ]; then
                echo "🪫${capacity}%"
            else
                echo "🪫${capacity}%"
            fi
        fi
    else
        echo "🔌AC"
    fi
}

get_disk() {
    df -h / | awk 'NR==2 {print $5}'
}

get_pantheon() {
    if curl -s --max-time 1 "http://localhost:9600/status" > /dev/null 2>&1; then
        heartbeat=$(curl -s --max-time 1 "http://localhost:9600/status" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['daemons']['leonardo']['heartbeats'])" 2>/dev/null || echo "?")
        echo "φ$heartbeat"
    else
        echo "φ○"
    fi
}

get_network() {
    if ping -c1 -W1 8.8.8.8 &>/dev/null; then
        echo "🌐"
    else
        echo "🌐✗"
    fi
}

# Format simple (défaut)
format_simple() {
    echo "$(get_pantheon) | 🖥️$(get_cpu) 🌡️$(get_temp) | 🧠$(get_ram) | $(get_battery) | 💾$(get_disk) | $(get_network) | $(get_time)"
}

# Format polybar
format_polybar() {
    echo "%{F#c9a227}$(get_pantheon)%{F-} %{F#888}|%{F-} %{F#4a9}🖥️$(get_cpu)%{F-} %{F#f80}🌡️$(get_temp)%{F-} %{F#888}|%{F-} %{F#69f}🧠$(get_ram)%{F-} %{F#888}|%{F-} %{F#4a9}$(get_battery)%{F-} %{F#888}|%{F-} %{F#fff}$(get_time)%{F-}"
}

# Format waybar JSON
format_waybar() {
    cat <<EOF
{"text": "$(get_pantheon) | $(get_cpu) | $(get_ram) | $(get_battery) | $(get_time)", "tooltip": "Pantheon Status\nCPU: $(get_cpu)\nRAM: $(get_ram)\nTemp: $(get_temp)\nBattery: $(get_battery)\nDisk: $(get_disk)"}
EOF
}

# Format pour notification
format_notify() {
    notify-send -t 3000 "φ Pantheon Status" "$(get_time) $(get_date)
CPU: $(get_cpu) | Temp: $(get_temp)
RAM: $(get_ram) | Disk: $(get_disk)
Battery: $(get_battery)
Pantheon: $(get_pantheon)" 2>/dev/null
}

# Mode terminal avec mise à jour
watch_mode() {
    while true; do
        clear
        echo "╭────────────────────────────────────────────────────────────╮"
        echo "│  φ PANTHEON STATUSBAR                    $(get_time) $(get_date)  │"
        echo "├────────────────────────────────────────────────────────────┤"
        printf "│  %-56s  │\n" "🖥️  CPU: $(get_cpu)  🌡️  Temp: $(get_temp)"
        printf "│  %-56s  │\n" "🧠 RAM: $(get_ram)  💾 Disk: $(get_disk)"
        printf "│  %-56s  │\n" "$(get_battery)  $(get_network)"
        printf "│  %-56s  │\n" "φ Pantheon: $(get_pantheon)"
        echo "╰────────────────────────────────────────────────────────────╯"
        echo ""
        echo "  Ctrl+C pour quitter"
        sleep 2
    done
}

# Main
case "${1:-simple}" in
    watch|w)
        watch_mode
        ;;
    polybar|p)
        format_polybar
        ;;
    waybar|json|j)
        format_waybar
        ;;
    notify|n)
        format_notify
        ;;
    simple|*)
        format_simple
        ;;
esac
