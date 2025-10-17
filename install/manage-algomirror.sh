#!/bin/bash

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
SERVICE_NAME="algomirror"
BASE_PATH="/var/python/algomirror"
APP_PATH="$BASE_PATH/app"
LOG_PATH="$BASE_PATH/logs"
DB_PATH="$BASE_PATH/instance/algomirror.db"

# Function to display header
show_header() {
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║       AlgoMirror Management Tool                       ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Function to check service status
check_status() {
    if systemctl is-active --quiet $SERVICE_NAME; then
        echo -e "${GREEN}● AlgoMirror is running${NC}"
        return 0
    else
        echo -e "${RED}● AlgoMirror is stopped${NC}"
        return 1
    fi
}

# Function to show status
show_status() {
    show_header
    echo -e "${YELLOW}Service Status:${NC}"
    sudo systemctl status $SERVICE_NAME --no-pager
    echo ""

    echo -e "${YELLOW}System Information:${NC}"
    echo "Installation Path: $BASE_PATH"
    echo "Database: $DB_PATH"
    echo "Logs: $LOG_PATH"
    echo ""

    if [ -f "$DB_PATH" ]; then
        echo -e "${YELLOW}Database Info:${NC}"
        ls -lh $DB_PATH
        echo ""
    fi

    # Check disk usage
    echo -e "${YELLOW}Disk Usage:${NC}"
    du -sh $BASE_PATH
    echo ""
}

# Function to start service
start_service() {
    echo -e "${BLUE}Starting AlgoMirror...${NC}"
    sudo systemctl start $SERVICE_NAME
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ AlgoMirror started successfully${NC}"
    else
        echo -e "${RED}✗ Failed to start AlgoMirror${NC}"
        echo "Check logs: sudo journalctl -u $SERVICE_NAME -n 50"
    fi
}

# Function to stop service
stop_service() {
    echo -e "${BLUE}Stopping AlgoMirror...${NC}"
    sudo systemctl stop $SERVICE_NAME
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ AlgoMirror stopped successfully${NC}"
    else
        echo -e "${RED}✗ Failed to stop AlgoMirror${NC}"
    fi
}

# Function to restart service
restart_service() {
    echo -e "${BLUE}Restarting AlgoMirror...${NC}"
    sudo systemctl restart $SERVICE_NAME
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ AlgoMirror restarted successfully${NC}"
    else
        echo -e "${RED}✗ Failed to restart AlgoMirror${NC}"
        echo "Check logs: sudo journalctl -u $SERVICE_NAME -n 50"
    fi
}

# Function to view logs
view_logs() {
    local lines=${1:-50}
    echo -e "${BLUE}Viewing last ${lines} lines of logs...${NC}\n"
    sudo journalctl -u $SERVICE_NAME -n $lines --no-pager
}

# Function to follow logs
follow_logs() {
    echo -e "${BLUE}Following logs (Ctrl+C to exit)...${NC}\n"
    sudo journalctl -u $SERVICE_NAME -f
}

# Function to view application logs
view_app_logs() {
    echo -e "${BLUE}Application Logs:${NC}\n"
    if [ -f "$LOG_PATH/algomirror.log" ]; then
        tail -50 $LOG_PATH/algomirror.log
    else
        echo "No application log file found"
    fi
}

# Function to view error logs
view_error_logs() {
    echo -e "${BLUE}Error Logs:${NC}\n"
    if [ -f "$LOG_PATH/error.log" ]; then
        tail -50 $LOG_PATH/error.log
    else
        echo "No error log file found"
    fi
}

# Function to backup database
backup_database() {
    if [ ! -f "$DB_PATH" ]; then
        echo -e "${RED}Database not found at $DB_PATH${NC}"
        return 1
    fi

    BACKUP_DIR="$HOME/algomirror_backups"
    mkdir -p $BACKUP_DIR

    DATE=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="$BACKUP_DIR/algomirror_${DATE}.db"

    echo -e "${BLUE}Backing up database...${NC}"
    sudo cp $DB_PATH $BACKUP_FILE

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Database backed up to: $BACKUP_FILE${NC}"
        ls -lh $BACKUP_FILE
    else
        echo -e "${RED}✗ Backup failed${NC}"
    fi
}

# Function to show configuration
show_config() {
    echo -e "${BLUE}Configuration (.env):${NC}\n"
    if [ -f "$APP_PATH/.env" ]; then
        # Show non-sensitive config
        grep -E "^(FLASK_ENV|DATABASE_URL|LOG_LEVEL|CORS_ORIGINS|DEFAULT_OPENALGO|PING_MONITORING)" $APP_PATH/.env | while read line; do
            echo "  $line"
        done
        echo ""
        echo -e "${YELLOW}Note: Sensitive keys (SECRET_KEY, ENCRYPTION_KEY) are hidden${NC}"
    else
        echo "No .env file found"
    fi
}

# Function to edit configuration
edit_config() {
    if [ ! -f "$APP_PATH/.env" ]; then
        echo -e "${RED}.env file not found${NC}"
        return 1
    fi

    echo -e "${YELLOW}Opening .env file for editing...${NC}"
    echo "After saving, restart the service for changes to take effect"
    read -p "Press Enter to continue..."

    sudo nano $APP_PATH/.env

    read -p "Restart AlgoMirror now? (y/n): " restart
    if [[ $restart =~ ^[Yy]$ ]]; then
        restart_service
    fi
}

# Function to update AlgoMirror
update_algomirror() {
    echo -e "${YELLOW}=== Updating AlgoMirror ===${NC}\n"

    # Backup first
    echo -e "${BLUE}Creating backup...${NC}"
    backup_database

    # Stop service
    echo -e "${BLUE}Stopping service...${NC}"
    sudo systemctl stop $SERVICE_NAME

    # Pull latest code
    echo -e "${BLUE}Pulling latest code...${NC}"
    cd $APP_PATH
    sudo git pull

    if [ $? -ne 0 ]; then
        echo -e "${RED}Failed to pull latest code${NC}"
        echo "Starting service with current version..."
        sudo systemctl start $SERVICE_NAME
        return 1
    fi

    # Update dependencies
    echo -e "${BLUE}Updating dependencies...${NC}"
    cd $BASE_PATH
    sudo bash -c "source venv/bin/activate && uv pip install -r app/requirements.txt"

    # Rebuild CSS
    if [ -f "$APP_PATH/package.json" ]; then
        echo -e "${BLUE}Rebuilding CSS...${NC}"
        cd $APP_PATH
        sudo npm install
        sudo npm run build-css
    fi

    # Run migrations
    echo -e "${BLUE}Running database migrations...${NC}"
    cd $APP_PATH
    sudo bash -c "source ../venv/bin/activate && flask db upgrade"

    # Restart service
    echo -e "${BLUE}Restarting service...${NC}"
    sudo systemctl start $SERVICE_NAME

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Update completed successfully${NC}"
    else
        echo -e "${RED}✗ Service failed to start after update${NC}"
        echo "Check logs: sudo journalctl -u $SERVICE_NAME -n 50"
    fi
}

# Function to check database
check_database() {
    echo -e "${BLUE}Database Information:${NC}\n"

    if [ ! -f "$DB_PATH" ]; then
        echo -e "${RED}Database not found${NC}"
        return 1
    fi

    echo "Location: $DB_PATH"
    ls -lh $DB_PATH
    echo ""

    echo -e "${BLUE}Database Tables:${NC}"
    sqlite3 $DB_PATH ".tables"
    echo ""

    echo -e "${BLUE}User Count:${NC}"
    sqlite3 $DB_PATH "SELECT COUNT(*) FROM user;" 2>/dev/null || echo "Unable to query"
    echo ""

    echo -e "${BLUE}Account Count:${NC}"
    sqlite3 $DB_PATH "SELECT COUNT(*) FROM trading_account;" 2>/dev/null || echo "Unable to query"
}

# Function to reset admin password
reset_password() {
    echo -e "${YELLOW}=== Reset Admin Password ===${NC}\n"
    echo -e "${RED}Warning: This will reset the password for the admin user${NC}"
    read -p "Continue? (y/n): " confirm

    if [[ ! $confirm =~ ^[Yy]$ ]]; then
        echo "Cancelled"
        return
    fi

    read -sp "Enter new password: " new_password
    echo ""
    read -sp "Confirm new password: " confirm_password
    echo ""

    if [ "$new_password" != "$confirm_password" ]; then
        echo -e "${RED}Passwords do not match${NC}"
        return 1
    fi

    if [ ${#new_password} -lt 8 ]; then
        echo -e "${RED}Password must be at least 8 characters${NC}"
        return 1
    fi

    echo -e "${BLUE}Resetting password...${NC}"
    cd $APP_PATH
    sudo bash -c "source ../venv/bin/activate && python << EOF
from app import create_app, db
from app.models import User

app = create_app()
with app.app_context():
    user = User.query.first()
    if user:
        user.set_password('$new_password')
        db.session.commit()
        print('Password reset successfully')
    else:
        print('No user found')
EOF"

    echo -e "${GREEN}✓ Password reset complete${NC}"
}

# Function to show help
show_help() {
    echo "Usage: $0 {command}"
    echo ""
    echo "Commands:"
    echo "  status         - Show service status and system info"
    echo "  start          - Start AlgoMirror service"
    echo "  stop           - Stop AlgoMirror service"
    echo "  restart        - Restart AlgoMirror service"
    echo "  logs [N]       - View last N lines of logs (default: 50)"
    echo "  follow         - Follow logs in real-time"
    echo "  applogs        - View application logs"
    echo "  errorlogs      - View error logs"
    echo "  backup         - Backup database"
    echo "  config         - Show configuration"
    echo "  edit           - Edit configuration"
    echo "  update         - Update AlgoMirror"
    echo "  database       - Check database info"
    echo "  reset-password - Reset admin password"
    echo "  help           - Show this help"
    echo ""
}

# Main menu
show_menu() {
    show_header
    check_status
    echo ""

    echo -e "${YELLOW}Select an action:${NC}"
    echo "  1) Start service"
    echo "  2) Stop service"
    echo "  3) Restart service"
    echo "  4) View logs (last 50 lines)"
    echo "  5) Follow logs (live)"
    echo "  6) View application logs"
    echo "  7) View error logs"
    echo "  8) Show status"
    echo "  9) Backup database"
    echo " 10) Show configuration"
    echo " 11) Edit configuration"
    echo " 12) Update AlgoMirror"
    echo " 13) Check database"
    echo " 14) Reset admin password"
    echo "  0) Exit"
    echo ""
    read -p "Enter choice [0-14]: " choice

    case $choice in
        1) start_service ;;
        2) stop_service ;;
        3) restart_service ;;
        4) view_logs 50 ;;
        5) follow_logs ;;
        6) view_app_logs ;;
        7) view_error_logs ;;
        8) show_status ;;
        9) backup_database ;;
        10) show_config ;;
        11) edit_config ;;
        12) update_algomirror ;;
        13) check_database ;;
        14) reset_password ;;
        0) echo -e "${GREEN}Goodbye!${NC}"; exit 0 ;;
        *) echo -e "${RED}Invalid choice${NC}" ;;
    esac

    echo ""
    read -p "Press Enter to continue..."
    show_menu
}

# Command line mode
if [ $# -gt 0 ]; then
    case $1 in
        status) show_status ;;
        start) start_service ;;
        stop) stop_service ;;
        restart) restart_service ;;
        logs) view_logs ${2:-50} ;;
        follow) follow_logs ;;
        applogs) view_app_logs ;;
        errorlogs) view_error_logs ;;
        backup) backup_database ;;
        config) show_config ;;
        edit) edit_config ;;
        update) update_algomirror ;;
        database) check_database ;;
        reset-password) reset_password ;;
        help) show_help ;;
        *)
            echo -e "${RED}Invalid command${NC}"
            show_help
            exit 1
            ;;
    esac
else
    # Interactive mode
    show_menu
fi
