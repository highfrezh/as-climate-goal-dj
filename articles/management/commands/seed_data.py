from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify
from articles.models import Author, ClimateArticles, ResearchResources
import random

class Command(BaseCommand):
    help = 'Seeds the database with 5 Authors, 10 detailed Climate Articles, and 10 Research Resources.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Clearing existing Authors, Articles, and Research Resources..."))
        
        # Safe deletion to avoid constraints issues
        ClimateArticles.objects.all().delete()
        Author.objects.all().delete()
        ResearchResources.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Database cleared! Beginning database seed..."))

        # -------------------------------------------------------------
        # 1. CREATE 5 AUTHORS
        # -------------------------------------------------------------
        authors_data = [
            {
                "name": "Dr. Alimat Adesina",
                "role": "Lead Climate Scientist & Agronomist",
                "bio": "Dr. Alimat Adesina is an expert in ecological conservation and agricultural resilience in sub-Saharan Africa. She holds a PhD in Environmental Science and designs adaptive farming models."
            },
            {
                "name": "Prof. Benjamin Mensah",
                "role": "Director of Renewable Energy Systems",
                "bio": "Prof. Benjamin Mensah conducts cutting-edge research on solar grid integration and rural off-grid electrification pathways across West Africa."
            },
            {
                "name": "Dr. Chidi Okeke",
                "role": "Urban Hydrologist & Watershed Specialist",
                "bio": "Dr. Chidi Okeke specializes in flood mitigation strategies, city drainage infrastructure design, and coastal delta conservation under extreme rainfall pressures."
            },
            {
                "name": "Engr. Amina Yusuf",
                "role": "Sustainable Infrastructure Engineer",
                "bio": "Engr. Amina Yusuf develops eco-friendly construction standards, low-carbon building materials, and green transit systems for rapidly growing smart cities."
            },
            {
                "name": "Ms. Joy Mutua",
                "role": "Youth Climate Advocacy Coordinator",
                "bio": "Ms. Joy Mutua leads international climate literacy outreach campaigns, high school eco-clubs, and youth-led reforestation activities."
            }
        ]

        authors = []
        for a_data in authors_data:
            author = Author.objects.create(
                name=a_data["name"],
                role=a_data["role"],
                bio=a_data["bio"]
            )
            authors.append(author)
            self.stdout.write(f"  Created Author: {author.name}")

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {len(authors)} Authors!"))

        # -------------------------------------------------------------
        # 2. CREATE 10 ARTICLES
        # -------------------------------------------------------------
        articles_data = [
            {
                "title": "The Silent Threat: How Rising Temperatures are Transforming African Agriculture",
                "description": "An in-depth analysis of rising temperatures across sub-Saharan Africa and the critical crop adaptations necessary to safeguard local farming systems.",
                "content": """
<h2>Understanding the Impact on Crop Yields</h2>
<p>Climate change is no longer a distant projection; it is a current reality disrupting farming cycles across the continent. With temperatures rising 1.5 times faster in sub-Saharan Africa than the global average, major staple crops like maize, millet, and sorghum are facing unprecedented heat stress.</p>

<blockquote>
    "We are witnessing a shift in traditional planting seasons, forcing smallholder farmers to gamble with their harvests. Adaptation is no longer optional — it is our only survival mechanism."
</blockquote>

<h3>Innovative Solutions for Climate Resilience</h3>
<p>To combat these shifts, scientists and agronomists are introducing several critical measures:</p>
<ul>
    <li><strong>Drought-Resilient Seeds:</strong> Biofortified and drought-tolerant seed varieties capable of yielding under extreme weather conditions.</li>
    <li><strong>Smart Irrigation Systems:</strong> Shifting away from rain-fed agriculture toward solar-powered drip irrigation.</li>
    <li><strong>Regenerative Agroforestry:</strong> Planting native trees alongside crops to maintain soil nutrients, improve water retention, and cool the microclimate.</li>
</ul>
                """,
                "category": "Climate Science",
                "status": "published",
                "author": authors[0], # Dr. Alimat
                "video_url": "https://www.youtube.com/watch?v=y7z99W3_XbQ",
                "is_featured": True
            },
            {
                "title": "Quick Guide: 3 Daily Habits to Combat Climate Change Right Now!",
                "description": "Think climate action is too complex? Think again! Watch this quick vertical breakdown on three tiny changes you can make in your home today.",
                "content": """
<h2>Tiny Habits, Massive Global Impact</h2>
<p>Individual action is the foundation of global change. While systemic policies are crucial, modifying our daily interactions with energy, water, and waste builds a culture of environmental accountability.</p>

<h3>1. Master the Phantom Load</h3>
<p>Did you know that appliances still consume energy when plugged in, even if they are turned off? Unplugging chargers, microwaves, and television consoles when not in use can save up to 10% on your household electrical consumption.</p>

<h3>2. The 5-Minute Shower Challenge</h3>
<p>Reducing your daily shower duration by just two minutes saves thousands of gallons of clean water annually and drastically decreases the energy required to heat and pump water.</p>

<h3>3. Plant One Native Shrub</h3>
<p>If you have access to a small patch of land or even a balcony container, planting a native plant or flower provides crucial sanctuary for local pollinators and extracts carbon dioxide directly from the atmosphere.</p>
                """,
                "category": "Youth Advocacy",
                "status": "published",
                "author": authors[4], # Ms. Joy
                "video_url": "https://www.tiktok.com/@unitednations/video/7212456789012345678",
                "is_featured": False
            },
            {
                "title": "Green Energy Horizons: Accelerating Off-Grid Solar Power in Rural Villages",
                "description": "Exploring how localized solar mini-grids are bypassing legacy utility grids, lighting up rural African villages, and fostering sustainable economic growth.",
                "content": """
<h2>The Off-Grid Revolution</h2>
<p>Across rural Africa, thousands of communities are skipping the centralized, fossil-fuel-dependent grid infrastructure entirely. Instead, clean solar mini-grids are lighting homes, powering schools, and driving local micro-economies forward without carbon footprints.</p>

<h3>Empowering Local Communities</h3>
<p>Decentralized energy systems provide far more than electricity; they offer economic liberation. Solar-powered refrigeration allows agricultural markets to store fresh produce, while clinics safely preserve vital vaccines overnight.</p>
                """,
                "category": "Renewable Energy",
                "status": "published",
                "author": authors[1], # Prof. Benjamin
                "video_url": "https://www.youtube.com/watch?v=gT8Z9Fz4tE0",
                "is_featured": True
            },
            {
                "title": "Decoding Carbon Footprint: What Does 1 Ton of CO2 Look Like?",
                "description": "Have you ever wondered what carbon emissions actually look like? Here is a fast, visually engaging breakdown of one ton of CO2 gas.",
                "content": """
<h2>Visualizing the Invisible</h2>
<p>Carbon dioxide is an invisible greenhouse gas, making it difficult for many to grasp its scale. One metric ton of CO2 would occupy a giant sphere roughly 33 feet (10 meters) in diameter! That is equivalent to the height of a three-story building.</p>

<h3>Where Does it Come From?</h3>
<p>An average gas-powered passenger vehicle emits approximately 4.6 metric tons of CO2 per year. This constant invisible accumulation traps solar heat within our atmosphere and accelerates global temperature rise.</p>
                """,
                "category": "Climate Science",
                "status": "published",
                "author": authors[1], # Prof. Benjamin
                "video_url": "https://www.tiktok.com/@climatetalks/video/7222345678912345678",
                "is_featured": False
            },
            {
                "title": "Rising Tides, Crowded Cities: Developing Coastal Defenses for Lagos and Accra",
                "description": "Analyzing how coastal urbanization and sea-level rise are threatening African economic hubs, and the modern engineering defenses deployed to save them.",
                "content": """
<h2>The Threat to Coastal Megacities</h2>
<p>Lagos, Accra, and Maputo are growing at breakneck speeds, but their coastal geography puts millions of citizens directly in the path of rising sea levels. High tides combined with heavy seasonal rainfall frequently submerge low-lying residential sectors.</p>

<h3>Building the Defenses of Tomorrow</h3>
<p>Engineers are shifting away from rigid concrete sea walls toward nature-based soft infrastructure. Restoring expansive mangrove forests and coastal wetlands absorbs storm waves far more effectively while rejuvenating marine biodiversity hubs.</p>
                """,
                "category": "Infrastructure",
                "status": "published",
                "author": authors[2], # Dr. Chidi
                "video_url": "https://www.youtube.com/watch?v=kYJv1zN_yE0",
                "is_featured": False
            },
            {
                "title": "Avoid Greenwashing! Spotting Real vs Fake Eco-Friendly Brands in 30 Seconds",
                "description": "A rapid checklist to help you see past marketing hype and identify companies that are genuinely sustainable.",
                "content": """
<h2>What is Greenwashing?</h2>
<p>Greenwashing occurs when brands spend more time and money marketing their green credentials than actually implementing eco-friendly operational standards. Don't be fooled by green leaf icons or Earth-friendly buzzwords!</p>

<h3>The Real Sustainability Checklist</h3>
<p>Look for concrete data, third-party certifications (like B-Corp or OEKO-TEX), transparent supply chain disclosures, and verifiable carbon offset program auditing report pages.</p>
                """,
                "category": "Youth Advocacy",
                "status": "published",
                "author": authors[4], # Ms. Joy
                "video_url": "https://www.tiktok.com/@climatechoice/video/7233456789012345678",
                "is_featured": False
            },
            {
                "title": "Rethinking Waste: Circular Economy Strategies in Emerging African Cities",
                "description": "Transitioning urban waste crises into economic engines through sustainable organic composting, recycling cooperatives, and eco-friendly consumer goods.",
                "content": """
<h2>From Waste to Wealth</h2>
<p>Rapid urban migration generates massive challenges for traditional sanitation systems. However, forward-thinking waste cooperatives are rewriting the script by transforming discarded plastics and organic waste into raw manufacturing materials and soil compost.</p>

<h3>Strengthening City Economies</h3>
<p>Providing formal training and health equipment to localized recyclers integrates marginalized communities directly into the formal municipal green economy and prevents toxic landfill accumulation.</p>
                """,
                "category": "Infrastructure",
                "status": "published",
                "author": authors[3], # Engr. Amina
                "video_url": "https://www.youtube.com/watch?v=R532D_K823Q",
                "is_featured": False
            },
            {
                "title": "Stop throwing away food! How compost fights climate change in your kitchen",
                "description": "Did you know that rotting food waste in landfills emits methane, a highly potent greenhouse gas? Here is how to compost easily.",
                "content": """
<h2>The Methane Danger</h2>
<p>When food waste is trapped in landfills, it decomposes anaerobically (without oxygen), releasing massive amounts of methane gas. Methane is over 25 times more effective at trapping heat in the atmosphere than carbon dioxide!</p>

<h3>Enter Composting</h3>
<p>By composting kitchen leftovers with dry leaves or sawdust in an aerated bin, you allow aerobic decomposition. This creates nutrient-rich soil food and completely prevents methane emissions.</p>
                """,
                "category": "Sustainability",
                "status": "published",
                "author": authors[3], # Engr. Amina
                "video_url": "https://www.tiktok.com/@compostclub/video/7244567890123456789",
                "is_featured": False
            },
            {
                "title": "Sustaining the Congo Basin: Protecting the Planet's Second Largest Rainforest",
                "description": "Exploring conservation policies, forest monitoring technologies, and local indigenous partnerships working to protect the lungs of Africa.",
                "content": """
<h2>The Green Lungs of Africa</h2>
<p>The Congo Basin forest spans over six nations and represents one of the world's most critical carbon sinks. Protecting this dense wilderness is essential to keeping global climate targets within realistic reach.</p>

<h3>Indigenous Stewardship</h3>
<p>Scientific studies prove that forest sectors managed directly by indigenous populations undergo far lower rates of deforestation. Empowering forest dwellers with legal land titles represents our strongest environmental shield.</p>
                """,
                "category": "Climate Science",
                "status": "published",
                "author": authors[0], # Dr. Alimat
                "video_url": "https://www.youtube.com/watch?v=g1e16f7P29Q",
                "is_featured": False
            },
            {
                "title": "Is electric the future? Electric motorbikes are conquering East Africa's roads!",
                "description": "Watch how lightweight, solar-powered electric motorbikes are scaling up, lowering urban noise, and slashing local air pollution.",
                "content": """
<h2>East Africa's Two-Wheel Revolution</h2>
<p>Motorbikes (commonly called boda-bodas) represent the vital lifeblood of urban transport. A major transition is underway as local tech ventures scale up swappable battery networks, allowing riders to swap to solar charging stations in minutes.</p>

<h3>Cleaner, Cheaper, Quieter</h3>
<p>Riders report a 40% reduction in operating and fuel costs, while city centers experience cleaner, breathable air and peaceful streets free from heavy combustion engine noise.</p>
                """,
                "category": "Sustainability",
                "status": "published",
                "author": authors[3], # Engr. Amina
                "video_url": "https://www.tiktok.com/@ebikesafrica/video/7255678901234567890",
                "is_featured": False
            }
        ]

        for index, art_data in enumerate(articles_data):
            # Parse YouTube/TikTok ID manually inside command to ensure save() is executed cleanly
            article = ClimateArticles.objects.create(
                title=art_data["title"],
                description=art_data["description"],
                content=art_data["content"],
                category=art_data["category"],
                status=art_data["status"],
                author=art_data["author"],
                video_url=art_data["video_url"],
                is_featured=art_data["is_featured"],
                date=timezone.now().date() - timezone.timedelta(days=index * 2) # distribute dates
            )
            self.stdout.write(f"  Created Article: {article.title} ({article.platform.upper()})")

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {len(articles_data)} Climate Articles!"))

        # -------------------------------------------------------------
        # 3. CREATE 10 RESEARCH RESOURCES LINKS
        # -------------------------------------------------------------
        resources_data = [
            {
                "title": "IPCC Sixth Assessment Report on Climate Impacts",
                "description": "Access the comprehensive IPCC assessment report outlining key regional impacts, adaptation strategies, and vulnerable sectors in sub-Saharan Africa.",
                "external_url": "https://www.ipcc.ch/report/ar6/wg2/"
            },
            {
                "title": "UNEP Environmental Outlook & Action Plan for Africa",
                "description": "An exhaustive UN policy document describing current desertification, water conservation frameworks, and continental ecosystem restoration targets.",
                "external_url": "https://www.unep.org/regions/africa"
            },
            {
                "title": "World Bank Climate Change Interactive Knowledge Portal",
                "description": "Explore detailed meteorological projection maps, historic rainfall charts, and climate risk assessments mapped by specific country.",
                "external_url": "https://climateknowledgeportal.worldbank.org/"
            },
            {
                "title": "Green Climate Fund Projects & Capital Investment Portfolio",
                "description": "Examine operational project papers detailing active international investments in drought defenses and renewable networks across developing states.",
                "external_url": "https://www.greenclimate.fund/projects"
            },
            {
                "title": "African Development Bank Ten-Year Climate Risk Framework",
                "description": "Learn about institutional financing initiatives targeted toward sustainable agriculture, coastal protection, and rural mini-grid scaling.",
                "external_url": "https://www.afdb.org/en/topics-and-sectors/sectors/climate-change"
            },
            {
                "title": "Nature Climate Change: Crop Yield Resiliency Studies",
                "description": "An academic paper outlining laboratory progress in developing biofortified and heat-resilient crop varieties to protect food cycles.",
                "external_url": "https://www.nature.com/nclimate/"
            },
            {
                "title": "NASA Live Global Climate Change Indicator Dashboard",
                "description": "Track live global telemetry metrics covering atmospheric CO2 saturation, ocean heat anomalies, polar ice melt, and sea level rise.",
                "external_url": "https://climate.nasa.gov/"
            },
            {
                "title": "FAO Global Soil Partnership & Soil Organic Carbon Map",
                "description": "An interactive digital map mapping topsoil carbon density and providing sustainable management practices to combat soil degradation.",
                "external_url": "https://www.fao.org/global-soil-partnership/en/"
            },
            {
                "title": "World Resources Institute Global Forest Watch Initiative",
                "description": "Utilize high-resolution satellite imagery tracking and monitoring live tree cover loss, carbon sequestration, and forest fire threats.",
                "external_url": "https://www.wri.org/"
            },
            {
                "title": "WHO Climate Change, Heatwaves, and Public Health Risk Sheets",
                "description": "Review international research guidelines detailing the impact of temperature waves on vectors, urban heat index pressures, and local healthcare structures.",
                "external_url": "https://www.who.int/news-room/fact-sheets/detail/climate-change-and-health"
            }
        ]

        for res_data in resources_data:
            resource = ResearchResources.objects.create(
                title=res_data["title"],
                description=res_data["description"],
                external_url=res_data["external_url"]
            )
            self.stdout.write(f"  Created Research Resource: {resource.title}")

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {len(resources_data)} Research Resources!"))
        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully! DONE"))
