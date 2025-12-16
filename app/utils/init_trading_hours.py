"""
Initialize default trading hours templates and market holidays
"""

from datetime import time, date
from app import db
from app.models import TradingHoursTemplate, TradingSession, MarketHoliday


def create_default_nse_template():
    """Create default NSE trading hours template"""
    
    # Check if default template already exists
    existing = TradingHoursTemplate.query.filter_by(name='NSE Default').first()
    if existing:
        print("Default NSE template already exists")
        return existing
    
    # Create NSE Default template
    template = TradingHoursTemplate(
        name='NSE Default',
        description='Standard NSE trading hours (Monday-Friday, 9:15 AM - 3:30 PM IST)',
        market='NSE',
        is_active=True
    )
    db.session.add(template)
    db.session.flush()  # Get the template ID
    
    # Add trading sessions for Monday to Friday
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    for day_num in range(5):  # 0=Monday to 4=Friday
        # Regular trading session only
        normal_session = TradingSession(
            template_id=template.id,
            session_name=f'{days[day_num]} Regular Hours',
            day_of_week=day_num,
            start_time=time(9, 15),  # 9:15 AM
            end_time=time(15, 30),    # 3:30 PM
            session_type='normal',
            is_active=True
        )
        db.session.add(normal_session)
    
    db.session.commit()
    print(f"Created default NSE template with ID: {template.id}")
    return template


def create_default_holidays_2025():
    """Create default NSE holidays for 2025"""
    
    holidays_2025 = [
        # Sr. No 1
        {
            'holiday_date': date(2025, 2, 26),
            'holiday_name': 'Mahashivratri',
            'market': 'NSE',
            'holiday_type': 'trading'
        },
        # Sr. No 2
        {
            'holiday_date': date(2025, 3, 14),
            'holiday_name': 'Holi',
            'market': 'NSE',
            'holiday_type': 'trading'
        },
        # Sr. No 3
        {
            'holiday_date': date(2025, 3, 31),
            'holiday_name': 'Id-Ul-Fitr (Ramadan Eid)',
            'market': 'NSE',
            'holiday_type': 'trading'
        },
        # Sr. No 4
        {
            'holiday_date': date(2025, 4, 10),
            'holiday_name': 'Shri Mahavir Jayanti',
            'market': 'NSE',
            'holiday_type': 'trading'
        },
        # Sr. No 5
        {
            'holiday_date': date(2025, 4, 14),
            'holiday_name': 'Dr. Baba Saheb Ambedkar Jayanti',
            'market': 'NSE',
            'holiday_type': 'trading'
        },
        # Sr. No 6
        {
            'holiday_date': date(2025, 4, 18),
            'holiday_name': 'Good Friday',
            'market': 'NSE',
            'holiday_type': 'trading'
        },
        # Sr. No 7
        {
            'holiday_date': date(2025, 5, 1),
            'holiday_name': 'Maharashtra Day',
            'market': 'NSE',
            'holiday_type': 'trading'
        },
        # Sr. No 8
        {
            'holiday_date': date(2025, 8, 15),
            'holiday_name': 'Independence Day / Parsi New Year',
            'market': 'NSE',
            'holiday_type': 'trading'
        },
        # Sr. No 9
        {
            'holiday_date': date(2025, 8, 27),
            'holiday_name': 'Ganesh Chaturthi',
            'market': 'NSE',
            'holiday_type': 'trading'
        },
        # Sr. No 10
        {
            'holiday_date': date(2025, 10, 2),
            'holiday_name': 'Mahatma Gandhi Jayanti / Dussehra',
            'market': 'NSE',
            'holiday_type': 'trading'
        },
        # Sr. No 11
        {
            'holiday_date': date(2025, 10, 21),
            'holiday_name': 'Diwali - Laxmi Pujan',
            'market': 'NSE',
            'holiday_type': 'trading'
        },
        # Sr. No 12
        {
            'holiday_date': date(2025, 10, 22),
            'holiday_name': 'Diwali - Balipratipada',
            'market': 'NSE',
            'holiday_type': 'trading'
        },
        # Sr. No 13
        {
            'holiday_date': date(2025, 11, 5),
            'holiday_name': 'Prakash Gurpurb Sri Guru Nanak Dev',
            'market': 'NSE',
            'holiday_type': 'trading'
        },
        # Sr. No 14
        {
            'holiday_date': date(2025, 12, 25),
            'holiday_name': 'Christmas',
            'market': 'NSE',
            'holiday_type': 'trading'
        }
    ]
    
    added_count = 0
    for holiday_data in holidays_2025:
        # Check if holiday already exists
        existing = MarketHoliday.query.filter_by(
            holiday_date=holiday_data['holiday_date'],
            market=holiday_data['market']
        ).first()
        
        if not existing:
            holiday = MarketHoliday(**holiday_data)
            db.session.add(holiday)
            added_count += 1
    
    db.session.commit()
    print(f"Added {added_count} holidays for 2025")
    return added_count


def create_default_holidays_2026():
    """Create default NSE holidays for 2026"""

    holidays_2026 = [
        # Sr. No 1
        {
            'holiday_date': date(2026, 1, 26),
            'holiday_name': 'Republic Day',
            'market': 'NSE',
            'holiday_type': 'trading'
        },
        # Sr. No 2
        {
            'holiday_date': date(2026, 3, 3),
            'holiday_name': 'Holi',
            'market': 'NSE',
            'holiday_type': 'trading'
        },
        # Sr. No 3
        {
            'holiday_date': date(2026, 3, 26),
            'holiday_name': 'Shri Ram Navami',
            'market': 'NSE',
            'holiday_type': 'trading'
        },
        # Sr. No 4
        {
            'holiday_date': date(2026, 3, 31),
            'holiday_name': 'Shri Mahavir Jayanti',
            'market': 'NSE',
            'holiday_type': 'trading'
        },
        # Sr. No 5
        {
            'holiday_date': date(2026, 4, 3),
            'holiday_name': 'Good Friday',
            'market': 'NSE',
            'holiday_type': 'trading'
        },
        # Sr. No 6
        {
            'holiday_date': date(2026, 4, 14),
            'holiday_name': 'Dr. Baba Saheb Ambedkar Jayanti',
            'market': 'NSE',
            'holiday_type': 'trading'
        },
        # Sr. No 7
        {
            'holiday_date': date(2026, 5, 1),
            'holiday_name': 'Maharashtra Day',
            'market': 'NSE',
            'holiday_type': 'trading'
        },
        # Sr. No 8
        {
            'holiday_date': date(2026, 5, 28),
            'holiday_name': 'Bakri Eid',
            'market': 'NSE',
            'holiday_type': 'trading'
        },
        # Sr. No 9
        {
            'holiday_date': date(2026, 6, 26),
            'holiday_name': 'Moharram',
            'market': 'NSE',
            'holiday_type': 'trading'
        },
        # Sr. No 10
        {
            'holiday_date': date(2026, 9, 14),
            'holiday_name': 'Ganesh Chaturthi',
            'market': 'NSE',
            'holiday_type': 'trading'
        },
        # Sr. No 11
        {
            'holiday_date': date(2026, 10, 2),
            'holiday_name': 'Mahatma Gandhi Jayanti',
            'market': 'NSE',
            'holiday_type': 'trading'
        },
        # Sr. No 12
        {
            'holiday_date': date(2026, 10, 20),
            'holiday_name': 'Dussehra',
            'market': 'NSE',
            'holiday_type': 'trading'
        },
        # Sr. No 13
        {
            'holiday_date': date(2026, 11, 10),
            'holiday_name': 'Diwali - Balipratipada',
            'market': 'NSE',
            'holiday_type': 'trading'
        },
        # Sr. No 14
        {
            'holiday_date': date(2026, 11, 24),
            'holiday_name': 'Prakash Gurpurb Sri Guru Nanak Dev',
            'market': 'NSE',
            'holiday_type': 'trading'
        },
        # Sr. No 15
        {
            'holiday_date': date(2026, 12, 25),
            'holiday_name': 'Christmas',
            'market': 'NSE',
            'holiday_type': 'trading'
        }
    ]

    added_count = 0
    for holiday_data in holidays_2026:
        # Check if holiday already exists
        existing = MarketHoliday.query.filter_by(
            holiday_date=holiday_data['holiday_date'],
            market=holiday_data['market']
        ).first()

        if not existing:
            holiday = MarketHoliday(**holiday_data)
            db.session.add(holiday)
            added_count += 1

    db.session.commit()
    print(f"Added {added_count} holidays for 2026")
    return added_count


def init_trading_hours_defaults():
    """Initialize all default trading hours data"""
    try:
        # Create default template
        template = create_default_nse_template()

        # Create default holidays
        holidays_added_2025 = create_default_holidays_2025()
        holidays_added_2026 = create_default_holidays_2026()

        print("Trading hours defaults initialized successfully")
        return {
            'template': template,
            'holidays_added': holidays_added_2025 + holidays_added_2026
        }
    except Exception as e:
        db.session.rollback()
        print(f"Error initializing trading hours defaults: {e}")
        raise