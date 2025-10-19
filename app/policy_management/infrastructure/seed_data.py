from sqlalchemy.orm import Session
from datetime import date, timedelta
from .models import PolicyModel, PolicyStatusModel, PolicyTypeModel
from ..domain.entities import PolicyStatus, PolicyType


def seed_database(db: Session):
    """Seed the database with statuses, types, and sample policies"""
    print("Seeding database with initial data...")

    # First, seed statuses and types
    seed_statuses_and_types(db)

    # Then seed policies
    seed_policies(db)

    print("Database seeding completed successfully!")


def seed_statuses_and_types(db: Session):
    """Seed policy statuses and types lookup tables"""
    print("Seeding policy statuses and types...")

    # Clear existing data (optional - for clean reset)
    db.query(PolicyModel).delete()
    db.query(PolicyStatusModel).delete()
    db.query(PolicyTypeModel).delete()
    db.commit()

    # Seed policy statuses with comprehensive descriptions
    statuses_data = [
        {
            "name": PolicyStatus.ACTIVE.value,
            "description": "Policy is currently active and providing coverage",
        },
        {
            "name": PolicyStatus.PENDING.value,
            "description": "Policy is created but not yet activated",
        },
        {
            "name": PolicyStatus.INACTIVE.value,
            "description": "Policy is no longer active (expired or suspended)",
        },
        {
            "name": PolicyStatus.CANCELLED.value,
            "description": "Policy has been cancelled by insurer or insured",
        },
    ]

    print("Adding policy statuses...")
    for status_data in statuses_data:
        status = PolicyStatusModel(**status_data)
        db.add(status)
        print(f"{status_data['name']} - {status_data['description']}")

    db.commit()

    # Seed policy types with comprehensive descriptions
    types_data = [
        {
            "name": PolicyType.PROPERTY.value,
            "description": "Insurance for buildings, contents, and business interruption",
        },
        {
            "name": PolicyType.CASUALTY.value,
            "description": "Liability insurance for injuries and damages to others",
        },
        {
            "name": PolicyType.MARINE.value,
            "description": "Insurance for ships, cargo, and marine liabilities",
        },
        {
            "name": PolicyType.CONSTRUCTION.value,
            "description": "Insurance for construction projects and contractors",
        },
    ]

    print("Adding policy types...")
    for type_data in types_data:
        policy_type = PolicyTypeModel(**type_data)
        db.add(policy_type)
        print(f"{type_data['name']} - {type_data['description']}")

    db.commit()
    print("Policy statuses and types seeded successfully!")


def seed_policies(db: Session):
    """Seed sample policies with realistic data"""
    print("Seeding sample policies...")

    # Get status and type IDs for foreign keys
    status_map = {
        status.name: status.id for status in db.query(PolicyStatusModel).all()
    }
    type_map = {
        policy_type.name: policy_type.id
        for policy_type in db.query(PolicyTypeModel).all()
    }

    today = date.today()

    # Comprehensive sample policies data
    policies_data = [
        # ACTIVE PROPERTY POLICIES
        {
            "policy_number": "TMPROP2024001",
            "insured_name": "Acme Corporation Ltd",
            "premium_amount": 12500.00,
            "premium_currency": "GBP",
            "period_start_date": today - timedelta(days=30),
            "period_end_date": today + timedelta(days=335),
            "status_id": status_map[PolicyStatus.ACTIVE.value],
            "type_id": type_map[PolicyType.PROPERTY.value],
        },
        {
            "policy_number": "TMPROP2024002",
            "insured_name": "Global Logistics Inc",
            "premium_amount": 8750.50,
            "premium_currency": "GBP",
            "period_start_date": today - timedelta(days=15),
            "period_end_date": today + timedelta(days=350),
            "status_id": status_map[PolicyStatus.ACTIVE.value],
            "type_id": type_map[PolicyType.PROPERTY.value],
        },
        {
            "policy_number": "TMPROP2024003",
            "insured_name": "Safe Hands Hospital",
            "premium_amount": 45200.00,
            "premium_currency": "GBP",
            "period_start_date": today - timedelta(days=60),
            "period_end_date": today + timedelta(days=305),
            "status_id": status_map[PolicyStatus.ACTIVE.value],
            "type_id": type_map[PolicyType.PROPERTY.value],
        },
        # PENDING POLICIES (Ready for activation)
        {
            "policy_number": "TMMAR2024001",
            "insured_name": "Ocean Freight Services",
            "premium_amount": 23400.00,
            "premium_currency": "GBP",
            "period_start_date": today + timedelta(days=7),
            "period_end_date": today + timedelta(days=372),
            "status_id": status_map[PolicyStatus.PENDING.value],
            "type_id": type_map[PolicyType.MARINE.value],
        },
        {
            "policy_number": "TMCONST202401",
            "insured_name": "Tech Innovations Ltd",
            "premium_amount": 6800.00,
            "premium_currency": "GBP",
            "period_start_date": today + timedelta(days=14),
            "period_end_date": today + timedelta(days=379),
            "status_id": status_map[PolicyStatus.PENDING.value],
            "type_id": type_map[PolicyType.CONSTRUCTION.value],
        },
        {
            "policy_number": "TMCAS2024001",
            "insured_name": "Metro Transport Ltd",
            "premium_amount": 18900.00,
            "premium_currency": "GBP",
            "period_start_date": today + timedelta(days=3),
            "period_end_date": today + timedelta(days=368),
            "status_id": status_map[PolicyStatus.PENDING.value],
            "type_id": type_map[PolicyType.CASUALTY.value],
        },
        # INACTIVE/EXPIRED POLICIES
        {
            "policy_number": "TMCAS2023001",
            "insured_name": "City Construction Group",
            "premium_amount": 15600.75,
            "premium_currency": "GBP",
            "period_start_date": today - timedelta(days=400),
            "period_end_date": today - timedelta(days=35),
            "status_id": status_map[PolicyStatus.INACTIVE.value],
            "type_id": type_map[PolicyType.CASUALTY.value],
        },
        {
            "policy_number": "TMPROP2023001",
            "insured_name": "Retail Chain UK Ltd",
            "premium_amount": 8900.00,
            "premium_currency": "GBP",
            "period_start_date": today - timedelta(days=395),
            "period_end_date": today - timedelta(days=30),
            "status_id": status_map[PolicyStatus.INACTIVE.value],
            "type_id": type_map[PolicyType.PROPERTY.value],
        },
        # CANCELLED POLICIES
        {
            "policy_number": "TMMAR2023001",
            "insured_name": "Port Authority Ltd",
            "premium_amount": 32150.00,
            "premium_currency": "GBP",
            "period_start_date": today - timedelta(days=200),
            "period_end_date": today + timedelta(days=165),
            "status_id": status_map[PolicyStatus.CANCELLED.value],
            "type_id": type_map[PolicyType.MARINE.value],
        },
        {
            "policy_number": "TMCAS2023051",
            "insured_name": "Manufacturing Solutions Inc",
            "premium_amount": 11200.00,
            "premium_currency": "GBP",
            "period_start_date": today - timedelta(days=150),
            "period_end_date": today + timedelta(days=215),
            "status_id": status_map[PolicyStatus.CANCELLED.value],
            "type_id": type_map[PolicyType.CASUALTY.value],
        },
        # ADDITIONAL VARIED POLICIES
        {
            "policy_number": "TMPROP2024004",
            "insured_name": "University Campus Ltd",
            "premium_amount": 28700.00,
            "premium_currency": "GBP",
            "period_start_date": today - timedelta(days=45),
            "period_end_date": today + timedelta(days=320),
            "status_id": status_map[PolicyStatus.ACTIVE.value],
            "type_id": type_map[PolicyType.PROPERTY.value],
        },
        {
            "policy_number": "TMMAR2024002",
            "insured_name": "Coastal Shipping Co",
            "premium_amount": 15600.00,
            "premium_currency": "GBP",
            "period_start_date": today + timedelta(days=10),
            "period_end_date": today + timedelta(days=375),
            "status_id": status_map[PolicyStatus.PENDING.value],
            "type_id": type_map[PolicyType.MARINE.value],
        },
        {
            "policy_number": "TMCONST202402",
            "insured_name": "Bridge Builders Ltd",
            "premium_amount": 54300.00,
            "premium_currency": "GBP",
            "period_start_date": today - timedelta(days=20),
            "period_end_date": today + timedelta(days=345),
            "status_id": status_map[PolicyStatus.ACTIVE.value],
            "type_id": type_map[PolicyType.CONSTRUCTION.value],
        },
    ]

    print("Adding sample policies...")
    policies_added = 0

    for policy_data in policies_data:
        policy = PolicyModel(**policy_data)
        db.add(policy)

        # Get status and type names for display
        status_name = next(
            (k for k, v in status_map.items() if v == policy_data["status_id"]),
            "Unknown",
        )
        type_name = next(
            (k for k, v in type_map.items() if v == policy_data["type_id"]), "Unknown"
        )

        print(
            f"{policy_data['policy_number']} - {policy_data['insured_name']} ({status_name} {type_name})"
        )
        policies_added += 1

    db.commit()
    print(f"Successfully seeded {policies_added} sample policies!")


def get_status_id(db: Session, status_name: str) -> int:
    """Helper to get status ID by name"""
    status = (
        db.query(PolicyStatusModel)
        .filter(PolicyStatusModel.name == status_name)
        .first()
    )
    return status.id if status else None


def get_type_id(db: Session, type_name: str) -> int:
    """Helper to get type ID by name"""
    policy_type = (
        db.query(PolicyTypeModel).filter(PolicyTypeModel.name == type_name).first()
    )
    return policy_type.id if policy_type else None


def seed_sample_policy(db: Session) -> PolicyModel:
    """Seed a single sample policy for testing - returns the created policy"""
    today = date.today()

    # Get status and type IDs
    status_id = get_status_id(db, PolicyStatus.PENDING.value)
    type_id = get_type_id(db, PolicyType.PROPERTY.value)

    sample_policy = PolicyModel(
        policy_number="TMSAMPLE001",
        insured_name="Sample Insurance Company",
        premium_amount=5000.00,
        premium_currency="GBP",
        period_start_date=today,
        period_end_date=today + timedelta(days=365),
        status_id=status_id,
        type_id=type_id,
    )

    db.add(sample_policy)
    db.commit()
    db.refresh(sample_policy)
    print(f"Added sample policy: {sample_policy.policy_number}")
    return sample_policy


def clear_policies(db: Session):
    """Clear all policies from the database (for testing/reset)"""
    print("Clearing all policies from database...")
    deleted_count = db.query(PolicyModel).delete()
    db.commit()
    print(f"{deleted_count} policies cleared from database")


def clear_all_data(db: Session):
    """Clear all data including statuses and types (complete reset)"""
    print("Clearing ALL database data...")
    db.query(PolicyModel).delete()
    db.query(PolicyStatusModel).delete()
    db.query(PolicyTypeModel).delete()
    db.commit()
    print("All database data cleared")


def get_seeding_summary(db: Session):
    """Get a summary of seeded data"""
    status_count = db.query(PolicyStatusModel).count()
    type_count = db.query(PolicyTypeModel).count()
    policy_count = db.query(PolicyModel).count()

    print("\nSEEDING SUMMARY:")
    print(f"   Policy Statuses: {status_count}")
    print(f"   Policy Types: {type_count}")
    print(f"   Policies: {policy_count}")

    # Breakdown by status
    print("\n   Policies by Status:")
    policies = db.query(PolicyModel).all()
    status_stats = {}
    for policy in policies:
        status_name = policy.status_rel.name if policy.status_rel else "Unknown"
        status_stats[status_name] = status_stats.get(status_name, 0) + 1

    for status, count in status_stats.items():
        print(f"     {status}: {count}")

    # Breakdown by type
    print("\n   Policies by Type:")
    type_stats = {}
    for policy in policies:
        type_name = policy.type_rel.name if policy.type_rel else "Unknown"
        type_stats[type_name] = type_stats.get(type_name, 0) + 1

    for policy_type, count in type_stats.items():
        print(f"     {policy_type}: {count}")
