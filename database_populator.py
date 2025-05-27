from database import Lead, engine, Staff, Club, Member, Subscription
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, case
from collections import defaultdict
from datetime import datetime, timedelta
from decimal import Decimal
import json
import logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.CRITICAL)


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



#------------ Query--------------------



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


("---------------------------------------------------------------------------------------------------")



# percentage of staff with 


given_date = datetime(2024, 9, 1).date()
three_months_ago = given_date - timedelta(days=90)

all_staff_ids = (
    session.query(Lead.staff_id)
    .filter(Lead.creation_date >= three_months_ago)
    .filter(Lead.creation_date <= given_date)
    .distinct()
    .all()
)

results = []


all_relevant_leads = (
    session.query(Lead)
    .filter(Lead.creation_date >= three_months_ago)
    .filter(Lead.creation_date <= given_date)
    .all()
)


#info mapping 
staff_ids_set = {staff_tuple[0] for staff_tuple in all_staff_ids}
all_staff_info = (
    session.query(Staff)
    .filter(Staff.staff_id.in_(list(staff_ids_set)))
    .all()
)
staff_info_map = {staff.staff_id: staff for staff in all_staff_info}

# calculate total leads and conversions for each staff member
staff_lead_data = {}
for staff_id in staff_ids_set:
    staff_lead_data[staff_id] = {'total_leads': 0, 'conversions': 0}

for lead in all_relevant_leads:
    if lead.staff_id in staff_lead_data:
        staff_lead_data[lead.staff_id]['total_leads'] += 1
        if lead.conversion_date is not None:
            staff_lead_data[lead.staff_id]['conversions'] += 1

for staff_id, data in staff_lead_data.items():
    staff_info = staff_info_map.get(staff_id)
    total_leads = data['total_leads']
    conversions = data['conversions']
    rate = (conversions / total_leads) * 100 if total_leads > 0 else 0

    staff_name = f"{staff_info.first_name} {staff_info.last_name}" if staff_info else "Unknown"

    results.append({
        'staff_id': staff_id,
        'staff_name': staff_name,
        'total_leads': total_leads,
        'conversions': conversions,
        'rate': rate
    })


results.sort(key=lambda x: x['rate'], reverse=True)

print(f"CONVERSION RATES FOR ALL STAFF ({three_months_ago} to {given_date}):")
print("Staff ID | Staff Name           | Total Leads | Conversions | Rate")
print("-" * 70)

for result in results:
    print(f"{result['staff_id']:<8} | {result['staff_name']:<20} | {result['total_leads']:<11} | {result['conversions']:<11} | {result['rate']:.2f}%")


("--------------------------------------------------------------------------------------------------")
("--------------------------------------------------------------------------------------------------")
("--------------------------------------------------------------------------------------------------")

user_id = input("Enter staff ID : ")
given_date = datetime(2024, 9, 1).date()
three_months_ago = given_date - timedelta(days=90)

print(f"\nAnalyzing Staff ID: {user_id}")
print(f"Date range: {three_months_ago} to {given_date}")
print("-" * 50)


recent_leads = (
    session.query(Lead)
    .filter(Lead.staff_id == user_id)
    .filter(Lead.creation_date >= three_months_ago)
    .filter(Lead.creation_date <= given_date)
    .all()
)

print(f"\nLEADS CREATED by Staff {user_id} in the period:")
print("Lead ID | Creation Date | Name | Status")
print("-" * 50)
for lead in recent_leads:
    print(f"{lead.lead_id} | {lead.creation_date} | {lead.first_name} {lead.last_name} | {lead.status}")

print(f"\nTotal leads created: {len(recent_leads)}")


recent_leads_count = len(recent_leads)


converted_leads = (
    session.query(Lead)
    .filter(Lead.staff_id == user_id)
    .filter(Lead.creation_date >= three_months_ago)
    .filter(Lead.creation_date <= given_date)
    .filter(Lead.conversion_date.isnot(None))
    .all()
)

print(f"\nCONVERTED LEADS (has conversion_date):")
print("Lead ID | Name | Created | Converted")
print("-" * 50)
for lead in converted_leads:
    print(f"{lead.lead_id} | {lead.first_name} {lead.last_name} | {lead.creation_date} | {lead.conversion_date}")


recent_conversions_count = len(converted_leads)

print(f"\nTotal conversions: {recent_conversions_count}")

#  conversion rate calculation
recent_leads_count = len(recent_leads)
conversion_rate = (recent_conversions_count / recent_leads_count) * 100 if recent_leads_count > 0 else 0

print(f"\nFINAL RESULT:")
print(f"Staff ID {user_id}: {recent_conversions_count}/{recent_leads_count} = {conversion_rate:.2f}%")

("--------------------------------------------------------------------------------------------------")
("--------------------------------------------------------------------------------------------------")
("--------------------------------------------------------------------------------------------------")


sql_logger = logging.getLogger('sqlalchemy.engine')
sql_logger.setLevel(logging.CRITICAL)
if sql_logger.hasHandlers():
    sql_logger.handlers.clear()

root_logger = logging.getLogger()
root_logger.setLevel(logging.CRITICAL)
if root_logger.hasHandlers():
    root_logger.handlers.clear()




Session = sessionmaker(bind=engine)
session = Session()


all_staff_ids = session.query(Lead.staff_id).distinct().all()
staff_ids = [staff_id[0] for staff_id in all_staff_ids]

print("Analyzing subscription revenue percentage for ALL STAFF:")
print("=" * 80)


all_subscriptions = session.query(Subscription).all()
total_revenue = Decimal(0)
for sub in all_subscriptions:
    total_revenue += Decimal(str(sub.amount))

print(f"Total subscription revenue across all members: ${total_revenue}")
print("-" * 80)


staff_results = []

for staff_id in staff_ids:
    
    converted_leads = (
        session.query(Lead)
        .filter_by(staff_id=staff_id)
        .filter(Lead.status == "converted")
        .filter(Lead.conversion_date.isnot(None))
        .all()
    )
    
    if converted_leads:
        total_staff_revenue = Decimal(0)
        processed_members = set()
        
        for lead in converted_leads:
            member = (
                session.query(Member)
                .filter(
                    Member.first_name == lead.first_name,
                    Member.last_name == lead.last_name,
                    Member.date_of_birth == lead.date_of_birth
                )
                .first()
            )
            
            if member and member.member_id not in processed_members:
                processed_members.add(member.member_id)
                
                
                member_subscriptions = (
                    session.query(Subscription)
                    .filter_by(member_id=member.member_id)
                    .all()
                )
                
                member_revenue = Decimal(0)
                for sub in member_subscriptions:
                    member_revenue += Decimal(str(sub.amount))
                
                total_staff_revenue += member_revenue
        
        
        if total_revenue > 0:
            percentage = (total_staff_revenue / total_revenue) * 100
        else:
            percentage = 0

        
        average_revenue = Decimal(0)
        if len(processed_members) > 0:
            average_revenue = total_staff_revenue / len(processed_members)
        
        staff_results.append({
            'staff_id': staff_id,
            'converted_leads': len(converted_leads),
            'unique_members': len(processed_members),
            'revenue': float(total_staff_revenue),
            'average_revenue': float(average_revenue),
            'percentage': float(percentage)
        })


staff_results.sort(key=lambda x: x['percentage'], reverse=True)


print("SUBSCRIPTION REVENUE ANALYSIS BY STAFF:")

print("Staff ID | Converted Leads | Unique Members | Revenue | Avg. Revenue | Percentage")
print("-" * 90) 

for result in staff_results:
    
    print(f"{result['staff_id']:<8} | {result['converted_leads']:<15} | {result['unique_members']:<14} | ${result['revenue']:<7.2f} | ${result['average_revenue']:<11.2f} | {result['percentage']:.2f}%")

print("-" * 90) 
print(f"Total Staff Analyzed: {len(staff_results)}")


if staff_results:
    print(f"\nTOP 5 STAFF BY SUBSCRIPTION REVENUE PERCENTAGE:")
    print("-" * 50)
    for i, result in enumerate(staff_results[:5], 1):
        print(f"{i}. Staff {result['staff_id']}: {result['percentage']:.2f}% (${result['revenue']:.2f})")

print("=" * 80)