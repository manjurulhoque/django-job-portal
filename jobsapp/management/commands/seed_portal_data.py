import random
from datetime import timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from accounts.models import User
from categories.models import Category
from jobsapp.models import (
    Company,
    CompanySize,
    ExperienceLevel,
    Job,
    JobStatus,
    JobType,
    SalaryPeriod,
    WorkplaceType,
)
from tags.models import Tag


class Command(BaseCommand):
    help = "Seed realistic bulk data for categories, tags, users, companies, and jobs."

    def add_arguments(self, parser):
        parser.add_argument("--categories", type=int, default=20)
        parser.add_argument("--tags", type=int, default=30)
        parser.add_argument("--users", type=int, default=50)
        parser.add_argument("--jobs", type=int, default=300)
        parser.add_argument("--seed", type=int, default=42)

    @transaction.atomic
    def handle(self, *args, **options):
        random.seed(options["seed"])

        categories = self._seed_categories(options["categories"])
        tags = self._seed_tags(options["tags"])
        users = self._seed_users(options["users"])
        companies = self._seed_companies(users["employers"])
        jobs_created = self._seed_jobs(options["jobs"], users["employers"], companies, tags, categories)

        self.stdout.write(self.style.SUCCESS("Seeding completed successfully."))
        self.stdout.write(f"Categories: {len(categories)}")
        self.stdout.write(f"Tags: {len(tags)}")
        self.stdout.write(
            f"Users: employees={len(users['employees'])}, employers={len(users['employers'])}, admins={len(users['admins'])}"
        )
        self.stdout.write(f"Companies: {len(companies)}")
        self.stdout.write(f"Jobs created this run: {jobs_created}")

    def _seed_categories(self, target_count):
        base_categories = [
            ("Software Engineering", "Backend, frontend, and full-stack software roles."),
            ("Data & AI", "Data science, analytics, machine learning, and AI jobs."),
            ("DevOps & Cloud", "Infrastructure, cloud platform, and reliability engineering."),
            ("Cybersecurity", "Security operations, risk, compliance, and testing roles."),
            ("UI/UX Design", "Product design, user research, and design system jobs."),
            ("Product Management", "Product owner, analyst, and delivery leadership roles."),
            ("Digital Marketing", "SEO, performance marketing, and growth campaigns."),
            ("Content & Copywriting", "Content strategy, technical writing, and editorial roles."),
            ("Sales & Business Development", "B2B sales, partnerships, and account growth."),
            ("Customer Support", "Support operations and customer success positions."),
            ("HR & Recruitment", "Talent acquisition, HR operations, and people roles."),
            ("Finance & Accounting", "Budgeting, payroll, taxation, and financial analysis."),
            ("Legal & Compliance", "Corporate legal, contracts, and compliance management."),
            ("Operations", "Business operations, process improvement, and logistics."),
            ("Healthcare", "Clinical and non-clinical healthcare opportunities."),
            ("Education & Training", "Teaching, curriculum, and educational program roles."),
            ("Media & Communications", "Public relations, communications, and media jobs."),
            ("Architecture & Engineering", "Civil, mechanical, and construction engineering."),
            ("Hospitality & Travel", "Hotel, tourism, and travel services positions."),
            ("Supply Chain & Procurement", "Sourcing, inventory, and supply chain operations."),
        ]

        created = []
        for idx, (name, desc) in enumerate(base_categories[:target_count], start=1):
            category, _ = Category.objects.get_or_create(
                name=name,
                defaults={"description": desc},
            )
            created.append(category)

        while len(created) < target_count:
            n = len(created) + 1
            category, _ = Category.objects.get_or_create(
                name=f"Category {n}",
                defaults={"description": f"General category {n}."},
            )
            created.append(category)
        return created

    def _seed_tags(self, target_count):
        base_tags = [
            "Python",
            "Django",
            "FastAPI",
            "JavaScript",
            "TypeScript",
            "React",
            "Next.js",
            "Node.js",
            "PostgreSQL",
            "MySQL",
            "Redis",
            "Docker",
            "Kubernetes",
            "AWS",
            "GCP",
            "Azure",
            "Terraform",
            "CI/CD",
            "Git",
            "Linux",
            "Data Analysis",
            "Machine Learning",
            "Power BI",
            "Figma",
            "UI Design",
            "SEO",
            "Content Writing",
            "Communication",
            "Project Management",
            "Problem Solving",
        ]

        created = []
        for name in base_tags[:target_count]:
            tag, _ = Tag.objects.get_or_create(name=name)
            created.append(tag)

        while len(created) < target_count:
            n = len(created) + 1
            tag, _ = Tag.objects.get_or_create(name=f"Skill-{n}")
            created.append(tag)
        return created

    def _seed_users(self, target_count):
        if target_count < 3:
            raise ValueError("users count must be at least 3")

        employer_count = int(target_count * 0.5)
        employee_count = int(target_count * 0.4)
        admin_count = target_count - employer_count - employee_count

        first_names = [
            "Arafat",
            "Nusrat",
            "Tanvir",
            "Farhana",
            "Sabbir",
            "Mim",
            "Rahim",
            "Mahi",
            "Rafi",
            "Tania",
            "Sadia",
            "Nayeem",
            "Shila",
            "Arman",
            "Ishrat",
            "Rasel",
            "Adiba",
            "Fahim",
            "Tahsin",
            "Nabila",
        ]
        last_names = [
            "Rahman",
            "Ahmed",
            "Hossain",
            "Islam",
            "Khan",
            "Sarker",
            "Miah",
            "Karim",
            "Akter",
            "Chowdhury",
        ]

        employees = self._bulk_create_users(
            count=employee_count,
            role="employee",
            prefix="candidate",
            first_names=first_names,
            last_names=last_names,
            is_staff=False,
            is_superuser=False,
        )
        employers = self._bulk_create_users(
            count=employer_count,
            role="employer",
            prefix="employer",
            first_names=first_names,
            last_names=last_names,
            is_staff=False,
            is_superuser=False,
        )
        admins = self._bulk_create_users(
            count=admin_count,
            role="admin",
            prefix="admin",
            first_names=first_names,
            last_names=last_names,
            is_staff=True,
            is_superuser=False,
        )
        return {"employees": employees, "employers": employers, "admins": admins}

    def _bulk_create_users(self, count, role, prefix, first_names, last_names, is_staff, is_superuser):
        created = []
        i = 1
        while len(created) < count:
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            email = f"{prefix}{i}@jobpilot.dev"
            i += 1
            if User.objects.filter(email=email).exists():
                continue
            user = User.objects.create_user(
                email=email,
                password="Pass@1234",
                role=role,
                first_name=first_name,
                last_name=last_name,
                gender=random.choice(["male", "female"]),
                is_staff=is_staff,
                is_superuser=is_superuser,
            )
            created.append(user)
        return created

    def _seed_companies(self, employers):
        company_names = [
            "Pathao Technologies",
            "bKash Limited",
            "Brain Station 23",
            "TigerIT Bangladesh",
            "DataSoft Systems",
            "Aamra Networks",
            "Reve Systems",
            "ShopUp",
            "Chaldal",
            "Sheba.xyz",
            "SSL Wireless",
            "LeadSoft Bangladesh",
            "Augmedix Bangladesh",
            "Southtech Group",
            "Dynamic Solution Innovators",
            "Portonics Limited",
            "Genex Infosys",
            "TechnoNext Software",
            "Enosis Solutions",
            "BJIT Group",
            "Nascenia",
            "Kona Software Lab",
            "PriyoShop",
            "ShareTrip",
            "MonstarLab Bangladesh",
            "Mediusware",
            "Riseup Labs",
            "Cefalo Bangladesh",
            "W3 Engineers",
            "Selise Bangladesh",
        ]
        industries = [
            "Information Technology",
            "FinTech",
            "E-commerce",
            "Telecommunications",
            "Healthcare Technology",
            "SaaS",
            "Logistics",
            "EdTech",
        ]
        headquarters = ["Dhaka, Bangladesh", "Chattogram, Bangladesh", "Sylhet, Bangladesh"]

        created = []
        for idx, employer in enumerate(employers):
            base_name = company_names[idx % len(company_names)]
            name = f"{base_name} {idx // len(company_names) + 1}" if idx >= len(company_names) else base_name
            company, _ = Company.objects.get_or_create(
                user=employer,
                name=name,
                defaults={
                    "tagline": random.choice(
                        [
                            "Building scalable digital products.",
                            "Empowering careers through technology.",
                            "Innovation-driven workplace culture.",
                        ]
                    ),
                    "description": (
                        f"{name} is a growth-focused organization hiring top talent for modern digital teams."
                    ),
                    "website": f"https://{name.lower().replace(' ', '').replace('.', '')}.com",
                    "industry": random.choice(industries),
                    "headquarters": random.choice(headquarters),
                    "size": random.choice(CompanySize.values),
                    "culture_benefits": (
                        "Flexible hours, hybrid work options, learning budget, health coverage, and performance bonuses."
                    ),
                    "is_verified": random.choice([True, False, True]),
                    "featured": random.choice([True, False, False]),
                },
            )
            created.append(company)
        return created

    def _seed_jobs(self, target_count, employers, companies, tags, categories):
        if not employers or not companies:
            raise ValueError("At least one employer and one company are required to create jobs.")
        if not categories:
            raise ValueError("At least one category is required to create jobs.")

        role_pool = [
            "Software Engineer",
            "Backend Engineer",
            "Frontend Engineer",
            "Full Stack Developer",
            "DevOps Engineer",
            "QA Engineer",
            "Product Designer",
            "UI/UX Designer",
            "Data Analyst",
            "Data Scientist",
            "Project Manager",
            "HR Executive",
            "Digital Marketing Specialist",
            "Accountant",
            "Customer Success Executive",
        ]
        location_pool = [
            "Dhaka, Bangladesh",
            "Chattogram, Bangladesh",
            "Sylhet, Bangladesh",
            "Khulna, Bangladesh",
            "Rajshahi, Bangladesh",
            "Remote",
        ]

        jobs_created = 0
        attempts = 0
        while jobs_created < target_count and attempts < target_count * 3:
            attempts += 1
            employer = random.choice(employers)
            employer_companies = [company for company in companies if company.user_id == employer.id]
            company = random.choice(employer_companies) if employer_companies else random.choice(companies)

            title = f"{random.choice(['Junior', 'Mid', 'Senior', 'Lead'])} {random.choice(role_pool)}"
            now = timezone.now()
            application_deadline = now + timedelta(days=random.randint(10, 90))
            salary_min = Decimal(random.randint(30000, 120000))
            salary_max = salary_min + Decimal(random.randint(10000, 150000))

            job = Job.objects.create(
                user=employer,
                company=company,
                category=random.choice(categories),
                title=title,
                description=(
                    f"We are hiring a {title} to work on impactful products and collaborate with cross-functional teams."
                ),
                responsibilities=(
                    "Build high-quality features, collaborate with team members, and improve system reliability."
                ),
                requirements=(
                    "Strong communication, practical problem-solving, and relevant professional experience."
                ),
                location=random.choice(location_pool),
                type=random.choice(JobType.values),
                workplace_type=random.choice(WorkplaceType.values),
                experience_level=random.choice(ExperienceLevel.values),
                application_deadline=application_deadline,
                website=company.website,
                filled=False,
                status=random.choices(
                    [JobStatus.PUBLISHED, JobStatus.DRAFT, JobStatus.CLOSED],
                    weights=[75, 20, 5],
                    k=1,
                )[0],
                salary=int(salary_max),
                salary_min=salary_min,
                salary_max=salary_max,
                salary_currency="BDT",
                salary_period=random.choice(SalaryPeriod.values),
                vacancy=random.randint(1, 8),
                is_featured=random.choice([True, False, False, False]),
            )

            picked_tags = random.sample(tags, k=random.randint(3, min(7, len(tags))))
            job.tags.set(picked_tags)
            jobs_created += 1

        return jobs_created
