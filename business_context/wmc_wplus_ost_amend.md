# 🛒 WMC, Walmart+, OST & Amend Banner — Full Business Context
## Keel Agent Knowledge Base | Utility Modules, W+ Strategy, OST/Amend, Timers

*Source: Handover Doc.docx, Notes on WMC Cost_Benefit Analysis.docx, OST BRDs (Dedupe + White Space),*  
*W+ BRD, W+ Targeting Testing docs, WPlus and July Deals HP Options.docx,*  
*Utility Update.pptx, OST_Amend Analysis.pptx, Utility Mission and Strategy FY26.pptx, FY26 July W+ Homepage.pptx*  
*Maintained by: Keel Agent*

---

## 🧩 What Is "Utility"?

**Utility modules** = non-Site Merch driven homepage modules whose primary goal is **customer engagement and lifetime value** (not GMV/CTR-first).

| Utility Module | Business Owner | Purpose |
|---------------|---------------|---------|
| **WMC (Walmart Media Connect)** | Arundhati Sampath (Dir PM) | Paid ad placements in HPOV cards |
| **Walmart+ (W+)** | Emily Karp (Acq), Natalie Beck (Ret), Connor Schroeder (C&E) | Member acquisition, engagement, retention |
| **OST (Order Status Tracker)** | Emily Johnson | Post-purchase order status on Homepage |
| **Amend Banner** | Bryan Silver | Time-limited order change window |
| **Social** | Katherine Burrington / Caroline Lau | Social content placements |

**Utility Mission:** Build partnerships with utility teams to increase customer engagement, grow CLTV, and improve overall homepage performance.

---

## 📺 WMC — Walmart Media Connect (Ads)

### What WMC Is
WMC = the **paid advertising** layer on the Homepage. Advertisers (suppliers/brands) buy placements in HPOV cards 2 and 3 primarily.

### WMC Card Placement
| Card | WMC Role |
|------|---------|
| AutoScroll Card 2 | Primary WMC display ad placement (~92% sold) |
| AutoScroll Card 3 | Primary WMC sponsored product placement (~92% sold) |
| AutoScroll Card 1 | NOT a WMC card — Tier 1 site merch only |
| AutoScroll Card 4 | NOT a WMC card — Services only |
| AutoScroll Card 5 | NOT a typical WMC card |

> ⚠️ **WMC sells ~92% of Cards 2 & 3** — this limits site merch SOV in those positions.

### WMC Daily QA Process
- Pull ads from App POV 2 & 3
- Review all live ads ATF/BTF across all platforms
- Check for: copy overlap/cutoff, linking issues, prohibited categories
- Prohibited/Restricted list + POV guidelines on Confluence

### WMC Reporting Beacons (Key Data Issues)
1. **Delayed Ads Loading Flag**: When a customer sees default content THEN an ad loads — a flag is needed to measure the scale of this issue
2. **Ad Content Flag**: Flag applied to ad content to access ad performance on the full page
   - HeroPOV ad performance can be pulled based on ad dates + card placement via Autoscroll flag

### WMC vs Merch Cost/Benefit Analysis (Key Finding)
> *"Merch engagement far outperforms Ads engagement across all key metrics (CTR, exit rate, ATC)"*

| Metric | Merch (8 key msgs) | Ads (10 msgs) | Delta |
|--------|-------------------|---------------|-------|
| CTR | **0.64%** | 0.17% | Merch +277% |
| Exit Rate | **43.58%** | 58.80% | Merch better |
| ATC/1K Impressions | **1.67** | 0.24 | Merch +596% |
| GMV/Impression | **$2.07** | $0.49 | Merch +322% |

**But when Ad Revenue is added:**
| Slot | Merch GMV | Ads GMV + Ad Revenue | Winner |
|------|-----------|---------------------|--------|
| Card 1 position | Higher by +511% | — | Merch wins on GMV alone |
| Card 3 position | Lower by -69% | Ads wins (with revenue) | Ads wins when Ad Revenue included |
| Card 2 position | Higher by +56% | Lower by -93% (with revenue) | Ads wins (with revenue) |

> 📌 **Implication**: Merch wins on GMV and engagement. Ads wins when you factor in direct Ad Revenue. Leadership must weigh both when setting card assignment strategy.

### WMC Product Roadmap Items (FY26)
| Initiative | Status / Notes |
|-----------|---------------|
| 10-Card Placement | Alignment pending with Kate |
| P13N work on Default vs Personalized as Ads backup | In progress |
| Fresh/Frozen excluded from sales placements | Limits SOV in Hero, limits Video |
| Desktop full-bleed Hero | WMC needs 6 weeks post-test to launch |
| SIG Sponsored testing | In development |
| Video and Single SKU | Q3 testing |
| Beaconing: default + ad simultaneous flag | Jira created, ENG sizing |

### WMC Key Contacts
| Name | Role |
|------|------|
| Arundhati Sampath | Director PM |
| Akshay Gupta | PM Display |
| Deepali Reddy | PM Sponsored |
| Joanna Leung | Mgr, Yield Operations |
| Kate Popp | Sr. Mgr, Creative (Lightbox) |
| Sneha Peddireddy (Reddy) | Staff PM (Analytics) |
| Melinda Rusconi → Devki Desai | Staff, Tech Operations |
| Mara Crespi | Sr. Mgr, Business Development |

---

## 🟡 Walmart+ (W+) on Homepage

### W+ Homepage Strategy Overview
- Homepage = only **5% of GMV** — it is one part of a broader W+ site content strategy
- Currently **two placement types** on Homepage:
  1. **Targeted ATF event placements** (W+ Week, July Deals, AE1, AE2, October Deals)
  2. **Evergreen BTF placements** (low performance — likely to be eliminated)

### W+ Evergreen BTF Performance (Current State)
| Metric | Value |
|--------|-------|
| Impressions share | 13.7% of Homepage impressions |
| CTR | 0.16% |
| Total content benchmark | 0.40% |
| Homepage banner → signups | Only 3% of all trial signups; 8% of homepage signups |

### W+ ATF Event Performance
| Event | Impressions |
|-------|------------|
| W+ Week (Card 1) | **55M impressions** (47% SOV for Card 1) |

### W+ Member States (4 States — Used for Targeting)
| State | Description |
|-------|------------|
| **Paid** | Active W+ paying member |
| **Trial** | In free trial period |
| **Churned** | Was a member, cancelled/expired |
| **Nevermember** | Never signed up for W+ |

> ⚠️ A 5th dimension: **EBT eligible** — non-W+ members who qualify for Walmart+ Assist (discounted W+ membership)

### W+ Targeting Types
| Type | How It Works |
|------|-------------|
| **Soft targeting** | Customer sees SBU OR targeted message; P13N decides; NEVER shows wrong member state |
| **Hard targeting** | Only targeted users see the message; arbitration engine picks from eligible set; does NOT guarantee visibility |
| **Override targeting** | Targeted users see the message AND it's guaranteed — Q3 priority ask |

### W+ Arbitration / P13N Rules
- New messages launch in **exploration mode** — algorithm takes time to learn and allocate impressions
- New messages need **no more than 2 other assets in the same card** to get early visibility
- W+ member 'Plan' field should only be used WITH 'Status' (narrows targeting further)
- 'Status' and 'Segment' can be used independently
- W+ 'Restricted' persona checkbox may not show in MMUI but backend still works

### W+ Targeting Testing Learnings (June 2025)
| Scenario | Expected | Rule |
|----------|---------|------|
| EBT churned or never-member | Must see "Discounted W+ membership" | Hard rule |
| EBT trial member | Should NOT see EBT messaging | Hard rule |
| Paid member | Sees paid-member messaging only | Never wrong state |
| Incognito / no targeting | Random SBU messages, NOT W+ Week asset | Correct |

### W+ ATF Event Placement — July Deals 2025 Strategy

**Gap identified**: Jul 10–13, no ATF W+ discounted membership coverage

| Option | Placement | Recommended? |
|--------|-----------|-------------|
| **Option 1** | Add W+ discounted membership in HeroPOV as algorithmic message | ✅ **YES** |
| Option 2 | Timer countdown | ❌ NO (causes Deals timing confusion) |
| Option 3 | Below-fold Triple Pack | ❌ NO (too low, low impact) |

**Full July Deals W+ Timeline:**
| Period | Dates | Placement | States |
|--------|-------|-----------|--------|
| Discounted Membership lead-in | Jul 2 – Jul 9 7pm ET | Timer | All 4 states |
| Early Access | Jul 9 7pm – Jul 10 12am ET | Timer | All 4 states |
| Full Access gap | Jul 10–13 | HPOV (Option 1) or Timer | Trial/Churned/Nevermember |
| Last Chance | Jul 18–20 | Timer | Trial/Churned/Nevermember |

### W+ Strategic Pivots Needed (From BRD)
1. **Persistent ATF placements** by member state (acquisition + engagement)
   - High propensity non-members must see membership messaging **every visit, ATF**
   - High-risk low-engagement members (ZBU, 1BU) must see ATF engagement messaging every visit
   - Multi-benefit users (MBU) → less prominent placement sufficient
2. **Supplementary event-driven integrated ATF+BTF placements** (add W+ language to seasonal events where relevant)
3. **Supplementary ATF placements** for member-only launches, pre-sales, pre-orders
4. **New module placements** (e.g., 2×2 grid takeovers)
5. **BTF placements** (current evergreen likely eliminated)

### W+ Tech Gaps (From BRD — Must-Have Builds)
| Gap | Description |
|-----|------------|
| **Arbitration with W+ metrics** | W+ messages lose vs merch on CTR/GMV — need CLTV/acquisition metrics in arbitration engine |
| **Override targeting at asset level** | Guarantee specific member state sees specific message — critical for pre-sales/launches |
| **Dynamic badging** | Add "Ships free with Walmart+" language dynamically to non-W+ merch assets |
| **Benefit-linked SIG** | Link recently browsed category to W+ benefit and message it in a SIG card |

### W+ Homepage Signup Data (FY25)
| Flow | Share of Trial Signups |
|------|----------------------|
| Integrated Flow | 34% |
| MLP (homepage banner → MLP) | 31% |
| Splash | 23% |
| Unmapped | 12% |

| Source on Homepage | Share of Homepage Signups |
|-------------------|--------------------------|
| Splash page | 78% |
| Subnav | 12% |
| Evergreen banner | 8% |

> 📌 51% of FY25 trial signups came from **New to Digital customers** (no order in past year)
> 📌 40% of **prospective members** come from **desktop** — larger desktop opportunity for W+ than most businesses

### W+ Pretrial Segments (FY26 Signups)
| Segment | Share |
|---------|-------|
| Never Store, Never eComm | 29% |
| Dotcom | 22% |
| Delivery | 15% |
| Pickup | 13% |
| Store Only | 12% |
| Lapsed eComm | 10% |

### W+ Key Contacts
| Name | Role |
|------|------|
| Ryan Rash | Sr. Mgr, Site Merch C&E (campaigns/messaging) |
| Lance Woerner | Mgr, Site Merch C&E (timers) |
| Emma Matzko | Mgr, Site Merch C&E (W+ backup) |
| Emma Schaumann | Mgr, Business Strategy — W+ Acquisition |
| Tyler McKay | Sr. Mgr, Business Strategy — W+ Acquisition |
| Ryan Schudy | Dir, Business Strategy — W+ Acquisition |
| Russell Berger | Sr. Mgr, Business Strategy — W+ Retention |
| Lisa Grignon | Dir, Business Strategy — W+ Retention |
| Banani Mohapatra | Sr. Mgr, Data Science — W+ Analytics |
| Talha Rehman | Primary contact for W+ Prism/targeting setup review |

---

## 📦 OST — Order Status Tracker

### What OST Is
OST = the **Order Status Tracker banner** that appears on the Homepage showing a customer's current order status (delivery time, pickup time, etc.)

### OST Key Metrics (FY26 YTD)
| Metric | Value |
|--------|-------|
| **CTR** | **3.41%–4.6%** (varies by measurement) |
| **CPTS (HP L1 metric)** | **14.99** |
| **Dismissal rate** | 0.5% |
| **Session frequency** | Shows in ~50% of sessions on App |
| vs ATF P13N carousel | OST CTR (3.41%) < ATF P13N CTR (4.89%) |
| vs Amend Banner | OST CTR (3.41%) < Amend CTR (7.73%) |
| vs AutoScroll Carousel | OST CTR > AutoScroll overall CTR (0.37%) |

### OST by Order Type (FY26 YTD)
| Order Type | CTR | Share of Orders | Notes |
|-----------|-----|-----------------|-------|
| Unscheduled Deliveries | 9.06% | ~50% of orders | Highest engagement |
| Express Delivery | 10.36% | 6.5% of orders | Highest CTR |
| Scheduled + Unscheduled Pickups | 1.17% | ~24% of orders | Lowest CTR |

> 📌 Pickup orders have lowest CTR (1.17%) → **Hypothesis: pickup customers get other status communications (email/text) so they don't need OST**

### OST Problems
1. **Disproportionate space** — OST takes up large vertical space (driven by graphic); pushes all content down
2. **Duplication with Amend Banner** — when a customer has a modifiable order, both OST + Amend show simultaneously for the same order
3. Even on large phones, customers only see **half the first carousel** when OST is showing

### OST Business Impact of Fixing
| Fix | Annual Lift |
|-----|------------|
| Reduce OST white space | **+1.0%–1.4% lift** in Clicks & GMV to Content Zone 4 |
| Dedupe Amend + OST | **+2.3%–3.1% lift** in clicks to Content Zone 4 |

### OST Module in BigQuery
- `hp_module_name`: Look for **OST-related** module names (e.g., `Order Status Tracker`, `OST`)
- `moduletype`: Look for the OST-specific moduletype value
- FY26 estimated full-year impressions: **288M**

---

## ✏️ Amend Banner

### What Amend Banner Is
The **Amend Banner** = a homepage banner that shows when a customer still has time to modify their order (change items, quantities, etc.). It displays a countdown of time remaining to make changes.

### Amend Banner Key Metrics (FY26 YTD)
| Metric | Value |
|--------|-------|
| **CTR** | **7.73%** (one measurement); **15.01%** (another period measurement) |
| **CPTS** | **9.17** |
| **Dismissal rate** | Negligible — no way to close/dismiss Amend Banner |
| **Session frequency** | Shows in ~5% of sessions on App |
| **YoY impressions** | +27% FYTD YoY |
| FY26 est. full-year impressions | **288M** |
| Est. impressions where both Amend + OST show | ~75% = **216M impressions** |

> 🏆 **Amend Banner has the HIGHEST CTR of any ATF module** — higher than OST (3.41%), ATF P13N carousel (4.89%), and AutoScroll Carousel (0.37%)

### Amend Banner Problem
- Amend Banner AND OST appear **simultaneously** for the same order
- Amend shows the time left to change the order; OST shows the arrival time
- This is **duplicative information** consuming double the page real estate

### Amend + OST Deduplication Solution
**Recommendation:**
1. Update Amend Banner language to include BOTH time-left-to-change AND arrival time
2. Change logic: **don't show OST until Amend window expires** (for the same order)

**Success Metrics for Dedupe:**
- Maintain/improve Amend CTR
- No increase in customer contacts
- Maintain/improve OST CTR
- No increase in cancels/substitutions/returns
- Maintain/increase CTR in Content Zones 3, 4, 5

### OST / Amend in BigQuery
When analyzing OST and Amend Banner in `hp_summary_asset`:

```sql
-- OST module
WHERE LOWER(hp_module_name) LIKE '%order status%'
   OR LOWER(hp_module_name) LIKE '%ost%'

-- Amend Banner
WHERE LOWER(hp_module_name) LIKE '%amend%'

-- Both together (utility high-CTR modules)
WHERE LOWER(hp_module_name) IN (
  -- Use actual values from the table; query distinct values:
  -- SELECT DISTINCT hp_module_name, moduletype FROM hp_summary_asset WHERE LOWER(hp_module_name) LIKE '%order%' OR LOWER(hp_module_name) LIKE '%amend%'
)
```

> ⚠️ **Query the table to confirm exact hp_module_name and moduletype strings for OST and Amend** — run:
> ```sql
> SELECT DISTINCT hp_module_name, moduletype, COUNT(*) as row_count
> FROM `wmt-site-content-strategy.scs_production.hp_summary_asset`
> WHERE session_start_dt >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
>   AND (LOWER(hp_module_name) LIKE '%order%' 
>     OR LOWER(hp_module_name) LIKE '%amend%'
>     OR LOWER(hp_module_name) LIKE '%status%'
>     OR LOWER(hp_module_name) LIKE '%timer%'
>     OR LOWER(hp_module_name) LIKE '%walmart%plus%'
>     OR LOWER(hp_module_name) LIKE '%w+%')
> GROUP BY 1, 2
> ORDER BY row_count DESC
> ```

---

## ⏱️ Timers

### What Timers Are
**Timers** = countdown clock banners that appear at the top of the Homepage (above HPOV) during major events. They are the **first thing customers see** when they open the app.

### When Timers Are Used
| Event | Timer Function |
|-------|---------------|
| W+ Week | Countdown to event start; Last Chance |
| July Deals | Countdown to Early Access / Full Access |
| AE1 / AE2 | Countdown to Early Access / Full Access |
| October Deals | Countdown |
| Any "Last Chance" message | Final hours countdown |

### Timer States by W+ Member State
During July Deals (example):
| Member State | Timer Message |
|-------------|--------------|
| **Paid** | Countdown to Deals / "Access to Deals" |
| **Trial** | Switch to Paid → get Deals Access |
| **Churned** | Come Back → get Deals Access |
| **Nevermember** | Sign up → get Deals Access |

> ⚠️ Using a Timer for W+ discounted membership during Deals is **NOT recommended** — countdown clock causes confusion between Deals end time and "Last Chance" W+ messaging

### Timer in BigQuery
```sql
-- Timer module
WHERE LOWER(hp_module_name) LIKE '%timer%'
   OR LOWER(moduletype) LIKE '%timer%'
-- Confirm exact values using discovery query above
```

### Timer Key Facts
- Timer is the **first module customers see** — highest visibility position on page
- Managed by: Lance Woerner (Mgr, Site Merch C&E) — go-to for timer questions
- Process documented in Confluence
- Timers Info file has: UTC conversion chart, cloned timer links

---

## 📊 ATF Module CTR Hierarchy (FY26 YTD)

| Rank | Module | CTR |
|------|--------|-----|
| 🥇 1 | **Amend Banner** | **7.73%–15.01%** |
| 🥈 2 | **ATF P13N Carousel** | **4.89%** |
| 🥉 3 | **OST** | **3.41%–4.6%** |
| 4 | **AutoScroll Carousel (HPOV)** | **0.37% avg** |
| — | HPOV Card 5 benchmark | 0.25% |
| — | HPOV Card 1 benchmark | 0.23% |
| — | HPOV Card 4 benchmark | 0.17% |
| — | HPOV Card 2 benchmark | 0.15% |
| — | HPOV Card 3 benchmark | 0.13% |
| — | W+ Evergreen BTF | 0.16% |

> 📌 Utility modules (Amend, OST) dramatically outperform all HPOV cards on CTR because they are highly personalized to the customer's current situation.

---

## 🗺️ Known / Suspected Module Names in hp_summary_asset

> These need to be **confirmed by querying the table** — use the discovery query above.

| Module | Likely hp_module_name | Likely moduletype |
|--------|----------------------|------------------|
| HPOV AutoScroll | `AutoScroll Card 1–5` | `PrismAdjustableCardCarousel` |
| SIG | `SIG Card 1–6` | `PrismScrollableItemGrid` |
| OST | `Order Status Tracker` or similar | TBD — confirm via query |
| Amend Banner | `Amend Banner` or similar | TBD — confirm via query |
| Timer | `Timer` or `Countdown` or similar | TBD — confirm via query |
| W+ Evergreen BTF | `Walmart Plus` or `W+ Banner` | TBD — confirm via query |
| ATF P13N Carousel | `Jump Right Back In` or similar | TBD — confirm via query |

---

## 🔑 Key Operational Notes

### WMC Cadence
| Meeting | Frequency | Who |
|---------|-----------|-----|
| WMC Weekly | Weekly | Akshay, Melinda |
| Sponsored | Bi-Weekly/Monthly | Deepali |
| Roadmap Review | Bi-Weekly | WMC team |
| Leadership | Monthly | WMC leadership |

### W+ Cadence
| Meeting | Frequency | Who |
|---------|-----------|-----|
| W+ Sync | Bi-Weekly | Emma S, Ryan R, Ryan S, Russell, Lisa |

### OST/Amend Cadence
| Meeting | Frequency | Who |
|---------|-----------|-----|
| OST/Amend sync | Monthly + as needed | Emily J, Gabe, Michele, Bryan |

### Key Stakeholders — OST/Amend
| Role | Name |
|------|------|
| Dir, Tech Operations (sign-off) | Emily Johnson |
| Staff, Tech Operations (day-to-day) | Gabe Carter |
| Sr. Mgr, PM (OST) | Michele Dime |
| Sr. Mgr, PM (Amend) | Bryan Silver |
| Sr. Mgr, UX Design | Michael DeSilva |
| Business Lead | Kate Watson |
| Product | Jorge Tinoco |
| Engineering | Bhawna Bhandari |
| Design | Alison Medland |

---

## 💡 WMC POV1 Message Performance (Reference Data)

**POV1 = AutoScroll Card 1 (site merch Tier 1)**

| Period | Avg CTR | Notes |
|--------|---------|-------|
| 4/19–4/20 (Easter Last Minute Express) | **0.44%** | Event message |
| 4/21–4/27 (11 msgs, excl. Switch 2) | **0.21%** | Normal week |
| 4/21–4/27 (Nintendo Switch 2 Pre-Order) | **4.25%** | Viral pre-order |
| 4/28–5/3 (W+ Week) | **0.58%** | Event week |
| 5/15–5/22 (Memorial Day) | **0.19%** | Normal event |

Notable individual message CTRs (Card 1):
- W+ Week Paid: 1.11%
- W+ Week Trial: 0.34%
- W+ Week Discounted Membership: 0.19%
- Crocs: 0.55%
- Easter Last Minute Express: 0.44%
- Memorial Day Last Minute: 0.32%
- Memorial Day Rollbacks: 0.24%
- Peppa Pig: 0.24%
- Household Essentials Rollbacks: 0.29%

---

*Last updated by Keel Agent | Source: WMC and Walmart+ folder (22 files, Jul 2025)*
