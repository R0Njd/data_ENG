from database import Lead, engine, Staff, Club, Member, Subscription
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, case
from datetime import datetime
from collections import defaultdict
import json
import pandas as pd


Session = sessionmaker(bind=engine)
session = Session()

def parse_date(date_str):
    if date_str:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    return None

def populate_club(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    data = data["clubs"]

    for item in data:
        club = session.query(Club).filter_by(club_id=item['club_id']).first()
        if not club:
            club = Club(
                club_id=item['club_id'],
                preffered_contact_method=item['preffered_contact_method'],
                status=item['status'],
                city=item['city'],
                country=item['country'],
            )
            session.add(club)
        else:
            club_id = item['club_id']
            club.preffered_contact_method = item['preffered_contact_method']
            club.status = item['status']
            club.city = item['city']
            club.country = item['country']

    session.commit() 




def populate_member(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    data = data["members"]

    for item in data:
        members = session.query(Member).filter_by(member_id=item['member_id']).first()
        if not members:
            members = Member(
                member_id=item['member_id'],
                first_name=item['first_name'],
                last_name=item['last_name'],
                date_of_birth=parse_date(item['date_of_birth']),
                gender=item['gender']
            )
            session.add(members)
        else:
            members.first_name = item['first_name']
            members.last_name = item['last_name']
            members.date_of_birth = parse_date(item['date_of_birth'])
            gender = item['gender']
        
    session.commit()        



def populate_staff(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    data = data["staff"]

    for item in data:
        staff = session.query(Staff).filter_by(staff_id=item['staff_id']).first()
        print(item)
        if not staff:
            staff = Staff(
                staff_id=item['staff_id'],
                first_name=item['first_name'],
                last_name=item['last_name'],
                preffered_contact_method=item['preffered_contact_method'],
                club_id=item['club_id'],
                dept_name=item['dept_name'],
                working_status=item['working_status'],
                rating=item['rating']
            )
            session.add(staff)
        else:
            staff.first_name = item['first_name']
            staff.last_name = item['last_name']
            staff.preffered_contact_method = item['preffered_contact_method']
            staff.club_id = item['club_id']
            staff.dept_name = item['dept_name']
            staff.working_status = item['working_status']
            staff.rating = item['rating']

    session.commit()
    
def populate_sub(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    data = data["subscription"]

    for item in data:
        subscription = session.query(Subscription).filter_by(sub_id=item['sub_id']).first()
        
        if not subscription:
            subscription = Subscription(
                sub_id=item['sub_id'],
                conversation_date=item['conversion_date'],
                member_id=item['member_id'],
                end_date=parse_date(item['end_date']),
                status=item['status'],
                type=item['type'],
                amount=item['amount']
            )
            session.add(subscription)
        else:
            subscription.sub_id = item['sub_id']
            subscription.conversation_date = item['conversion_date']
            subscription.member_id = item['member_id']
            subscription.end_date = parse_date(item['end_date'])
            subscription.status = item['status']
            subscription.type = item['type']
            subscription.amount = item['amount']
    session.commit()


def populate_lead(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    data = data["leads"]

    for item in data:
        lead = session.query(Lead).filter_by(lead_id=item['lead_id']).first()

        if not lead:
            lead = Lead(
                lead_id=item['lead_id'],
                address=item['address'],
                city=item['city'],
                club_id=item['club_id'],
                staff_id=item['staff_id'],
                conversion_date=parse_date(item['conversion_date']),
                country=item['country'],
                creation_date=parse_date(item['creation_date']),
                date_of_birth=parse_date(item['date_of_birth']),
                first_name=item['first_name'],
                gender=item['gender'],
                last_name=item['last_name'],
                notes=item['notes'],
                preffered_contact_method=item['preffered_contact_method'],
                status=item['status'],
            )
            session.add(lead)
        else:

            lead.address = item['address']
            lead.city = item['city']
            lead.club_id = item['club_id']
            lead.staff_id= item['staff_id']
            lead.conversion_date = parse_date(item['conversion_date'])
            lead.country = item['country']
            lead.creation_date = parse_date(item['creation_date'])
            lead.date_of_birth = parse_date(item['date_of_birth'])
            lead.first_name = item['first_name']
            lead.gender = item['gender']
            lead.last_name = item['last_name']
            lead.notes = item['notes']
            lead.preffered_contact_method = item['preffered_contact_method']
            lead.status = item['status']

    session.commit()
    print(f"Database populated with {len(data)} leads!")

populate_lead('json_files/lead_data.json')
populate_staff('json_files/staff_data.json')
populate_member('json_files/member_data.json')
populate_club('json_files/club_data.json')
populate_sub('json_files/sub_data.json')

# subscriptions = session.query(Subscription).all()
# for subscription in subscriptions:
#     print(f"{subscription.sub_id}")



# Query



results = (
    session.query(
        Lead.conversion_date,
        Lead.staff_id,
        Subscription.amount,
        Subscription.type,
        Staff.rating
    )
    .join(Subscription, Lead.conversion_date == Subscription.conversation_date)
    .join(Staff, Lead.staff_id == Staff.staff_id) 
    .filter(Lead.conversion_date.isnot(None))
    .filter(Subscription.amount > 100)
    .all()
)

for r in results:
    print(r)



from collections import defaultdict
from datetime import datetime, timedelta


converted = defaultdict(int)
seen = set()

for r in results:
    key = (r.staff_id, r.conversion_date)
    if key not in seen:
        converted[r.staff_id] += 1
        seen.add(key)


staff_totals = defaultdict(int)
all_leads = session.query(Lead.staff_id).all()
for staff_id, in all_leads:
    staff_totals[staff_id] += 1

#fake 3 months for conssitency in the example
today = datetime.today().date()
three_months_ago = datetime(2024, 6, 1).date()


recent_converters = set()
for r in results:
    conversion_date = r[0]
    staff_id = r[1]
    if conversion_date >= three_months_ago:
        recent_converters.add(staff_id)


print("\n  Conversion Rate per Staff (last 3 months only):")
for staff_id in recent_converters:
    total = staff_totals[staff_id]
    converted_count = converted.get(staff_id, 0)
    rate = (converted_count / total) * 100 if total else 0
    print(f"Staff ID {staff_id}: {rate:.2f}%")



